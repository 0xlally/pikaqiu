# Professional / Community 2025.9

Source: https://portswigger.net/burp/releases/professional-community-2025-9
Fetched: 2026-06-28T09:16:55.672782+00:00

This release introduces support for custom Java scan checks, a more streamlined scan configuration panel in the scan launcher, and several quality of life improvements.

Custom scan checks in Java

You can now write custom Burp Scanner checks in Java, with access to most Burp functionality through the Montoya API. This gives you the flexibility to implement advanced logic and fully tailor scans to your needs. For simpler cases, you can continue to use our lightweight BChecks language.

To help you get started, our researchers have published a set of Java scan checks in our Bambda scripts repository. You can also use the built-in templates as a starting point to create your own.

To get started, go to Extensions > Custom scan checks, then select New > Blank script. For more information, see Custom scan checks.

Improved scan configuration panel

We've redesigned the Scan configuration tab in the scan launcher. It's now a single, unified panel where you can configure your crawl settings, audit settings, and scan checks.

The new design gives you:

Direct access to scan checks - Quickly view all available checks, including built-in, custom, and extension-provided, and enable and disable them as needed.

Better visibility of settings - View all settings without switching between different views, giving you more visibility and control when fine-tuning your scans.

Customizable preset modes - Start quickly with our presets, then tweak them to suit your needs.

To try the new layout, click New scan from the dashboard.

Quality of life improvements

We've made the following quality of life improvements:

You can now send multiple messages at once from Burp Logger or Search to Repeater and Organizer. Simply select the items you want to send, right-click, and choose the appropriate option.

You can now export and reuse your resource pools across projects. This makes it easier to apply consistent task configurations when creating new projects. For more information, see Resource pools.

We’ve disabled the Browser cross-site scripting filter disabled built-in scan check by default. This keeps Burp Scanner aligned with modern browser behavior and avoids outdated findings.

Bug fixes

We've fixed the following bugs:

A bug where, when configuring logins in the scan launcher's Application login tab, the password box appeared too small, making it difficult to see what you were typing.

A bug where Burp sometimes used the wrong HTTP version after a DNS lookup returned a new IP address.

A bug where in the scan results Issues list, the up and down arrow keys sometimes stopped working.

A bug where only the last loaded extension could successfully drop proxy requests.

We've fixed a bug where leading spaces in Bambda script files caused formatting issues on export.

A bug where individual Repeater requests weren't able to be sent after being ungrouped.

We've fixed an issue where workspace layouts were sometimes not saved after closing Burp.

Browser upgrade

We've upgraded Burp's browser to Chromium 140.0.7339.81 (Win/Mac) and 140.0.7339.80 (Linux). For more information, see the Chromium release notes.
