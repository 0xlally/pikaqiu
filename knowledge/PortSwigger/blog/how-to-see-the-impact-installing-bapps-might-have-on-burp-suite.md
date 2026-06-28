# How to see the impact installing BApps might have on Burp Suite

Source: https://portswigger.net/blog/how-to-see-the-impact-installing-bapps-might-have-on-burp-suite
Fetched: 2026-06-28T09:15:17.377151+00:00

How to see the impact installing BApps might have on Burp Suite

Matt Atkinson |

Thursday, 16 June 2022 at 13:50 UTC

Burp Suite

burp extender

BAppStore

If you've ever installed any Burp extensions from the BApp Store, you'll know that it's a great way to extend your capabilities and tailor Burp Suite to your every need. If you've not, then what are you waiting for? Go check out the BApp Store's online site.

The BApp Store is full of great (and free) Burp extensions written by community members and PortSwigger researchers alike. And we just made it even better!

To navigate to the BApp Store in Burp Suite Professional or Community Edition, click Extender > BApp Store .

As of Burp Suite 2022.5.1, you can add BApps without wondering about the impact they're going to have on your system performance - thanks to our new Estimated system impact feature. This shows itemized impact estimates for every BApp in the BApp Store - as well as an aggregated estimate, based on any BApps you have installed (see images below).

Get a detailed estimate of the impact a BApp might have on your system - with Burp Suite's Estimated system impact feature.

This enables you to more easily troubleshoot any instances where you find you're experiencing performance issues while testing. You'll also get visibility of the potential impact a particular BApp might have on your system - before you've installed it.

You can now see the aggregate effect that installed BApps might be having on your system.

Of course, system impact isn't indicative of a particular BApp's overall utility. Some extensions will always be more resource intensive than others by their very nature.

Ratings for individual BApps are split across four areas (plus an Overall estimate):

Memory (estimated RAM usage).

CPU (estimated processor usage).

Time (estimated impact on manual Burp tools and / or UI latency).

Scanner (estimated impact on Burp Scanner).

It's important to note that Estimated system impact refers to the background impact a BApp might have, rather than impact based on its usage. Some BApps rated as "Low", for instance, could still be resource intensive during use. When not in use though, such BApps should have a low impact on system performance.

Download the latest version of Burp Suite to try this new feature and more. You can also see BApp estimated system impact on the BApp Store's online site. And don't forget to follow our accounts on Twitter for news on all the latest BApps and new Burp Suite features.

Burp Suite

burp extender

BAppStore

Matt Atkinson

@mattatkinson42

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
