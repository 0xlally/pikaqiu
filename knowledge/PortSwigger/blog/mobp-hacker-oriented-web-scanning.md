# [MoBP] Hacker-oriented web scanning

Source: https://portswigger.net/blog/mobp-hacker-oriented-web-scanning
Fetched: 2026-06-28T09:15:20.191121+00:00

[MoBP] Hacker-oriented web scanning

Dafydd Stuttard |

Monday, 17 November 2008 at 07:08 UTC

MoBP

burp

Pen Testing

scanners

Next month will see an exciting addition to the Burp family: a brand new web application vulnerability scanner.

Before going any further, I'll note that this new product will only be available to users who pay a nominal subscription to use the commercial version of Burp, so if for some reason you object to people writing software for a living, please look away now.

Burp Scanner is designed for hackers, and fits right into your existing techniques and methodologies for performing semi-manual penetration tests of web applications. You have fine-grained control over each request that gets scanned, and direct feedback about the results.

Using most web scanners is a detached exercise: you provide a start URL, click "go", and watch a progress bar update until the scan is finished and a report is produced. Using Burp Scanner is very different, and is much more tightly integrated with the actions you are already carrying out when attacking an application. Let's see how.

When you are testing an application and find an interesting request, you might intercept it with Burp Proxy to modify parts of the request. You might send it to Repeater to reissue the same request with different inputs. Or you might send it to Intruder to perform various automated custom attacks. In future, you can also send the request to Burp Scanner to scan for a wide range of vulnerabilities within that single request. The results of the scan are shown immediately, and can inform your other actions in relation to that request. You can even modify the base request in arbitrary ways, and re-scan it, combining your own knowledge and understanding of how web applications commonly fail with Burp Scanner's powerful capabilities for discovering many types of vulnerabilities.

It's time for some eye candy. Below, we have intercepted a request, and send it to Burp Scanner to perform an active scan (this is one which sends crafted requests to the target application, and analyses its responses looking for vulnerabilities):

All requests sent for active scanning land in the scan queue. Below, we have sent a large number of requests for scanning. A typical request with a dozen parameters is scanned in a couple of minutes, and the scan queue is processed by a configurable thread pool, so the number of waiting items rarely grows very large:

As each item is scanned, the scan queue table indicates its progress - the number of requests made, the percentage complete, and the number of vulnerabilities identified. This last value is colourised according to the significance and confidence attached to the most serious issue. We can double-click any item in the scan queue to display the issues identified so far:

Each issue contains a bespoke advisory, and also the full requests and responses which Burp Scanner used to identify the vulnerability. Of course, you can send these requests to other tools, to further understand the issue and perform follow-up attacks:

In addition to tracking the issues that are identified for each individual scanned request, Burp maintains a central record of all the issues it has discovered, organised in a tree view of the target application's site map. Selecting a host or folder in the tree shows a listing of all the issues identified for that branch of the site, enabling you to quickly locate interesting vulnerable areas of the application for further exploration:

Used in this way, Burp Scanner can be of huge benefit when you are testing a web application. Being able to perform quick and reliable scans for many common vulnerabilities on a per-request basis reduces your manual effort, enabling you to direct your human expertise towards vulnerabilities whose detection cannot be reliably automated. This mode of scanning also addresses a common frustrating problem, in which a monolithic automated scan takes an age to complete, with little assurance over whether the scan has worked, or whether it encountered problems that impacted on its effectiveness. By controlling exactly what gets scanned, and by monitoring in real time both the scan results and the wider effects on the application, you combine the virtues of reliable automation with intuitive human intelligence, often with devastating results.

In this post, I've described just one way in which Burp Scanner can be used to help automate the discovery of web application vulnerabilities. In the next few days, I'll explore some other key aspects of its functionality, and other ways in which it can be used to help you hack web applications.

MoBP

burp

Pen Testing

scanners

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
