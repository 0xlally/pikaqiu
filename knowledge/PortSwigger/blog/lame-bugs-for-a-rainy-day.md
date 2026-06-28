# Lame bugs for a rainy day

Source: https://portswigger.net/blog/lame-bugs-for-a-rainy-day
Fetched: 2026-06-28T09:15:19.040677+00:00

Lame bugs for a rainy day

Dafydd Stuttard |

Monday, 2 July 2007 at 19:00 UTC

Pen Testing

Most web applications contain enough serious security defects to produce an impressive pen test report, demonstrate a job well done, and (implicitly) justify your fee. In this situation, it is easy to overlook, or fail to report, a wide range of less exciting vulnerabilities that do not provide a direct means of compromising the application.

Just occasionally, you encounter an application which is so nailed down that you can find little bad to say about it. I think I even remember one app that didn't have any XSS, but I may be wrong. Even here, there are usually a bunch of "lame" issues you can identify, to at least demonstrate your attention to detail. Some common examples include:

names and email addresses appearing in HTML comments;

overly liberal cookie scope;

autocomplete enabled;

failure to timeout user sessions;

broken logout functions;

informative error messages;

sensitive information transmitted in the query string;

session fixation;

directory listings;

caching of sensitive data;

arbitrary redirection.

Why do we think these bugs are lame? Presumably, because you cannot normally exploit them to do anything seriously malicious against your target. But this thought overlooks the possibility of chaining multiple low-risk flaws together. Very often, vulnerabilities that present no threat in isolation can, in skilled hands, be leveraged to completely compromise an application. RSnake's entertaining Death By A Thousand Cuts provides a classic example of this. If we are doing our jobs properly, we should be reporting all of these issues any time they arise, regardless of whether it is raining.

Pen Testing

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
