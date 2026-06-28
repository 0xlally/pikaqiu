# "The entire internet is broken": ethical hacking expert John Hammond meets James Kettle

Source: https://portswigger.net/blog/the-entire-internet-is-broken-ethical-hacking-expert-john-hammond-meets-james-kettle
Fetched: 2026-06-28T09:15:25.526701+00:00

"The entire internet is broken": ethical hacking expert John Hammond meets James Kettle

Amelia Coen |

Wednesday, 27 August 2025 at 09:11 UTC

In a brand-new collaboration between ethical hacking and AppSec expert John Hammond and world-renowned security researcher James Kettle, the pair explore how tens of millions of websites are compromised.

In this video, John and James dive deep into James’ new HTTP/1.1 Must Die research, the cutting edge of web security, focusing on the inherent insecurity of HTTP/1.1. As James explains, upstream HTTP/1.1 routinely exposes millions of websites to hostile takeover. For over six years, vendors have rolled out mitigation after mitigation, but researchers have consistently found ways to bypass them.

Watch the video

Why must HTTP/1.1 Die?

In PortSwigger’s latest research, James introduces new classes of HTTP desync attack and demonstrates critical vulnerabilities affecting tens of millions of websites, including core infrastructure within major CDNs. A live demo makes the threat all the more tangible, showing how attackers exploit fundamental protocol flaws to devastating effect.

The takeaway is clear: HTTP/1.1 has a fatal flaw. It allows attackers to create dangerous ambiguity about where one request ends and the next begins. By contrast, HTTP/2 eliminates this ambiguity, making desync attacks virtually impossible—provided it’s used not only at the edge, but also for the upstream connection between reverse proxies and origin servers.

What do I need to do?

Act Now: Join the Mission to Kill HTTP/1.1

Read the research: HTTP/1.1 Must Die: The Desync Endgame

Sharpen your skills: Try the 20+ free request smuggling labs, including the new 0.CL lab, on the Web Security Academy.

Defend systems still using HTTP/1.1: Detect threats with Burp Suite extensions, including HTTP Request Smuggler v3.0 and HTTP Hacker, and use recurring scans to stay ahead.

Move to HTTP/2: Ensure your origin servers support HTTP/2, then enable upstream HTTP/2 across your front-end systems.

Join the movement

There’s thousands of security testers, bug bounty hunters, and AppSec professionals over on the official PortSwigger Discord.

Join the server today to join the discussion and hear about how others are killing HTTP/1.1 across their applications.

Amelia Coen

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
