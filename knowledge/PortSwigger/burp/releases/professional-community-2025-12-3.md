# Professional / Community 2025.12.3

Source: https://portswigger.net/burp/releases/professional-community-2025-12-3
Fetched: 2026-06-28T09:16:51.294069+00:00

This release adds collections for secure sharing, OAuth2 support for API scanning, smarter SQLi detection, Comparer enhancements, as well as other improvements, bug fixes, and a browser update.

Share messages securely using collections

We've introduced collections to Burp Suite Professional, enabling you to share one or more HTTP messages with other Pro users via a single secure Burp link. This provides an easy, secure way to pass on findings, reproduction steps, or proof-of-concept requests without copy-pasting or exporting files.

Collections are created using Burp Organizer and support traffic from across your tools. The data is encrypted end-to-end and never visible to PortSwigger.

To create a collection, highlight messages in Organizer and use the Create collection link context menu item. To import a collection, open the link in your browser or paste it into the command palette.

OAuth2 support for API scanning

Burp now supports OAuth2 Client Credentials flow authentication for API scanning. If your OpenAPI definition or Postman Collection specifies this flow, Burp automatically detects it and fills in the details for you, helping you get your scan running more quickly with less manual setup. Burp then uses this information to obtain and refresh your access tokens during the scan, so you do not need to manage tokens manually.

You can also configure OAuth2 yourself by entering the token URL, client ID, client secret, and optional scope.

Burp can also detect other types of OAuth2, but does not currently support them.

Quick actions for URLs in the command palette

The command palette now recognizes when you enter a URL and offers quick actions for it. You can:

Instantly open the URL in Burp's browser.

Send the URL to Repeater.

Launch a scan.

Add or exclude it from your suite scope.

Use hotkeys and commands across bulk selections

Extension hotkeys now enable you to apply actions to multiple selected items at once. This makes it possible to trigger extensions or repeat actions across large sets of requests.

Comparer enhancements

We've made a number of enhancements to Comparer in this release:

We've added a setting to control whether panels in Comparer's result windows stay in sync by default. You can find it under Settings > Comparer > Comparer results sync view.

Comparer now soft-wraps long lines, making side-by-side comparisons easier to read. This helps you visually align changes without needing to scroll horizontally.

Burp now saves the state of Comparer's Sync views setting between sessions. This saves you from re-enabling it each time you restart.

We've added Previous and Next buttons to Comparer so you can quickly jump between changes.

Smarter time-based SQL injection detection

Burp Scanner now filters out false positives caused by web application firewalls (WAFs) delaying suspicious payloads. This improves accuracy in detecting genuine time-based SQL injection in these scenarios.

Quality of life improvements

The memory hover in Burp's footer bar now shows how many extensions are currently loaded, making it easier to spot whether the number of active extensions might be affecting performance.

You can now copy requests and responses in pretty-printed format from the message editor. This makes it easier to share or include them in reports.

Burp's CA certificate now includes the "Key Usage" X509v3

extension. This improves compatibility with tools using Python 3.13

and above.

Bug fixes

We've fixed a bug where using Ctrl+Click to copy a column in Intruder results would also sort the column.

We've fixed a bug where using Send to Organizer after running a custom action in Repeater would send the original response instead of the updated one.

We've fixed a bug where canceling a request with a Host header ending in a : caused UI issues in Repeater.

We've fixed a bug in Comparer that was stopping you from scrolling to the end of the first request text when the second request had additional data. You can now view the full content as expected.

Burp Scanner no longer tries to audit very large responses (such as MP4 files) that can't be meaningfully scanned.

Browser upgrade

We've upgraded Burp's browser to Chromium 143.0.7499.193 for Windows & Mac and 143.0.7499.192 for Linux. For more information, see the Chromium release notes.
