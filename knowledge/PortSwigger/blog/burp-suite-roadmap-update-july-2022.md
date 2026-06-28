# Burp Suite roadmap update: July 2022

Source: https://portswigger.net/blog/burp-suite-roadmap-update-july-2022
Fetched: 2026-06-28T09:15:11.312357+00:00

Burp Suite roadmap update: July 2022

Matt Atkinson |

Thursday, 21 July 2022 at 13:45 UTC

Burp Suite

The roadmap shown here is out of date. Please see our January 2023 roadmap update.

With six (and a bit) months of 2022 already gone, it's time to bring you an update on the latest happenings down at Burp Towers. Find out what we've been up to, and what our plans are for the next year.

Burp Suite Enterprise Edition

Burp Suite Enterprise Edition is now very close to 1,000 subscribers. Over the next 12 months, we're going to make it easier than ever before to scale scanning across your whole web portfolio - by creating more resources for users of Kubernetes deployments, better systems for user onboarding / subscription management, and enabling even more flexible CI/CD integration.

Done Elastic deployments - Version 2022.3 introduced Burp Suite Enterprise Edition Kubnernetes deployment via a Helm chart. This has enabled users to reduce infrastructure costs and maintenance effort - especially where larger deployments are concerned.

Done Compliance reporting - The 2022.4 release added support for compliance reporting formats directly relating to the PCI DSS and the OWASP Top 10. This makes it easier than ever to check for relevant vulnerabilities across your whole web portfolio.

WIP Dashboards - Work is progressing on adding a number of new dashboards to the Burp Suite Enterprise Edition UI, based on your feedback. This feature will also add the ability for you to create custom dashboards.

WIP Issue tracking with GitHub - Work is progressing on integrating GitHub issue tracking with Burp Suite Enterprise Edition, to sit alongside our existing integrations with other systems.

WIP Replay of recorded login sequences - Work is underway on making it possible to view recorded login (authenticated scanning) sequences being executed during scans, so that you can test their operation.

WIP Simplified browser-powered scanning on Linux - Work is progressing on simplifying the deployment of browser-powered scanning on Linux. We are using Docker containers to ensure that browser-powered scanning works straight out of the box, in any environment - dramatically increasing coverage over traditional DAST scanners.

WIP Folder-level configuration - Work is progressing on enabling you to make a number of configuration changes at folder level as a bulk action in the UI. This will be a quick way to reconfigure all of the sites in a particular folder - including scan configurations, scanning pools, and any extensions used.

Added License key rollover - We will remove the need for Burp Suite users to enter a new license key when their subscription is extended. Your license key will instead roll over seamlessly.

Added Hourly metered billing - In addition to current methods of billing, we will enable users to pay for Burp Suite Enterprise Edition scans as and when they use them - further simplifying the process of scanning web portfolios at scale.

Added CI/CD inversion of control - We will enable users to start a Burp Suite Enterprise Edition scanning machine in a container, controlled by a CI system. This will make it possible to run scans from within temporary environments not previously accessible by Enterprise Edition scanning machines - and potentially help users to save on infrastructure costs.

Added Export scan results in Burp's XML format - In addition to its current HTML export capability, Burp Suite Enterprise Edition will enable users to export scan results as Burp XML - enabling easier integration with systems such as Defect Dojo and other vulnerability management tools.

Added GCP and Azure reference templates for Kubernetes - We will provide templates containing reference stack implementations for deployment of Burp Suite Enterprise Edition on a managed Kubernetes cluster on either GCP or Azure (using the native format in either case). This will greatly simplify the process of deploying Enterprise Edition to these services for most users, and comes in addition to our existing AWS reference stack implementation.

Added Improved user onboarding - We will continue to improve the usability of Burp Suite Enterprise Edition - especially for users new to the software. This comes in addition to the new usability features we added in the first half of 2022 - such as Burp Scanner's four new preset scan modes (version 2022.6).

Note that the Burp Scanner roadmap described below also applies to Burp Suite Enterprise Edition.

