# Ethical hacking tools

Source: https://portswigger.net/solutions/penetration-testing/ethical-hacking-tools
Fetched: 2026-06-28T09:17:33.574873+00:00

Ethical hacking tools

Ethical hacking tools enable white hat hackers to better secure the web. And with over 47,000 users, Burp Suite is the world's go-to web app hacking software. But how did it become such celebrated hacking software? And if you've not used it yet, why do we think you should take a free trial of Burp Suite Professional?

Types of ethical hacking tool

As an umbrella term, ethical hacking covers a number of subtly different activities. At their heart though, all operators in this sphere are trying improve the online world by making it more secure. Ethical hacking includes (but isn't limited to), penetration testing, bug bounty hunting, red teaming, and cybersecurity research.

Because ethical hacking covers many different areas, there can never really be one "best tool." A hardware hacker requires very different solutions to a pentester attempting to breach a corporate network from afar, and so on. Burp Suite Professional is the world's dominant toolkit in the field of web application hacking.

Web app hacking software that does it all

Burp Suite Pro is made up of a number of components - each of which is useful in different ways to ethical hackers. The diagram below illustrates how some of the major Burp Suite components intersect, and you can also see how they fit into manual and automated workflows:

Burp Suite's ethical hacking workflow

Burp Suite is sometimes called the "the ethical hacker's Swiss Army knife". This moniker wasn't gained without good reason. Most people are amazed at its flexibility as a hacking tool when they use it for the first time. From the most granular of manual testing use cases, to automated scans of entire web apps, Burp Suite Pro makes it easy.

Hacking with Burp Suite Pro almost always begins with Burp Proxy. This man-in-the-middle (MitM) HTTP proxy is where Burp Suite hacking software began, and it still lies at the heart of our toolkit. Once intercepted by the proxy, interesting items can be sent to other areas of Burp Suite for further testing - all within one window.

As you can probably imagine, this gives ethical hackers a powerful framework for dynamic application security testing (DAST). Burp Suite Pro puts a whole array of powerful hacking, pentesting, and bug bounty tools within easy reach. We aim to make it the most streamlined, convenient, and versatile solution of its type.

Burp Suite Professional's hacking tools by type

Let's take a look at some of Burp Suite's ethical hacking tools on an individual basis. Please note that this is only a selection of some of Burp's more popular functions:

Proxy tools

As we mentioned earlier, Burp Proxy sits at the very core of Burp Suite. Thanks to a self-signed CA certificate, Burp Suite allows you to view your own HTTP requests and responses even when they are encrypted (HTTPS). This is invaluable, given that the majority of the web now uses the HTTPS standard.

As well as simply viewing HTTP(S) traffic, Burp Proxy also allows you to edit it. However, there will be times when this editing involves manual trial and error. This can be a cumbersome process. Burp Repeater makes these situations easier - by allowing you to "repeat" different iterations of a request until you find one that works.

Reconnaissance tools

You can't hack something if you don't know it exists - so reconnaissance is key for ethical hackers. There may well be content that falls within the scope of your testing that's not readily accessible, or which is dynamic. Burp Suite includes tools to get around these problems.

The content discovery function deploys a variety of methods to find hidden content and functionality. These items then get added to the site map. The methods employed include brute force techniques - but can also involve extrapolation from previous guesses. Burp Scanner (below) is especially useful when dealing with dynamically generated content.

Automated scanning tools

Burp Suite allows for extremely fine-grained manual hacking, but one of its big power features is its vulnerability scanner. Burp Scanner first uses advanced crawling logic to analyze a web application. With this complete, our customizable scanning can then throw the book at your target - including your own custom routines if you wish.

PortSwigger Research ensures that Burp Suite remains at the cutting edge of automated testing. Burp Collaborator is a case in point. This was the first out-of-band application security testing (OAST) tool to fully integrate with an automated vulnerability scanner. It makes OAST easy, while opening up large amounts of otherwise hidden attack surface.

Brute forcing tools

Sometimes it's necessary to use brute force to hack a web application's defences. Burp Intruder is designed specifically with such instances in mind. Intruder allows you to set up "positions" within an HTTP request where you want to insert payloads. It will then cycle through combinations of values - logging the target application's response in each case.

One of Burp Suite Pro's great strengths is its extensibility (see below), and one of its most popular free extensions is Turbo Intruder. Configured using Python, Turbo Intruder is slightly more complex than its standard cousin - but also much faster. Designed to achieve flat memory usage, Turbo Intruder can be reliably run for days if necessary.

Limitless expansion options

Ethical hacking tools can vary greatly depending on their specific target. Burp Suite's biggest strength is its flexibility, but it's impossible to build a tool that can do everything. That's why PortSwigger introduced the legacy Burp Extender API and the more recent Montoya API (supported from

Burp Suite 2022.9.5). These APIs enable you to write your own Burp extensions and submit them to our free BApp Store. Some BApps have achieved almost "must have" status among the Burp user community.

BApp extensions like Backslash-Powered Scanner and Param Miner can make your life as an ethical hacker much easier. They make it possible to quickly find a variety of bugs, including server-side template injection (SSTI) and susceptibility to web cache poisoning (respectively).

Why do we think Burp Suite is the best ethical hacking software?

It's true - we would say that. But the statistics don't lie. With over 50,000 users, in more than 140 countries, Burp Suite Pro is the most widely used toolkit for anyone interested in hacking web applications.

This didn't happen by chance. Our aim has always been to make Burp Suite the most flexible, most extensible, most powerful hacking software on the market. We think we've achieved that. Our users certainly seem to agree.

Of course, you don't have to take our word for any of this. Take Burp Suite for a spin with a free, no-obligation trial. We think you'll like it.

Burp Suite is an essential tool for anyone performing web application testing.

Source: TechValidate survey of PortSwigger customers

See more customer stories

Alex Lauerman

Penetration Tester

Learn more about Burp Suite Professional

Find out more
