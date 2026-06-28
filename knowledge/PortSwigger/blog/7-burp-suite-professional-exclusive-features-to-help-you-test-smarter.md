# 7 Burp Suite Professional-exclusive features to help you test smarter

Source: https://portswigger.net/blog/7-burp-suite-professional-exclusive-features-to-help-you-test-smarter
Fetched: 2026-06-28T09:15:06.177645+00:00

7 Burp Suite Professional-exclusive features to help you test smarter

Matt Atkinson |

Friday, 26 February 2021 at 15:25 UTC

Burp Suite

Welcome to the Pro user community

So, you've downloaded Burp Suite Professional. What now? It's a big piece of software, and there's a lot of functionality you're probably not aware of - even if you've used Burp Suite Community Edition in the past.

We want to help you get the most from Pro, and show you how its features combine to help speed up and improve your testing. With this in mind, we put together a list of power features we recommend checking out. All of these are exclusive to Burp Suite Professional - and they're a big part of the reason so many users (62,000 and counting) subscribe to it.

Burp Suite's feature set is always growing. If you'd like to see what else is likely to drop in the near future (spoiler alert: it's going to be awesome), check out our July 2022 roadmap update. Now, without further ado, here are some of our favorite Burp Suite Professional-exclusive features:

1. Project files

How to save a project in Burp Suite Professional.

It might seem a little odd to lead this article with Burp Suite's "save" function, but hear us out. Burp Suite Professional project files are more useful than you might realize at first glance.

Project files are capable of saving literally everything you do in Burp Suite Professional while on an engagement. You don't even need to click "save" before you exit. Ok - great - but what's so cool about that?

Well firstly, the obvious. Project files give you peace of mind that you're not about to lose a bunch of urgent testing work to some weird technical issue. Having your data saved also makes the dreaded pentest report a whole lot easier to write.

Furthermore, as we all know, being a pentester often means dealing with the requests of clients. Picture this scene, if you will:

"Oh - hey - remember that pentest you did for us six months ago? Well, it turns out that we're being audited, and now we need a list of literally everything you did. You've got that, right?"

Well actually, with Burp Suite Professional project files, you do. We don't call it "Pro" for nothing.

2. Full speed Burp Intruder

How to use Burp Intruder.

Whenever we speak to customers about Burp Suite Professional, you can be fairly sure that Burp Intruder will get flagged as a favorite tool. It's a real classic; just select the insertion point(s) you'd like to attack, choose an attack type, and configure a list of payloads to drop. Then use Intruder's filtering tools to harvest useful data from your responses.

This approach is incredibly flexible. Whether you're doing something as simple as brute force guessing web directory entries, or hunting something more complex - like blind SQL injection - Burp Intruder's got your back.

Intruder runs fast - which means it can produce a lot of data. Because of this, we've included features to help users find interesting responses as easily as possible. Take the extract grep function, for example. Once set up, Intruder will pull out whatever it is you're looking for, and arrange it nicely for you in sortable columns.

If you're new to Intruder, you might like to check out one of our tutorials. Learn how to use Intruder to brute-force a login mechanism, or to enumerate subdomains.

3. Free, Pro-exclusive BApp extensions

The BApp Store.

With Burp Suite Professional, our aim is to help our users perfect their security testing workflows - enhancing both speed and reliability. But pentesting is a huge subject, with many specialized areas. Enter: the BApp Store - containing over 250 free curated Burp Suite extensions sourced from Burp's huge user community - including PortSwigger's researchers themselves.

Many BApps are exclusive to Burp Suite Professional. These include perennial user favorites like Backslash Powered Scanner (great for finding server-side injection vulnerabilities) and Param Miner (which finds hidden, unlinked parameters, and is awesome for hunting web cache poisoning vulnerabilities) - as well as more situational extensions like Detect Dynamic JS and NGINX Alias Traversal.

Check out the BApp Store to discover the extensions that'll help you fine-tune Burp Suite Professional for your particular use case, no matter what party you're due to attend.

4. The search function

How to search in Burp Suite Professional.

Another of Burp Suite Professional's useful added features over Community Edition is its search function. As the name suggests, this enables you to quickly search everything you have open in Burp Suite for specific references. You can narrow your focus to particular Burp tools, search by regex, have your search update itself dynamically, and much more.

While this might sound like an obvious feature, we've lost count of the number of times it's saved us time during testing. Use it to quickly search for intermittent issues, sensitive content, or places where your own specific inputs resurface.

More specifically, a great example of the power of search in Burp Suite Professional comes when testing for server-side request forgery (SSRF) and needing to find an internal IP address or hostname to create a successful exploit. The ability to quickly search everywhere in Burp Suite Pro is brilliant for this, and can save you a lot of time on an engagement.

5. Burp Collaborator client

How to use Burp Collaborator client.

Most testers know that PortSwigger pioneered automated OAST testing when we released Burp Collaborator. This made Burp Scanner capable of performing the (formerly tricky, but ultra-reliable) OAST testing method quickly, and at the touch of a button.

But did you know that Burp Suite Professional makes manual OAST a lot more accessible too? Burp Collaborator client is the tool for this - and makes a whole range of advanced vulnerabilities much easier to find.

Either use Burp Collaborator's public server to have Burp Suite Professional check for dangerous interactions straight out of the box, or deploy your own private Collaborator server. Either way, Burp Collaborator client makes manual OAST testing much quicker and easier.

6. Content discovery

How to use content discovery in Burp Suite Professional.

The content discovery feature is another great example of how Burp Suite Professional's automation can help to speed up and improve your manual testing. This feature can automatically discover content and functionality that isn't linked to from anywhere visible within an application - logging these locations for further sleuthing.

To start content discovery, simply select a request in Burp Suite Professional's site map, right click, and select "engagement tools" followed by "discover content". The software will then use a range of automated techniques to look for things you might be interested in.

Techniques applied include name guessing, web crawling, and extrapolation from naming conventions observed elsewhere in the application. And of course, being part of Burp Suite Professional, this feature is fully adjustable - allowing you to tailor it for the particularities of your target application.

7. Burp Scanner

How to use Burp Scanner in Burp Suite Professional.

Burp Scanner is one of Burp Suite Professional's headline features - so it's perhaps a little unsurprising that we'd mention it here. But with Burp Suite Professional you can use the scanner for a whole lot more than simply running an automated scan of an entire target application.

In fact, as counterintuitive as it might sound, Burp Scanner contains a number of features that can give footholds to manual testers. This can improve the depth of your testing, save you from tedium, and give you more time to investigate the types of things you actually enjoy.

Focused Burp scans are a great way to gain footholds for manual testing.

Imagine you're manually looking through a bunch of HTTP requests, and you come across something you think looks exploitable. Did you know you can perform a Burp Scan on just that one request? Simply right click on the request, and click "Do active scan", to fire up a focused Burp scan.

Couple the above technique with Burp Intruder to zoom in even further. Right click a request, send it to Intruder, and manually add insertion points in your desired positions. Then right click the request and select "Scan defined insertion points". Because this technique limits the number of requests made by Burp Scanner, it can yield results for you to play with extremely quickly.

Want to go further still? Try using the Logger tool to watch your target server's responses to Burp Scanner's payloads. This is a great way to watch for interesting behavior you might be able to exploit.

Put Burp Suite Pro through its paces

Burp Suite Professional is a huge product, with a wealth of new functionality to try, even if you've used Burp Suite Community Edition in the past. If you've not already checked it out, then the free Web Security Academy is a great way to get to grips with what Burp Suite is capable of, while learning about the latest hacking techniques.

More specifically, certain Web Security Academy labs offer a great way to experience how some of the tools we've mentioned above can make your life as a tester much easier. We'd particularly recommend the labs on broken 2FA authentication (to see how fast you can bruteforce things with Burp Intruder), or blind SQL injection with out-of-band data exfiltration (to try out Burp Collaborator client). You might also like to check out our Burp Suite tutorials.

Last, but by no means least, we've released a series of Burp Suite Professional video guides. These are probably the fastest way for new users of Burp Suite Pro to get to grips with the product - and they're even voiced over by Burp Suite's original creator, Dafydd Stuttard.

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
