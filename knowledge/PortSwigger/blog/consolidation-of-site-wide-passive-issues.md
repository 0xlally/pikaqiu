# Consolidation of site-wide passive issues

Source: https://portswigger.net/blog/consolidation-of-site-wide-passive-issues
Fetched: 2026-06-28T09:15:14.300334+00:00

Consolidation of site-wide passive issues

Dafydd Stuttard |

Friday, 10 August 2018 at 16:13 UTC

MoBP

Burp Suite

How many times have you seen Burp reporting hundreds or thousands of instances of the same passive issue on the same web site?

This happens because some passively-detected issues are liable to exist at many different locations within an application, and sometimes even in every single response.

This can arise for various reasons:

A chosen approach to development. For example, developers might not care about cross-site request forgery, so it is reported in numerous locations.

A page template includes a feature that Burp reports, such as a cross-domain script include or an undefined character set.

A platform configuration means every response has a feature that Burp reports, such as frameable responses or strict transport security not being enforced.

Previously, Burp scanned each item in isolation, and reported all of the issues found, leading to the problem illustrated above. This can cause noise in scan results, as well as consuming memory and disk space unnecessarily.

The new multi-phase scanning model handles this situation differently. In the first passive phase, Burp counts up issues and tracks the locations at which they are found. In the second phase, Burp consolidates these issues based on their frequency and location. Where applicable, this results in a single issue being reported at either the web root or a particular folder beneath which all of the instances are located.

So the results for the scan shown above now look like this:

As you can see, the 310 separate Clickjacking issues are now a single issue. The issue detail states that it was found at multiple locations under the reported path, and includes a sample of concrete requests and responses to illustrate the issue.

The new consolidation of frequently occurring passive issues is optional (on by default) so you can easily revert to the old behavior if you want an exhaustive audit of every instance of these kinds of issues.

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
