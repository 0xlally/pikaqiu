# The history of OAST in Burp Suite

Source: https://portswigger.net/blog/the-history-of-oast-in-burp-suite
Fetched: 2026-06-28T09:15:25.719129+00:00

The history of OAST in Burp Suite

Matt Atkinson |

Tuesday, 17 August 2021 at 12:00 UTC

Burp Suite

burp collaborator

OAST

At PortSwigger, we pride ourselves on pushing the boundaries of web security. Just take a peek at some of our researchers' recent and upcoming talks from the likes of Black Hat and DEF CON if you'd like any proof of that.

But, believe it or not, one of our team's most popular breakthroughs so far is now six years old …

Making waves with Burp Collaborator

It's become so normal to have automated OAST in your Burp scans now that it seems weird to call it revolutionary. But back in 2015 when we introduced Burp Collaborator, it really did shake things up. By making cumbersome and underutilized out-of-band (OAST) testing methods much easier to use, Burp Collaborator opened up new possibilities for testers - saving you considerable time in the process.

Burp Collaborator's OAST can now help you to zap everything from blind SQL injection and blind XSS, to even trickier vulnerabilities …

Nowadays, Burp Collaborator's automated component is so well integrated that many of you tell us you didn't even realize you were using it at first. But make no mistake - a sizable chunk of the blind and asynchronous vulnerabilities you see flagged in Burp Scanner's results wouldn't be there if it wasn't for Burp Collaborator.

And the best part is that OAST testing is ultra-reliable. It's rare that OAST will put a false positive in front of you - again saving considerable time and effort.

Read more: what the hell is OAST testing anyway?

Six years of world-class research and development

We don't rest on our laurels around here, and over the past six years, PortSwigger Research and the Burp Suite development teams have been busy sharpening Burp Collaborator's claws. PortSwigger Research regularly leverage Burp Suite Professional's OAST capabilities as part of their work, and this has led to a wealth of new scan checks and functionality being added over the years.

Burp Collaborator's OAST can now help you to zap everything from blind SQL injection and blind XSS, to even trickier vulnerabilities - like asynchronous SQL injection, blind SSRF, or even deferred asynchronous command injection. Without OAST, this stuff is easy to miss (or just plain invisible), so Burp Collaborator has been important in maintaining Burp Scanner's reputation for delivering research-led results you can rely on.

Read more: Hunting asynchronous vulnerabilities (James Kettle).

Of course, if you want to create your own scan checks on the back of Burp Collaborator, then the Burp Extender API makes that possible. Extensions can be written in Java, Python, or Ruby, and the API gives you a wealth of options to play with.

Burp Collaborator Client gives you the ability to carry out manual OAST testing without the rigmarole involved in setting up your own server, or creating your own OAST payloads. Of course, Burp Collaborator does offer the option to deploy your own private server for both automated and manual OAST testing, if you'd prefer not to use our public setup.

The future

Even with all of this capability included, we've still got big plans for where we can go with Burp Collaborator. Watch this space, because you'll be seeing some cool new features soon. These of course will be on top of pending updates like enabling Burp Scanner to find blind server-side template injection (SSTI) using Burp Collaborator.

For more information on upcoming Burp features, check out our July 2021 Burp Suite roadmap update. And don't forget to follow us on Twitter, for all the latest from around the PortSwigger community.

Burp Suite

burp collaborator

OAST

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
