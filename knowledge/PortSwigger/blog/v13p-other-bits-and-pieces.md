# [V13P] Other bits and pieces

Source: https://portswigger.net/blog/v13p-other-bits-and-pieces
Fetched: 2026-06-28T09:15:27.555949+00:00

[V13P] Other bits and pieces

Dafydd Stuttard |

Sunday, 29 November 2009 at 09:06 UTC

V13P

I've described most of the major additions to Burp's functionality that are arriving in v1.3. There are a few other smaller tweaks that are worth drawing attention to:

The tables in the site map and search results now include a timestamp column. Sorting the results on this column lets you easily see when new items are added. This is handy when you are running spidering or content discovery exercises, or when performing dynamic searches, all of which add new entries to these tables periodically.

The background autosave feature now optionally performs a final autosave on exit, so that you will always have a current snapshot of your work provided Burp closes down gracefully.

Repeater now shows a response timer in milliseconds, which can help you verify time-delay-based tests for code injection bugs.

Scope rules can be individually toggled on and off, so you can easily switch between different targets which you have configured.

Scanner and Spider now support request throttling with optional random variations, to help you avoid overwhelming flimsy applications, and avoid alerting pattern-based intrusion detection systems.

Apologies to the many people whose requests haven't been met on this occasion - there will be further development efforts fairly early in 2010.

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
