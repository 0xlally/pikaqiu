# Handling application errors during scans

Source: https://portswigger.net/blog/handling-application-errors-during-scans
Fetched: 2026-06-28T09:15:16.206712+00:00

Handling application errors during scans

Dafydd Stuttard |

Sunday, 12 August 2018 at 15:37 UTC

MoBP

Burp Suite

How many times have you seen this?

As we have already described, Burp's current Scanner processes each item in the scan queue in isolation. If it runs into connection errors and transmission timeouts, then it eventually abandons the item and moves on to the next. There are two quite annoying limitations in this approach:

There is no retry mechanism for items that were abandoned. If an intermittent problem arises, for example where the application stops responding to requests for a few minutes, then the user needs to manually find the abandoned items and re-queue them.

If an application becomes permanently unavailable, then Burp continues regardless, starting each item in turn, running into errors, and eventually abandoning it.

Burp's new Scanner addresses these issues with a robust approach to handling application errors. This comprises the following key elements:

Burp tracks error conditions in as granular a way as possible. If an individual action causes an error, Burp marks that action as failed and moves on to the next. If repeated actions fail at the same level of activity, then that whole level is marked as failed, and Burp moves on to the next.

Following completion of each phase of a scan, Burp can perform a configurable number of follow-up passes to retry the specific operations that failed. This handles intermittent outages without the need for the user to manually re-scan any items.

If too many errors occur (either in succession or in total), then Burp can optionally pause the entire scan. This avoids plowing on indefinitely when an application is down, and lets the user or the application owner resolve the issue before the scan is resumed.

There are separate options to configure how Burp handles application errors during the crawl and audit phases of a scan:

The ability to track errors at a granular level and bubble up when repeated errors occur is particularly useful during the audit phase of a scan. Burp tracks errors first at the level of individual audit checks, then individual insertion points, then the request that is being audited, and ultimately the entire scan. This nicely deals with web application firewalls that might selectively drop connections based on specific payloads that are used in some audit checks, and also cases where they drop connections that make any modifications to a specific parameter.

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
