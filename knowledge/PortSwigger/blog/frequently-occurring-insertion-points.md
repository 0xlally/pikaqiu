# Frequently occurring insertion points

Source: https://portswigger.net/blog/frequently-occurring-insertion-points
Fetched: 2026-06-28T09:15:15.714934+00:00

Frequently occurring insertion points

Dafydd Stuttard |

Saturday, 11 August 2018 at 15:53 UTC

MoBP

Burp Suite

As we've already described, Burp's current Scanner audits each individual request in isolation, performing all of the configured checks, and reporting all of the resulting issues. This includes carrying out a full audit of all the configured insertion points.

This approach is perfectly fine when auditing a single request, but it can quickly become inefficient when auditing an entire application.

Some insertion points are liable to exist within many or all requests used by the application, but might not represent interesting attack surface. Examples of this include:

Cookies which, once set, are automatically submitted within every subsequent request.

Cachebuster parameters that are placed into URL query strings to prevent caching, but not processed in any way by the server-side application.

Performing a full audit of these insertion points in every request represents a considerable overhead of redundant effort.

In the new Scanner, Burp will by default identify frequently occurring insertion points that have proven to be uninteresting. If the same insertion point is observed many times in different requests, and if prior scans of that insertion point resulted in either no issues or the same set of issues every time, then Burp deems the insertion point to be uninteresting.

Insertion points flagged as uninteresting are still audited, but in a more lightweight manner. Burp first sends a small number of requests designed to flush out any anomalous behavior that indicates server-side processing. If this is confirmed, then Burp proceeds with a full normal audit of the insertion point. If not, then work that is most likely pointless is avoided.

This new behavior is configurable per individual insertion points type, so you can revert to carrying out a full audit of some or all insertion points if you prefer:

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
