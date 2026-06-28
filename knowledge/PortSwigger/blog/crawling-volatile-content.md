# Crawling volatile content

Source: https://portswigger.net/blog/crawling-volatile-content
Fetched: 2026-06-28T09:15:14.632006+00:00

Crawling volatile content

Dafydd Stuttard |

Monday, 6 August 2018 at 16:23 UTC

MoBP

Burp Suite

Modern web applications frequently contain volatile content, where the "same" location or function will return responses that differ substantially on different occasions, not (necessarily) as the result of any action by the user. This behavior can result from factors such as feeds from social media channels or user comments, inline advertising, or genuinely randomized content (message of the day, A/B testing, etc.).

The simple approach of Burp's current Spider tool isn't much affected by volatile content. It fetches each request a single time, and processes whatever version of the response is received, looking for new links.

Burp's new crawler takes a radically different approach, making no assumptions about URL structure, only navigating around an application via the intended pathways, and identifying locations within the application based on their contents. This means that it is obliged to handle volatile content in a robust manner.

The new crawler uses various algorithms allowing it to identify many instances of volatile content, and correctly re-identify the same location on different visits. This allows the crawler to focus attention on the "core" elements within a set of application responses, which is likely to be the most important in terms of discovering the key navigational paths to interesting application content and functionality:

In some cases, visiting a given link on different occasions will return responses that just differ too much to be treated as the "same". In this situation, Burp's crawler will capture both versions of the response as two different locations, and will plot a non-deterministic edge in the graph. Provided the extent of non-determinism across the application is not too great, Burp can still crawl the associated content, and reliably find its way to content that is behind the non-deterministic link:

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
