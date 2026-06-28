# [MoBP] Filtering and deleting content

Source: https://portswigger.net/blog/mobp-filtering-and-deleting-content
Fetched: 2026-06-28T09:15:20.431838+00:00

[MoBP] Filtering and deleting content

Dafydd Stuttard |

Monday, 3 November 2008 at 07:09 UTC

MoBP

burp

One frequent complaint about Burp is that it can easily accumulate a huge amount of data, in locations such as the proxy history. After lengthy usage, these repositories can become unwieldy, making it hard to find what you are looking for. Further, in noisy applications, such as those making frequent asynchronous Ajax requests, browsing a few pages can generate hundreds of individual requests, causing interesting items to get lost.

The new version of Burp uses display filters to address this problem. For example, at the top of the site map, there is a filter bar. Clicking on this shows a popup enabling you to configure exactly what content will be displayed within the map:

You can choose to display only requests with parameters, or which are in-scope for the current target (of which more shortly). You can filter by MIME type and HTTP status code. If you set a filter to hide some items, these are not deleted, only hidden, and will reappear if you unset the relevant filter. This means you can use the filter to help you systematically examine a complex site map to understand where different kinds of interesting content reside.

Sometimes, however, you accumulate data within Burp that you just don't need - for example, if you have browsed to off-target domains. In this situation, you can permanently delete the superfluous items using the context menu. For example, you can select multiple hosts or folders within the tree view and delete them altogether:

You can do the same thing by selecting single or multiple items in the tree view, proxy history, etc.

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
