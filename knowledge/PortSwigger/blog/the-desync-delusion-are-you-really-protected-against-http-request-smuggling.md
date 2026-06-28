# The Desync Delusion: Are You Really Protected Against HTTP Request Smuggling?

Source: https://portswigger.net/blog/the-desync-delusion-are-you-really-protected-against-http-request-smuggling
Fetched: 2026-06-28T09:15:25.311465+00:00

The Desync Delusion: Are You Really Protected Against HTTP Request Smuggling?

Andrzej Matykiewicz |

Wednesday, 6 August 2025 at 22:22 UTC

The Hidden Threat That's Slipping Past Your Security

HTTP request smuggling remains one of the most dangerous yet frequently overlooked web vulnerabilities today. Despite being a widely known issue since 2019, traditional Dynamic Application Security Testing (DAST) tools barely scratch the surface, leaving critical blind spots in many enterprise environments. Vendors often claim to offer comprehensive desync detection, but what does that really mean?

Most DAST tools depend on pre-canned payloads, targeting simple desync vectors like CL.TE or TE.CL, or worse, merely fingerprinting specific CVEs. These simplistic methods primarily identify common, well-known attack scenarios but utterly fail to detect the more complex or novel desync variations that could still be wide open to exploitation by attackers.

Burp Suite DAST changes this entirely. Developed in close collaboration with James "albinowax" Kettle, the leading expert in request smuggling research, Burp Suite DAST is currently the only enterprise-grade solution capable of comprehensive, scalable HTTP request smuggling detection.

Why Other DAST Tools Fall Short

Many enterprise-grade DAST solutions, from open-source scanners to heavyweight AST platforms, claim to offer automated HTTP request smuggling detection. Yet our analysis reveals some common shortcomings:

Highly brittle, pre-canned detection methods: Often rely on basic regexes detecting obvious header obfuscation or spraying well-known exploits to identify vulnerabilities.

Tunnel vision for CVEs: Detection typically targets specific platform versions or known misconfigurations, not underlying flaws, resulting in massive blindspots to the nuances of different server or proxy implementations.

Blind to HTTP downgrade vectors: Rarely testing HTTP/2, and even fewer handling downgrade scenarios between protocols.

Some tools simply test a single, request smuggling scenario, look for a timeout or basic error, then stop. This approach is a blunt instrument that simply fails against today's evolving threats.

Burp Suite DAST: Request Smuggling Detection Reinvented, for the Scale You Need

Burp Suite DAST doesn't rely on simplistic signatures. Instead, it probes deeper into desync primitives—the foundational parsing discrepancies between front-end and back-end servers that enable request smuggling in the first place.

This method:

Identifies vulnerabilities by performing automated analysis at the root-cause level, not just superficial symptoms.

Provides clues about the presence of as-yet-unknown attack vectors.

Significantly reduces false positives and false negatives caused by fundamentally flawed mitigation attempts.

This revolutionary approach, driven by PortSwigger's groundbreaking research, represents a complete shift in detection strategy. Instead of merely verifying known payloads, Burp Suite DAST automatically analyses parsing discrepancies unique to your infrastructure, identifying the root cause of desync vulnerabilities. This approach enables significantly more reliable detection of dangerous parsing behavior and potential request smuggling vulnerabilities that may have remained undetected in your systems for years.

Backed by the World's Leading Authority on Desync Attacks

James Kettle, PortSwigger's Director of Research, introduced HTTP request smuggling to the broader security community in 2019 and continues to redefine the landscape. His latest 2025 Black Hat and DEF CON talks introduced entirely new classes of desync attacks and advanced detection techniques. As Burp Suite DAST aligns directly with this cutting-edge research, its smuggling detection capabilities consistently outpace the industry.

While other tools scramble to catch up, Burp Suite DAST continuously integrates fresh detection logic in parallel with ongoing research developments, enabling you to scan your estate, at any scale, the moment new threats are revealed.

The Only True Choice for Comprehensive Coverage

Request smuggling is an insidious threat that easily evades conventional testing. If you're tasked with securing complex web apps, especially those involving layered proxies, cloud edge networks, or mixed HTTP protocols, superficial coverage is not enough. Even tools boasting robust automation features can't match Burp's ability to identify a target's unique HTTP parsing quirks and the resulting weaknesses.

Burp Suite DAST stands alone as the only research-grade, enterprise-ready tool capable of robust, automated request smuggling detection. With Burp, you're equipped not only to find vulnerabilities others miss but to proactively secure your infrastructure against emerging threats.

Burp doesn't just find the vulnerabilities others miss; it's designed to be the first tool that can.

Keep Up with the Next Wave of Desync Attacks

Burp Suite DAST already anticipates future desync threats. As James Kettle unveils new vulnerabilities at Black Hat 2025, Burp Suite DAST is prepared.

Is your current DAST solution?

Read our technical whitepaper to learn more about the state of request smuggling in 2025.

Ready to experience the difference firsthand? Request a demo today.

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
