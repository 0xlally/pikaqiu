# [MoBP] Search me

Source: https://portswigger.net/blog/mobp-search-me
Fetched: 2026-06-28T09:15:21.174507+00:00

[MoBP] Search me

Dafydd Stuttard |

Sunday, 9 November 2008 at 09:41 UTC

MoBP

burp

Several of the Burp tools accumulate a wealth of information about the applications you access. Digging through these different repositories to find specific items just got a whole lot easier, with the addition of a suite-wide search function. You can access this from the "burp" menu:

The search function is nice and simple. You just enter an expression, and tell Burp where to look - whether in request headers, response bodies, etc., in specific tools, or everywhere. The key details of each search match are shown in a sortable table, with a preview pane where you can see the full request and response, included highlighted matches for your search item. The usual context menus can be used to initiate attacks against specific items, or send them to other tools for further analysis.

One situation recently where I found the new search function to be useful was when looking for leakage of specific information from a target application. I was looking at an application which held users' credit card numbers, and these were supposed to be masked everywhere following the point of initial submission, to mitigate the impact of a user's account being compromised. Testing whether this was the case was a simple matter of stepping through all of the relevant functionality using my browser, with proxy interception turned off, and then using the search function to look for the credit card number I had earlier registered. Although the number was masked everywhere on-screen, using the search function identified a couple of obscure locations where the number was transmitted to the client within HTML source.

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
