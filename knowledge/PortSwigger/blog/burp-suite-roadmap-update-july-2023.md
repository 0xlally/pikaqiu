# Burp Suite roadmap update: July 2023

Source: https://portswigger.net/blog/burp-suite-roadmap-update-july-2023
Fetched: 2026-06-28T09:15:11.093065+00:00

Burp Suite roadmap update: July 2023

Matt Atkinson |

Monday, 17 July 2023 at 14:26 UTC

Burp Suite

Check out our roadmap for Burp Suite and find out what exciting features are coming your way over the next 12 months.

Burp Suite Professional

Added to the roadmap

Added BChecks - testing tool - When creating custom BChecks for Burp Scanner, it's vital to test them thoroughly, to gain confidence that they're working correctly. We're going to make it just as easy to test your BChecks as it was to write them, by introducing a BCheck testing tool. You'll be able to send suitable requests to the tool, and use them as test cases to confirm that your BCheck is working.

Added Code your own view filters - Sometimes, Burp's built-in options for filters like the Proxy HTTP history filter don't do exactly what you need. You're limited by the checkboxes provided and the ways the settings are combined. We're going to give you a brand new way to customize Burp Suite using your own code, directly from the UI. You'll be able to quickly and easily create a view filter that does exactly what you need, showing just the items you are interested in.

Added Burp Scanner auto configuration - Currently, you have to manually configure Burp Scanner to ensure good performance when scanning certain types of web application. Failure to do this could mean missed attack surface. We will give Burp Scanner the ability to configure itself based on the type of web application you are scanning. This will improve crawl coverage, without the need for any manual configuration.

Added Notes everywhere - If you've used comments in Burp's tables to record information about HTTP messages, then you'll know that they can be a bit cramped and difficult to use. We're going to introduce a much-improved Notes feature - enabling you to write free-form multi-line notes, to capture everything you know about an HTTP message.

Added Enhanced tables - If you've ever used Burp Suite in anger, you'll know that it makes heavy use of tables to display key data. But these can be somewhat inflexible, with little scope for customization. We're going to change tables in Burp so that they work more consistently - and enhance them to give you more control. You'll be able to show and hide different columns, move them around, and you'll gain new capabilities for search and export.

Added Service worker networking - Burp Scanner's crawler doesn't properly support service workers and WebSockets messages that occur during scans. This can cause some applications to function incorrectly - potentially leading to incomplete scan coverage. We will give Burp Scanner the ability to properly crawl service workers and WebSockets messages - eliminating this problem.

Added API scanning improvements - Although Burp Scanner can understand many features of an OpenAPI definition and scan them appropriately, coverage isn't always as good as it could be. This is because scanning currently doesn't support some popular API features. We will add these features to Burp Scanner - enabling greatly improved coverage of web APIs.

Added Browser performance enhancements - Burp Scanner uses embedded browsers to navigate web sites effectively while scanning. But using a pool of browsers can consume significant system resources, which impairs performance. We will change Burp Scanner so that it uses fewer browser instances, each containing multiple isolated tabs, to enable parallel navigation. This will make scanning more efficient.

Work in progress

WIP Improved Burp Scanner interface - It's not always easy to see the actions that Burp Scanner has carried out during a scan - or the attack surface it's discovered. Burp Suite Professional 2023.5.2 brought you a new crawl paths view - which goes some way to addressing this problem. But more improvements to Burp Scanner's interface are currently in development, and in coming releases, you'll see some exciting new ways to visualize scan activity.

WIP Customizable user interface - Burp is a complex beast - and most testers have their own idiosyncratic way of working with it. This means that a fixed user interface will never be optimized for everyone. Especially once you start extending Burp Suite with BApps, you might find that real estate among your tabs is limited, to say the least. So work is underway to make Burp's user interface far more customizable. You'll finally be able to make it your own. And (because I know some of you will ask) - yes - if you want to hide Sequencer, you'll be able to hide Sequencer.

