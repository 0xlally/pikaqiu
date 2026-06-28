# Meet Burp Suite DAST: Your questions answered

Source: https://portswigger.net/blog/meet-burp-suite-dast-your-questions-answered
Fetched: 2026-06-28T09:15:19.629783+00:00

Meet Burp Suite DAST: Your questions answered

Andrzej Matykiewicz |

Thursday, 29 May 2025 at 09:29 UTC

We recently hosted a webinar to introduce Burp Suite DAST, the new name for Burp Suite Enterprise Edition, the best-in-class, automated web application and API security scanning solution for modern AppSec teams at any scale.

We were thrilled to see the high level of engagement and insightful questions from the thousands of attendees from across the AppSec industry. In this post, we'll answer some of the most frequently asked questions from the webinar.

Why have you changed the name to Burp Suite DAST?

How does Burp Suite DAST complement Burp Suite Professional?

How does Burp Suite DAST perform with larger web estates comprising hundreds of apps?

Can it also scan my APIs?

How does Burp Suite DAST integrate with the other tools in my AppSec workflow?

Can I use Burp Suite DAST to run vulnerability scans from my CI/CD pipeline?

Does Burp Suite DAST come with additional capabilities?

What's on the roadmap for Burp Suite DAST?

What onboarding and support are available?

Can I use my existing extensions from Burp Suite Professional in Burp Suite DAST?

What next?

Watch the full webinar

Honorable mention

Why have you changed the name to Burp Suite DAST?

The transition from "Burp Suite Enterprise Edition" to "Burp Suite DAST" was driven by the need for clarity and precision in conveying the product's purpose. The previous name often led to confusion, with some assuming it was merely a multi-user version of Burp Suite Professional. As a result, some organizations were unaware that we offered a distinct, but complementary DAST solution to sit alongside Burp Suite Professional and they've been needlessly putting up with subpar DAST scanners for years.

By adopting the name "Burp Suite DAST", we aim to alleviate this confusion and more clearly articulate the product's core value: a scalable, automated solution for dynamic application security testing that integrates seamlessly with the tools your team are already using, including Burp Suite Professional. This change ensures that potential users immediately recognize the product's role in their security stack, especially when evaluating DAST solutions to enhance their broader security strategies or integrate automated security testing into their CI/CD pipelines.

Burp Suite DAST continues to be powered by the same industry-leading scanning engine trusted by over 17,000 organizations, including SAP, Microsoft, and Mastercard, and we have ambitious plans to further optimize our solution for organizations at any scale.

How does Burp Suite DAST complement Burp Suite Professional?

Burp Suite DAST and Burp Suite Professional are built to work together. Burp Suite DAST handles automated, scheduled scanning at scale, helping teams identify potential vulnerabilities across their web estate. Security teams can then use Burp Suite Professional to dive deeper, validating issues, eliminating false positives, and crafting detailed remediation advice. This workflow ensures efficient use of time and resources.

No other DAST vendor offers a complementary manual testing toolkit, and your manual testers are almost certainly using Burp Suite Professional already. So if you're not familiar with Burp Suite DAST, now is the perfect time to see how you can level up your AppSec by bridging the gap between automation and manual testing.

How does Burp Suite DAST perform with larger web estates comprising hundreds of apps?

For organizations with large web estates, Burp Suite DAST scales seamlessly to scan thousands of applications. Supporting large web estates has been a key focus over the last six months, with a number of improvements introduced explicitly targeting enhanced performance for customers scanning hundreds of apps. These include:

Bulk scheduling of scans

Bulk management of APIs

Optimized CI/CD integration

Faster scan throughput, with intelligent audit item prioritization and parallel crawl and audit phases

These features make it ideal for enterprises looking to integrate security into their DevSecOps processes.

Can Burp Suite DAST scan my APIs?

Yes. We know that API security is a top priority for AppSec teams everywhere and this is another core focus area for our engineering teams. Burp Suite DAST can scan APIs either as part of a broader web app scan, or in isolation.

It currently supports the following formats for API targets:

Postman Collection

OpenAPI

SOAP

GraphQL

