# [MoBP] Deflate support

Source: https://portswigger.net/blog/mobp-deflate-support
Fetched: 2026-06-28T09:15:20.399886+00:00

[MoBP] Deflate support

Dafydd Stuttard |

Wednesday, 26 November 2008 at 06:54 UTC

deflate

MoBP

burp

Burp has always been able to unpack GZIP-encoded responses, but for some reason never supported deflate encoding, which you see occasionally. Joe Hemler wrote a handy plugin to do the job, but the new release will support this encoding natively. So while before you would have seen this:

in future you will see this:

If time permits, the Decoder will also be updated to unpack deflate-encoded content for you.

deflate

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
