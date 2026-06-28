# Burp 2.0: Where are the Spider and Scanner?

Source: https://portswigger.net/blog/burp-2-0-where-are-the-spider-and-scanner
Fetched: 2026-06-28T09:15:08.026996+00:00

Burp 2.0: Where are the Spider and Scanner?

Liam Tai-Hogan |

Monday, 1 October 2018 at 14:00 UTC

This week, we'll be publishing a series of blog posts aimed at helping people move from Burp 1.x to Burp 2.0. We'll be looking at various Burp features that work in a different way in Burp 2.0, and help you to find and use the new versions of the features.

Firstly, the Spider and Scanner tools have disappeared from the main Burp window. Where have they gone?

Burp 1.x

Burp 1.x had top-level tabs for Spider and Intruder, and you could send selected items to these tools from the context menu:

Burp 2.0

Burp 2.0 has moved to a task-based model.

One way to initiate a scan is by clicking the "New scan" on the Dashboard tab. This opens a wizard that lets you configure the details of the scan:

Each scan has its own configuration settings. For example, for crawling tasks you can configure crawl optimization, crawl limits, options for login functions and error handling:

Configurations can be saved to the new configuration library.

With the new task-based model, you can configure multiple parallel scans, each with their own settings, and independently monitor and control each task. This gives you much more power and flexibility which wasn't possible with the previous singleton top-level tools.

Liam Tai-Hogan

@MetalF0X

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
