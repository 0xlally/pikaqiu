# Burp Suite roadmap update: January 2023

Source: https://portswigger.net/blog/burp-suite-roadmap-update-january-2023
Fetched: 2026-06-28T09:15:10.647177+00:00

Burp Suite roadmap update: January 2023

Matt Atkinson |

Friday, 27 January 2023 at 14:48 UTC

Burp Suite

The roadmap shown here is out of date. Please see our July 2023 roadmap update.

Believe it or not, it's January once again. And this can mean only one thing - it's time to update you on the changes we've got in store for Burp Suite over the next six months.

But this edition of the Burp roadmap also comes with a slight caveat - because this year we can neither confirm nor deny that we may also have a few surprises up our collective sleeves. Watch this space to stay in the know.

Burp Scanner

Burp Scanner is used in Burp Suite Enterprise Edition, Burp Suite Professional, and now (to a slightly more limited extent) in our free CI/CD product,  Dastardly. It enables tens of thousands of users to scan the modern web both efficiently and effectively.

But PortSwigger isn't exactly known for resting on its laurels, and the first half of 2023 is looking good for Burp Scanner users in terms of releases. Over the next six months, you'll see Burp Scanner gain yet more automated capability - and an exciting new way to customize your scans.

Done Support for popups in recorded login sequences - The 2022.12.4 release added support for recorded login sequences that open new windows or tabs. This enables you to run authenticated scans on websites with login mechanisms that require you to interact with popups, such as Microsoft and Amazon's SSO services.

Done Revamped browser powered scanning - The 2022.12.4 release fundamentally changed the way that Burp Scanner navigates using its built-in browser. This improves scanning of applications that make heavy use of client-side JavaScript for navigation, and lays a strong foundation for further development of the scanner.

WIP Declarative scan checks - Work is progressing on a new framework to add scan checks to Burp Scanner using a simplified language we've created specifically for this purpose. This will enable you to create custom scan checks more easily (without writing a BApp extension).

WIP React form handling - Work is progressing on improving the way Burp Scanner handles forms when scanning single page applications (SPAs) built on React. Specifically, this will improve Burp Scanner's handling of input elements that do not have an enclosing form tag.

Added Improved scanning of JavaScript frameworks - Further to the improvements we have already made to Burp Scanner's coverage of applications built using the React library, we will continue to develop our capabilities in this area, and include apps built using Angular, Vue.js, and other frameworks.

Added Seed scan from uploaded API definition - We will give Burp Scanner the ability to ingest an API definition as part of its launch process. It will use this API definition to seed its scan - enhancing Burp Suite's ability to scan APIs and microservices.

Added GraphQL scan checks - We will give Burp Scanner the ability to check for a number of security vulnerabilities relating to APIs using the GraphQL language.

Added Access control scan checks - We will give Burp Scanner the ability to check for a number of security vulnerabilities relating to access control.

Note that Burp Suite Enterprise Edition and Burp Suite Professional both contain Burp Scanner and will benefit from its roadmap.

Burp Suite Enterprise Edition

As I write, Burp Suite Enterprise Edition is now sitting at well over 1,000 subscribers. But as well as users, 2022 saw Enterprise Edition gain some powerful new features - like the ability to replay recorded login sequences. And with the plans outlined in this roadmap, 2023 is shaping up to be another cracker.

This year, you'll see some efficient new ways to scale scanning across your whole web portfolio. And further improvements to Burp Suite Enterprise Edition's already class-leading scanning engine will take its ability to scan the modern web to the next level.

Done Export scan results in XML - The 2022.11 release added the ability to export scan results from Burp Suite Enterprise Edition in XML format - enabling easier integration with systems such as Defect Dojo and other vulnerability management tools.

Done Replay of recorded login sequences - The 2022.10 release added support for recorded login replays in Burp Suite Enterprise Edition. This enables you to make sure that Burp Scanner can log in successfully when carrying out authenticated scans.

