# Multi-phase scanning

Source: https://portswigger.net/blog/multi-phase-scanning
Fetched: 2026-06-28T09:15:21.454465+00:00

Multi-phase scanning

Dafydd Stuttard |

Wednesday, 8 August 2018 at 16:14 UTC

MoBP

Burp Suite

Burp's current Scanner maintains a queue of items that have been sent for auditing, and processes them in turn. Each item is processed in isolation, and its status moves from waiting, to in-progress, to done.

Burp's new Scanner uses a different model. There is still a collection of items that are to be audited. But Burp divides the work into multiple phases.

The audit phases are divided into three areas:

Passive phases

Active phases

JavaScript analysis phases

Within each area, there are multiple distinct phases: for example, there are five different phases of active work. Within each area, each phase is performed for all items, before moving on to the next phase.

Below is what the new UI for monitoring the progress of an audit scan looks like. This is now shown for all kinds of scan, even those that only employ passive detection techniques.

The new UI lets you clearly track the progress of individual items, as each phase transitions from not started, to in progress, to complete. Over the next few days, we'll be describing various exciting new capabilities that are made possible by the new multi-phase scanning model.

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
