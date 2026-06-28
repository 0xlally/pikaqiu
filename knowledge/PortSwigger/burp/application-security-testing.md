# Web application security testing

Source: https://portswigger.net/burp/application-security-testing
Fetched: 2026-06-28T09:15:29.517591+00:00

Web application security testing

What is web application security testing?

Web application security testing aims to determine whether or not a web app is vulnerable to attack. It covers both automated and manual techniques across a number of different methodologies.

Web applications are everywhere

Years ago, when desktop applications were still the order of the day, web apps were much rarer than they are now. Technically, any client-server program that's accessed using a web browser is a "web application" - which nowadays includes the vast majority of the internet. Web apps are just more flexible for many purposes.

From simple contact forms and e-commerce checkouts, right the way up to social media platforms and online banking systems. If you access it through a browser, then it's a web app. A web application could form a small part of a website, or it could be a website in its own right.

Everyone is at risk of a data breach

One thing all web applications have in common is that they handle data - a valuable commodity. And like any commodity, data has a storage risk. Groups exist who want to steal data - whether it's for surveillance purposes, to commit fraud, or simply to sell on.

This means web application security is crucial. But in the real world, securing a web application is no easy task. For starters, the developers who build web apps tend not to be security specialists. And new security vulnerabilities are being discovered all the time - so it's hard to keep up.

Enter: web application security testing

The solution is to test your web apps to see where their weaknesses lie. To use the analogy of a bank vault, you would first ensure that it was designed correctly. Then you might employ a team of specialists to try and break into it. You would keep doing this as time went on and new weaknesses were discovered - altering the vault accordingly.

You'll see below that this is not so different to web app security testing. The walls of the "vault" are now code, and many (but not all) of the actors involved are automated, but the theory is the same. Build it strong and keep it strong - testing every attack method you can.

Types of web application security testing

There are various concepts in web application security testing. Among the best-known are:

Dynamic application security testing (DAST)

DAST works from the outside-in on a running app. It's a lot like having a team of experts try and break into your bank vault for you. This is what's known as a "black box" security testing technique - because the code running behind the web app is not visible to the test. This mimics a real attack. Burp Suite evolved largely out of a DAST methodology.

Because DAST is a practical technique - simulating a real attack on a running web app - its results can generally be assumed to be correct. All things being equal, DAST will generally report far fewer false positives than SAST, for instance (see below).

Static application security testing (SAST)

SAST is more or less the opposite of DAST. It works from the inside-out on static code. A good analogy would perhaps be having an expert view the blueprints for your bank vault to look for flaws. This is what's known as a "white box" security testing technique - because the test can see the web app's code in its entirety (unlike most real attackers).

Unfortunately, because SAST works on a theoretical, rather than a practical level, it is prone to reporting false positives. These then require manual investigation, which costs time and money. And, like the boy who cried wolf, SAST's nature can cause its warnings to be ignored by users in real-world scenarios.

Interactive application security testing (IAST)

IAST modifies a running application in order to find vulnerabilities. It's a lot like placing sensors inside your bank vault to see what effect your (DAST) attacks are having. This is known as a "gray box" security testing technique - effectively being a mixture of black box and white box methodologies. It can see vulnerabilities that DAST alone would be "blind" to.

Because of its invasive nature, IAST should not be used in production systems. This limits its application to a test environment. It's also a reason that OAST (see below) can be considered a "best of all worlds" security testing technique.

Out-of-band application security testing (OAST)

OAST is a technique PortSwigger pioneered. As we know, because DAST doesn't see things unless they cause a visible difference from the outside, it's possible to for it to miss "blind" vulnerabilities. OAST fixes this - while reporting virtually no false positives and without modifying the application.

So OAST reaps many of the benefits of the three techniques above, while minimizing their downsides. Like SAST and IAST it can see vulnerabilities that DAST cannot - but it's not prone to reporting false positives in the way that SAST is. And while IAST is an invasive method to use, OAST doesn't make such changes - so it's much safer.

Different uses for web app security testing

As we've already seen, nowadays, almost every website is also a web application. But different situations come with different security testing challenges.

Testing every type of web technology

Web applications themselves come in a number of different flavors. These include mobile apps, single page apps (SPA) and progressive web apps (PWA). Each has a distinct set of requirements for security testing. SPAs, for instance, make heavy use of JavaScript - which is notoriously difficult for automated scanners to process.

Staying compliant

Certain industries also have their own very specific needs. Finance and e-commerce, for instance, are heavily regulated by cybersecurity compliance standards due to the level of data they hold on their customers. This makes security testing critical.

Automating at scale

The size of an organization using security testing will also affect its chosen solution. Certainly at the enterprise level - where many thousands of web apps might sit within a single portfolio - automation is vital. But an automated vulnerability scanner can't employ creativity like a human can, so manual penetration tests should always be carried out.

Penetration testing

Penetration testers (or pentesters) are the experts who can simulate attacks on your "vault" in order to improve it. And pentesting itself sits under the larger umbrella of ethical hacking. Ethical hacking also includes bug bounty hunters, who will race to find security bugs in a web app if a bounty is offered. One way to initiate this is through a scheme like HackerOne.

Secure development

As we touched on earlier, a prime factor in securing a bank vault would be to ensure that it was built well in the first place. Traditionally, web app security is delayed until after development has ended, which causes delays and can cost a great deal of money. Quite simply, it's difficult to develop software and worry about security at the same time.

But the power of automated security testing allows a DevSecOps approach. DevSecOps empowers developers to write secure code. And because security is built in, rather than tagged on at the end, apps are more secure on release day. The best DevSecOps solutions even educate the developers who use them - meaning fewer bugs to fix in the first place.

Web application security testing software

PortSwigger makes Burp Suite - a widely adopted software solution for web security testing. Burp Suite is available in two main versions. Both include our acclaimed web vulnerability scanner, but package it in very different ways:

Burp Suite DAST

If you manage a portfolio of web apps, or you're looking for software to support DevSecOps, you'll be interested in Burp Suite DAST. Burp Suite DAST offers fully automated and scheduled scanning, extreme scalability, and integration with any development environment.

Burp Suite Professional

Burp Suite Professional includes our scanner as part of an advanced toolkit aimed at penetration testers and bug bounty hunters. The most widely used software of its type, with over 40,000 users, Burp Suite Professional is often called the ethical hacker's Swiss Army knife.

Burp Suite has been my standard tool for some years now when it comes to web app testing. No other tool that I know of is so flexible and offers the functionality in one suite.

Source: TechValidate survey of PortSwigger customers

See more customer stories

Jan Muenther

Application Security Manager

Learn more

Find out what Burp Suite could do for you, according to your particular use case:

Development teams

Organizations

Penetration testers
