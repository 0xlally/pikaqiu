# Burp Suite roadmap for 2021

Source: https://portswigger.net/blog/burp-suite-roadmap-for-2021
Fetched: 2026-06-28T09:15:10.489886+00:00

Burp Suite roadmap for 2021

Dafydd Stuttard |

Monday, 25 January 2021 at 14:23 UTC

Burp Suite

This roadmap has now been updated. Please see our July 2021 roadmap update.

We’re all hoping that 2021 will prove to be a better year for humanity. And we’re also planning a great year for Burp Suite! Here, we’re excited to share some key details of our roadmap for each of our products.

Burp Suite Enterprise Edition

Burp Suite Enterprise Edition is being used now by over 600 companies to scale scanning across their web estates and to achieve DevSecOps.

In 2020, we added a huge amount of enterprise functionality including a full API, cloud-friendly installation, and single-sign on. Automated scanning coverage has improved significantly with the release of recorded logins and the ability to parse API definitions. Here is an update on our plans for the next 12 months:

Done Directory integrations – The 2020.6 release included a user management integration with Active Directory using LDAP, and the 2020.10 release added SAML integration..

Done Cloud-friendly installation – The 2020.6 release introduced support for easy installation into cloud environments.

WIP Elastic deployments – Work is progressing on other cloud-friendly features, including auto-scaling of resources to support scan workloads and hourly metered billing.

WIP Issue-tracking integrations – We will integrate with additional systems for issue tracking, including GitHub and Azure DevOps.

WIP Burp extensions – We will support Burp extensions in Enterprise Edition, for both BApps and custom extensions.

WIP Agent affinity – We will support affinity between scan agents and web sites to be scanned. This will ensure scans can be carried out using the most suitable agents, based on network location, system resources, or other factors.

Added Bulk operations – We will support bulk actions through the UI for importing sites from CSV files, applying scan configurations and application logins across a group of sites, and cancelling or deleting a selection of scans.

Added UX improvements – We will update the Scan results page to our new look and feel and make information easier to access. We will display scanned URLs as a tree to make it easier to see the structure of your site. We will improve navigation through the UI.

Added Improved CI/CD integrations – We will add support for site-driven scans within CI/CD plug-ins and the ability to download the end-of-scan report. We will allow a maximum number of issues that will combine with severity and confidence to determine when a build fails.

Note that the Burp Scanner roadmap described below also applies to Burp Suite Enterprise Edition.

Burp Suite Professional

We are committed to maintaining Burp Suite Pro as the best-of-breed toolkit for hands-on web penetration testing. We will be prioritizing various new features aimed at advanced technical users, as well as improving the core of the product, making it more reliable, stable, and usable for everyone.

Done User interface – A series of releases during 2020 introduced pretty-printing of JSON, rendering of non-printing characters, and the message inspector, which provides a quick way to analyze and work with interesting features of HTTP and WebSocket messages without having to switch between different tabs.

Done Automatic updates – The 2020.11 release introduced support for background automatic updates.

WIP Early adopters releases – We will introduce an early adopters’ track, giving earlier access to new and experimental features.

WIP Burp Intruder – Work is underway on various enhancements based on user feedback, including new payload types, new options for payload placement, richer analysis of attack results, and incremental saving of data.

Added Native HTTP logging – Based on the popularity of some BApps (Logger++ and Flow), we will provide native, resource-efficient logging functionality..

Added Performance improvements – We will improve the memory and processing efficiency of various Burp features and provide feedback of resource-hungry BApps that can impair performance.

Added DOM testing tools – We will release some add-ons to Burp’s embedded browser to enhance manual testing for DOM-based vulnerabilities.

Note that the Burp Scanner roadmap described below also applies to Burp Suite Professional.

Burp Scanner

We will continue to invest heavily in Burp Scanner, to ensure our users have best-in-class scan coverage and performance. In 2020, we did exactly that with the release of browser-powered scanning, recorded login sequences, and API scanning.

During the next year, our development plans are focussed on ensuring that Burp Scanner can uncover more attack surface and find more vulnerabilities in modern web applications.

Done Browser-powered scanning – The 2020.8.1 release enabled browser-powered scanning by default for Burp Suite Professional.

Done Recorded login sequences – The 2020.9.2 release added recorded login sequences using a browser extension, and the 2020.11 release enabled visual testing of recorded logins using a headed browser.

Done API scanning – The 2020.11 release added automatic scanning of JSON- and YAML-based APIs for vulnerabilities.

WIP Report vulnerable JavaScript libraries – Burp Scanner will perform software composition analysis (SCA) of client-visible code and report JavaScript libraries in use containing known vulnerabilities.

Added Improved navigational coverage – Burp Scanner will detect and interact with additional DOM elements that can cause JavaScript-triggered navigation, not only conventional links and forms.

Added Improved SPA scanning – Burp Scanner will handle navigational actions that cause a DOM update without a synchronous request to the server, enabling better handling of single-page applications.

Added Audit of asynchronous traffic – Burp Scanner will automatically audit in-scope requests that are issued from client-side JavaScript using XHR and Fetch.

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
