# Burp Suite roadmap update: July 2020

Source: https://portswigger.net/blog/burp-suite-roadmap-update-july-2020
Fetched: 2026-06-28T09:15:11.054352+00:00

Burp Suite roadmap update: July 2020

Dafydd Stuttard |

Tuesday, 14 July 2020 at 11:22 UTC

Burp Suite

We’re half-way through 2020, and we’ve made a lot of progress towards the Burp Suite roadmap that we announced in January. We’d like to update everyone on our progress so far, and add some new items to our roadmap for the coming 12 months.

Burp Suite Enterprise Edition

Our vision for Burp Suite Enterprise Edition is to give security and development teams a new layer of defense for their expanding web estates. It schedules and scales scans across tens, hundreds, or thousands of sites to highlight vulnerabilities earlier, prioritize threats, and speed the time to address critical issues.

Over the coming 12 months, we will continue to add new user-facing features based on customers’ priorities. And we will improve support for a range of different use cases and deployment scenarios.

Done Improved APIs – The 2020.4 release introduced a new GraphQL-based API that exposes most core functionality, to enable integration with external systems and other automated use cases.

WIP Cloud friendly – The 2020.6 release included beta support for easy installation into cloud environments. Work is progressing on other cloud-friendly features, including auto-scaling of resources to support scan workloads and hourly metered billing.

WIP Enterprise integrations – The 2020.6 release included a user management integration with Active Directory using LDAP, and work is underway on SAML. We will also integrate with additional issue tracking systems, including GitHub and Azure DevOps.

Added Burp extensions – We will support Burp extensions in Enterprise Edition, for both BApps and custom extensions.

Added Agent affinity – We will support affinity between scan agents and web sites to be scanned. This will ensure scans can be carried out using the most suitable agents, based on network location, system resources, or other factors.

Note that the Burp Scanner roadmap described below also applies to Burp Suite Enterprise Edition.

Burp Suite Professional

We are committed to maintaining Burp Suite Pro as the best-of-breed toolkit for hands-on web penetration testing. We will be prioritizing various new features aimed at advanced technical users, as well as improving the core of the product, making it more reliable, stable, and usable for everyone.

Done HTTP/2 – The 2020.6 release included experimental support for HTTP/2 in all tools. This will be enabled by default soon, based on user feedback and further testing.

WIP User interface – Recent releases have included pretty-printing of JSON and other content types, and rendering of non-printing characters. Work is underway on improving workflows for in-place decoding and analysis.

WIP Burp Intruder – Work is underway on various enhancements based on user feedback, including new payload types, new options for payload placement, richer analysis of attack results, and incremental saving of data.

Added Automatic updates – We will support optional automatic updates without the need to re-run an installer. We will also introduce an early adopters’ track, giving earlier access to new and experimental features.

Note that the Burp Scanner roadmap described below also applies to Burp Suite Professional.

Burp Scanner

Our ambition is for Burp Scanner to deal with all common technologies and application features, while maintaining its strong scan coverage and performance.

WIP Browser-powered scanning – We are close to enabling browser-powered scanning by default for Burp Suite Professional. We will continue to improve performance and coverage of modern navigational patterns. We will deliver excellent coverage of traditionally challenging targets such as AJAX-heavy single page applications. When ongoing testing is completed, browser-powered scanning will be enabled by default for Burp Suite Enterprise Edition.

WIP Recorded login sequences – Work is underway on letting the user record login sequences using their browser. This will provide improved coverage and accuracy over simple configured credentials, work with JavaScript-heavy login functions and single sign-on, and be much easier to configure than session handling rules.

WIP Report vulnerable JavaScript libraries – Burp Scanner will perform software composition analysis (SCA) of client-visible code and report JavaScript libraries in use containing known vulnerabilities.

Added API scanning – Burp Scanner will support automatic scanning of APIs based on standard service definitions, including OpenAPI/Swagger.

Burp Suite

Dafydd Stuttard

@DafyddStuttard

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
