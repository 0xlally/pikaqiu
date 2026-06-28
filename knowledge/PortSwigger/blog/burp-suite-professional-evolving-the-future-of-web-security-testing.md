# Burp Suite Professional - evolving the future of web security testing

Source: https://portswigger.net/blog/burp-suite-professional-evolving-the-future-of-web-security-testing
Fetched: 2026-06-28T09:15:10.280907+00:00

Burp Suite Professional - evolving the future of web security testing

Dayna Shoemaker |

Tuesday, 15 December 2020 at 15:58 UTC

With every new release of Burp Suite Professional, we bake in the latest research findings to ensure that you are able to catch vulnerabilities, faster. We always recommend updating to the latest version to get the most out of the product and our groundbreaking research. The product has made leaps and bounds since version 1.7 and Burp Suite 2.0, which launched in 2018. This blog post covers the following recent additions to Burp Suite Professional, all of which have been introduced in 2020:

Browser-powered scanning.

Recorded login sequences.

API vulnerability scanning.

HTTP Message improvements.

Cache poisoning vulnerability checks.

HTTP/2 Support.

Here are some of the latest and greatest features that our customers are using to increase penetration testing productivity, agility, and reliability:

Browser-powered scanning

Burp Scanner sits at the heart of Burp Suite and is tried, tested, and trusted by over 51k users. Burp Scanner continued its long tradition of innovation this year - with the addition of browser-powered scanning.

Burp Scanner can now use an

embedded, pre-configured Chromium browser to crawl and audit sites. This allows it to fully render applications - "seeing" content exactly as a user would. Because of this, Burp Suite is now able to crawl apps that make heavy use of JavaScript. This really is a huge step forward - both for automated vulnerability scanners and for the industry in general.

Behind all our innovations stands considerable research and expertise. We've invested a great deal of time making browser-powered scanning reliable - and this is a continuous process. Browser-powered scanning is foundational to a number of Burp Scanner enhancements - including

recorded logins - and in future, will allow further improvements in coverage for single page web apps.

Recorded login sequencesA known - and painful - limitation to many automated testing is the inability to authenticate to target web apps for scanning due to them having complex login sequences. We have released new functionality to help address this challenge for users of Burp Suite Professional.

You can now

record login sequences using a dedicated browser plugin. This information can then be passed through to Burp Suite - giving access to your application and allowing Burp Scanner to check for vulnerabilities. With the problem of complex login sequences solved, you can further automate scanning, saving you time to focus on deep manual penetration testing.

API vulnerability scanningAPIs represent a huge attack surface for many organizations.

Gartner predicts that by 2022, API abuses will be the most-frequent attack vector resulting in data breaches for enterprise applications.

In line with our mission to help you secure the web, PortSwigger plans to support the

security testing of APIs and microservices to cover even more of your web application portfolio.

November’s

2020.11 Burp Suite Professional release includes the ability to scan both JSON and YAML-based APIs for vulnerabilities, supporting the OpenAPI (/Swagger) version 3 specification.

We will be expanding our support for enumerating API endpoints, so please let our team know your feedback and requirements.

UI improvementsThe message editor is used throughout Burp Suite for viewing and manipulating HTTP requests and responses, as well as WebSocket messages. This tool comes with a number of features to help you edit and analyze messages. Throughout the year we have made a number of changes and improvements to the messaging capabilities, including:

Introducing the inspector which streamlines workflows especially working with encoded data.

Rendering non-printing characters in the Burp Suite message editor.

Syntax highlighting and pretty-printing of data in the HTTP message editor.

Message editor UI improvements to simplify functionality.

By popular demand we have also improved light and dark themes.

Cache poisoning vulnerability checksAt PortSwigger, we are proud of our

world-renowned research team. They are constantly hunting for undiscovered vulnerabilities and new innovative ways of exploiting them. When it comes to product development we use a research-led approach to ensure that you can test applications for the latest vulnerabilities. Following James Kettle’s "Web Cache Entanglement: Novel Pathways to Poisoning" research presented at BlackHat USA 2020, Burp Scanner can now identify a variety of recently discovered cache poisoning issues. To hone your skills, why not check our labs on this topic on the Web Security Academy.

HTTP/2 Support (experimental)HTTP/2 significantly revised the HTTP protocol principally to improve performance.

Experimental HTTP/2 support was added to Burp which enables testing of sites that only support HTTP/2. Additionally, significant speed improvements can be achieved using HTTP/2 when sending large numbers of requests to the same site.

We'd love to hear what you thinkUpdate to the latest version of Burp Suite Professional and give us your feedback on Twitter by following

@Burp_Suite. Not using Burp Suite Professional yet? Start a trial to see how you can accelerate penetration testing with Professional features including Burp Scanner and Burp Intruder.

Dayna Shoemaker

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
