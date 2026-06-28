# Enterprise Edition: configuring web sites

Source: https://portswigger.net/blog/enterprise-edition-configuring-web-sites
Fetched: 2026-06-28T09:15:14.378688+00:00

Enterprise Edition: configuring web sites

Dafydd Stuttard |

Sunday, 26 August 2018 at 15:57 UTC

MoBP

Burp Suite

Enterprise Edition

Burp Suite Enterprise Edition will let you configure details of all your organization's web sites, so that they are available for scheduled scanning.

Sites can be organized into a tree structure using folders. You can use this to reflect the structure of your organization or infrastructure. You can also restrict user access to only parts of the sites tree, based on this structure:

Each site must be configured with the URL(s) at which it is accessed. You can also configure any sub-URLs which should be excluded, any application login credentials that should be used when scanning the site, and any default scan configurations that should be used:

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
