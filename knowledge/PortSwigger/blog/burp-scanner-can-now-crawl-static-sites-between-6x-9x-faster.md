# Burp Scanner can now crawl static sites between 6x - 9x faster

Source: https://portswigger.net/blog/burp-scanner-can-now-crawl-static-sites-between-6x-9x-faster
Fetched: 2026-06-28T09:15:08.773508+00:00

Burp Scanner can now crawl static sites between 6x - 9x faster

Matt Atkinson |

Wednesday, 6 April 2022 at 10:43 UTC

Burp Suite

Burp Suite Professional version 2022.2.3 made Burp Scanner's crawler between 6x - 9x faster when used against static or stateless sites. This helps you to carry out automated reconnaissance much faster than before. Ensure you are using the latest version of Burp Suite Professional - and select the "Fastest" crawl strategy when creating a new Burp Scanner task, to see it in action.

To access Burp Scanner's crawl strategies in Burp Suite Professional, go to the Dashboard, click the New scan button, then click Scan configuration > New … > Crawling > Crawl Optimization > Crawl strategy.

Crawler? What's that?

When we released Burp Suite 2.0 back in 2018, it brought with it a lot of changes. Not least of these was the replacement of the venerable Spider tool with an all-new crawler. This meant that for the first time, the reconnaissance phase of testing could be fully integrated with Burp Scanner.

The crawler is far better suited to the demands of the modern web than the Spider ever was. It's smart enough to navigate and perform reconnaissance even on today's dynamic, stateful, and / or JavaScript-heavy apps - and we are continuously developing these capabilities.

We'd like to introduce the new improved "Fastest" crawl strategy. You could call it an "incy wincy" version of the crawler …

The problem with overthinking

The trouble is that not every web application you might use Burp Suite to test is based on cutting-edge technology. There are plenty of sites out there that lack any of the complex functionality described above, and instead make do with good old-fashioned static HTML.

Static HTML sites aren't particularly complicated - but performing manual reconnaissance on these basic applications still takes time. While Burp's crawler can help you at this point, by automatically navigating your target site, in the past it hasn't been ideally suited to simplistic static applications of this type. Effectively, the problem was that the crawler was too smart for its own good - it was overthinking things.

In testing, we've seen crawl speeds improve by between 6x - 9x

Because of this, some Burp users noted that the crawler wasn't always faster than the original Spider when crawling static sites. While Burp Scanner's "Fastest" crawl strategy was optimized for applications lacking in stateful functionality, we knew there was much more performance to be had from it in this context.

As part of the 2022 Burp Suite Roadmap, we've been looking at various ways to improve scan speeds - and as such, we've been working on improving the issue above. So we'd like to introduce the new improved, stripped-down "Fastest" crawl strategy. You could call it an "incy wincy" version of the crawler …

If you've read our deep dive, "Web application cartography: mapping out Burp Suite's crawler" by PortSwigger scanner engineer Tom Shelton-Lefley, you'll know that automatically navigating a complex modern web application is no mean feat. Because of this, the crawler has to do some fairly heavy lifting.

In analyzing the crawler's actions on basic static sites, we could see one process in particular standing in the way of a faster crawl. This was the process allowing Burp's crawler to navigate stateful applications - where being aware of the path it has taken to arrive at a page is important - but is not required when state is not an issue.

Stateful application architecture means that a change in state from one page could easily change what you find when you open a different page. The addition of items to a shopping cart is a good example of this change in state. This means that for a stateful app, Burp's crawler needs to be aware of the actions it has taken to arrive at a page in a certain state.

But this problem becomes irrelevant when dealing with an app that isn't stateful. This meant that we could remove this process from Burp Scanner's "Fastest" crawl strategy. And because Burp Scanner is no longer concerned about an application's state, it's able to crawl and scan it for vulnerabilities much faster - making fewer requests in the process.

Benchmarking the new strategy - how much faster is it?

Burp Suite's documentation is a great example of some entirely static content. While there's a wealth of knowledge contained within its hallowed pages, there certainly isn't anything revolutionary going on in terms of functionality. For this reason, it made a great benchmark to measure the new "Fastest" crawl strategy by.

When you do this, the results are nothing short of astounding. In testing, we've seen crawl speeds improve by between 6x - 9x, depending on whether or not Burp's browser is enabled. (Burp's browser enables crawling of applications where pages are built on the client side using JavaScript - see our deep dive on browser powered scanning for more details.)

In short: using the improved "Fastest" strategy

Burp Scanner has five crawl strategies for you to choose from - ranging from "Fastest" to "Most complete". Generally speaking, these range from being suitable for completely static sites without any stateful functionality ("Fastest"), to being best suited to complex applications which are heavily stateful, including modern single page applications ("Most complete").

If you were to use the "Fastest" crawl strategy on a single page application written using a library like React, you would probably be disappointed - because it would find little attack surface to test. Equally, if you were to use the "Most complete" strategy on a totally static site with no stateful functionality, you would find yourself waiting much longer than necessary for the crawl to complete.

The key is context. By selecting the right crawl strategy for your target application, you can maximize the extra value Burp Suite Professional enables you to deliver - finding more vulnerabilities, faster. For more information, see our documentation on Burp Scanner crawl strategies - or check out our guide to running your first Burp Suite Pro scan if you're not yet acquainted with Burp Scanner.

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
