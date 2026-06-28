# DAST without disruption: Burp Suite DAST winter update 2025

Source: https://portswigger.net/blog/burp-suite-dast-winter-update-2025
Fetched: 2026-06-28T09:15:09.556234+00:00

DAST without disruption: Burp Suite DAST winter update 2025

Rob Samuels |

Thursday, 11 December 2025 at 13:09 UTC

AppSec teams are under constant pressure to secure fast-moving applications without slowing anything down. But scanning windows, fragile authentication, and sprawling API estates often get in the way of true automation.

The latest updates to Burp Suite DAST are designed to remove that friction. We’ve introduced a set of new features that make scanning more reliable, more flexible, and far easier to manage at scale, so you can keep improving security without disrupting your workflow.

Here’s a quick summary of what’s new:

1. Run scans on your terms

Scan freeze windows

Many teams need scans to respect deployment cycles, maintenance windows, and change freezes. Until now, that often meant manually pausing or cancelling scans.

Scan freeze windows automate all of this. Define the times when scans shouldn’t run, and Burp Suite DAST will pause scanning automatically. No babysitting, no lost progress, and far smoother automation overall.

Take a demo of scan freeze windows.

Improved performance for large portfolios

Managing large site inventories is now quicker and more consistent. Whether you’re structuring folders, scheduling scans, or reshaping your site tree, Burp Suite DAST handles large estates more smoothly than before.

Intuitive folder-based organisation for CI-driven scans

If you trigger scans through CI/CD, Burp Suite DAST will now place them into the right folders automatically. This keeps environments tidy and makes it much easier to track results across teams and pipelines.

2. Stronger, clearer authenticated scanning

Simplified recorded login management

Login flows change, and when they do, authenticated scans often break. Instead of re-recording everything from scratch, the new recorded login editor lets you update individual steps directly. You can adjust fields, selectors, and interactions in seconds, keeping scans accurate with far less effort.

Try the interactive demo here.

Authentication visibility

Diagnosing authentication issues shouldn’t rely on guesswork. Burp Suite DAST now shows you what’s happening behind the scenes in real time, including screenshots and responses when something fails. Troubleshooting becomes much simpler and faster.

XPath/CSS authentication checks

Modern single-page applications rely heavily on dynamic UI changes. Flexible XPath and CSS checks help DAST confirm whether a session is still authenticated, making scans more reliable across dynamic and JavaScript-heavy apps.

Authentication status checker

This gives you immediate visibility when a session drops. If authentication breaks mid-scan, you’ll know straight away, reducing blind spots and preventing wasted scanning time.

3. Scanning built for the age of APIs

Support for environment variables when scanning Postman Collections

You can now import Postman collections together with environment variables. This means faster, cleaner setup and more accurate reproduction of real-world API traffic.

Auto-validation of OpenAPI definitions

If an OpenAPI definition contains issues, a scan may fail before it even begins. Burp Suite DAST now highlights these problems upfront so you can fix them before running the scan, improving reliability and reducing manual rework.

More consistent accuracy across API scans

With better handling of authentication, environment variables, and definition structure, Burp Suite DAST delivers more stable results across modern API estates, especially at scale.

Experience DAST without disruption

These updates are all about making scanning smoother, more predictable, and better aligned with how enterprise engineering teams actually work.

Ready to see it in action?

Request a demo to find out how Burp Suite DAST can streamline your AppSec program.

Rob Samuels

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
