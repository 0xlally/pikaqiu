# Enterprise Edition: performing scans

Source: https://portswigger.net/blog/enterprise-edition-performing-scans
Fetched: 2026-06-28T09:15:14.947707+00:00

Enterprise Edition: performing scans

Dafydd Stuttard |

Monday, 27 August 2018 at 16:10 UTC

MoBP

Burp Suite

Enterprise Edition

Burp Suite Enterprise Edition can scan multiple web sites in parallel. Scans can be performed on demand, or on a schedule, or using the REST API. Today, we're going to look at how you perform scans using the web interface.

After you've configured your web sites, you can easily set up scans of an individual site. You need to specify when to start the scan, whether the scan is one-off or recurring, any particular scan configurations to use:

Scan configurations can be used to control numerous details of how a scan is performed, such as the maximum link depth of the crawl, or what types of issues to report. The Enterprise Edition has the same set of built-in scan configurations as Burp Suite Professional has in its configuration library.

You can view in one place all of the scans that are scheduled, in progress, and completed:

The sites view also shows details of the last scan that was performed for each site:

You can click into an individual scan to see more details, including the reported issues:

You can click into an individual reported issue to see full details, including the severity and confidence, description, HTTP requests and responses, and any Burp Collaborator interactions:

MoBP

Burp Suite

Enterprise Edition

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
