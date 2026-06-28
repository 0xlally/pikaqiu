# [V13P] Laser-guided scanning

Source: https://portswigger.net/blog/v13p-laser-guided-scanning
Fetched: 2026-06-28T09:15:27.580419+00:00

[V13P] Laser-guided scanning

Dafydd Stuttard |

Wednesday, 25 November 2009 at 12:39 UTC

V13P

To my great pride, nearly everyone who has tried out Burp Scanner absolutely loves it. But people still helpfully come back with tons of feature requests for it.

One of the biggest complaints is the relatively crude way in which Burp lets you send items for active scanning from the site map. For example, when you have mapped out all of the content and functionality within your target application, you can select the relevant host (or branch within the host), and choose "actively scan selected items" from the context menu. Currently, when you do this, Burp will perform an active scan on every single item within this selection, which often is not quite what you want: your selection may include multiple superfluous submissions to the same form handlers, items you have scanned already, items with irrelevant file extensions or MIME types, and specific items which you have excluded from the target scope, such as logout or administrative functions. Currently, the only workarounds for this limitation are to go through the site map individually selecting the specific items which you do actually want to scan, or to send everything for scanning and then cancel the irrelevant items within the scan queue. Neither option is painless.

The new release gives you much easier and fine-grained control over what gets scanned in this situation. Any time you select multiple items for active scanning, Burp launches a brief wizard which lets you fine-tune your selection. The first screen of the wizard offers you various intuitive filters to remove potentially unnecessary items (duplicates, already scanned items, media content, etc.), and shows you how many items will be affected by each filter:

The second screen of the wizard shows you a list of the remaining items, and lets you sort the table by various relevant properties, view the full requests and responses, and delete individual items:

The wizard then completes and the selected items are sent for scanning in the usual way.

Hopefully this feature will let you make much more effective use of Burp's scanning capabilities, avoid filling the scan queue with junk, and find more bugs more quickly than before.

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