Burp Suite DAST is able to reliably handle authenticated scanning of APIs. We support authentication via both static and dynamic refresh token flows, offering flexibility for complex environments.

How does Burp Suite DAST integrate with the other tools in my AppSec workflow?

We've expanded our ecosystem to integrate seamlessly with the tools your teams already use. We provide a range of native integrations, as well as a powerful GraphQL API for custom integrations with whatever tools your organization currently uses. These include:

Ticketing platforms like Jira, Trello, GitLab

ASPMs, such as ArmorCode

VMS and SIEM platforms like Splunk

Collaboration tools like Slack

Identity and access management solutions via LDAP, SCIM, SAML, and more

These integrations streamline reporting, triage, and remediation workflows.

Can I use Burp Suite DAST to run vulnerability scans from my CI/CD pipeline?

Absolutely. In addition to scheduling recurring scans of your apps and APIs, you can easily integrate scans into your existing CI/CD pipelines, regardless of which platform you use.

With built-in configurations optimized for CI-driven scanning and highly granular customization options, you can set up your scans to fail the build based on issue count, severity, and confidence levels, ensuring you cut out vulnerabilities before they make it into your core branches.

Our platform-agnostic CI/CD integration also enables you to consume the scan results either directly in the pipeline, through the same dashboard as your regular scans, or via your existing vulnerability management platform.

With detailed remediation advice and reference material from the Web Security Academy, CAPEC, and CWEs, Burp Suite DAST also empowers your developers to resolve basic issues for themselves, freeing up your expert manual testers to focus on the complex problems that require their expertise.

Does Burp Suite DAST come with additional capabilities?

Burp Suite DAST is just a new, clearer name for Burp Suite Enterprise Edition. However, even if you evaluated Burp Suite Enterprise Edition previously, over the past year or so, we've incorporated several major upgrades based on the following key themes:

Enhanced scalability: Handle vast estates with bulk scheduling and customized CI/CD scans.

Faster vulnerability detection: Improved scanning engine performance through parallel crawl and audit phases and intelligent prioritization of audit items.

Native API scanning: Scan Postman Collections, OpenAPI, SOAP, and GraphQL with native support for the most common authentication methods, including those that rely on dynamic tokens that need to be refreshed mid-scan.

Expanded integrations: Better visibility, issue management, and enhanced connections with tools like Jira, Splunk, and more.

What's on the roadmap for Burp Suite DAST?

Looking ahead to 2025, our roadmap includes a number enhancements designed to further optimize Burp Suite DAST for modern AppSec teams to streamline their workflows. These include:

Asset tagging

Scan freeze windows

Enhanced authentication

Simplified scope control

Full issue history and enhanced issue management features

These features are designed to help you gain more control, visibility, and efficiency in remediating issues.

What onboarding and support are available?

We offer both standard and premium onboarding packages:

Standard: Includes a dedicated Customer Success Manager (CSM), collaborative onboarding workspace, and goal-oriented rollout planning.

Premium: Adds bespoke engagement, module-based training, and flexible check-in cadences. These options ensure you get the most value from Burp Suite DAST, tailored to your organization's needs.

Can I use my existing extensions from Burp Suite Professional in Burp Suite DAST?

Yes - Burp Suite DAST and Burp Suite Professional are both built on the same underlying scanning engine. This means you can reuse your existing scan configurations, custom scan checks, and scanning extensions from Burp Suite Professional.

What next?

Thanks to everyone who joined us for the webinar. We're excited to help you scale your application security testing with Burp Suite DAST.

Got more questions or want to see it in action? Book a personalized call.

Watch the full webinar

Did you miss the live session? All registrants will receive a full recording via email and we'll upload this to the website shortly for everyone else.

Honorable mention

Not strictly a question, but we very much appreciated this suggestion from one attendee:

Drink every time the presenter strokes his beard pensively.

After a quick research spike, we were unable to validate the efficacy of this novel approach to application security and the initial data doesn't look promising. We may look into this again in future but, for now, further R&D in this area has been shelved.

If you've got any other suggestions, or just want to hang out with PortSwigger researchers, developers, as well as the largest community of AppSec pros and enthusiasts, join the PortSwigger Discord server.

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
