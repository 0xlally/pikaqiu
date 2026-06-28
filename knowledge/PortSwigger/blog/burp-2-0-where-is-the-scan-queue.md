# Burp 2.0: Where is the scan queue?

Source: https://portswigger.net/blog/burp-2-0-where-is-the-scan-queue
Fetched: 2026-06-28T09:15:08.309164+00:00

Burp 2.0: Where is the scan queue?

Liam Tai-Hogan |

Tuesday, 2 October 2018 at 14:00 UTC

Burp 1.x had a fairly prominent view of the active scan queue, which you could monitor to see how your scanning was progressing. Where has this gone?

Burp 1.x

Previously, the top-level Scanner tab let you view progress, in the Scan queue tab:

Burp 2.0

In Burp 2.0, each individual task maintains its own queue of work. The Dashboard shows a summary of the progress of each task. If you need more information, click on "More details" for the applicable task:

Clicking "More details" opens the task details window for that task, showing various information. For tasks that involve auditing, click on the audit items tab to see the queue of work and Burp's progress through it:

You can also view other information about the task, including its event log, which shows alerts or other information that may be useful to troubleshoot network connection or other problems:

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
