# Professional / Community 2022.12.4

Source: https://portswigger.net/burp/releases/professional-community-2022-12-4
Fetched: 2026-06-28T09:16:37.012772+00:00

This release introduces support for popup windows when recording logins and a new live crawl view for Burp Scanner. We have also added several new features to DOM Invader, including the ability to detect DOM clobbering vulnerabilities, and various minor improvements and bug fixes for Burp Suite. It also upgrades Burp's browser to a later version of Chromium.

Authenticated crawling of applications with popup-based login mechanisms

Burp Scanner can now replay recorded login sequences that open new windows or tabs. This enables you to run authenticated scans on websites with login mechanisms that require you to interact with popups, such as Microsoft and Amazon's SSO services.

Live crawl view for Burp Scanner

We have added a new Live crawl view tab to the Scan details dialog. This tab enables you to watch Burp Scanner render web pages in real time, helping you to diagnose unusual crawl activity or simply get a better understanding of Burp Scanner's behaviors when scanning a particular target.

Major improvements to Burp Scanner

This release significantly improves Burp Scanner's resilience and provides increased support for a wider range of applications, especially SPAs.

Most importantly, we've fundamentally changed the way Burp Scanner navigates using its built-in browser. As a result, you may now be able to successfully scan a number of sites that were previously incompatible with automated vulnerability scans. In particular, you should see much better results on sites that rely heavily on navigation initiated by client-side JavaScript.

We've also dramatically improved our browser process management, resulting in much lower memory usage during scans.

DOM Invader enhancements

This release adds a number of new features to DOM Invader, as well as some usability improvements.

Detect DOM clobbering vulnerabilities - DOM Invader can now scan for DOM clobbering vulnerabilities as you browse. This feature is disabled by default as it can potentially interfere with your other testing activities. You can enable it from the DOM Invader settings menu.

Detect injectable service workers - DOM Invader now attempts to inject the canary into service workers during registration and flags any controllable properties. You can then manually investigate whether the service worker uses these properties in an unsafe way.

Improved URL injection - We've removed the Inject URL button, which injected a test string into every URL parameter at once. In most cases, this wasn't very useful as it just prevented the site from working properly. Instead, you can now click Inject URL params to inject the canary into each URL parameter separately in individual windows. This is far more practical and yields significantly better results.

Restrict the parameters used for auto-injection - When using the Inject into all sources option, you can now define a custom list of parameters that DOM Invader uses to inject the canary. This makes this feature more useful as injecting all parameters at once typically just prevents the site from working at all.

We have also divided the main settings menu into collapsible categories to make it easier to use.

Rolling licenses

We have added support for rolling licenses in Burp Suite. If your Burp license key has expired but you have a new, valid license associated with your account, then Burp Suite automatically applies your new license key the next time it starts up.

Change to Java requirements

Burp Suite now requires Java 17 or later to run. This change should not impact you unless you launch Burp Suite from the command line, as the installer includes a bundled private Java Runtime Environment so that you don't need to worry about installing or updating Java.

Minor improvements

This release includes several minor improvements, including:

The Collaborator client now shows the source port in the interaction details panel. This can help you to gauge how vulnerable a particular server is to certain attacks.

In Repeater, you can now drag and drop a tab into a collapsed group. The dragged tab is added to the end of the group.

We have changed the way in which Intruder attack results are stored in order to minimize the impact on project file size.

Bug fixes

We have fixed the following bugs:

Previously, Burp was stripping out manually-modified Connection headers when using NTLM authentication. This has now been fixed.

We have fixed a request time discrepancy between Intruder and Logger, in which Intruder was incorrectly reporting that requests were sent to the server a few seconds before the request was actually sent.

We have fixed a bug whereby reports were not saving correctly on Windows machines. Burp was displaying a "Failed to open file" error at the point the report was saved.

We have fixed a bug whereby Burp's browser was unable to register service workers, causing issues with recorded login sequences and manual testing.

We have fixed a bug whereby if you attempted to cancel while loading a user configuration file, then Burp was displaying a "Configuration File" error.

Browser upgrade

This release upgrades Burp's browser to Chromium 108.0.5359.124/.125.
