# [MoBP] Alert overload

Source: https://portswigger.net/blog/mobp-alert-overload
Fetched: 2026-06-28T09:15:19.702059+00:00

[MoBP] Alert overload

Dafydd Stuttard |

Monday, 24 November 2008 at 06:57 UTC

MoBP

burp

While we're on the subject of network errors, take another look at the alerts table in yesterday's post. Pretty messy, yeah? Although it's essential to know that your work has run into problems, you probably don't need to be told about the same error several hundred times per second.

We've seen already how the new release of Burp will help you filter out unnecessary noise, and the alerts table is another example. In future, when an alert is received which matches the previous alert, they are simply aggregated, and a counter is shown. You can determine the nature, time and extent of the problem, without your UI filling with thousands of table entries. Here is what the alerts table now looks like when the target server stops responding during an Intruder attack:

MoBP

burp

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
