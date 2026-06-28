# [V13P] Improved search

Source: https://portswigger.net/blog/v13p-improved-search
Fetched: 2026-06-28T09:15:27.059681+00:00

[V13P] Improved search

Dafydd Stuttard |

Friday, 20 November 2009 at 08:12 UTC

V13P

The suite-wide search function has had a revamp, with a number of useful features added:

regex mode;

optional restriction to target scope;

optional dynamic updating of existing search results as new requests are made;

ability to search selected hosts/branches within the site map, via the site map context menu.

Here's an example of using a regex search term with dynamic updating, to monitor all responses containing HTML comments as they are received from the server:

The searchable text viewer/editor used throughout Burp also now supports regex and case sensitive searches. These features are accessed via a new pop-up panel at the left of the search bar:

When you are viewing items found in a suite-wide search, the relevant options which you used in that search are automatically copied to the text viewer, so that the correct items are highlighted.

V13P

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
