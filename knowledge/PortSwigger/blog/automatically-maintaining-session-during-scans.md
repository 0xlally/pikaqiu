# Automatically maintaining session during scans

Source: https://portswigger.net/blog/automatically-maintaining-session-during-scans
Fetched: 2026-06-28T09:15:07.127652+00:00

Automatically maintaining session during scans

Dafydd Stuttard |

Tuesday, 7 August 2018 at 16:18 UTC

MoBP

Burp Suite

Over the last few days, we've described how Burp's new crawler can deal with a wide variety of challenges presented by modern applications. But crawling applications is only part of the story. The reason we want to crawl an application's content and functionality is generally because we want to audit what we discover for security vulnerabilities.

Burp's current Scanner contains a world-class scanning engine that can accurately audit for a wide range of vulnerabilities. But a key limitation relates to handling application sessions during the audit. As with the current Spider, the Scanner works quite well with simple cookie-based session handling mechanisms, but fails in more complex cases. You can improve things somewhat with session handling rules, but this is tedious and error prone to set up.

What if the Scanner could automatically maintain session during the audit, with zero configuration by the user? In a typical application, Burp would reach way more attack surface, and uncover a lot more vulnerabilities.

We've rebuilt Burp Scanner's core logic to do exactly that. When an audit follows on from an automated crawl, the new Scanner makes use of the graph of navigational pathways through the application to automatically maintain session during the audit.

Let's see how this works.

When Burp is about to audit an individual request, it begins by identifying the shortest path to reach that request from the starting location of the crawl. For example:

Burp then determines the most efficient way to deliver that same request repeatedly within a valid session. It does this by first rewalking the path to obtain a fresh sample of any session tokens, and then testing various simplifications of the path to see if the session is correctly maintained.

In many cases, it is possible to simply reissue the final request over and over. This can happen because the request doesn't actually contain any session tokens at all:

Or because the only session tokens are cookies, which can typically be used multiple times:

Or because, although the request contains both cookies and CSRF tokens, the CSRF tokens can be used repeatedly:

In some cases, it is necessary to reissue the preceding request on each occasion prior to issuing the request that is being audited. This normally happens because the application uses single-use CSRF tokens. Because the tokens are single-use, it is necessary to reissue the preceding request on each occasion, to obtain a fresh token:

In extreme cases, every transition between requests is protected by a single-use token. This happens occasionally in high-security applications where navigation is tightly controlled. In this situation, the most reliable way to repeatedly issue the request to be audited is to always return to the starting location and walk the full path to that request:

So far, Burp has figured out the most efficient way to repeatedly issue the request that is to be audited, while remaining in-session. But during the audit itself, Burp will be sending different requests, containing all kinds of payloads designed to discover vulnerabilities. For various reasons, these audit requests might cause the session to become invalid, in a way that issuing the original request does not. An obvious example would be a web application firewall that flags certain scan payloads as malicious, and terminates the session.

To deal with this situation, when the new Scanner carries out its various audit checks, it periodically monitors the application's responses to ensure that a valid session is maintained. If Burp positively confirms the validity of the session, then it sets a checkpoint on the audit checks that have been fully completed. If Burp identifies that the session is no longer valid, it rolls back to the latest checkpoint and resumes from there. This logic is carried out in a way that minimizes the overhead of session management and avoids indefinite loops if sessions are frequently lost. For example:

The overall effect of these changes in the new Scanner is that Burp will:

Obtain a valid session automatically.

Recover gracefully when a session is lost for any reason.

Hugely increase the attack surface that is reached when scanning.

Eliminate the need for users to set up complex macros and session handling rules.

MoBP

Burp Suite

Dafydd Stuttard

@DafyddStuttard

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.
