# Burp 2.0: How do I scan individual items?

Source: https://portswigger.net/blog/burp-2-0-how-do-i-scan-individual-items
Fetched: 2026-06-28T09:15:08.067538+00:00

Burp 2.0: How do I scan individual items?

Liam Tai-Hogan |

Wednesday, 3 October 2018 at 14:00 UTC

When manually testing an application you often want to perform a scan of a single item of interest or a small range of requests. Burp 2 gives you more powerful ways of doing this.

Burp 1.x

In Burp 1.x, there is a single queue of pending scanning work. You can send individual selected items to this queue via the context menu:

Burp 2.0

In Burp, you can send selected items for scanning in exactly the same way, by choosing "Scan" from the context menu:

The new scan wizard gives you various options. To scan the specific items you selected, leave the scan type selection as "Audit selected items". You can configure anything else you want about the scan, including its configuration, using the wizard:

Once started, the scan appears in Burp's Dashboard, where you can monitor and control its progress.

What makes Burp 2.0 so much more powerful is what happens the next time you select items to be scanned. Burp lets you send those items straight to the task that you already created, or open the scan launcher to create a new task for the selected items:

This new flexibility can considerably improve the efficiency of your testing workflow. You can create multiple parallel scans with different configurations that are optimized for different purposes. For example, you might perform a default scan on all items that look interesting, a very quick scan for just XSS on requests where you see input reflected, or a thorough scan for file path traversal vulnerabilities on any requests relating to file handling.

Liam Tai-Hogan

@MetalF0X

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
