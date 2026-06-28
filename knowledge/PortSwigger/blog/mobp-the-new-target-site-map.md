# [MoBP] The new target site map

Source: https://portswigger.net/blog/mobp-the-new-target-site-map
Fetched: 2026-06-28T09:15:21.713460+00:00

[MoBP] The new target site map

Dafydd Stuttard |

Sunday, 2 November 2008 at 08:24 UTC

MoBP

burp

The first difference you will notice when you fire up Burp is the new "target" tab. This is where you can view all of the information which Burp has gathered about the application you are attacking. This includes all the resources which have been directly requested, and also items which have been inferred by analysing the responses to those requests. For example, if you open your browser and make a single request to the front page of BBC news, you will see the following in the target site map:

Items that your browser requested are shown in black; those which Burp has inferred are shown in grey. Clearly, from browsing to a single page, we can deduce a large amount of information about the target application.

The site map interface works pretty much like a graphical email client. A tree view of hosts and directories is shown on the left. Selecting one or more nodes in the tree view causes all of the items below these nodes to be shown in table form on the top right. This table includes the key detail about each item (URL, status code, page title, etc.) and allows the items to be sorted according to any column. Selecting an item in the table causes the request and response for that item to show in a preview pane on the bottom right. This preview pane contains all of the functions familiar from elsewhere in Burp - analysis of headers and parameters, text search, media rendering, etc.

As well as displaying all of the information gathered about your target, the site map enables you to control and initiate specific attacks against it, using the context menus that appear everywhere. For example, you can select a host or folder within the tree view, and perform actions on the entire branch of the tree, such as spidering or scanning:

Or you can select an individual file within the tree or table, and send the associated request to other tools, such as Intruder or Repeater. If the item has not yet been requested by your browser, Burp will construct a default request for the item, based on the URL and any cookies received from the target domain:

Much of this information and functionality is present somewhere within the current release of Burp. But having everything accessible together via a single prominent and powerful interface will hopefully make it easier to keep track of your target's attack surface, and initiate the right attacks against it.

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
