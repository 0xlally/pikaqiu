# [MoBP] SOAP parameter parsing

Source: https://portswigger.net/blog/mobp-soap-parameter-parsing
Fetched: 2026-06-28T09:15:20.877924+00:00

[MoBP] SOAP parameter parsing

Dafydd Stuttard |

Friday, 14 November 2008 at 06:47 UTC

MoBP

burp

When you send a request to Intruder to perform custom automated attacks, it makes a guess at where you will want to place your attack payloads. By default, it places payload markers around the values of each URL and body parameter, and each cookie value. If you've ever tried to attack a SOAP request using Intruder, you'll know that this auto-placement doesn't help you very much.

In the new release, auto-placement also supports XML request bodies, and by default places payload markers around the values of each XML element and attribute. If you need to fuzz several SOAP requests, this will now be a simple task of sending each request to Intruder, and starting an attack using the default payload positions:

The new support for parameters in XML request bodies is used elsewhere within the new release, including automated vulnerability scanning, of which more shortly.

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
