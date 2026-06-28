# Goodbye state files, we won't miss you

Source: https://portswigger.net/blog/goodbye-state-files-we-wont-miss-you
Fetched: 2026-06-28T09:15:15.731924+00:00

Goodbye state files, we won't miss you

Dafydd Stuttard |

Tuesday, 21 August 2018 at 15:41 UTC

MoBP

Burp Suite

It's over two years since we introduced Burp project files as the long-term replacement for state files.

Project files are vastly superior to the old state files:

Data is saved automatically, incrementally in real time. There is no need to specifically save your work when you are finished. If Burp exits abnormally, all its data is preserved.

Burp reopens project files considerably faster than state files.

Various areas of data that were never included in state files (such as the Scanner's issue activity log) are included in project files.

Since project files were introduced, we've made numerous enhancements to the feature:

You can import another project file, to merge two projects together.

You can save a backup copy of your project file, either manually or automatically on a schedule.

If the OS filesystem becomes damaged, Burp can repair any recoverable data from corrupted project files very effectively.

Until now, we've preserved the ability to save state files, to support people who were slow to make the transition.

That will soon change, and you will no longer be able to save new state files. So if you haven't started using project files, now is definitely the time to do so.

You'll still be able to load old state files for the foreseeable future, so you'll have no problems reopening old work that was saved in that format.

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
