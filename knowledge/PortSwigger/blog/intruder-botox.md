# Intruder botox

Source: https://portswigger.net/blog/intruder-botox
Fetched: 2026-06-28T09:15:18.676284+00:00

Intruder botox

Dafydd Stuttard |

Monday, 22 March 2010 at 15:33 UTC

burp intruder

I'll shortly be releasing to Burp Suite Pro users a new beta version of Burp Intruder, which contains a bunch of frequently-requested enhancements:

You can now configure multiple attacks indepedently in separate tabs (as with Burp Repeater). You can copy attack configurations between tabs, or save configurations for later use.

Payload positioning now uses the same feature-rich editor as other tools, and fully preserves binary/non-printing characters.

There are several new payload sources, including a bit flipper, character frobber and username generator.

The existing simple payload processing options (for encoding, etc.) are replaced with a rules-based processor which can perform arbitrarily many actions, such as match/replace, prefix/suffix, substring, case modification, encoding, decoding and hashing.

All feasible attack configuration options can now be modified during a live attack, and have immediate effect, including the base request template, payloads, grep settings and thread count.

Each attack optionally performs an unmodified baseline request, to enable easy comparison with the results of actual attack requests.

The attack results table contains the same rich functionality as the Proxy history, with a configurable filter, annotation of items with comments and highlights, and a preview pane for quick viewing of requests and responses.

Selected result items can be flagged to be re-requested (e.g. if network errors or timeouts have occurred).

When an attack is configured to follow redirects, all intermediate responses and requests are recorded in the results viewer.

Following the enhancements made to other tools in recent releases, Burp Intruder was starting to look a bit left behind. This upgrade brings Intruder up to the same level of functionality as the rest of the suite, and you will hopefully find it more powerful and easier to use than previously. There are a lot of requested features which didn't make the cut on this occasion, and these will hopefully make an appearance later this year.

The new release should be available later this week.

burp intruder

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
