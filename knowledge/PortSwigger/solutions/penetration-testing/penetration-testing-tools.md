# The top 10 best pentesting tools and extensions in Burp Suite

Source: https://portswigger.net/solutions/penetration-testing/penetration-testing-tools
Fetched: 2026-06-28T09:17:33.674975+00:00

The top 10 best pentesting tools and extensions in Burp Suite

Skip the intro - show me the top 10 pentest tools

Penetration testing tools allow proper assessment of a system's cybersecurity within a sensible timeframe. Of these tools, Burp Suite Professional is one of the most widely used. With more than 55,000 users in over 150 countries, it's the world's go-to tool for web app penetration testing.

One of Burp Suite Pro's great strengths is its extensibility through free plugins. Here, we're going to look at 10 of the best pentesting tools you can add to Burp Suite. We're also going to recap some of Burp's core functions and discuss what makes them so good for security testing.

Methodology

To produce our list of top penetration testing tools, we first looked at popularity figures from the BApp store - PortSwigger's free online library for Burp Suite extensions (BApps). Next we canvassed the opinion of the PortSwigger Research team, before consulting the Burp Suite user community.

The top 10 Burp Suite extensions for pentesters

Updated: December 2019

Logger++

Author: Soroush Dalili & Corey Arthur

Burp Suite Pro allows you to proxy every request and response you put through it. But there are occasions when you need to see more. What is Burp Scanner, or a particular extension doing behind the scenes, for instance?

Well, whether you're debugging an issue, or just want to take a closer look at what Burp Suite is doing, Logger++ gives you what you need. It stores all Burp's requests and responses in an easily exported and sortable table.

Read more

"Logger++ is essential when I'm testing a site. The ability to log outgoing requests is really important when using other extensions like Hackvertor that modify them."

Gareth Heyes

Web Security Researcher

Autorize

Author: Barak Tawily

If you've ever manually tested a reasonably large web application for access control issues, then you probably know it's no fun. It takes forever and bores most pentesters to tears. Fortunately, a convenient pentesting tool called Autorize can help you make light work of this task.

The first step in using Autorize is generally to feed it the cookies of a non-privileged user within a web application. Next, browse the app, using the cookies of a user who does have privileged access. As you use privileged functions, Autorize will repeat your requests as if it is a non-privileged user. It then logs the status of these attempts in a color-coded table.

Read more

I LOVE AUTORIZE! BEST BURP EXTENSION? That is all...

Curtis Brazzel

Turbo Intruder

Author: James Kettle, Director of Research, PortSwigger

Simple to use and eminently stable, Burp Intruder is a powerful bruteforcing tool. But for some tasks, you really can't have enough power. Enter: Turbo Intruder. Built for speed using a custom HTTP stack, and configured in Python, Turbo Intruder is blisteringly quick. In fact, it's capable of making tens of thousands of HTTP requests per second, if necessary.

Turbo Intruder is great for finding race conditions, as well as performing complex attacks involving multiple steps, or signed requests, for example. It's highly configurable and is designed to achieve flat memory use - so it can run for days if it has to. If you're half-decent in Python and this sounds like fun, we highly recommend taking Turbo Intruder for a spin.

Read more

Thank you @albinowax for the incredible Turbo Intruder. Intruder took 13 mins to send 52709 payloads. Turbo Intruder took just 30 seconds. Loving this speed.

nav

J2EEScan

Author: Enrico Milanese

Straight out of the box, Burp Scanner can find a whole host of vulnerabilities. But there's always room for improvement - especially if you're operating in any type of a niche. If you find yourself testing applications that make use of J2EE on a regular basis, then J2EEScan is for you.

J2EEScan adds a catalogue of over 40 J2EE-specific vulnerabilities to Burp Scanner's automated pentesting repertoire. This is a great add-on that expands Burp Suite Pro's web vulnerability scanning capabilities into a useful new area.

Read more

