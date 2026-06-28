# Detecting changes in application state

Source: https://portswigger.net/blog/detecting-changes-in-application-state
Fetched: 2026-06-28T09:15:14.210317+00:00

Detecting changes in application state

Dafydd Stuttard |

Saturday, 4 August 2018 at 15:34 UTC

MoBP

Burp Suite

Modern web applications are heavily stateful, and it is common for the same application function to return different content and have different behavior on different occasions, as a result of actions that were performed by the user in the meantime. Burp's new crawler is able to detect changes in application state that result from actions that it has performed during the crawl.

In the example below, navigating the path BC causes the application to transition from state 1 to state 2. Link D goes to a logically different location in state 1 versus state 2. So the path AD goes to the empty shopping cart, while ABCD goes to the populated cart. Rather than just concluding that link D is non-deterministic, the new crawler is able to identify the state-changing path that link D depends on. This allows the crawler to reliably reach the populated cart location in future, to access the other functions that are available from there:

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
