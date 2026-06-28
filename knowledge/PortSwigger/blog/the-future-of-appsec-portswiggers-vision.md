# The Future of Application Security: key insights from the webinar

Source: https://portswigger.net/blog/the-future-of-appsec-portswiggers-vision
Fetched: 2026-06-28T09:15:25.766658+00:00

The Future of Application Security: key insights from the webinar

Tom Ryder |

Thursday, 3 April 2025 at 09:17 UTC

PortSwigger's Vision

In March, PortSwigger hosted its biggest webinar to date and the turnout spoke volumes. With over 7,500 registrants, it’s clear that the future of application security is top of mind for security professionals around the world.

We’re going to dive into the key takeaways from the session including a preview of what’s next for Burp Suite, insights into the evolving AppSec landscape, and a first look at how we’re introducing AI across our products. Whether you missed the live session or want a quick recap, read on for a closer look at the trends, tools, and tech shaping the future of secure software development.

Application security is changing fast

There’s no denying that the web application security landscape is shifting. As organizations accelerate digital transformation, the scope and complexity of modern applications is evolving faster than ever.

Source: PortSwigger, Pre-webinar survey of 582 AppSec professionals.

We asked you about the biggest challenges you’re facing in our survey before the webinar, and security teams are undoubtedly feeling the pressure. Time constraints, expanding attack surfaces, and signal-to-noise challenges are all combining to create a difficult environment for defenders. While secure coding practices remain a cornerstone of protection, they’re not enough on their own.

To keep up, organizations are rethinking their approach, moving away from siloed solutions and instead aiming to better integrate specialized tools across the application security lifecycle.

This brings us to one of the biggest conversations in security today: shift-left, and why it’s no longer enough on its own.

Shift-Left alone isn’t enough

For years, the mantra in security circles has been “shift-left”; however, as we explored in the webinar, embedding security earlier in the software development lifecycle only works if the protections hold up in production.

Source: PortSwigger, Pre-webinar survey of 582 AppSec professionals.

What teams need today is full-spectrum coverage across the software development lifecycle (SDLC) from design and threat modelling methodologies, to coding and testing, to deployment and beyond. That’s why we’re focused on solutions that scale testing across environments, without compromising signal quality.

False positives, production blind spots, and tool sprawl continue to drain security resources. The good news? Our solutions are evolving to help you tackle these issues head-on, starting with Burp Suite DAST (formerly known as Burp Suite Enterprise Edition).

Burp Suite DAST: dynamic testing that keeps pace

In fast-paced development environments, traditional testing tools can’t keep up. That’s why we’ve evolved Burp Suite DAST to help your team stay ahead of threats without slowing down delivery.

Here’s how Burp Suite DAST delivers real value where it counts:

Secure APIs with confidence

APIs are now the backbone of modern applications and one of the biggest attack surfaces. Burp Suite DAST brings native support for REST (OpenAPI/Swagger) and SOAP along with advanced authentication handling, so you can scan complex APIs with minimal setup and maximum coverage.

Scale without compromise

Whether you're scanning a handful of microservices or a sprawling application estate, Burp Suite DAST scales with you. Bulk scan scheduling, smart issue detection, and automated scope control ensure comprehensive coverage, without flooding your team with noise.

Test at the speed of DevOps

Security shouldn’t be a bottleneck. With deep integrations into tools like GitHub, GitLab, and Jenkins, Burp Suite DAST fits seamlessly into your CI/CD pipeline, so you can catch critical issues before they reach production, without interrupting the build process.

Tighten the feedback loop

Security teams need clarity, not clutter. Burp Suite DAST prioritizes high-quality results with fewer false positives, robust integrations with tools like Jira and Splunk, and upcoming features like scan freeze windows and asset tagging, helping you triage faster and act on what matters.

Built for real-world complexity

From cloud-native flexibility (SaaS, cloud, on-prem) to enterprise-grade controls, Burp Suite DAST is designed to work the way you do - no matter your infrastructure, workflows, or scale.

Looking Ahead: What’s Next for DAST?

As we look to 2025, our roadmap includes even more ways to give you control, visibility, and impact, including full issue histories, custom Jira workflows, smarter validation loops, and enhanced API authentication.

Coming soon to Burp Suite DAST

Scan freeze windows: Prevent scans during critical release windows in CI/CD.

Advanced scope control: Fine-tune what gets tested and when.

Full issue history: Track and review how issues evolve over time.

