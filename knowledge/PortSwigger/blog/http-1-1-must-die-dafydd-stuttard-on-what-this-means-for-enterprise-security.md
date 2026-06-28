# HTTP/1.1 must die: Dafydd Stuttard on what this means for enterprise security

Source: https://portswigger.net/blog/http-1-1-must-die-dafydd-stuttard-on-what-this-means-for-enterprise-security
Fetched: 2026-06-28T09:15:16.709122+00:00

HTTP/1.1 must die: Dafydd Stuttard on what this means for enterprise security

Andrzej Matykiewicz |

Thursday, 9 October 2025 at 14:06 UTC

At Black Hat USA 2025 and DEF CON 33, PortSwigger's Director of Research, James Kettle, unveiled new HTTP desync techniques that prove one thing beyond doubt: HTTP/1.1 is broken, and every organization still relying on it is at risk.

To understand what this means for enterprises, we spoke to Dafydd Stuttard, creator of Burp Suite, PortSwigger CEO, and author of the seminal Web Application Hacker's Handbook. His message to security leaders is clear: "If there's any HTTP/1.1 hop in your stack, assume you're vulnerable.”

Why should security leaders still care about "old” protocol flaws in 2025?

I think the first thing I'd say is that they're not "old” at all; they're very much alive. HTTP/1.1 is still used for around half of internet traffic today. The protocol itself is old, and was designed for a different internet, one that didn't anticipate today's sprawling, layered infrastructures. When you chain CDNs, proxies, and app servers together, subtle disagreements in how they handle requests become inevitable.

This is especially true with HTTP/1.1 as it's an inherently text-based protocol. As a result, each system that interacts with the traffic must independently parse a stream of bytes to identify distinct HTTP messages and any relevant data encoded within them. Doing this consistently is notoriously challenging, especially in a world where third-party services and the associated infrastructure are so prevalent.

Where exactly is the weak link?

It's often not where people think. The connection between a browser and the edge is usually solid: it's encrypted, and HTTP/2 is widely supported. The real danger lurks upstream, in the conversations between your CDN and your origin, your proxy and your application server, or even between internal microservices.

If any of those hops still use HTTP/1.1, you're exposed. That's why this isn't a "bug” in the traditional sense. It's not something you can patch and move on. It's an architectural flaw, and the only real fix is to eliminate HTTP/1.1 altogether.

The uncomfortable truth is that many seemingly HTTP/2+ services, including major CDNs, downgrade HTTP/2 traffic sent by clients to HTTP/1.1 internally. If your infrastructure downgrades to HTTP/1.1 anywhere upstream of the front-end webserver, you've not only reopened the door to desync attacks, you've in fact made the threat even worse.

This downgrading often occurs within third-party infrastructure, and you may not even have the option to disable it. Why not? Because vendors need backwards compatibility with legacy systems still used by a significant proportion of their customers. I think James puts it best in his research paper, noting that "an overlooked danger with adopting cloud-based proxies is that you're effectively implementing another company's tech debt into your own security posture".

What makes this especially dangerous for large organizations?

For enterprises, the challenge is scale and complexity. You're not just running a web application, you're orchestrating an entire ecosystem: multiple CDNs, layered reverse proxies, service meshes, microservices, APIs, and these are often from a range of different vendors. That complexity is fertile ground for hard-to-spot, protocol-level issues that often have critical implications for your security.

In a large organization, a single successful desync attack isn't just about hijacking one user session. It's about exposure at scale — leaked credentials, stolen data, injected malicious content, trust undermined across your entire platform. For an attacker, that's a goldmine. For you, it's a systemic business risk.

To put things in perspective, James and his collaborators netted over $350k in bug bounties during this year's research after compromising virtually every customer of several major CDNs - a total of around 30 million websites. This only serves to highlight both the severity and persistence of these issues, despite years of supposed hardening.

What's the real business risk if organizations don't act?

The risk is that attackers gain site-wide compromise. With HTTP desync (AKA request smuggling) attacks, an attacker can manipulate the way servers handle traffic, which opens up a range of serious outcomes: stealing active sessions, intercepting sensitive responses belonging to other users, or injecting malicious code that affects users at scale.

It's the kind of vulnerability that doesn't just hit your security posture, it hits customer trust, compliance obligations, and ultimately, the reputation of your business.

Do you think most organizations are underestimating this?

