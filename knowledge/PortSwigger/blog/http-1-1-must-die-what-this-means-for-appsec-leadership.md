# HTTP/1.1 Must Die: What This Means for AppSec Leadership

Source: https://portswigger.net/blog/http-1-1-must-die-what-this-means-for-appsec-leadership
Fetched: 2026-06-28T09:15:17.128038+00:00

HTTP/1.1 Must Die: What This Means for AppSec Leadership

Andrzej Matykiewicz |

Wednesday, 6 August 2025 at 22:23 UTC

At Black Hat USA and DEFCON 2025, PortSwigger's Director of Research, James Kettle, issued a stark warning: request smuggling isn't dying out, it's evolving and thriving.

Despite years of defensive efforts, new research unveiled by Kettle proves that HTTP request smuggling (or "desync" attacks) remains a systemic, protocol-level threat, compromising tens of millions of supposedly well-secured websites worldwide.

In his groundbreaking new research, HTTP/1.1 Must Die: The Desync Endgame, Kettle challenges the security community to completely rethink its approach to request smuggling. He argues that, in practical terms, it's nigh on impossible to consistently and reliably determine the boundaries between HTTP/1.1 requests, especially when implemented across the chains of interconnected systems that comprise modern web architectures. Mistakes such as parsing discrepancies are inevitable, and when using upstream HTTP/1.1, even the tiniest of bugs often have critical security impact, including complete site takeover.

This research demonstrates unequivocally that patching individual implementations will never be enough to eliminate the threat of request smuggling. Using upstream HTTP/2 offers a robust solution.

If we are serious about securing the modern web, it's time to retire HTTP/1.1 for good.

In the meantime, audit your portfolio using the only DAST scanner capable of reliably testing for desync vulnerabilities: Burp Suite DAST.

Widespread Exposure with Critical Consequences

Desync attacks exploit the ambiguity in HTTP/1.1 parsing to hijack sessions, poison caches, and leak user data. What's now clear is that HTTP/1.1's core design, with its lenient text-based message parsing, multiple length-specification mechanisms, and decades-old compatibility quirks, make it impossible to defend reliably.

PortSwigger's 2025 research demonstrates how supposedly "patched" systems, including those protected by major CDNs and WAFs, are still vulnerable on a widespread scale. This isn't an academic risk; the research team were awarded over $200,000 in bug bounties from these techniques over just two weeks, proving that several major CDNs were vulnerable, potentially compromising every one of their 24m customers' web infrastructure. This only serves to highlight the prevalence and severity of the problem.

For AppSec leaders, this presents a strategic concern: even if your organization believes it's covered, you may be relying on brittle defenses and dangerous assumptions that simply don't stand up to scrutiny.

Complacency is the Enemy

You may have implemented the available defensive measures and patched request smuggling bugs over the years as new vectors are discovered. But the attack class hasn't gone away; it's simply evolved. PortSwigger's latest research reveals that desync vulnerabilities are still extremely prevalent, especially where systems quietly downgrade HTTP/2 to HTTP/1.1 behind the scenes, adding yet more complexity and ambiguity that can potentially be exploited.

Key takeaways:

If you use HTTP/1.1 anywhere in your architecture you may be at risk.

Supposedly mature defenses often rely on regex-based heuristics or input sanitization that fail to provide any protection whatsoever against novel payloads and desync variants. In fact, they merely mask the problem by preventing standard detection techniques.

Downgrade scenarios are especially dangerous. Many systems appear to use HTTP/2 but secretly rely on vulnerable HTTP/1.1 internally, including some CDNs that claim to provide end-to-end HTTP/2 support.

What Security Leaders Should Do Next

AppSec leaders are in a unique position to drive meaningful change. Here's what we recommend:

Audit for desync exposure: Conduct a protocol-layer audit to locate legacy HTTP/1.1 dependencies. Use tooling like Burp Suite's HTTP Request Smuggler and HTTP Hacker to identify parser discrepancies, or scan your estate at scale with Burp Suite DAST; the only DAST scanner capable of genuine automated detection of the latest request smuggling threats.

Revise threat models: Include request smuggling and desync attacks explicitly in your threat models and pentesting checklists. Many organizations deprioritized this class of vulnerability due to a lack of deep understanding and an overreliance on heavily flawed defences.

Upskill your team: Equip your pentesters and developers with training. PortSwigger's Web Security Academy provides free educational resources and over 20 request smuggling labs, including a new one demonstrating a practical 0.CL attack first discovered as part of our 2025 research.

Start planning your HTTP/1.1 exit strategy: The only real fix is eliminating HTTP/1.1 altogether. Start roadmapping a phased deprecation, particularly for internal connections and APIs.

Pressure your vendors: If you rely on third-party infrastructure, such as a CDN, ask whether they support upstream HTTP/2 and if not, when they will.

Rethinking Security Strategy

The implications go beyond bug fixes. As Kettle writes, "You've got the illusion of security thanks to toy mitigations and selective hardening that only serves to break the established detection methodology. In truth, HTTP/1.1 is so densely packed with critical vulnerabilities, you can literally find them by mistake."

Protecting your systems now means acknowledging that the protocol itself is broken.

This demands a shift in mindset:

From reactive patching to protocol modernization.

From trusting legacy defenses to verifying parser consistency.

From app-layer focus to cross-layer coordination between security, engineering, and infrastructure teams.

How PortSwigger Can Help

PortSwigger isn't just raising the alarm; we're arming defenders with the tools to act:

Burp Suite offers unmatched desync detection and exploration capabilities, thanks to rich HTTP/1 and HTTP/2 support, HTTP Request Smuggler and the new HTTP Hacker extensions. This ensures your expert pentesters aren't shackled by subpar tooling with superficial support for testing anything beyond simple, application-level issues.

DAST at scale: Burp Suite DAST identifies request smuggling vectors across your estate using reliable, primitive-level detection techniques that bypass flawed defences and reveal the true extent of your exposure to desync attacks.

Education-first: Our free labs and industry-defining research translate cutting-edge insights into actionable training.

Join the Desync Endgame

Ignoring HTTP/1.1's flaws is no longer an option. As an AppSec leader, you have the opportunity, and the responsibility, to lead the transition toward safer infrastructure.

Scan your apps. Prove the risk. Demand better infrastructure.

Join us in declaring: HTTP/1.1 must die.

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
