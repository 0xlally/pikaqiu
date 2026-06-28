# PortSwigger at Black Hat & DEF CON 33

Source: https://portswigger.net/blog/portswigger-at-black-hat-amp-def-con-33
Fetched: 2026-06-28T09:15:23.462746+00:00

PortSwigger at Black Hat & DEF CON 33

Tom Ryder |

Tuesday, 8 July 2025 at 09:17 UTC

Las Vegas. August. Protocols are getting torn apart.

This summer, PortSwigger returns to Black Hat USA

and DEF CON 33 with a host of new talks, events and ways to meet PortSwigger and the the teams behind Burp Suite.

This year, we have a bold message:

HTTP/1.1 must die.

Although it's been six years since PortSwigger Research first brought request smuggling to mainstream attention, attempts to mitigate these attacks have repeatedly proven to be ineffective at best and, in some cases, to actually make the situation worse.

The time has come to acknowledge that request smuggling is an inherent flaw in the HTTP/1.1 protocol itself and, as such, its continued use should be considered a vulnerability in its own right.

Learn more at http1mustdie.com.

BSides Las Vegas - Monday 4 August

There will be a PortSwigger presence at BSides Las Vegas, meeting the community. If you're attending, let us know on socials with #BurpOnTour and #BSidesLV.

Upstream HTTP/1.1 is inherently insecure: The Desync Endgame

Wednesday, August 6, 3.20pm

At Black Hat and DEFCON33, PortSwigger's Director of Research, James Kettle (@albinowax), will demonstrate how it was still possible to compromise every single customer of three major CDNs, leaving tens of millions of websites exposed to potentially critical attacks.

He'll unveil new classes of desync attacks and a toolkit to help you identify request smuggling vulnerabilities more easily and reliably than ever before, the same techniques and tools he used to earn over $200k in bug bounties in just two weeks.

Tune in to our coverage of Black Hat and DEFCON33:

Learn cutting-edge smuggling techniques others aren’t using (yet)

A free toolkit to identify critical flaws in CDNs and edge infrastructure

Whether you still use HTTP/1.1 intentionally, or are forced to due to the limitations of your CDN's infrastructure, we want to challenge the industry to sunset this vulnerable, legacy technology. If we want a secure web, HTTP/1.1 must die!

Where to watch:

Black Hat USA – August 6 (3.20pm PDT, 10.20pm UTC)

DEF CON 33 – August 8 (4.30pm PDT, 11.30pm UTC)

PortSwigger post-con stream - TBD

DEF CON Workshop: Advanced HTTP Smuggling Exploitation

In this session, Martin Doyhenard (@tincho_508

) will show you how to dissect HTTP at the stream level, revealing hidden behaviors that traditional tools miss and turning them into powerful exploits. You’ll learn how to spot hidden proxies, exploit subtle errors to desynchronize connections, hijack requests, and uncover vulnerabilities that evade traditional tools.

Through real-world case studies, Martin reveals exactly how you can chain advanced HTTP Desync attacks to secure bounties that others have left behind, transforming complex network architectures into your playground.

Arsenal Tools That Hit Beyond the Application Layer

We’re not just bringing research, we’re arming you with tools built for modern web security.

HTTP Hacker

Martin Doyhenard (@tincho_508) — Black Hat Arsenal | August 6, 1:00–1:55pm

Your proxy might be lying to you. HTTP Hacker gives you raw stream-level access to see what’s really happening across persistent connections, pipelining, and edge infrastructure.

Built as a Burp Suite extension, it helps you:

Go beyond what scanners see. Find bugs hidden behind multi-hop routing and caching layers

Identify smuggling and cache bugs that could enable full credential theft in enterprise systems

If you care about HTTP smuggling, caching bugs, or infrastructure-level attacks, this is the tool you've been waiting for.

WebSocket Turbo Intruder

Zakhar Fedotkin (@d4d89704243

) — Black Hat Arsenal | August 6, 1:00–1:55pm

WebSockets are everywhere but security testing them has been a pain. That ends now with WebSocket Turbo Intruder.

Under the hood, WebSocket Turbo Intruder allows you to:

Fuzz WebSockets at scale and find deep protocol-level bugs that others miss

Automate complex, multi-step WebSocket attacks with ease even without deep scripting skills

If you’ve been ignoring WebSockets because the tooling wasn’t there, this is your moment to start looking at this vast and under-explored attack surface.

ArmorCode PBC Security Leadership event

Kick off August 6 with two security-leadership focussed panels: “Rethinking Risk as the World Embraces AI” and “The Cyber Resilience Act”, with insights coming your way, as PortSwigger sponsor and attend this event. If you’re in Las Vegas on August 6, RSVP here.

Meet the Researchers. Join the Movement.

We’re hosting an informal meetup in Las Vegas (details coming soon) where you can:

Talk directly with the PortSwigger Research team

Share ideas and feedback on Burp Suite

Grab exclusive swag: tees, stickers, and event-only surprises

Let us know via this form to keep up-to-date with all of our plans.

Bug Bounty Village Triage CTF

PortSwigger sponsor this year’s Bug Bounty Village Triage CTF.

The Top 10 Web Hacking Techniques of 2024 Awards

We’re thrilled to recognize the researchers behind the Top 10 Web Hacking Techniques of 2024 with individual awards for each of the top 10 entries.

Every year, security researchers from all over the world share their findings. Their research is recognized for not only their individual innovation, but for their potential to be re-applied or adapted in new ways, helping to push the boundaries of web security.

This year saw a staggering 121 nominations, with some incredible research and intense competition.

This year, we will host an official awards ceremony. Watch this space.

Read the Top 10 Web Hacking Techniques of 2024 here.

What’s Coming Next

We’re going big this summer with a full-spectrum launch across channels:

Exclusive technical deep-dives

New partnerships

Live coverage from Vegas

More ways to meet PortSwigger in Vegas

A new Academy lab, enabling you to sharpen your request smuggling skills and test out the new tools in a safe environment

Post-event write-up, demos and behind-the-scenes stories

Interactive discussions and post-event exclusives on the PortSwigger Discord

Don’t Miss a Beat

We’ll be bringing everything to you via our social media channels, so if you’re not attending, you’ll still have access to the groundbreaking research and tooling from PortSwigger.

Follow the action in real-time:

Twitter/X:

@Burp_Suite |

@PortSwigger

Follow PortSwigger on LinkedIn

Join our Discord for post-event tool drops and Q&A

Keep an eye on

PortSwigger’s blog and

PortSwigger Research for demo walkthroughs and expert write-ups

You’ll get early exclusive content, and a front-row seat to all of the action.

Can’t make it to Vegas? Follow along with #BurpOnTour and live updates from Black Hat and DEFCON33.

Tom Ryder

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
