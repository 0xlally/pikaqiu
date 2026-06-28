# Live scanning

Source: https://portswigger.net/blog/live-scanning
Fetched: 2026-06-28T09:15:19.419519+00:00

Live scanning

Dafydd Stuttard |

Sunday, 19 August 2018 at 15:56 UTC

MoBP

Burp Suite

For a very long time, Burp has had two cool capabilities that are of huge value to manual testers:

Automatically scan requests that are made via the Proxy.

Automatically add items to the site map as you browse.

The way that you do these things is changing, and getting a lot more powerful. In the new Scanner, these are called live scanning tasks.

One big change is that you will now be able to perform live scanning of traffic from other Burp tools, not just the Proxy. You can select which tools to monitor, the URL scope, and whether to deduplicate items:

There are two types of live scanning tasks, corresponding to the legacy features described above:

Live audit - This scans each request for vulnerabilities.

Live passive crawl - This populates the site map with items derived from the request.

Another change with the new passive crawling is that you will have much finer-grained control over what gets added to the site map. Currently, Burp adds every single link that is found in responses. In modern web sites, this means that browsing a single page often causes Burp's site map to be polluted with dozens of uninteresting domains. You will now be able to configure exactly what gets added to the site map:

For example, you could tell Burp to add only links that belong to the same domain that was requested, or belong to any in-scope domain.

Another huge benefit of the new live scanning capability is that you can create as many distinct tasks as you like, each with a different scope and configuration. So you could, for example, create tasks to perform:

A passive audit of all traffic.

A quick audit for XSS and SQL injection on a certain domain.

A full audit of URLs that match a specific pattern.

The possibilities here are endless, and we look forward to hearing your stories of what you have achieved with the new live scanning tasks.

MoBP

Burp Suite

Dafydd Stuttard

@DafyddStuttard

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
