# HTTP/1.1 Must Die: What This Means for Bug Bounty Hunters

Source: https://portswigger.net/blog/http-1-1-must-die-what-this-means-for-bug-bounty-hunters
Fetched: 2026-06-28T09:15:16.915887+00:00

HTTP/1.1 Must Die: What This Means for Bug Bounty Hunters

Andrzej Matykiewicz |

Wednesday, 6 August 2025 at 22:23 UTC

At Black Hat USA and DEFCON 2025, PortSwigger's Director of Research, James Kettle, issued a stark warning: request smuggling isn't dying out, it's evolving and thriving.

Despite years of defensive efforts, new research unveiled by Kettle proves that HTTP request smuggling (or "desync" attacks) remain not only rampant but dangerously underestimated, compromising tens of millions of supposedly well-secured websites worldwide, netting $200k+ in bounties in the space of just two weeks.

In his groundbreaking new research, HTTP/1.1 Must Die: The Desync Endgame, Kettle challenges the security community to completely rethink its approach to request smuggling. He argues that, in practical terms, it's nigh on impossible to consistently and reliably determine the boundaries between HTTP/1.1 requests, especially when implemented across the chains of interconnected systems that comprise modern web architectures. Mistakes such as parsing discrepancies are inevitable, and when using upstream HTTP/1.1, even the tiniest of bugs often have critical security impact, including complete site takeover.

This research demonstrates unequivocally that patching individual implementations will never be enough to eliminate the threat of request smuggling. Upstream HTTP/2 offers a robust solution.

If we are serious about securing the modern web, it's time to retire HTTP/1.1 for good.

As a bug bounty hunter, this is a huge opportunity. The attack surface is bigger than ever. If you've not got request smuggling in your arsenal, now's the time to dive in, with new vectors, new tooling, and new strategies that bypass current defenses.

Why This Research Matters to Bug Bounty Hunters

It still pays. Big time.

This research reveals critical desync flaws leading to mass compromise of top-tier platforms that may have remained undetected for years. In fact, Kettle and the team behind the research netted over $200k in bug bounties in the course of just a couple of weeks. Desync attacks are still massively underexplored, especially on CDN-backed apps and microservices. While the rest of the crowd is spraying for XSS or hoping to bag an IDOR, you can be honing in on high-impact, high-reward request smuggling vulns.

Unmined Gold in Familiar Places.

You might think the targets you've tested aren't vulnerable due to WAFs, patches and other supposed defences. This research shows that traditional fixes can be easily bypassed by making minor tweaks to known attacks. These subtle variations can be detected much more reliably by looking for desync primitives, or the underlying parser discrepancies at the root of the issue, rather than jumping straight to firing exploits to see what sticks. That means your old targets just became a fertile hunting ground for critical vulnerabilities.

It gives you an edge.

Burp Suite's new and improved tools like HTTP Request Smuggler v3.0 and HTTP Hacker help you surface the underlying desync primitives that indicate potential request smuggling vectors. Understanding how to wield them gives you a real advantage over hunters who are still blasting outdated payloads that are blocked by superficial, fingerprint-based defences.

It reveals hidden vulnerabilities.

Some of the most successful bugs came from places you might not be testing: internal redirects, backend APIs, and edge case behaviors like handling of Expect headers. The lesson? You don't need a massive attack surface, just the right parser mismatch.

Underestimated Angles that Could Net You Bounties

Vulnerabilities beyond the application layer: These bugs live deep in the HTTP stack, between CDNs, load balancers, and backend servers. They're invisible to most tools, and often untouched by traditional bounty hunters, especially those using subpar tooling with limited support for testing beyond basic injection flaws.

New Desync Variants: The paper introduces brand new forms of request smuggling and new techniques for detecting classic desync vectors. By testing for the parsing discrepancies at the heart of the problem, rather than sending payloads, you can find swathes of request smuggling bugs that may have remained undetected until now.

Forget WAFs: Most of the affected platforms used edge protections. But regex-based defenses don't cut it when the flaw is buried in protocol-level behavior. One of the best findings came from a simple mistake that turned into control over 24 million websites via a CDN cache poisoning.

What to Do Now

Dive Into the Whitepaper

The 2025 whitepaper is packed with actionable payloads, confirmed exploit paths, and methodology that works against live targets. It's free and full of ideas that other hunters haven't caught onto yet.

Hit the Web Security Academy

In addition to the 20+ free, interactive request smuggling labs that were already available, we've just added a brand new one demonstrating one of the novel desync vectors discovered by Kettle during his research. This shows you how subtle tweaks to headers lead to major bugs. It's not just theory; you can use the same techniques on real bounty targets, potentially yielding huge payouts.

Upgrade Your Toolkit

Even if you're using Burp Community (or a "creatively sourced" Pro license) update your extensions. James's HTTP Request Smuggler has been overhauled to use his new and vastly superior primitive-level desync probes.

Revisit Old Targets

Go back to assets where you ruled out desyncs. Use the latest techniques and Burp Suite tooling to check again. You may be surprised (and rewarded!) by what you find.

Join the Desync Endgame

HTTP/1.1 is broken, but that's your opportunity: Find it. Prove it. Get paid.

The new research doesn't just hand you a few pre-canned exploits; it gives you a way to uncover the low-level parser discrepancies and visibility mismatches that sit at the root of thousands of undiscovered bugs.

Burp Suite's latest tools and techniques don't provide a fixed playbook. They help you observe, probe, and experiment with how targets actually parse requests. This means you can go beyond the known and explore new desync variants that others haven't even imagined yet.

So get out there. Tweak the tools, customize your probes, and break assumptions. Give yourself an edge that nobody else has. Desync bugs don't follow a fixed pattern; they emerge from subtle, target-specific quirks. And with the right mindset and tooling, you can discover them too, potentially bagging some serious bounties in the process.

You don't need to be a full-time researcher. You don't need a Black Hat badge. You just need curiosity, persistence, and a willingness to experiment.

Andrzej Matykiewicz

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
