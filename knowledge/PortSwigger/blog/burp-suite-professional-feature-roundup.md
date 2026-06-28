# Burp Suite Professional: feature roundup

Source: https://portswigger.net/blog/burp-suite-professional-feature-roundup
Fetched: 2026-06-28T09:15:10.861683+00:00

Burp Suite Professional: feature roundup

Matt Atkinson |

Thursday, 30 September 2021 at 13:39 UTC

Burp Suite

The modern web is an increasingly complex beast. Each passing year brings with it new frameworks, technologies, and design trends - not to mention vulnerabilities. All of this adds to your testing workload. It also makes AppSec daunting to learn for beginners, who lack the benefit of ever having operated in simpler times.

With Burp Suite Professional, our aim has always been to help you cut through that complexity - saving you time and making life easier. We're also educating the next generation of pentesters - with free learning in the Web Security Academy, and initiatives like our $99 Burp Suite Certified Practitioner qualification.

How Burp Suite Pro helps you to test the modern web

There are many ways Burp Suite Professional makes life easier for testers when dealing with modern web apps, but here are three major features we've introduced recently:

Testing HTTP/2

It's kind of impossible to talk about Burp Suite's feature set right now without mentioning HTTP/2 testing. HTTP/2's attack surface has barely been audited up until now - due to the complete lack of any suitable tooling - but we're changing all that.

We've now added a number of convenient manual HTTP/2 testing features developed with PortSwigger Research. These include the ability to carry out HTTP/2 exclusive attacks we pioneered, which can't be represented using HTTP/1. And of course Burp Scanner now has the ability to carry out these attacks automatically. For more information, check out James Kettle's Black Hat USA 2021 presentation: "HTTP/2: The Sequel is Always Worse".

Scanning API endpoints

The rise of single-page applications (SPAs) has gone hand in hand with an increasing reliance on APIs and microservices - which in turn has created swathes of new attack surface. To put this in perspective, Okta recently cited Gartner in predicting that by 2022, API abuses will be the most frequent attack vector resulting in data breaches for enterprise applications. And of course, since 2019, there's been an OWASP Top 10 just for API vulnerabilities.

Burp Scanner has gained the ability to scan for API security vulnerabilities - automatically parsing OpenAPI v3 REST API definitions written in JSON. This can often reveal attack surface that a traditional scanner would miss. API scanning is a feature that will grow in power alongside Burp Scanner's JavaScript scanning functionality, as well as something that will greatly strengthen the scanner itself, as it is further developed.

Cutting through complexity

The introduction of Burp Suite's embedded Chromium browser has been revolutionary for testing workflows - providing a foundation for many new features. Functionality built on the back of the embedded browser includes DOM Invader, authenticated scanning, and JavaScript scanning - and there'll be more to come.

On top of this, the embedded browser provides Burp Suite users with a quick and easy out-of-the-box setup. Simply open the embedded browser and begin proxying traffic (including HTTPS) immediately. All of the necessary proxy listener settings are automatically adjusted, and there's no need to manually install a CA certificate.

New and upcoming features in Burp Suite Professional

The features above are only the tip of the iceberg. Version 2.0 brought Burp Suite Professional bang up to date back in 2018 - with a raft of new functionality - but we didn't stop there. Check out some of the cool new stuff we've introduced, and some other features that will be dropping any day soon:

A Burp Scanner crawl and audit provides great visibility, and is designed to complement your manual testing workflow.

Burp Scanner does more

The crawler - Burp Suite 2.0's crawler was a game changer in testing the modern web when it replaced Burp 1.x's outdated Spider. This paved the way to JS scanning.

API scanning - (as above) Burp Scanner can now automatically parse many API definitions. This can be very helpful when testing microservice-based apps.

Authenticated scanning - (as above) record complex logins using Burp Suite Pro's embedded Chromium browser, and scan privileged areas of many modern web apps.