Done Licence key rollover - The 2022.10 release brought rolling license key renewals to Burp Suite Enterprise Edition. If you renew your license before it expires, we now automatically update your license key information.

Done Improved user onboarding - The 2022.9 release brought a number of improvements to the onboarding process - including the ability to quickly set up a scan of PortSwigger's deliberately vulnerable website, to see an example of scan results.

WIP Hourly metered billing - Work is progressing on enabling Burp Suite Enterprise Edition users to pay for scans as and when they use them - further simplifying the process of scanning web portfolios at scale.

WIP CI/CD inversion of control - Work is progressing on enabling Burp Suite Enterprise Edition users to start a scanning machine in a container (controlled by a CI system, for example). This will make it possible to run Enterprise Edition from within any CI/CD environment - much like our recently released free CI/CD product, Dastardly.

Added Improve site setup - We will make it easier to set up sites in Burp Suite Enterprise Edition. This work will include enabling you to define the scope of a scan more easily.

Added Pre-built Amazon Machine Images (AMIs) - We will provide pre-built AMIs for Burp Suite Enterprise Edition, enabling you to auto-generate a suitable EC2 instance. This will make it easier to get Burp Suite Enterprise Edition running on AWS.

Added Supply-Chain Levels for Software Artifacts (SLSA) Level 2 - Burp Suite Enterprise Edition will be certified to SLSA Level 2 - addressing customer requirements.

Note that the Burp Scanner roadmap described above also applies to Burp Suite Enterprise Edition.

Burp Suite Professional

The last 12 months have been huge for Burp Suite Professional. It's now got a brand new API - opening up new ways to tailor it to your every need - as well as some slick UI changes, to enable more efficient testing.

2023 will see us further develop these themes - by bringing you loads of new UI and customization options. And that's not to mention the Burp Scanner roadmap - which (as usual) includes some killer new features for scanning the modern web.

Done New API - The 2022.9.5 release introduced the new Montoya API, which replaces the Wiener API in Burp Suite Professional and Burp Suite Community Edition. Montoya brings a more modern design to Burp's extensibility, and will enable richer capabilities in the future (see "Additional API functionality", below).

Done Collaborator client - The 2022.9.5 release also brought with it major improvements to Burp Collaborator client. As well as gaining its own top-level tab, the client now uses a tabbed interface, and saves its interactions in project files, among other improvements.

Done User and project options - The 2022.11 release saw Burp's user and project options move to a single new Settings dialog, accessible from a button on the main toolbar or via a configurable hotkey. This dialog is much more user friendly than the old option menus, and includes a search function.

WIP Additional API functionality - We will continue to develop Burp's new Montoya API, including improved support for WebSockets, and the addition of functionality around project files - enabling extensions to save data.

Added Collaborator payloads in Intruder attacks - We will introduce the ability to generate and include Burp Collaborator payloads as part of a Burp Intruder attack. Any interactions detected by Burp Collaborator will then be included in the results for your Burp Intruder attack.

Added Testing workflow - We will introduce a brand new tool to help you organize your testing workflow, and keep track of pending actions.

Added Improved Burp Scanner interface - We will adjust Burp Scanner's interface within Burp Suite Pro - surfacing information to improve visualization of scan activity in both the crawl and audit phases. This will enable you to more easily understand the extent of coverage that a particular scan configuration has achieved, and how any discovered issues fit into the target's navigational structure.

Added User interface - customization - We will enable you to greatly alter and customize the layout of your Burp workspace. Tailor Burp Suite's top level tools to the particularities of your workflow.

Added ARM64 support - Burp Suite Professional and Burp Suite Community Edition will support machines running Linux on an ARM64-based processor.

Note that the Burp Scanner roadmap described above also applies to Burp Suite Professional.

And of course, don't forget to follow us on Twitter - to stay in the know about all things Burp Suite.

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
