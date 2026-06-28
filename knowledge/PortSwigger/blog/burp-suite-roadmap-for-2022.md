# Burp Suite roadmap for 2022

Source: https://portswigger.net/blog/burp-suite-roadmap-for-2022
Fetched: 2026-06-28T09:15:10.842796+00:00

Burp Suite roadmap for 2022

Matt Atkinson |

Thursday, 13 January 2022 at 15:45 UTC

Burp Suite

The roadmap shown here is out of date. Please see our July 2022 roadmap update.

With 2022 now underway, it's about time we gave you the latest on where Burp Suite is heading this year. Here we take a look at the powerful new Burp Suite features we'll be working on in 2022 - as well as updating you on what we added during 2021.

Burp Suite Enterprise Edition

Burp Suite Enterprise Edition is now being used by 800 organizations to scale dynamic (DAST) scanning right across their web estates. In 2022, new features will make it easier for customers to deploy in enterprise environments, deliver rich reporting, and control scanning.

Done Burp extensions - The 2021.8 release added support for Burp extensions in Burp Suite Enterprise Edition. This includes custom extensions, as well as many BApps.

Done Bulk operations - The 2021.11 and 2021.12 releases added support for bulk actions in the UI. This allows you to add sites, move and delete sites and folders, launch quick scans, and cancel or delete scans - all in bulk.

Done Single sign-on - The 2021.11 release added support for SCIM, to simplify the process of provisioning and decommissioning users and groups from a central identity provider. This has been fully tested with Okta and OneLogin.

Done Issue tracking integrations - The 2021.11 and 2021.12 releases added support for issue tracking integration using Slack, Trello, and GitLab.

WIP Compliance reporting - Work is underway on adding support for the reporting of scan results against compliance frameworks, including PCI and the OWASP Top 10.

WIP Elastic deployments - Work is progressing on a number of cloud-friendly features, including auto-scaling of resources to support scan workloads, and hourly metered billing. This work will include simplification of our existing cloud deployment options.

WIP Dashboards - Work is progressing on adding a number of new dashboards to the Burp Suite Enterprise Edition UI, based on your feedback. This feature will also add the ability for you to create custom dashboards.

WIP Issue tracking with GitHub - Work is progressing on integrating GitHub issue tracking with Burp Suite Enterprise Edition, to sit alongside existing integrations with other systems.

Added Replay of recorded login sequences - We will make it possible to view recorded login (authenticated scanning) sequences being executed during scans, so you can test that they are working.

Added Containerization of deployments - We will simplify the deployment of Burp Suite Enterprise Edition, by introducing deployment options based around the use of Docker and virtual machines (VMs).

Added Folder-level configuration - We will enable you to make a number of configuration changes at folder level as a bulk action in the UI. This will be a quick way to reconfigure all of the sites in a particular folder - including scan configurations, agent pools, and any extensions used.

Note that the Burp Scanner roadmap described below also applies to Burp Suite Enterprise Edition.

Burp Suite Professional

We're committed to maintaining Burp Suite Pro as the world's leading toolkit for web security testing. Over the next 12 months, we'll release new features and updates to further improve Burp Suite Pro's user experience, and its ability to help you find more vulnerabilities, faster.

Done HTTP/2 - The 2021.8 release added new capabilities to the HTTP message inspector and Burp Extender API. These changes enable you to make HTTP/2-specific attacks as seen in James Kettle's Black Hat USA 2021 presentation, HTTP/2: The Sequel is Always Worse.

Done Burp Intruder - The 2021.5, 2021.9, and 2021.12 releases made numerous enhancements to Burp Intruder based on your feedback. Changes included new attack types, options for payload placement, richer analysis of attack results, and incremental saving of data.

WIP Message inspector - Work is underway on various improvements to the usability of the HTTP message inspector, based on your feedback.

WIP Performance improvements - Work is progressing on improving the memory and processing efficiency of various Burp features, as well as providing feedback on resource-hungry BApps that can impair performance.

Added New API and multi-language extensibility - We will completely rewrite Burp Suite's extensibility framework. This revision will support Burp extensions written in Java, JavaScript, and Python 3, and will lay the foundation for much richer capabilities in the future.

Added Improved user experience - Based on your feedback, we will make a number of changes to improve your experience in Burp Suite Professional. These changes will include new options for customizing Burp's user interface and layout.

Note that the Burp Scanner roadmap described below also applies to Burp Suite Professional.

Burp Scanner

We will continue to invest heavily in Burp Scanner - ensuring that you have best-in-class scan coverage and performance when using both Burp Suite Enterprise Edition and Burp Suite Professional.

Over the next 12 months, we'll be focused on enhancing Burp Scanner's ability to navigate and scan modern web applications such as SPAs (single page applications), fine-tuning its class-leading performance, and adding scan checks for novel vulnerabilities.

Done HTTP/2 - The 2021.8 release added scan checks for a number of new classes of HTTP/2-specific vulnerability. For more information, please see James Kettle's Black Hat USA 2021 presentation, HTTP/2: The Sequel is Always Worse.

Done Server-side template injection - The 2021.9 release added scan checks for injection into a number of templating engines, and additional OAST detection methods using Burp Collaborator.

Done Payloads within data formats - The 2021.9 release improved the placement and encoding of scan payloads within JSON and XML data structures.

WIP Scan speed - The 2021.7.1 release optimized scan performance using default settings, to enable faster scans without compromising coverage. Work is ongoing to make further improvements in this area.

WIP Audit of asynchronous traffic - The 2021.9 release introduced the auditing of API calls triggered by the crawler interacting with page elements, but work is ongoing to further improve this functionality. This will further increase coverage of single page applications (SPAs).

Added Improved coverage of popular JavaScript libraries and frameworks - We will fine-tune Burp Scanner to optimize its performance when used to scan sites built using React and AngularJS.

Added Support for popups in recorded login sequences - We will add support for popup page elements when using Burp Scanner's recorded login (authenticated scanning) feature.

Added JWT scan checks - We will give Burp Scanner the ability to check for a number of security vulnerabilities relating to JSON Web Tokens (JWT).

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