Asset tagging: Organize and prioritize scans across large environments.

Faster validation: Accelerate triage with smarter issue feedback loops.

Custom Jira workflows: Match your team’s process with better automation.

Enhanced authentication support: Including more robust API auth flows.

These enhancements help you achieve security at scale with a DAST solution designed to move at the speed of modern development, because dynamic testing should empower you to move fast and stay secure.

Automated scanning is just one piece of the puzzle. When you need deep, manual control for things like exploit validation or testing edge cases, Burp Suite Professional remains the go-to toolkit for the job.

Burp Suite Professional: still the gold standard

For hands-on security professionals, Burp Suite Professional continues to be the most powerful and customizable toolkit available for penetration testing, code review, and manual testing of web applications and APIs.

Here’s what makes it so powerful in 2025:

Rich manipulation of HTTP/1, HTTP/2, and WebSocket traffic.

Best-in-class tolls like Repeater, Intruder, and DOM Invader.

Native out-of-band testing via Burp Collaborator.

Full control through fine-grained configuration options.

We’ve also expanded extensibility through the Montoya API and Bambdas - lightweight scripting modules designed for custom automation. You can access a library of reusable scripts and write extensions faster, whether you're creating your own checks or tailoring Burp to your workflows.

Power and flexibility are core to Burp Suite Professional but we're also laser-focused on performance, scalability, and making life easier for testers. That’s exactly what our recent improvements deliver.

What’s new in Burp Suite Professional?

The past year for Burp Suite Professional has focused on three things: performance, extensibility, and ensuring we continue to provide optimal support for modern workflows.

Performance:

Faster response times across large datasets.

Lower memory usage.

UI enhancements that reduce lag and streamline interactions.

Extensibility:

Continued evolution of the Montoya API.

Bambda scripting for powerful, modular automation.

Easier authorship and sharing of internal tooling.

Modernized workflows:

Streamlined UI and polished navigation.

Fewer clicks to get where you need.

Better visibility across the testing process.

Together, these updates help security professionals work faster, reduce friction, and scale their expertise. But we’re not stopping there. The next frontier of AppSec is already here: Burp AI.

Introducing Burp AI: augmenting human expertise

One of the biggest moments in the webinar was the announcement of Burp AI, bringing AI-powered assistance to Burp Suite Professional, available now in the latest stable version of Burp Suite Professional.

Source: PortSwigger, Pre-webinar survey of 582 AppSec professionals.

But make no mistake: this isn’t about replacing human testers. It’s about augmenting them. Our AI roadmap prioritizes transparency, control, and genuine value. No buzzwords, no gimmicks - just genuine additions to the toolkit you already know and love.

Burp AI acts like a power tool for security professionals speeding up routine tasks, improving precision, and helping teams focus on what matters most.

Burp AI includes:

Explainer: Understand issues faster.

Explore Issue: Investigate root causes with AI-powered assistance.

False Positive Reduction: Greater accuracy in detecting issues like Broken Access Control.

Recorded Login Sequences: Improve scan coverage with minimal setup.

For a full look at what Burp AI includes, and how these help AppSec professionals streamline their work, check out Burp AI's capabilities.

The pre-webinar survey revealed fascinating insights into how pentesters view AI in security testing. A major theme was the importance of privacy and control, core values that Burp AI has prioritized from the very beginning, ensuring users stay fully in charge of their testing data and decisions.

We can’t do it without you

The users, the testers, the bug bounty hunters, you’re not just using Burp Suite, you’re shaping it. You’re the reason we keep raising the bar. From the feedback you share, to the creative ways you stretch our tools and your ideas that spark creativeness here at PortSwigger.

You’re the engine behind the innovation.

Every improvement we’ve made, every workflow refined and every click saved was inspired by real people, solving real problems.

So when we say we’re building the best web security tool in the world, we mean we’re building it with the best web security community in the world.

Watch the full webinar

Did you miss the live session? Watch it on demand now to dive deeper into our plans and product updates.

Watch the webinar now

The future of application security

The world of application security is changing fast, but PortSwigger’s mission remains the same: to enable the world to secure the web.

We’re doing that by evolving our tools, expanding our capabilities, and listening closely to the needs of our community.

With powerful tools like Burp Suite DAST, Burp Suite Professional, and now Burp AI, we’re helping teams test deeper, scan smarter, and stay ahead of emerging threats without compromising on quality or control.

Stay tuned. The future of AppSec is here and we’re building it together.

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
