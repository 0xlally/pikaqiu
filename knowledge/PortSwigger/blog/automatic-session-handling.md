# Automatic session handling

Source: https://portswigger.net/blog/automatic-session-handling
Fetched: 2026-06-28T09:15:07.492099+00:00

Automatic session handling

Dafydd Stuttard |

Friday, 3 August 2018 at 18:04 UTC

MoBP

Burp Suite

One limitation of Burp's current Spider tool relates to session handling. It works well with simple cookie-based session handling mechanisms. But it fails in other situations, including many usages of CSRF tokens, and multi-step processes that must be performed in a specific order. You can work around some of these limitations by recording macros and configuring suitable session handling rules, but this is often tedious and error prone.

Burp's new crawler handles sessions automatically. Because it navigates around a target application in the same way as a user with a browser, it is able to automatically work with practically any session-handling mechanism that browsers are able to deal with. There is no need to configure session handling rules telling Burp how to obtain a session or verify that the current session is valid.

The new crawler employs multiple crawler "agents" to parallelize its work. Each agent represents a distinct individual navigating around with their own browser. Each agent has its own cookie jar, which is updated when the application issues it with a cookie. When an agent returns to the start location to begin crawling from there, its cookie jar is cleared, to simulate a completely fresh browser session.

The requests that the new crawler makes as it navigates around are constructed dynamically based on the preceding response, so CSRF tokens in URLs or form fields are handled automatically. This allows the crawler to correctly navigate functions that use more complex session handling mechanisms, with zero configuration by the user:

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
