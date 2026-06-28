# [MoBP] Saving and restoring state

Source: https://portswigger.net/blog/mobp-saving-and-restoring-state
Fetched: 2026-06-28T09:15:20.915414+00:00

[MoBP] Saving and restoring state

Dafydd Stuttard |

Saturday, 29 November 2008 at 09:28 UTC

MoBP

burp

Here is a feature that has been frequently requested, and which, like Burp Scanner, will be restricted to the professional edition of Burp.

The new version of Burp lets you save the state and configuration of the key tools, and restore this on another occasion. This facility is of huge benefit to penetration testers, enabling you to seamlessly resume yesterday's work, perform backups of key information throughout a job, and take a complete archive of the information accumulated at the end of an engagement. You can also create as many customised configurations of suite tools as you want, and save each configuration separately for reuse on future occasions.

The items that can be saved include:

The target site map, which includes all of the content discovered via the proxy and spider.

The proxy history.

The issues identified by the scanner.

The contents and histories of the repeater tabs.

The configuration of all suite tools.

The save and restore process is fully configurable, and really easy. First off, you select "save state" from the Burp menu:

This launches a wizard which lets you choose which items you want to save the state and configuration of:

You then choose your output file, and Burp does the rest:

To restore previously saved state and configuration, you select "restore state" from the Burp menu. Each save file can include the state and configuration for any combinations of tools, and Burp lets you choose which tools you want to restore, and how to do it (whether to add to or replace their existing state):

Again, Burp goes to work and restores everything you have selected:

In our testing, this new feature is working beautifully. Obviously, the files can grow pretty large, because they include the full requests and responses accumulated within the tools you are saving. A few hours' testing will typically save or restore in a minute or two. You can make this process leaner and quicker by deleting unneeded items from the site map and proxy history before performing a save.

I hope that everyone who has this feature will get into the habit of using it. Picking up exactly where you left off the night before is a time saver. Being able to re-open your work from a completed job, to answer a client question or re-test a fixed issue, is a real benefit. If your colleague has fully enumerated an application's content, they can save this out for you to add to the current state of your instance of Burp to save you duplicating the effort. If you have worked on a problem for a while and got stuck, you can pass your entire work to someone else to think about. And team leaders can optimise Burp's configuration for a particular engagement, including fine-grained target scope definition, and pass this configuration straight to other team members to begin testing. You can create configuration templates designed for different kinds of task, and switch between these easily. There are probably plenty of other applications of this new functionality - let me know if you think of any.

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