#ProTip: J2EEScan is another great @Burp_Suite plugin, to discover J2EE vulnerabilities.

raptor

Backslash Powered Scanner

Author: James Kettle, Director of Research, PortSwigger

Vulnerability scanners are great, but there are cases where there's no substitute for human deductive reasoning, right? Well, yes and no. Don't forget that scanners can do many things a human alone can't. There's really no replacement for either. Backslash Powered Scanner bridges this gap and helps pentesters find interesting items to investigate manually.

It does this by mimicking human intuition. As a result, it can detect many bugs traditional scanners would miss. Some of these are known; others will be completely novel. It's not a panacea - items marked as "interesting" do then require manual attention. But still, Backslash Powered Scanner is a potent tool in the hands of expert Burp Suite users.

Read more

Check out James's NorthSec presentation

"Backslash Powered Scanning: Automating Human Intuition."

Upload Scanner

Author: Tobias Ospelt

Web applications allowing users to upload their own files is a classic cause for concern in penetration testing. If users are allowed to upload files in a risky manner, there are myriad ways it can be exploited. This means that file upload functions can take some time to evaluate - time most pentesters don't have to waste.

Upload Scanner is a pentesting tool that could save you a lot of time. It has the ability to upload a number of different file types, laced with different forms of payload. Upload Scanner can test for vulnerabilities including server-side request forgery (SSRF) and XML external entity (XXE) injection using common file types like JPEG, PDF, and MP4 as vectors.

Read more

Upload Scanner plugin is fantastic. I've found quite a bit with it. @floyd_ch

cryptosecdev

Retire.js

Author: Philippe Arteau

With the abundance of JavaScript out there nowadays, it's easy to find yourself running outdated libraries that contain known vulnerabilities. Retire.js is a popular repository of JavaScript libraries that include known bugs, and this dedicated plugin makes it available within Burp Suite Pro as a passive scan check.

One of Burp's biggest strengths has always been its flexibility and adaptability. Retire.js may be simple, but it fits right into this philosophy. Small wonder it's the third most downloaded tool in the BApp Store.

Read more

If you use @Burp_Suite you need to use the Retire.js plugin, such a time saver: portswigger.net/bappstore/3623 ...

Jerry Gamblin

JSON Beautifier

Author: Jake Reynolds

JSON is many things, but in its compressed state, "beautiful" isn't one of them. How often have you intercepted a response including data set in scrunched-up JSON and let out a sigh? Given that JSON is used in more or less everything nowadays, you'll be pleased to know that this beautifier tool makes it much easier to work with in the pentesting context.

A simple tool, JSON Beautifier gives you the option to either "beautify" or "minify" (crunch back up) your target's JSON content. All of this takes place within Burp Suite. This is the most popular download in the BApp store, and it makes life as a pentester much easier. We love it.

Read more

AuthMatrix

Author: Mick Ayzenberg

