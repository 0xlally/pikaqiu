# [V13P] Upstream proxy rules

Source: https://portswigger.net/blog/v13p-upstream-proxy-rules
Fetched: 2026-06-28T09:15:27.776882+00:00

[V13P] Upstream proxy rules

Dafydd Stuttard |

Saturday, 21 November 2009 at 11:55 UTC

V13P

If I had a beer for every time someone has requested this feature, I'd have been way too wasted to implement it.

Burp already supports upstream web proxies, but only as a global configuration which affects all outgoing traffic. In the new release, Burp allows you to configure rules specifying different proxy settings for different (ranges of) destination hosts.

The following configuration will make Burp talk directly to staging.intranet.corp.com, use an internal proxy server without authentication for everything else on *.intranet.corp.com, and use an authenticated gateway web proxy for everything else, including the public internet:

You can use standard wildcards in the destination host specification. Rules are applied in sequence, and the first rule which matches the web server you are communicating with will be used. If no rule is matched, Burp defaults to direct, non-proxy connections.

V13P

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
