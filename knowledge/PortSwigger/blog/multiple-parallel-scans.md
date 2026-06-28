# Multiple parallel scans

Source: https://portswigger.net/blog/multiple-parallel-scans
Fetched: 2026-06-28T09:15:21.486057+00:00

Multiple parallel scans

Dafydd Stuttard |

Tuesday, 14 August 2018 at 15:57 UTC

MoBP

Burp Suite

The current Spider and Scanner tools are pretty good at letting you do one thing at a time. They let you define your configuration and scope. They each employ a single queue of work. They can be paused and resumed.

But if you want to do multiple scans of different areas, with different configurations, and different priorities, and monitor and control each scan independently, then you're stuck.

All of this will soon change. The Spider and Scanner are going to disappear as top-level singleton tools, with their global configuration and queues of work. In their place, you'll be able to kick off individual scans. Each scan can be assigned to do something different: crawl a particular web site, audit a bunch of selected requests, or perform an end-to-end crawl and audit.

Each scan has its own configuration and scope, manages its own pending work, and can be monitored and controlled independently. You can create as many parallel scans as you like, pause and resume them individually, and set priorities for use of resources. If you like to work by selecting individual items and sending them for scanning, you can choose which applicable task to send each item to.

There are many obvious use cases for the new capability:

You can create separate scans for different areas of an application, and separately monitor the progress and results of each.

You can create a high priority task to audit items that you manually select as being interesting, and a lower priority task working through a larger backlog of work.

You can create scans that are optimized for different purposes. For example, a quick scan for low-hanging fruit; a slow thorough and exhaustive scan; or a scan for a specific vulnerability like file path traversal.

Here is one view in the new UI showing the details of two parallel scans in progress:

Over the next few days, we'll describing some more upcoming features related to the new support for multiple parallel scans.

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