Burp Suite Professional

As the world's leading toolkit for web security testing, Burp Suite Professional continues to go from strength to strength. Over the next year, we will make it much easier to extend your testing capabilities - by improving the process for creating custom Burp extensions. You can also expect considerable improvements to some core Burp functionality. All of this adds up to faster, easier, and more reliable security testing - finding what you need to find, sooner.

Done Message Inspector - Version 2022.1 introduced a number of improvements to the HTTP Message Inspector, based on your feedback. This included numerous options for customizing the Inspector's appearance and behavior.

Done Performance improvements - We've made a number of changes to enhance Burp's performance. Notably, the 2022.5 release introduced feedback on BApp performance impact - providing an indication of the load we estimate BApps to place on your system.

Done Improved user experience - The 2022.6 release introduced new Burp Repeater features (including grouped tabs) to make testing easier and more efficient, as well as four new preset modes for Burp Scanner. Other new UI features include the customizable message editor tabs introduced in version 2022.3.

WIP New API - Work is underway on a complete rewrite of Burp Suite's extensibility framework. This revision will give feature parity with the existing API, and will lay the foundation for much richer capabilities in the future (see "Additional API functionality", below).

Added Additional API functionality - Once Burp Suite's new API is released, we will continue to develop it - adding potential for further customization. Initially this will include the exposure of functionality around project files and Burp Scanner configuration, as well as additional functionality around Burp Collaborator.

Added Collaborator client - We will overhaul Burp Collaborator client, and make it more prominent within Burp Suite. Collaborator client will use a new tabbed interface, and its data will be saved in project files.

Added User and project options - We will restructure Burp Suite's user and project options - making them much easier to use and navigate. This will include the addition of search functionality, and the ability to see which settings you have changed from default.

Note that the Burp Scanner roadmap described below also applies to Burp Suite Enterprise Edition.

Burp Scanner

Burp Scanner sits at the heart of both Burp Suite Enterprise Edition and Burp Suite Professional - and we continue to invest heavily in it. Burp Scanner's ability to navigate virtually any client-side technology that a modern browser can, coupled with PortSwigger's cutting-edge web security research, provides you with scanning and coverage that is truly leading the way for the industry as a whole.

Over the next 12 months, we will further improve the way Burp Scanner handles the modern web. We will also concentrate on making it easier to create / add custom scan checks to suit your needs - with an entirely new declarative framework for doing so.

Done Scan speed - We have made a number of improvements to Burp Scanner's scanning speed. Version 2022.2 introduced ultra-fast crawling of static content, while 2022.5 brought with it the option to skip unauthenticated crawling during authenticated scans.

Done Audit of asynchronous traffic - The 2022.2 release enabled Burp Scanner's crawler to identify API calls that are triggered when the browser renders components on the page - sending these calls for audit where necessary. In addition to this, the 2022.3 release gave Burp Scanner the ability to detect DOM-based vulnerabilities that rely on API calls.

Done Improved coverage of popular JavaScript libraries and frameworks - The 2022.2 release enabled Burp Scanner to recognize websites using URL fragments for client-side routing, and to adjust its behavior accordingly. This greatly enhanced Burp Scanner's ability to crawl single-page applications (SPAs) built on technologies like React.

Done JWT scan checks - The 2022.5 release brought with it scan checks for eight common JWT-based vulnerabilities - saving you time, and making it easier to secure sites that use JWTs.

WIP Support for popups in recorded login sequences - Work is underway adding support for popup page elements when using Burp Scanner's recorded login (authenticated scanning) feature.

Added Declarative scan checks - We will make it much easier for users to customize Burp Scanner to suit their own particular needs - by creating a new declarative framework for constructing custom scan checks without writing extensions.

Added React form handling - Burp Scanner will better handle forms when scanning single page web applications (SPAs) built on React. Specifically, we will improve Burp Scanner's handling of input elements that do not have an enclosing form tag.

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
