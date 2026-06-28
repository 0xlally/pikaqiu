# Professional / Community 2024.2.1

Source: https://portswigger.net/burp/releases/professional-community-2024-2-1
Fetched: 2026-06-28T09:16:45.890039+00:00

This release introduces specific API scanning functionality, and incorporates Bambdas into the Logger capture filter. We've also improved the functionality of DOM Invader and the Burp Suite Navigation Recorder, and made a number of other improvements and bug fixes.

API scanning

We've introduced specific API scanning functionality. You can now upload an OpenAPI definition (v3.0.x) to seed an API scan. In particular, you can upload an API definition from a local file. This enables you to start an API scan without having to host your definition on a web server. You can also view and configure the API endpoints that will be scanned for more visibility and control over the scan. In the future, we plan to add even more functionality, including endpoint authentication handling. Watch this space!

To start an API scan, click New scan > API scan on the Dashboard. To learn more about how to run an API scan, see Scanning APIs.

Advanced filtering of Logger capture filter with Bambdas

We're introducing Bambdas into more areas of Burp Suite. These Java-based code snippets enable you to customize Burp directly from the UI.

This release introduces Bambdas into the Logger capture filter. This enables you to customize Logger to capture exactly what you need, helping you to focus your analysis by filtering out unnecessary traffic.

To learn more about Bambdas in Burp, see Bambdas.

New scan checks: CSP vulnerabilities

We’ve added new passive scan checks that identify Content Security Policy (CSP) vulnerabilities. Burp Scanner can now identify issues like unsafe script permissions, clickjacking, form hijacking, and incorrect CSP syntax.

Improvements to Burp Suite Navigation Recorder

We've fixed a number of minor bugs in the Burp Suite Navigation Recorder:

We've removed the instrumentation of shadow DOM elements that were causing errors for some websites.

We've fixed a bug whereby non-Incognito windows were being recorded when in Incognito mode.

We've introduced a more reliable URL retrieval method to fix a bug whereby the reported URL was sometimes incorrect.

We've fixed a bug whereby XPath generation was sometimes incorrectly generated, resulting in a replay failure in Burp.

Improvements to DOM Invader

We've made some improvements to DOM Invader:

We've added support for instrumentation of custom sinks. This may enable you to find vulnerabilities in client side JavaScript that don't map to a JavaScript sink.

We've fixed a bug that impacted POC generation.

Java version update

We've updated the minimum version of Java that Burp Suite supports from 17 to 21. If you're launching Burp from the command line, you'll need to use Java 21 or later.

This update also enables you to create extensions using Java 21 or lower.

Other improvements

We've also made the following improvements:

To give you more control over memory optimization, we’ve added a setting that enables you to set a maximum memory allowance for Burp's Java Virtual Machine.

We've enhanced the table sorting functionality, restoring your ability to sort by up to three columns. This update gives you more control over how you organize table data.

We've introduced a feature to Collaborator that displays the number of unread interactions on the tab label, enabling you to easily monitor interaction counts at a glance.

We've removed the Password field with autocomplete enabled scan check, addressing the issue's redundancy due to modern browsers' behavior.

To facilitate easier copying of Bambdas between filters, we've introduced non-modal filter dialogs. This enables you to open multiple filter dialogs simultaneously and keep them open while using Burp Suite.

Bug fixes

We've fixed a number of minor bugs in Burp Scanner, including:

We've improved the recorded login functionality for complex websites.

We've fixed a bug where Burp Scanner wouldn't start a new scan if a task was paused and deleted during the audit phase.

We've optimized the Source code disclosure scan check to prevent excessive memory allocation.

We've fixed a bug where Burp Scanner's browser request handling was failing under high request concurrency.

We have fixed an issue where some browser-related errors were causing scan failures.

Browser upgrade

We've upgraded Burp's built-in browser to 122.0.6261.57 for Mac and Linux and 122.0.6261.57/.58 for Windows. For more information, see the Chromium release notes.
