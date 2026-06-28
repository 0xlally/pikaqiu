# Burp Suite roadmap for 2020

Source: https://portswigger.net/blog/burp-suite-roadmap-for-2020
Fetched: 2026-06-28T09:15:10.594781+00:00

Burp Suite roadmap for 2020

Dafydd Stuttard |

Wednesday, 15 January 2020 at 10:40 UTC

Burp Suite

We have big plans for Burp Suite during 2020, aimed at improving its value to professional testers, software development teams, and businesses with web assets to protect. Here, we’re sharing some key details of our roadmap for each of our products.

Burp Suite Enterprise Edition

Our vision for Burp Suite Enterprise Edition is to give security and development teams a new layer of defense for their expanding web estates. It schedules and scales scans across tens, hundreds, or thousands of sites to highlight vulnerabilities earlier, prioritize threats, and speed the time to address critical issues.

We have two broad areas of focus for Burp Suite Enterprise Edition in 2020. We will continue to add new user-facing features based on customers’ priorities. And we will improve support for a range of different use cases and deployment scenarios.

Highlights for 2020 include:

Improved APIs – We will provide richer APIs for integration with external systems and other automated use cases.

Cloud friendly – We will support easy installation into cloud environments, auto-scaling of resources to support scan workloads, and hourly metered licensing.

Enterprise integrations – We will integrate with popular platforms for user management (including Active Directory) and issue tracking (including GitHub and Team Foundation Server).

Note that the Burp Scanner roadmap described below also applies to Burp Suite Enterprise Edition.

Burp Suite Professional

We are committed to maintaining Burp Suite Pro as the best-of-breed toolkit for hands-on web penetration testing. We will be prioritizing various new features aimed at advanced technical users, as well as improving the core of the product, making it more reliable, stable, and usable for everyone.

Highlights for 2020 include:

User interface – We will make various improvements to the UI and usability, starting with the HTTP message editor. We will support colorizing and prettifying of JSON and other content types, and provide improved workflows for in-place encoding, analysis, and other common tasks.

HTTP/2 – We will support core features of HTTP/2, first in Burp Proxy and then in other applicable tools. As well as exposing additional attack surface, this will enable automated tools like Burp Intruder and Scanner to work much faster with some targets.

Burp Intruder – We will make various enhancements, including new payload types, new options for payload placement, richer analysis of attack results, and incremental saving of data.

Note that the Burp Scanner roadmap described below also applies to Burp Suite Professional.

Burp Scanner

Our ambition is for Burp Scanner to deal with all common technologies and application features, while maintaining its strong scan coverage and performance.

Highlights for 2020 include:

Browser-driven scanning – Building on the foundation of the new experimental feature, we will continue to improve performance and coverage of modern navigational patterns. We will deliver excellent coverage of traditionally challenging targets such as AJAX-heavy single page applications. When appropriate, we will enable browser-driven scanning by default.

Recorded login sequences – Burp will let the user record login sequences using their browser. This will provide improved coverage and accuracy over simple configured credentials, work with JavaScript-heavy login functions and single sign-on, and be much easier to configure than session handling rules.

Report vulnerable JavaScript libraries – Burp Scanner will perform software composition analysis (SCA) of client-visible code and report JavaScript libraries in use containing known vulnerabilities.

Note that Burp Suite Enterprise Edition and Burp Suite Professional both contain Burp Scanner and will benefit from its roadmap.

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
