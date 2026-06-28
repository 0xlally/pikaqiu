# Burp Suite Enterprise Edition spring update 2024

Source: https://portswigger.net/blog/burp-suite-enterprise-edition-spring-update-2024
Fetched: 2026-06-28T09:15:09.834326+00:00

Burp Suite Enterprise Edition spring update 2024

Amelia Coen |

Thursday, 16 May 2024 at 13:31 UTC

We understand the unique challenges AppSec teams face—from navigating the rapid pace of development to achieving comprehensive coverage against new vulnerabilities. That’s why we’ve focused our latest updates on not just improving the automated testing capabilities of Burp Suite Enterprise Edition, but also on simplifying and enhancing workflows for you and your teams.

Here's what we've recently released in Burp Suite Enterprise Edition...

At a glance:

Burp Suite Enterprise Edition in the Cloud

Custom scan checks

CI-driven scans

Scanning performance improvements

ISO 27001 2022

Coming soon in 2024

Burp Suite - now available in the Cloud

Burp Suite Enterprise Edition is now available in PortSwigger’s secure cloud.

Your team can now scale up your scanning efforts with automated, scheduled DAST scans, without the need to host and maintain your own infrastructure.

This new Cloud-based version enables you to:

Scan your applications like an actual attacker would.

Set up recurring, scheduled scans within minutes.

Share access and reports easily with all of your team.

Read full details in our launch blog post.

Being able to scan unlimited sites is very generous. I'm used to getting a maximum of 5 or 6 applications when we have tried other products. Unlimited is really nice!

A major UK-based university

Want a free trial of Burp Suite Enterprise Edition in the Cloud?

Book a call with one of our Enterprise Experts, and we’ll get you set up with a free trial of the new Cloud version for you and your team.

Custom scan checks

Building on the extensibility added to Burp Suite Professional, you can now import custom scan checks created in Burp Suite Professional into Burp Suite Enterprise Edition.

Custom scan checks - BChecks - enable you to extend Burp Scanner in a quick and simple way. Tailor scans to your own applications’ framework, and achieve targeted coverage for new and novel vulnerabilities.

When we came across [BChecks], we were just like, hey, this is this little nugget of awesome power and we can immediately start to see how we can use something like this across a massive scale.

Nicholas Anastasi, Sprocket Security

Take a look at our extensive GitHub repository of community-created scan checks, which can also be imported into Burp Suite Enterprise Edition.

Read more about custom scan checks here.

CI-driven scans

Preventing vulnerable apps from hitting production is one of the biggest AppSec challenges - we’re aiming to make this much easier with CI-driven scans.

It’s now quick and easy to integrate automated, scheduled DAST scans with any CI/CD platform. This enables you to get fast security feedback to your web developers - saving on time and costs, while keeping your web estate more secure.

You can choose to digest results in our centralized dashboard, or use our GraphQL API to import the results into your vulnerability management platform.

Learn more in our documentation.

Scanning performance improvements

There's also been improvements made to scanning performance recently, including:

Reducing the number of browsers that Burp Scanner creates during the audit phase, making scans more memory efficient.

Further improvements in memory usage for browser-powered scans.

Improved Burp’s ability to identify - and disregard - duplicate items in different areas of applications during scans.

These improvements are all designed to make Burp Scanner faster, more efficient, and more accurate than ever before.

ISO 27001 2022

We’re delighted to announce we have recently acquired a certification of compliance with ISO 27001 2022.

Compliance with these international standards is evidence of PortSwigger’s ongoing commitment to ensuring information security is at the forefront of our organization.

Coming soon in 2024

Improved API testing capabilities

Burp Suite Enterprise Edition will have the ability to ingest an API definition to seed scans from an uploaded API. This will allow you to properly scan APIs that lack a hosted definition, and also scan a specific API - ignoring the rest of the application it’s attached to.

You’ll also be able to upload and scan API specifications with authentication, improving the overall depth of your scan.

WebSockets support

Burp Suite Enterprise Edition is expanding its scanning capabilities to support applications that depend on WebSockets. This will ensure real-time comprehensive coverage when identifying vulnerabilities in applications that use WebSockets communications to operate.

Continued improvements to scanner performance

There will be further improvements made to scan performance. We aim to make scans achieve a greater level of coverage, and prioritise finding the important vulnerabilities earlier in your scan so that you can see the information that matters to you the most quicker.

Scan for web cache deception vulnerabilities

There will be a new scan check added to Burp Scanner that will allow you to test for web cache deception vulnerabilities without the need to write an extension or conduct manual exploration. This will help you ensure attackers can’t access any sensitive information from your web cache.

We plan to continue adding new scan checks to Burp Scanner in the future.

Multi-factor authentication

To help you meet your compliance requirements, Burp Suite Enterprise Edition will soon support multi-factor authentication. Use an authentication app to further strengthen your access with MFA.

Increased integration between Burp Suite Professional and Burp Suite Enterprise Edition

With the recent launch of BChecks, you can now create specific scan checks in Burp Suite Professional, and scan your entire web app portfolio with them using Burp Suite Enterprise Edition. But we’re just getting started with how our tools can seamlessly integrate.

You can expect to see more workflow improvements between our two tools - watch this space!

Want to speak with our Enterprise Experts?

If you’d like to hear more about Burp Suite Enterprise Edition, feel free to reach out to us.

You can either book a call directly with one of our team, or email us with any specific questions you might have: hello@portswigger.net

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