WIP Start scan from uploaded API definition - Work is progressing on giving Burp Scanner the ability to ingest an API definition you have given it, as part of its launch process. It will then use this API definition to seed its scan. This will bring you two main benefits when scanning APIs. Firstly, you will gain the ability to properly scan APIs that lack a hosted definition (as is often the case) - and secondly, you will be able to scan only a particular API - ignoring the rest of the application it's attached to.

WIP Access control scan checks - When you provide Burp with a set of credentials or a recorded login to authenticate with a site, it has a good understanding of what represents authenticated and unauthenticated content on that site. This puts it in a good position to understand access control vulnerabilities. We recognize the value of this area, and we are exploring the best ways to bring access control scan checks to Burp Scanner.

Released

Released BChecks - The 2023.6.2 release introduced BChecks - a quick and easy way to extend Burp Scanner in Burp Suite Professional, using a simple text-based language. Now you can use Burp Scanner to scan for anything you want to look for.

Released Additional Montoya API functionality - Following the release of Burp's new Montoya API, we have introduced a number of new API features. Among other things, you can now work with WebSockets when building Burp extensions (BApps), and your BApps are now able to store and manage data in project files. While we will continue to add features to the Montoya API, it is already more powerful than Burp's old API ever was.

Released Collaborator payloads in Intruder attacks - Burp Suite Professional's 2023.3.2 release gave you the ability to dynamically generate Collaborator payloads in Intruder attacks. This enables you to automate out-of-band (OAST) attacks much more easily than was previously possible in Burp Suite.

Released Burp Organizer - The 2023.5.2 release introduced Burp Organizer - a brand new tool within Burp Suite that makes it easier to manage your pentesting workflow. You can use Organizer for a multitude of purposes - including storing messages you want to investigate later, or saving messages you've already identified as interesting / want to add to a report at a later time. This should lead to you having far fewer open Repeater tabs ...

Released React form handling - The 2023.4 release brought changes to the way Burp Scanner handles forms when scanning single page applications (SPAs) built on React. You'll now notice improved performance when Burp Scanner is faced with input elements that don't have an enclosing form tag.

Released Improved scanning of JavaScript frameworks - We've made multiple improvements to Burp Scanner's performance when used to scan web applications built using popular JavaScript frameworks. While the team is currently set to focus on different things, this is an area that we will periodically revisit.

Released GraphQL scan checks - You can now use Burp Scanner to check for security vulnerabilities in APIs that use the GraphQL language. GraphQL scanning broadens the range of APIs you are able to test automatically.

Released ARM64 support - Burp Suite Professional 2023.4.3 brought you the ability to use Burp on an ARM64 machine running Linux. If you're one of the many testers running Kali Linux on an ARM64 virtual machine, then this one's for you.

Burp Suite Enterprise Edition

Added to the roadmap

Added BChecks - If you've used BChecks in Burp Suite Professional, you'll know just how awesome they are for quickly and easily adding custom scan checks. But Burp Suite Enterprise Edition has so far missed out on this. No more - because we're officially inviting Enterprise Edition to the BChecks party. You'll be able to import your favorite BChecks, easily extend the scanner's capabilities, and start checking for brand new vulnerabilities.

Added Audit log - When you manage enterprise-grade software, you need to be able to see what actions your users are performing. Not least, so you can investigate anything unexpected. This is something that's currently lacking in Burp Suite Enterprise Edition. So we will soon introduce this as a feature - giving you the ability to view full audit logs of user actions, containing a record of everything that has happened in your system.

Added More compliance report types - If you're a user of Burp Suite Enterprise Edition's existing compliance reporting feature, then you'll know that it's limited to two report types (OWASP Top 10, and PCI DSS). We're about to significantly extend this - by adding reporting for OWASP ASVS 4.0, NIST, and FedRAMP. This will enable you to demonstrate compliance with a range of frameworks, much more easily.

