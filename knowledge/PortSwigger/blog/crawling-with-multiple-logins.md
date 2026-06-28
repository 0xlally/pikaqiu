# Crawling with multiple logins

Source: https://portswigger.net/blog/crawling-with-multiple-logins
Fetched: 2026-06-28T09:15:12.567044+00:00

Crawling with multiple logins

Dafydd Stuttard |

Sunday, 5 August 2018 at 15:43 UTC

MoBP

Burp Suite

Burp's current Spider tool has a primitive login capability, in that you can configure a username and password that will be submitted in any login forms. You can do a bit better with macros and session handling rules, but this only works with a single login account at any one time.

Burp's new crawler hugely improves the handling of application logins. It lets you configure multiple logins for different user roles within the application. It also supports self-registration of user accounts.

The crawler begins with an unauthenticated phase in which no credentials are submitted. When this is complete, Burp will have discovered any login and self-registration functions within the application.

If the application supports self-registration, Burp will by default attempt to register a user.

The crawler then proceeds to an authenticated phase. It will visit the login function multiple times and submit:

The credentials for the self-registered account (if any).

The credentials for each account that the user configured (if any).

Bogus credentials (these might reach interesting functions such as account recovery).

For each set of credentials that are submitted to the login, Burp will crawl the content that is discovered behind the login. This allows the crawler to reach different functionality that is available to different types of user:

Although the crawler normally employs multiple crawler agents in parallel, some applications prohibit concurrent login by the same user. Burp is able to detect this behavior, and will only perform a single concurrent login for each distinct user account:

The core approach of the new crawler is to construct a graph representing the navigational pathways through the application that users are able to take. This means that once content has been discovered in a given user context, it is straightforward for the crawler to revisit that content when it needs to, because the navigational pathway to reach that content includes a login using the required credentials.

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
