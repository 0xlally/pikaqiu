# Burp Suite Enterprise Edition: six months of new features

Source: https://portswigger.net/blog/burp-suite-enterprise-edition-six-months-of-new-features
Fetched: 2026-06-28T09:15:09.615527+00:00

Burp Suite Enterprise Edition: six months of new features

Matt Atkinson |

Monday, 30 November 2020 at 15:20 UTC

Burp Suite

Over the past six months, we've added a number of new features to Burp Suite Enterprise Edition. We're also pleased to announce that the software is now being used by 572 organizations, across 63 countries. In this blog post, we'll cover the following new features:

Recorded login sequences.

Browser-powered scanning.

API vulnerability scanning.

Single sign-on.

API and integration improvements.

Cloud-friendly deployment.

PortSwigger launched Burp Suite Enterprise Edition for general release in June 2019. Its mission? To enable large enterprises to scan their web estates at scale, and support them in achieving DevSecOps.

Since then, we've been listening carefully to our users. Based on this invaluable feedback, we've launched numerous releases - adding a wealth of new features. This has improved overall functionality, and taken Burp Suite's scanning capability to new levels.

If you trialled Burp Suite Enterprise Edition before, but found it was missing something you needed, or if you're currently evaluating automated web vulnerability scanners, then now's a really great time to try the latest version.

Here are some of the latest and greatest features that our customers are using to free AppSec time, integrate with CI/CD, and supercharge the secure development process - both scalably and reliably:

Recorded login sequences

A known - and painful - limitation to many automated web vulnerability scanners is the inability to authenticate to target web apps for scanning due to them having complex log in sequences. This is no longer a problem for users of Burp Suite Enterprise Edition.

You can now record log in sequences using a dedicated browser plugin. This information can then be passed through to Burp Suite - giving access to your application and allowing Burp Scanner to check for vulnerabilities. With the problem of complex log in sequences solved, you can truly scan it all, at scale! This is a huge boon for many of our users.

Browser-powered scanning

Burp Suite Enterprise Edition contains the same trusted Burp Scanner found in Burp Suite Professional - tried, tested, and trusted by over 51k users. Burp Scanner continued its long tradition of innovation this year - with the addition of browser-powered scanning.

Burp Scanner can now use an embedded Chromium browser to crawl and audit sites. This allows it to fully render applications - "seeing" content exactly as a user would. Because of this, Burp Suite is now able to crawl apps that make heavy use of JavaScript. This really is a huge step forward - both for automated vulnerability scanners and for the industry in general.

Behind all our innovations stands considerable research and expertise. We've invested a great deal of time making browser-powered scanning reliable - and this is a continuous process. Browser-powered scanning is foundational to a number of Burp Scanner enhancements - including recorded logins - and in future, will allow further improvements in coverage for single page web apps.

API vulnerability scanning

APIs represent a huge attack surface for many organizations. Okta has previously cited Gartner in predicting that by 2022, API abuses will be the most-frequent attack vector resulting in data breaches for enterprise applications.

In line with our mission to help enterprises secure their entire web portfolios, PortSwigger plans to support the security testing of APIs and microservices.

November’s 2020.11 Burp Suite Enterprise Edition release includes the ability to scan both JSON and YAML-based APIs for vulnerabilities, supporting the OpenAPI (/Swagger) version 3 specification.

We will be expanding our support for enumerating API endpoints, so please let our team know your feedback and requirements.

Single sign-on

Many enterprises use third party identity management and authentication services to control access to their applications.

Being able to centrally control user access simplifies IT infrastructure - ensuring that only authorized users can access restricted applications. In the case of Burp Suite Enterprise Edition, single sign-on enables our customers to efficiently roll-out control of automated vulnerability scans to stakeholders across their organization.

This functionality, combined with Burp Suite Enterprise Edition’s role-based access controls, ensures that reporting is available to permitted individuals.

July 2020's release brought with it the ability to configure an LDAP connection between Burp Suite Enterprise Edition and your Active Directory server. This was then expanded in October 2020, with support for SAML integration. This has been fully tested with:

Active Directory Federation Services (ADFS).

Okta.

Azure Active Directory.

SAML integration will be of particular interest to Burp Suite Enterprise Edition users managing user authentication for cloud-based deployments.

API and integration improvements

Since launch, Burp Suite Enterprise Edition has had a REST API, to enable integration with other applications (e.g. CI/CD systems). To improve integration, in April 2020, we launched a GraphQL-based API, which exposes most of Burp Suite Enterprise Edition's core functionality.

You can use the new API to read and write most of the same data you can using the web UI. For example, you can now use the GraphQL API to:

Create and edit sites.

Schedule one-off and regular scans.

Create and edit custom scan configurations.

Add folders to your site tree.

Get scan results and reports.

Manage your pool of agent machines, including authorizing new agent machines.

There's a lot more we plan on doing to expand Burp Suite Enterprise Edition's API functionality. If you have a requirement that's not covered here, we'd love to hear from you to help shape our roadmap.

Cloud-friendly deployment

Organizations migrating to the cloud or starting out with a cloud-first mentality are looking for security solutions that fit into their cloud-based stacks. Those interested in cloud-hosted security can now deploy Burp Suite Enterprise Edition to the cloud.

We'd love to hear what you think

Ready to get started with Burp Suite Enterprise Edition, or perhaps you'd like to give it another try in light of the latest feature releases?

Request a trial here, or speak to us to find out more. And of course, you can also purchase a full Burp Suite Enterprise Edition licence, here.

Burp Suite

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
