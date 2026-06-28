# Black Hat USA 2021: PortSwigger's latest research to be unveiled

Source: https://portswigger.net/blog/black-hat-usa-2021-portswiggers-latest-research-to-be-unveiled
Fetched: 2026-06-28T09:15:07.428721+00:00

Black Hat USA 2021: PortSwigger's latest research to be unveiled

Emma Stocks |

Tuesday, 6 July 2021 at 12:11 UTC

Black Hat

Burp Suite

Research

Two years ago, PortSwigger's director of research James Kettle presented "HTTP Desync Attacks" on-stage at BlackHat USA and kicked off a wave of request smuggling, but at that time HTTP/2 escaped serious analysis. At this year's BlackHat USA event, James will be unveiling his latest research, "HTTP/2: The Sequel is Always Worse".

The PortSwigger briefing

In this latest presentation, James will be taking you beyond the frontiers of existing HTTP/2 research, to unearth horrifying implementation flaws and subtle RFC imperfections. He'll show you how these flaws enable HTTP/2-exclusive desync attacks, with case studies targeting high-profile websites powered by servers ranging from Amazon's Application Load Balancer to WAFs, CDNs, and bespoke stacks by big tech.

He'll then demonstrate critical impact by hijacking thick clients, poisoning caches, and stealing plaintext passwords to net multiple max-bounties. One of these attacks remarkably offers an array of exploit-paths surpassing all known techniques. After that, he'll unveil novel techniques and tooling to crack open a widespread but overlooked request smuggling variant affecting both HTTP/1 and HTTP/2 that is typically mistaken for a false positive.

For his grand finale, he'll drop multiple exploit-primitives that resurrect a largely forgotten class of vulnerability, and use HTTP/2 to expose a fresh application-layer attack surface.

View more details on the BlackHat USA website.

What improvements can you expect to see in Burp Suite?

Given the expansive new attack surface we'll be uncovering with this technique, you can rest assured that Burp Suite will be equipped to handle it. Our HTTP/2-exclusive product roadmap will include the following:

Extended discoverability capabilities for Burp Scanner, allowing detection of HTTP/2-exclusive desync attacks.

A brand new Inspector widget for HTTP/2 requests, enabling HTTP/2 attacks in Burp Repeater.

Support for BApps performing custom HTTP/2-exclusive attacks via the Extender API.

Major updates to three of James' ever-popular BApps - HTTP Request Smuggler, Turbo Intruder, and Param Miner.

Additionally, we'll be creating a brand new set of Web Security Academy labs for you to work your way through, to put James' novel techniques to the test. Make sure you're registered now, so you can access the new labs as soon as they drop!

Register for the event

BlackHat USA is taking place between July 31 - August 5, 2021. Don't forget to register and mark your calendars. James' latest research will also be made available through the PortSwigger website after the event.

About James

James 'albinowax' Kettle is the Director of Research at PortSwigger. He loves inventing novel techniques to hack websites. He has presented at numerous prestigious venues, including "Practical Web Cache Poisoning" at BlackHat USA.

Follow @albinowax to stay up to date on his latest work and findings.

Check out Black Hat USA 2021 briefs for additional AppSec briefings.

Can't attend?

Follow @albinowax to stay up to date on his work, and keep an eye on PortSwigger Research - @PortSwiggerRes - to make sure you don't miss the rest of the team's quality research.

The whitepaper for HTTP/2: The Sequel is Always Worse will be available on PortSwigger Research, along with the latest work by the entire team. Check out "Upcoming Talks" to see where we will be presenting next.

James is also presenting "HTTP/2: The Sequel is Always Worse" at this year's Def Con 29 event. The online-only event takes place between 5 - 8 August and you can register for that here. If you're lucky enough to be a US citizen, you can register to attend the Las Vegas in-person conference.

Finally, a few days after the events, a director's cut recording will be made available through the PortSwigger website.

Black Hat

Burp Suite

Research

Emma Stocks

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