Almost certainly. Request smuggling hasn't historically had the same visibility as SQL injection or cross-site scripting, despite its potential for similar impact. And because the problem often originates outside the enterprise in vendor-managed infrastructure, it's easy for leaders to overlook it. There's often an assumption that standard, widely used technologies from leading vendors are secure by default.

But James's latest research shows that this assumption is dangerous. Even when cloud providers advertise HTTP/2 support, many quietly downgrade to HTTP/1.1 internally. That means vulnerabilities can resurface in places you assumed were safe.

What happens if HTTP/1.1 continues to persist in upstream connections?

Then the cycle continues: patches, bypasses, and rediscoveries. History shows that ad-hoc mitigations don't solve the underlying flaw. Attackers simply adapt and route around them. As long as HTTP/1.1 remains in play, the problem isn't going away.

That's why we launched the HTTP/1.1 must die campaign. This isn't about treating request smuggling as just another bug class. It's about recognizing that the protocol itself is broken for modern use, and treating its removal as a strategic priority.

Who needs to take responsibility for fixing this?

There are three groups here.

Vendors, including cloud providers and CDNs, need to make it possible, and straightforward, to disable HTTP/1.1 on every upstream connection. Right now, some don't.

Researchers need to keep shining a light on these issues, both with new techniques and with tooling that lets defenders detect them. James's whitepaper suggests several potential avenues to explore, and his open-source HTTP Request Smuggler extension for Burp Suite provides a solid base for you to build on.

Enterprises need to examine their own environments with proper scanning, understand exactly where the cracks are, and hold their vendors accountable for closing them where necessary.

Why is Burp Suite uniquely suited to detecting this?

Burp is different because it implements its own HTTP stack. That means it can manipulate requests at the protocol level in ways other tools can't, and that's exactly what you need to uncover request smuggling.

We've also used James's brand new detection methodology to build capabilities into both the manual tools and automated scanning in Burp Suite Professional and Burp Suite DAST, so organizations can both explore edge cases and run repeatable tests across their environments. No other tool is able to detect request smuggling vulnerabilities anywhere near as effectively, if at all.

How can leaders know whether their vendors and partners are really protecting them?

The only reliable way today is to test. Run scans with the latest version of Burp Suite and James's HTTP Request Smuggler extension to see if you're exposed, and use the manual tools to validate findings. For larger estates, Burp Suite DAST is uniquely capable of testing for desync vulnerabilities at enterprise scale.

Configuration-based assurances may become realistic in the future as vendors mature, but we're not there yet. Right now, continual testing with state-of-the-art tooling is the only way to cut through assumptions and see reality.

What's the immediate value to leadership in doing this?

Clarity. You get fast, concrete answers to the questions that matter most: Are we vulnerable? Where? How bad is it? That gives you the ability to prioritize fixes, escalate issues with your vendors, and then re-test to confirm improvements. It's a clear feedback loop that moves this from unknown risk to measurable progress.

What's the single most important piece of advice for CISOs planning their HTTP/1.1 exit?

Think end-to-end. The fix isn't partial — it has to be pervasive. Every endpoint, every hop, every layer of your infrastructure needs to move beyond HTTP/1.1.

And recognize that most of your current AppSec tooling — SAST, SCA, traditional DAST — isn't even looking in the right place. This is a transport-layer flaw. You need tools and processes that can probe at that level, and you need the organizational will to make sure HTTP/1.1 really does die across your estate.

What security leaders should do now

Map your reality. Inventory every upstream connection — CDN to origin, proxy to app, service to service — and identify where HTTP/1.1 is still in use.

Set a no-HTTP/1.1 policy. Require HTTP/2 or higher everywhere, and hold vendors accountable for providing it.

Test like an attacker. Use Burp Suite to scan your applications and validate exposure at the protocol level. Use Burp Suite DAST to scan your portfolio at scale, and validate the results in Burp Suite Professional.

Institutionalize it. Build checks into architecture reviews, onboarding processes, and vendor assessments so HTTP/1 doesn't creep back in.

Closing thought

As Dafydd puts it: "This isn't just another bug you can patch. It's an architectural flaw that requires deliberate elimination. If you still have HTTP/1.1 in your stack, assume you're exposed.”

Additional resources

HTTP/1.1 must die campaign hub

Research whitepaper

The desync delusion: Are you really protected against HTTP request smuggling?

HTTP Request Smuggler

Web Security Academy: HTTP request smuggling

How to join the desync endgame: Practical tips from pentester Tom Stacey

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
