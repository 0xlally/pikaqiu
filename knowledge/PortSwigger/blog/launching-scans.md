# Launching scans

Source: https://portswigger.net/blog/launching-scans
Fetched: 2026-06-28T09:15:19.211623+00:00

Launching scans

Dafydd Stuttard |

Friday, 17 August 2018 at 16:08 UTC

MoBP

Burp Suite

In the past few days, we've been describing Burp's forthcoming support for multiple parallel scans, improved management of system resources, and the new configuration library. Today, we'll look at how you'll be able to launch scans.

Firstly, some terminology. In the past, we've talked about spidering (meaning discovering content) and scanning (meaning testing for vulnerabilities). In future, we're making a subtle change. All of this is now scanning. And scanning involves crawling for content, and auditing for vulnerabilities. It'll become clearer why this change makes sense as you read this post.

You can launch scans by selecting items anywhere within Burp, and choosing the "Scan" option from the context menu. (This replaces the previous context menu options to passively scan, actively scan, or spider). There will also be a prominent "New scan" button, which lets you initiate a scan without making a selection first.

This opens the scan launcher:

The scan launcher lets you select the type of scan you want:

If the scan involves crawling, then you must specify the URLs to scan from:

If the scan involves auditing items that you already selected, then these are listed, with an option to consolidate the items based on various criteria:

At this point, you can launch the scan without touching any other settings. Or you can continue to tweak other options as required.

You can select one or more configurations to use for the scan, chosen from your configuration library, or specified on the fly:

If you select multiple configurations, these will be applied sequentially in turn, to determine the final configuration that is used. Each configuration can be more or less specific, defining settings for multiple areas or only one. This capability lets you apply a general configuration first (for example, your preferred general scan settings), followed by a more specific configuration (for example, some specific options that are useful for this particular application).

You can also provide application login credentials that should be used to log in during crawling:

And you can specify the resource pool for the scan:

Astute readers will note that Burp's existing distinction between passive and active scans as fundamentally different actions is disappearing. In the forthcoming update, scans are just scans. You can, of course, still do a scan that only audits for passive issues, and this is achieved by setting the scan's configuration to only check for passive issues:

One welcome benefit of treating passive and active scanning in a uniform way is that both will now use the same UI, allowing full monitoring and control of passive-only scans:

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
