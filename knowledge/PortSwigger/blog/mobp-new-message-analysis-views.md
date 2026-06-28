# [MoBP] New message analysis views

Source: https://portswigger.net/blog/mobp-new-message-analysis-views
Fetched: 2026-06-28T09:15:20.410031+00:00

[MoBP] New message analysis views

Dafydd Stuttard |

Saturday, 15 November 2008 at 07:06 UTC

MoBP

burp

Here's another small new feature, before moving back to some more weighty stuff.

Anywhere in Burp where you can view web requests and responses, you have a number of tabs showing different views and analysis of the message (plain text, hex, headers, etc). These tabs now appear and disappear based on the content of the message being displayed, and whether it supports the relevant view. There are also some new tabs for analysing messages, including colourised display of HTML and XML content. This view makes it much easier to visually scan a piece of HTML to see what it contains:

If you are editing an HTML response within the Proxy, you can also use the auto-colourising feature to sense-check that you have preserved the syntactic validity of the content, before sending it on to the browser.

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