We already mentioned Autorize (#2), which is a simple tool for speeding up testing of user access control functions. AuthMatrix made our list because it's a really useful - if slightly more complex - addition to this setup.

AuthMatrix gives pentesters a simple matrix grid to define the desired levels of access privilege within an organization/web app. It then tests each function for different types of user. One of AuthMatrix's best features is a "chain" mode, which enables cross-site request forgery (CSRF) tokens to be grabbed from requests and attached to subsequent attempts.

Read more

Param Miner

Author: James Kettle, Director of Research, PortSwigger

That's right: a third extension from PortSwigger's very own James Kettle. You could accuse us of bias - but hear us out first. There's a reason James's tools are so popular. The idea for this one came back when he was initially researching web cache poisoning. He needed a way to quickly find unkeyed inputs - and so Param Miner was born. It finds hidden parameters that can be used for just about any purpose.

Param Miner makes it easy to find potential vectors for a web cache poisoning attack. It's capable of guessing up to 65,000 parameter names per request. And it was written by the researcher who proved that web cache poisoning is more than just a theoretical concern. To find out more, check out the whitepaper, or watch James's Black Hat presentation, below:

Read more

Check out James's Black Hat USA presentation

Practical Web Cache Poisoning: Redefining "Unexploitable"

Burp Suite Professional's core penetration testing tools

Our top 10 list here concentrated solely on extensions. Extensions are perfect for tweaking Burp Suite to suit your particular pentesting niche. But Burp Suite Pro gives you a veritable arsenal of pentesting tools to play with straight out of the box.

PortSwigger's founder, Dafydd Stuttard, developed the initial version of Burp as an intercepting HTTP proxy around the time he was writing the first edition of The Web Application Hacker's Handbook. Daf still leads our development team, and since those early days, we've seen Burp Suite grow in its capabilities with every update.

"When I started out as a security tester, web penetration testing was only just getting started. There weren't any decent software tools to help do the job. Testing for web security issues was highly manual, tedious, and error-prone. I was lazy enough to want to automate my job, so I decided to write my own tools. The result was Burp Suite - a toolkit with all the features I needed to make my work faster, easier, and more reliable. It's gratifying to see thousands of other testers now using Burp Suite as a force multiplier to make their work more effective."

Dafydd Stuttard

Founder of PortSwigger

Burp Scanner - customizable automation

Burp Scanner is without a doubt the most powerful pentesting tool in Burp Suite Professional. Capable of crawling just about any web app you might want it to, Burp Scanner's attack engine is a powerful ally for a tester to have on their side.

It's not just that Burp Suite can throw the book at your target; Burp Scanner's customization options are where it really shines. The ability to easily automate your own routines can be a real game changer for pentesters.

Burp Collaborator - see around corners

PortSwigger prides itself on its research credentials. Our team regularly present their findings at conferences like Black Hat and DEF CON. Burp Suite's continuous development stands as testament to this. Burp Collaborator is a great example.

When Burp Collaborator was released, it was a pioneer in the way it delivered fully automated out-of-band application security testing (OAST). This meant that without lifting an extra finger, users of Burp Scanner could suddenly "see around corners". This revealed many bugs previously hidden to dynamic application security testing (DAST) alone.

Burp Repeater - manual pentesting made easy

At its heart, Burp Suite is an intercepting proxy. Manually proxying HTTP(S) traffic can provide a great deal of insight into a target web application's behavior. But when a pentester has a lot of ground to cover in a short space of time, large amounts of manual hacking can soon become an unwelcome task.

Burp Repeater is designed to assist in these situations by making it simple to "repeat" an HTTP request numerous times. Of course, the request is rarely repeated verbatim. Rather, the beauty of Burp Repeater is that it allows a tester to manually edit such requests in order to find what they're looking for.

Burp Intruder - flexible bruteforcing

Brute force methods like fuzzing can open up whole new dimensions for pentesting. And Burp Intruder makes it easy to drop brute force payloads right where you want them. It's one of the most useful penetration testing tools on the market.

With a number of attack configurations available, Burp Intruder continues PortSwigger's philosophy of keeping powerful flexibility right on tap. Whether you're trying to bruteforce a value for a single position or a number of them in tandem, Intruder gives you the means.

A truly adaptable pentesting tool

The ability to adapt to any situation is key to successful pentesting. Whenever we add new features to Burp Suite, we design them with flexibility in mind. With our software, powerful pentesting tools are always kept close at hand.

The BApp Store exemplifies this philosophy by enabling you to further expand and customize Burp Suite's capabilities. If you need something done, then Burp Suite can probably do it. Take a free trial today and see what it could do for your pentesting.

With the wide range of different extenders, almost everything can be done directly from Burp Suite without needing to use Python scripting. I extensively use OAST and IAST, which is a perfect combination for pentesting.

Source: TechValidate survey of PortSwigger customers

See more customer stories

Andrej Šimko

Security associate manager, Accenture

Take a free trial of Burp Suite Professional

REQUEST A TRIAL
