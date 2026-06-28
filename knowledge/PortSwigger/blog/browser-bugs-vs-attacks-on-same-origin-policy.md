# Browser bugs vs. attacks on same origin policy

Source: https://portswigger.net/blog/browser-bugs-vs-attacks-on-same-origin-policy
Fetched: 2026-06-28T09:15:07.882575+00:00

Browser bugs vs. attacks on same origin policy

Dafydd Stuttard |

Wednesday, 15 August 2007 at 06:06 UTC

browser security

A bar-room conversation with a colleague at Black Hat led me to think about this question, and here are my thoughts, for what they're worth.

Today's browsers are full of Oday, particularly in the processing of images and other media, and in plug-ins like ActiveX controls. At the same time, a thriving area of current research is focused on attacks against the browser same origin policy, involving JSON hijacking, DNS rebinding, other workarounds and logic flaws. Which of these areas is more worthy of our attention?

Here are two polarised (and somewhat caricatured) opinions:

If I want to compromise a web user, I can just find a browser Oday and completely own them. Attacks against same origin policy are lame and unnecessary.

I agree we can't ignore browser bugs if we’re trying to protect web apps. We need to find defences in the application that can stand up to a compromised browser.

Of these two positions, the second is the easiest to shoot down. Aside from a narrow subset of browser bugs, no defences in the application can protect against a compromised browser. If an attacker can execute arbitrary machine-level code within a user's browser, then they completely own that user's interaction with any web application.

Does that mean we must accept the first position? There are several reasons why not:

Many would-be attackers are not capable of discovering and exploiting a browser Oday, but can understand and deliver attacks against the same origin policy. Defences that frustrate only some attackers are still worthwhile.

Attacks against the same origin policy make interesting research. Most security researchers are interested in class breaks and new genres of attacks, rather than individual bugs. The types of vulnerabilities that exist within browsers, and the ways they can be discovered, are more interesting than the latest bug in an image parser. Similarly, generic ways of circumventing the same origin policy are more interesting than the latest means of inducing network timeouts, to port scan other domains.

This area of web security is a weakest link problem, in that an attacker needs to find either a browser bug or a same origin policy bypass to compromise a user. Conventional defence-in-depth does not apply - a robust same origin policy can still be defeated through a bug in the browser, and vice versa. This means that protecting users entails resolving both problem areas. Browser vendors are taking security seriously, and bugs are going to get progressively harder to find and exploit. Meanwhile, research into attacking and defending same origin restrictions needs to continue, so that this is not left as the weak link when browsers become more resilient.

browser security

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
