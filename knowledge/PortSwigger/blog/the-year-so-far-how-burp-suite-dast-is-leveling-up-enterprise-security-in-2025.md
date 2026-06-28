# The year so far: How Burp Suite DAST is leveling up enterprise security in 2025

Source: https://portswigger.net/blog/the-year-so-far-how-burp-suite-dast-is-leveling-up-enterprise-security-in-2025
Fetched: 2026-06-28T09:15:26.368968+00:00

The year so far: How Burp Suite DAST is leveling up enterprise security in 2025

Andrzej Matykiewicz |

Thursday, 28 August 2025 at 12:07 UTC

Enterprise security teams are under more pressure than ever to secure sprawling application estates, without slowing down delivery. That's why, over the first half of 2025, we've delivered some of our biggest improvements yet to Burp Suite DAST, helping you scale testing, accelerate triage, and stay ahead of modern threats.

Whether you're already using Burp Suite DAST or evaluating options, here's a recap of what's new, and why it matters for your security maturity.

Security testing at scale, without the operational overhead

Large-scale teams told us they were spending too much time manually managing scan schedules and struggling to keep asset coverage aligned with changing environments. We listened, and delivered automation and organization tools designed to simplify scanning at scale.

These updates help you maintain consistent coverage and cut down on manual work, making it easier to stay secure as your web estate grows and evolves.

Bulk-scheduling of scans across multiple sites and folders

You can now schedule recurring scans for entire portfolios, not just individual sites, reducing admin overhead and ensuring full coverage without manual touchpoints.

Tagging for sites and folders

Custom tags now make it easier to organize, filter, and prioritize scanning across complex estates. For example, you can tag assets based on region, business unit, criticality, or whatever suits you and your team.

If you're interested in learning more about how Burp Suite DAST can help you scale your security coverage, request a demo today.

Secure modern APIs, even those with complex auth flows

As APIs become the backbone of modern applications, attackers are shifting focus. and your security testing needs to keep up. We've enhanced Burp Suite DAST to handle complex API environments effortlessly, so you can scan with confidence, at any scale.

You can now continuously scan authenticated APIs with minimal fuss, closing a gap that traditionally required manual oversight or custom workarounds.

Robust support for dynamic authentication tokens

Scans can now automatically refresh authentication tokens during scans, enabling continuous, hands-off security testing of APIs that rely on short-lived access tokens.

Postman Collection support

In addition to importing OpenAPI (Swagger) definitions and SOAP WSDLs, you can now trigger scans directly from Postman Collections, with the ability to merge them with environment variables, streamlining setup for teams already using Postman as part of their dev and QA workflows.

If you're struggling to successfully scan your sprawling APIs at the scale you need, request a demo today.

Better results, more coverage, less waiting around

Speed and coverage are core to effective DAST, but traditional scanners often make you wait or miss critical vulnerabilities in SPAs. We've overhauled the engine to crawl and audit in parallel, and to better understand dynamic front ends.

Faster scans mean quicker time-to-insight, while deeper SPA handling helps uncover more vulnerabilities in the modern front ends your users rely on.

Parallel crawl and audit

Scans now start simultaneously probing for vulnerabilities while crawling the target. This means you no longer have to wait for the crawl phase to finish before seeing any results. Not only do you benefit from massively reduced scan times, you can respond to critical threats as soon as they're identified.

Enhanced SPA coverage

We've massively improved the scanner's ability to identify and handle navigation triggered by non-standard clickable elements on the page, leading to significant improvements in ability to scan SPAs (single-page apps). The result is broader coverage and enhanced vulnerability detection in modern front-end frameworks.

Want to see Burp Suite DAST in action? Request a demo today.

Streamline remediation with enhanced Jira integration

Jira is the backbone of remediation tracking for many modern security and development teams, and we've rebuilt our integration from the ground up to meet those expectations.

Our enhanced Jira support is now fully aligned with how large-scale enterprises manage security issues in practice. From automated ticket creation to support for parent-child issue hierarchies, our goal is to make sure Burp Suite DAST fits seamlessly into your existing workflows, not the other way around.

The updates help you eliminate friction between security and development teams, improving both fix rates and the time it takes to get there.

Key improvements include:

Rule-based automation to create and update tickets at scale

Support for parent-child ticketing to reflect the structure of real-world vulnerability campaigns

Improved performance and reliability for high-volume environments

Custom field support, so security data flows through your Jira instance exactly how your teams need it

With these updates, you can be confident that your developers will receive actionable, well-structured tickets right where they expect them. No workarounds, no hacks, just tight alignment between discovery and remediation.

Get up and running faster with new onboarding and support packages

We know that getting the most out of Burp Suite DAST isn't just about having the right features; it's about getting set up for success from day one. That's why in 2025 we've launched a brand-new range of onboarding and support packages, designed to meet you exactly where you are.

Self-Serve Onboarding: Perfect for teams who prefer to move at their own pace. You'll get access to our self-serve onboarding hub, complete with step-by-step guides, product walkthroughs, and best-practice content. We'll keep an eye on your progress behind the scenes, so you can focus on moving forward at your own pace.

Standard Onboarding: A streamlined experience led by an Onboarding Specialist. Expect a kick-off call, a shared workspace packed with resources, a midpoint check-in, and a close-out session, and tailored guidance to align your setup with your goals.

Premium Onboarding: For those who want the white-glove treatment. You'll be paired with a dedicated specialist for 90 days, receive in-depth enablement sessions, a bespoke project plan, designed hand-in-hand with your team, ongoing progress reviews, and enhanced support to ensure your deployment hits every milestone.

Whether you're just starting your DAST journey or looking to scale confidently, our onboarding packages are here to shorten the learning curve, remove roadblocks, and make sure your investment delivers results fast.

Deployment flexibility for enterprise environments

Enterprises operating in highly controlled or modern IPv6 environments often need customization that one-size-fits-all DAST tools can't deliver. We've made Burp Suite DAST more adaptable than ever, without sacrificing performance.

TLS cipher suite configuration: Customize cipher groups to meet internal policies or compliance needs (e.g. in Kubernetes or self-hosted setups).

Clearer positioning, same commitment to excellence

We've rebranded the product to Burp Suite DAST, aligning the name with its core purpose: delivering dynamic application security testing at enterprise scale. While the name has changed, our focus on technical depth, usability, and best-of-breed DAST remains the same.

For more details, watch the recording of our recent webinar: Meet Burp Suite DAST

Explore what's new

These updates represent just some of what we've got planned for 2025, with even more innovation on the way. If you haven't explored these features yet, now's a great time to dive in.

Ready to see how these features can improve your security workflow? Request a demo to explore how Burp Suite DAST fits into your broader security strategy.

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
