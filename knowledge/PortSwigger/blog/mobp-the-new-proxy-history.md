# [MoBP] The new proxy history

Source: https://portswigger.net/blog/mobp-the-new-proxy-history
Fetched: 2026-06-28T09:15:22.193767+00:00

[MoBP] The new proxy history

Dafydd Stuttard |

Friday, 7 November 2008 at 06:52 UTC

MoBP

burp

If I had a pound for every time someone has asked me if you can clear the Burp Proxy history, I'd have quite a few quid by now.

Well, the Proxy history just got a whole lot more powerful, and yes, you can even clear it if you want to.

Without further ado, here is what the Proxy history now looks like:

The most obvious addition is the preview pane, which means you can quickly see the contents of requests and responses by selecting an individual item in the table. As previously, you can still double-click an item to pop up a new window showing the request and response details.

There are also a few new columns, showing the response MIME type, HTML page title and the time of day. The table content is now forward- and reverse-sortable by clicking on any column header, enabling you to quickly locate what you are looking for.

There is a filter bar above the table which works in the same way as the site map filter, allowing you to filter on MIME type or HTTP status code, or to show only requests containing parameters, only items that are within the defined attack scope, etc.

The context menu is improved with several new items including ... drum roll ... the facility to delete the selected item(s), so you can clear any or all unnecessary items from the history. By combining column sorting, multi-select, and item deletion, you can quickly eliminate items from the history that you don't need there:

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