JavaScript scanning - (as above) Burp Suite's embedded browser has given it the ability to execute and scan JavaScript - cutting through more of the complexity of SPAs.

New vulnerability classes and scan checks - stay up to date with the latest vulnerabilities from PortSwigger Research - including HTTP/2-exclusive threats.

Parallel scanning - scan multiple areas of your target concurrently - with the ability to set scan configurations and priorities independently, if desired.

Improved resource management - we've introduced a number of features to help you manage Burp's use of system resources and fine-tune it to suit your machine.

Scan configuration library - curate your own library of scan types to use in different situations - including custom configurations.

Dashboard view for automated tasks - the Dashboard tab gives you a single place to monitor, control, pause, and reorder Burp Suite Pro's automated activity.

Consolidation of site-wide passive issues - Burp Scanner will now consolidate widespread passively detected issues by default - making them easier to assess.

Download the latest version of Burp Suite Professional to access all of these features and more.

DOM Invader uses Burp Suite's embedded Chromium browser to make testing for DOM XSS much easier.

Manual features help you test faster

Embedded browser - embedding Chromium within Burp has enabled many of the features in this post. It also makes life much easier for beginners - because no configuration is necessary before proxying traffic through the embedded browser.

HTTP/2 functionality - (as above) we've added a wealth of functionality to help you test for HTTP/2 vulnerabilities - including the ability to easily "kettle" requests.

DOM Invader - (as above) designed in close collaboration with PortSwigger Research, DOM Invader uses Burp's embedded browser to make DOM XSS much easier to find.

Logger - by popular demand, desktop editions of Burp Suite now include native logging functionality - giving you a record of all Burp-generated HTTP traffic.

WebSocket messages - intercept and edit WebSocket messages - including the ability to reconfigure the negotiation requests used to create WebSockets.

Save Intruder attacks in project files - you can now save attacks made using Burp Intruder to your project files. This is very convenient when working on a large project.

Message Inspector - the Inspector gives the message editor access to many Burp Suite functions, without switching tabs. It includes useful features like auto-decoding.

Download the latest version of Burp Suite Professional to access all of these features and more.

Upcoming features

Further SPA scanning capability - by automatically auditing in-scope API requests made using XHR or Fetch, Burp Scanner will exploit more SPA attack surface.

New SSTI scan checks - use Burp Scanner to detect server-side template injection (SSTI) in a wider range of templating engines, and check for blind SSTI, using OAST.

More manual testing functionality for HTTP/2 - including additional support within Burp Repeater, Extender, and the Inspector. Test HTTP/2 more efficiently.

Burp Scanner speed enhancements - fine-tuning of Burp Scanner's default settings, to enable faster scanning without compromising coverage.

Payloads within data formats - placement and encoding of Burp Scanner payloads within JSON and XML will be improved when making API calls - enhancing reliability.

Inspector improvements - based on discussion with Burp Suite users, the message inspector will be developed to give further efficiency gains in manual testing.

Message editor improvements - again, based on feedback drawn from Burp Suite's user community, we will be looking to fine-tune the usability of the message editor.

Logger improvements - including the ability to export logs as CSV files for use externally.

Please see the Burp Suite Professional roadmap for more details of upcoming features.

The Burp Suite Pro user interface has had an overhaul - and now includes features like Dark Mode.

It doesn't stop there

Of course, the most important feature of Burp Suite is the one we can't automate - it's you - the person driving it. We want to help our users develop - which is why we've introduced features like the new embedded "Learn" tab, revamped our user interface to be more intuitive, and created a range of Burp Suite Pro video tutorials. There's also a new guide on getting started with Burp Suite, for users who are completely new to the software.

Finally, if you've not already, then it's well worth taking a look at the Web Security Academy. There you'll find free learning materials and almost 200 free labs - encompassing everything from classic bugs, to the very latest vulnerabilities. And did we mention that you can now get Burp Suite certified for just $99?

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