Added Scanner auto configuration - Burp Suite Enterprise Edition's scanner is not always optimized for certain tricky types of web application. This can lead to missed attack surface. We will give Burp Scanner the ability to configure itself based on the type of web application you are scanning. This will improve scan coverage, without the need for any manual configuration.

Added Service worker networking - Burp Suite Enterprise Edition's scanner doesn't properly support service workers and WebSockets messages that occur during scans. This can cause some applications to function incorrectly - potentially leading to incomplete scan coverage. We will give the scanner the ability to properly crawl service workers and WebSockets messages - eliminating this problem.

Added API scanning improvements - Although Burp Suite Enterprise Edition can understand many features of an OpenAPI definition and scan them appropriately, coverage isn't always as good as it could be. This is because scanning currently doesn't support some popular API features. We will add these features to the scanner - enabling greatly improved coverage of web APIs.

Added Browser performance enhancements - Under the hood, Burp Suite Enterprise Edition uses embedded browsers to navigate web sites effectively while scanning. But using a pool of browsers can consume significant system resources, which impairs performance. We will change the scanner so that it uses fewer browser instances, each containing multiple isolated tabs, to enable parallel navigation. This will make scanning more efficient.

Work in progress

WIP Pre-built Amazon Machine Images (AMIs) - Soon we will begin to provide pre-built AMIs for Burp Suite Enterprise Edition. This will make it much quicker and easier for you to get Burp Suite Enterprise Edition running on AWS - by enabling you to auto-generate a suitable EC2 instance.

WIP Supply-Chain Levels for Software Artifacts (SLSA) Level 2 - Work is progressing on getting Burp Suite Enterprise Edition certified to SLSA Level 2. This help to ensure that your scanner is as resilient as possible, and will address your requirements for this level of assurance.

WIP Start scan from uploaded API definition - Work is progressing on giving Burp Suite Enterprise Edition the ability to ingest an API definition you have given it, as part of its launch process. It will then use this API definition to seed its scan. This will bring you two main benefits when scanning APIs. Firstly, you will gain the ability to properly scan APIs that lack a hosted definition (as is often the case) - and secondly, you will be able to scan only a particular API - ignoring the rest of the application it's attached to.

WIP Access control scan checks - When you provide Burp Suite Enterprise Edition with a set of credentials or a recorded login to authenticate with a site, it has a good understanding of what represents authenticated and unauthenticated content on that site. This puts it in a good position to understand access control vulnerabilities. We recognize the value of this area, and we are exploring the best ways to bring access control scan checks to the scanner.

Released

Released Pay as you scan (PAYS) subscriptions - You can now choose our Pay as you scan subscription option when you purchase Burp Suite Enterprise Edition. As the name suggests, this enables you to pay only for the scans you actually use - and is ideal for organizations just beginning their security journey.

Released CI-driven scans - The 2023.6 release brought you the ability to quickly and easily integrate automated Burp Suite Enterprise Edition scans with any CI/CD platform. In turn, this enables you to get fast security feedback to your web developers - saving on time and costs, while keeping your web estate secure.

Released GraphQL scan checks - You can now use Burp Suite Enterprise Edition to check for security vulnerabilities in APIs that use the GraphQL language. GraphQL scanning broadens the range of APIs you are able to test automatically.

Released React form handling - The 2023.4 release brought changes to the way Burp Suite Enterprise Edition handles forms when scanning single page applications (SPAs) built on React. You'll now notice improved performance when the scanner is faced with input elements that don't have an enclosing form tag.

Released Improved scanning of JavaScript frameworks - We've made multiple improvements to Burp Scanner's performance when used to scan web applications built using popular JavaScript frameworks. While the team is currently set to focus on different things, this is an area that we will periodically revisit.

Released Improved site setup - Burp Suite Enterprise Edition's 2023.4 release made it much easier to define your site scope when setting up scans. This helps to ensure that you only scan the URLs you intend to.

That's all for now. Don't forget to follow us on Twitter, to get all the latest news about Burp Suite.

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
