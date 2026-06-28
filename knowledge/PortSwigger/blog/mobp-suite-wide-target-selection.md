# [MoBP] Suite-wide target selection

Source: https://portswigger.net/blog/mobp-suite-wide-target-selection
Fetched: 2026-06-28T09:15:21.068755+00:00

[MoBP] Suite-wide target selection

Dafydd Stuttard |

Tuesday, 4 November 2008 at 07:34 UTC

MoBP

burp

Burp can do lots of things to make your life easier when you are attacking a web application. Often, you want Burp to just go ahead and do these without being prompted. But, if you value your freedom, you don't want Burp going after just any target. Rather, you want Burp to know what is in scope for your attacks and what isn't.

In the new version, you can define at the Suite level what your targets are for your current activity. You can specify hosts, IP ranges, URL regexes, etc., as being in scope or out of scope. Currently, the UI looks like this, but I will hopefully make this a bit more sophisticated if time permits:

The target scope which you define here can affect the behaviour of the individual Burp tools in numerous ways. You can set display filters to show only in-scope items. You can tell the Proxy to intercept only in-scope requests. The Spider will only follow links that are in scope. You can automatically initiate vulnerability scans of in-scope items. You can configure Intruder and Repeater to follow redirects to any in-scope targets. And so on.

In all these cases, you can fine tune the target scope and the associated behaviour at the level of individual tools, or you can let them go after whatever is within the suite-wide scope. This provides a quick and easy way to tell Burp what is fair game and what is off limits, whilst also enabling the usual fine-grained control over everything that Burp does, if you need it.

MoBP

burp

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
