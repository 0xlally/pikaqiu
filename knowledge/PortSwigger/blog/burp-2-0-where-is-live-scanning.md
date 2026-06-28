# Burp 2.0: Where is live scanning?

Source: https://portswigger.net/blog/burp-2-0-where-is-live-scanning
Fetched: 2026-06-28T09:15:07.852579+00:00

Burp 2.0: Where is live scanning?

Liam Tai-Hogan |

Thursday, 4 October 2018 at 14:00 UTC

Burp 1.x had some features tucked away within the Spider and Scanner tools that controlled the automated processing that Burp performed on traffic passing through the Proxy. Where have these features gone?

Burp 1.x

In Burp 1.x, the "live scanning" feature by default carried out a passive-only scan on all traffic through the Proxy:

Burp 2.0

Burp 2.0 introduces the concept of a "live task". You can create a live task using the "New live task" button on the Dashboard:

The new-style live tasks are more flexible and versatile. you can monitor traffic from multiple Burp tools, not just the Proxy. You can create multiple tasks with different configurations. And you have fine-grained control over the scope of what traffic gets monitored and what actions are performed.

By default, Burp 2.0 creates two live tasks. These automatically populate the site map with links that are observed in traffic through the Proxy, and automatically perform auditing using passive techniques.

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
