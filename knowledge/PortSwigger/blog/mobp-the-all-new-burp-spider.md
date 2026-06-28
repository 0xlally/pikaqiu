# [MoBP] The all new Burp Spider

Source: https://portswigger.net/blog/mobp-the-all-new-burp-spider
Fetched: 2026-06-28T09:15:21.165859+00:00

[MoBP] The all new Burp Spider

Dafydd Stuttard |

Monday, 10 November 2008 at 06:59 UTC

MoBP

burp

In its current incarnation, the Spider is the weakest of the core Burp tools, with more than its fair share of old buggy code, and several obstacles to usability. I don't use it much myself, and I doubt if too many of you do either.

In the new release, Spider has been completely rewritten from scratch, with much improved content parsing and several new features. Spidering is now driven entirely via the target site map and other tools.

When you first map out a new application's content and functionality, it is generally best to work manually with your browser, giving you full control over the requests that are issued, and ensuring that you comply with any input validation, navigational structure and other constraints imposed on normal usage of the application. As you do this, Burp will passively compile its site map of all the items you have requested, as well as those which it has inferred from the application's responses.

When you have explored all of the content you can find with your browser, you will typically see a site map containing a number of unrequested items - these are shown in grey in the tree and table. At this point, you can still proceed manually, copying the relevant URLs into your browser and exploring further. Or you can let the Spider do its work to map out the rest of the application's content. The easiest way to do this is to select one or more nodes within the tree, and choose "spider from here" from the context menu:

When you tell Burp to spider a branch of the site map, it will perform the following actions:

Request any unrequested URLs identified within the branch.

Submit any forms whose action URLs lie within the branch.

Re-request any items which previously returned 304 status codes, to retrieve a fresh (uncached) copy of the application's responses.

Parse all content retrieved to identify new URLs and forms.

Recursively repeat these steps as new content is identified.

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
