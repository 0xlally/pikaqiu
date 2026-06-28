# Burp Suite roadmap update: July 2021

Source: https://portswigger.net/blog/burp-suite-roadmap-update-july-2021
Fetched: 2026-06-28T09:15:11.008840+00:00

Burp Suite roadmap update: July 2021

Matt Atkinson |

Friday, 9 July 2021 at 10:50 UTC

Burp Suite

This roadmap has now been updated. Please see our January 2022 roadmap update.

Apparently we're halfway through 2021 already (where does the time go?). Here's an update on what we've added to our products so far this year, as well as some exciting new features we're adding to our roadmaps for the 12 months ahead. This should keep us busy …

Burp Suite Enterprise Edition

Burp Suite Enterprise Edition is now being used by over 750 companies to scale scanning across their web estates, and to drive their journey toward DevSecOps. Over the next 12 months, we'll be further enhancing its capabilities.

Done Improved CI/CD integrations – CI/CD driver release 2021.3 added support for site-driven scans within CI/CD plug-ins, as well as the ability to download the end-of-scan report. Site-driven scanning especially, greatly improves the usability of the drivers. We now also allow a maximum number of issues that will combine with severity and confidence to determine when a build fails.

Done Agent affinity (agent machine pools) – The 2021.4 release added support for affinity between scan agents and the web sites to be scanned. This ensures that scans can be carried out using the most suitable agents, based on network location, system resources, or other factors.

Done UX improvements – The 2021.4 release updated the Scan results page to our new look and feel - making information easier to access. Scanned URLs can now be displayed as a tree to make it easier to see the structure of your site. Navigation has been improved through the UI.

WIP Elastic deployments – Work is progressing on other cloud-friendly features, including auto-scaling of resources to support scan workloads and hourly metered billing.

WIP Issue-tracking integrations – Work is progressing on integrating additional systems for issue tracking, including GitHub and Azure DevOps.

WIP Burp extensions – Work is underway on supporting Burp extensions in Enterprise Edition, for both BApps and custom extensions.

WIP Bulk operations – Work is progressing on supporting bulk actions through the UI for importing sites from CSV files, applying scan configurations and application logins across a group of sites, and cancelling or deleting a selection of scans.

Added Single sign-on - We will provide support for user management via SCIM (System for Cross-domain Identity Management), for integration with Okta and Azure Active Directory.

Added Dashboards - We will add new dashboard widgets providing additional data and views. We will provide new ways of configuring and sharing dashboards.

Added Compliance reporting - We will support reporting of scan results against compliance frameworks - such as HIPAA, PCI, etc.

Note that the Burp Scanner roadmap described below also applies to Burp Suite Enterprise Edition.

Burp Suite Professional

We're committed to maintaining Burp Suite Pro as the world's leading toolkit for web security testing. Over the next 12 months, we'll be prioritizing new features and updates that will allow users to test for a broader range of vulnerabilities in modern web applications.

Done Early adopters releases – The 2021.2.1 release introduced an early adopters’ track - giving earlier access to new and experimental features.

Done Native HTTP logging – the 2021.4.2 release added native, resource-efficient logging functionality - based on the popularity of the BApps Logger++ and Flow.

Done DOM testing tools – The 2021.7 release added DOM Invader - a powerful new tool to make testing manually for DOM XSS much simpler.

WIP Burp Intruder – Work is underway on various enhancements based on user feedback, including new payload types, new options for payload placement, richer analysis of attack results, and incremental saving of data.

WIP Performance improvements – Work is progressing on improving the memory and processing efficiency of various Burp features, as well as providing feedback on resource-hungry BApps that can impair performance.

Added Message inspector - We will make various improvements to the usability of the HTTP message inspector, based on user feedback.

Added HTTP/2 - The HTTP message inspector will be enhanced with new capabilities enabling manual exploitation of HTTP/2-specific vulnerabilities using Burp Repeater. The Burp Extender API will be enhanced to enable HTTP/2-specific attacks. For more information, please see our Black Hat USA presentation preview.

Note that the Burp Scanner roadmap described below also applies to Burp Suite Professional.

Burp Scanner

We will continue to invest heavily in Burp Scanner - ensuring that users of both Burp Suite Enterprise Edition and Burp Suite Professional have best-in-class scan coverage and performance.

Over the next 12 months, we'll be focussing on enhancing Burp Scanner's ability to navigate and scan modern web applications, as well as further tuning its class-leading performance, and adding scan checks for novel vulnerabilities.

Done Report vulnerable JavaScript libraries – The 2021.2 release added software composition analysis (SCA) of client-visible code. Burp Scanner can now report JavaScript libraries in use containing known vulnerabilities.

Done Improved navigational coverage – The 2021.7 release gave Burp Scanner the ability to detect and interact with additional DOM elements that can cause JavaScript-triggered navigation - not only conventional links and forms.

Done Improved SPA scanning – The 2021.7 release also gave Burp Scanner the ability to handle navigational actions that cause a DOM update without a synchronous request to the server - enabling better handling of single-page applications.

WIP Audit of asynchronous traffic – Work is progressing on adding automatic auditing of in-scope requests issued from client-side JavaScript using XHR and Fetch.

Added Server-side template injection - Burp Scanner will detect injection into a wider range of templating engines, and will employ OAST techniques to detect blind SSTI.

Added Payloads within data formats - We will improve the placement and encoding of scan payloads within JSON and XML data structures.

Added Scan speed - We will further optimize performance in default settings, to enable faster scans without compromising coverage.

Added HTTP/2 - Burp Scanner will report some new classes of HTTP/2-specific vulnerabilities. For more information, please see our Black Hat USA presentation preview.

Note that Burp Suite Enterprise Edition and Burp Suite Professional both contain Burp Scanner and will benefit from its roadmap.

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
