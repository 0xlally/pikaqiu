# Burp integrates with WebInspect

Source: https://portswigger.net/blog/burp-integrates-with-webinspect
Fetched: 2026-06-28T09:15:08.477801+00:00

Burp integrates with WebInspect

Dafydd Stuttard |

Thursday, 9 October 2014 at 10:45 UTC

integrations

burp

We're very pleased to announce that Burp is now integrated with the WebInspect vulnerability scanner, thanks to a new extension created by the WebInspect team. People who make use of both Burp and WebInspect can use this integration to share findings between the two products, and make your testing workflows more efficient.

To use the integration, first install the WebInspect Connector extension from the BApp Store. Then, in the WebInspect tab, enter the API URL for your instance of WebInspect (for example: http://localhost:8083/webinspect), and click "Connect":

The UI will display the list of WebInspect scans:

To start working with a WebInspect scan, select it from the list and click "Attach to scan". A new tab will open showing the results of the scan:

You can send items from WebInspect to Burp by selecting one or multiple vulnerabilities in the WebInspect scan tab, and use the context menu to perform the following actions:

Send to Spider

Send to Intruder

Send to Repeater

Create issue - this will add the vulnerability to Burp Scanner's results

Issues created in Burp's results are tagged with "[WebInspect]":

You can send items from Burp to WebInspect as follows:

Select one or multiple issues in the Burp Scanner results.

Use the context menu option "Send to WebInspect".

Select an open WebInspect scan.

This will create the issue in WebInspect, and will also create a crawling session based on the selected base request. Issues created in WebInspect's results are tagged with "[Burp]":

We hope that people who use both Burp and WebInspect will find the integration helpful. We plan to announce further integrations between Burp and other leading web security products in the coming months.

integrations

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
