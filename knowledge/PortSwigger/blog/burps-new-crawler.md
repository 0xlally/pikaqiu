# Burp's new crawler

Source: https://portswigger.net/blog/burps-new-crawler
Fetched: 2026-06-28T09:15:13.468662+00:00

Burp's new crawler

Dafydd Stuttard |

Thursday, 2 August 2018 at 17:24 UTC

MoBP

Burp Suite

Burp's current Spider tool has a number of significant limitations that prevent it from working effectively with modern web sites. Its core model is based on outdated assumptions about how web sites work, which don't apply today.

The Spider tool maintains a queue of pending requests. It works through the queue issuing each request, looks in the responses for new links and forms, and adds the relevant requests to the queue. This approach worked pretty well for sites that have unique and stable URLs for each function, use simple cookie-based session handling, return deterministic content in each response, and contain no server-side state. But most applications today aren't like that. So we're replacing the Spider tool with something better.

Burp's new crawler uses a radically different model. It navigates around a target application in the same way as a user with a browser, by clicking links and submitting input. It constructs a map of the application's content and functionality in the form of a directed graph, representing the different locations in the application and the links between those locations:

The new crawler makes no assumptions about the URL structure used by the application. Locations are identified (and re-identified later) based on their contents, not the URL that was used to reach them. This enables the crawler to reliably handle modern applications that place ephemeral data such as CSRF tokens or cache-busters into URL paths. Even if the entire URL within each link changes on every occasion, the crawler still constructs an accurate map:

The approach also allows the new crawler to handle applications that use the same URL to reach different locations, based on the state of the application or the user's interaction with it:

The old Spider tracked its remaining work using a queue of pending requests. The new crawler has to track its remaining work in a different way. As the crawler navigates around and builds up coverage of the target application, it tracks the edges in the graph that have not been completed. These represent the links (or other navigational transitions) that have been observed within the application but not yet visited. But the crawler never "jumps" to a pending link and visits it out of context. Instead, it either navigates via links from its current location, or reverts to the start location and navigates from there. This replicates as closely as possible the actions of a normal user with a browser:

Crawling in a way that makes no assumptions about URL structure is highly effective in dealing with modern web applications, but can potentially lead to problems in seeing "too much" content. Modern web sites often contain a mass of superfluous navigational paths (via page footers, burger menus, etc.), meaning that everything is directly linked to everything else. The new crawler employs a variety of techniques to address this issue: it builds up fingerprints of links to already visited locations to avoid visiting them redundantly; it crawls in a breadth-first order that prioritizes discovery of new content; and it has configurable cut-offs that constrain the extent of the crawl. These measures also help to deal correctly with "infinite" applications, such as calendars.

In the next few days, we'll be describing various other powerful capabilities of the new crawler that are built on this foundation.

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
