# New techniques and tools for web race conditions

Source: https://portswigger.net/blog/new-techniques-and-tools-for-web-race-conditions
Fetched: 2026-06-28T09:15:22.258845+00:00

New techniques and tools for web race conditions

Emma Stocks |

Thursday, 10 August 2023 at 06:56 UTC

Burp Suite

burp

featured

Black Hat

For too long, web race-condition attacks have focused on a tiny handful of scenarios. Testing for them is inherently unreliable, compounded by known challenges relating to time constraints and network jitter.

The latest work from PortSwigger Research

Debuted at Black Hat USA '23 and DEF CON 31, PortSwigger Research's James Kettle presents "Smashing the state machine: the true potential of web race conditions". This presentation introduces multiple new classes of web race condition, that go far beyond limit-overrun exploits and expose previously overlooked attack surface.

Delve into PortSwigger's latest research, to uncover the true potential of race conditions.

Recordings of the presentations from both Black Hat USA 2023 and DEF CON 31 will be available in the coming months, and will be publicly accessible from PortSwigger Research when published.

Testing for, and exploiting, web race conditions with Burp Suite

The true potential of web race conditions has long been masked, thanks to tricky workflows, missing tooling, and simple network jitter hiding all but the most trivial, obvious examples.

PortSwigger Research's latest work also unveils the single-packet attack, a technique that nullifies network jitter and enables you to send multiple requests in parallel within a 1ms time window. Find the new tooling in Burp Repeater, to experiment with a more reliable testing method that can make race conditions more easily discoverable.

The new single-packet attack capability, when sending requests over HTTP/2+, can also be performed with the updated version of James Kettle's Turbo Intruder BApp extension.

Upgrade to the latest version of Burp Suite Professional (and Burp Suite Community Edition) to access the newly released tooling.

Try out the new exploit techniques

Translating often complex, theoretical knowledge and techniques into usable, practical skills can be challenging, made more difficult by the continually evolving threat landscape of the modern web. That includes the multiple new classes of race condition introduced by PortSwigger Research, and the accompanying single-packet attack capability.

Try working through the new Web Security Academy topic to learn how to discover and exploit the more commonplace limit-overrun race conditions you might already be familiar with. Then, delve into the multiple new classes of web race condition and discover how to effectively test the newly uncovered attack surface with Burp Suite.

Visit the Web Security Academy to get started.

Burp Suite

burp

featured

Black Hat

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
