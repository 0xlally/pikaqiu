# It's now easier than ever to scan at scale with Burp Suite Enterprise Edition

Source: https://portswigger.net/blog/its-now-easier-than-ever-to-scan-at-scale-with-burp-suite-enterprise-edition
Fetched: 2026-06-28T09:15:18.975498+00:00

It's now easier than ever to scan at scale with Burp Suite Enterprise Edition

Matt Atkinson |

Wednesday, 25 August 2021 at 14:00 UTC

Burp Suite

Enterprise Edition

774 organizations in 68 countries are now using Burp Suite Enterprise Edition to improve and scale security across their web portfolios. As we pass the three-year anniversary of development on Burp Suite Enterprise Edition, we thought it was about time we gave you a roundup of some new features the software now includes.

This post includes recently introduced (as well as upcoming) feature highlights across some key areas of capability. These features enable:

Increased scan coverage for modern web applications.

Easier deployment for new users - both in the cloud and on-premise.

The ability to scale scanning right across your enterprise.

Remember that unlike most automated web vulnerability scanners, Burp Suite Enterprise Edition scans can be assigned and reassigned across any websites, applications, or URLs.

During the past three years of development, we've been listening closely to our users, and we've now addressed a number of specific needs and pain points that you've helped us to identify. Thanks to this, Burp Suite Enterprise Edition now enables you to automate trusted Burp scans across your portfolio more easily than ever before - paving the way to DevSecOps.

New and upcoming features in Burp Suite Enterprise Edition

Increased scan coverage

Improved single-page application scanning (SPAs) - Burp Scanner now handles navigational actions that cause DOM updates without a synchronous request to the server.

API scanning - automatically parse OpenAPI v3 REST API definitions written in JSON - enabling detection of more attack surface.

Authenticated scanning - record complex login sequences and play them back. This feature will soon receive an upgrade, allowing it to handle increased complexity.

HTTP/2 support - support for the latest web protocols.

New scan checks - representing the latest PortSwigger research (e.g. HTTP request smuggling via HTTP/2).

SCA - software composition analysis capable of detecting vulnerable client-side JavaScript libraries.

Coming soon Auditing of async traffic - greatly improved scanning of SPAs via an audit of in-scope API requests issued from client-side JavaScript using XHR or Fetch.

Ease of deployment

Optimized setup - when getting started and when creating recurring scans.

New and improved getting started documentation - content to help your team hit the ground running with Burp Suite Enterprise Edition.

Coming soon Streamlined cloud deployment - a simplified and improved cloud deployment experience.

PortSwigger also recently expanded its team of dedicated technical support specialists.

Scalable scanning

Extensions - support for both custom extensions written in Java, and compatible Burp extensions (BApps).

CI/CD plugin improvements - match specific sites and scans, download end of scan reports, and set parameters for build failure - all without leaving your CI/CD system.

Agent machine pools - assign specific scanning agents to specific tasks.

Coming soon Auto-scaling - save on cloud infrastructure and computing costs.

Coming soon Bulk operations - import sites, apply scan configs/application logins, and delete/cancel scans - all in bulk.

Coming soon More issue-tracking integrations - including Slack, GitHub, and Azure DevOps.

Coming soon Further improvements to scan speed - faster scans, without compromising coverage.

Coming soon Compliance reporting - reporting of scan results against compliance frameworks such as HIPAA, PCI, etc.

For more information on upcoming Burp Suite Enterprise Edition features, please see our July 2021 roadmap update.

Get started today

If you want the fastest way to see the majority of Burp Suite Enterprise Edition immediately then check out our live demo (no signup necessary). This includes a large portion of Burp Suite Enterprise Edition - although please note that some features (e.g. CI/CD integration) are not represented in the live demo.

Alternatively, please request a free 30-day trial, to deploy and test a fully-featured version of Burp Suite Enterprise Edition. You can also speak to a member of our dedicated Enterprise Advocates Team, if you'd like more information about the product/trial.

Burp Suite

Enterprise Edition

Matt Atkinson

@mattatkinson42

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
