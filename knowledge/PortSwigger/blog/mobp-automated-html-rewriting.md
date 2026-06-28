# [MoBP] Automated HTML rewriting

Source: https://portswigger.net/blog/mobp-automated-html-rewriting
Fetched: 2026-06-28T09:15:19.740122+00:00

[MoBP] Automated HTML rewriting

Dafydd Stuttard |

Thursday, 6 November 2008 at 07:35 UTC

MoBP

burp

Here are a bunch of handy new functions in Burp Proxy that you can use to achieve various tasks by automatically rewriting the HTML in application responses (all are off by default):

Unhiding hidden fields enables you to edit their values directly in the browser, rather than by intercepting subsequent requests. Similarly with enabling disabled fields, and removing length limitations. Here is what the Google Blogger application looks like with hidden fields unhidden:

On the web hacking course which me and Marcus deliver at Black Hat, we have around a dozen labs illustrating various cases of unsafe reliance on client-side controls. The first few examples involve easy scenarios like hidden and disabled fields, length limits and client-side input validation. Well, those labs will get even easier with the new version of Burp, because solving the lab will be a simple matter of checking the relevant box in Burp's configuration!

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
