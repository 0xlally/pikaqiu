# Professional / Community 2024.5.3

Source: https://portswigger.net/burp/releases/professional-community-2024-5-3
Fetched: 2026-06-28T09:16:47.253286+00:00

This release introduces Burp Scanner support for WebSockets, improvements for the recorded login editor, WebSocket match and replace rules, and a number of performance improvements. We also removed some redundant scan checks.

Burp Scanner support for WebSockets

We've updated the configuration of our internal proxy to allow WebSocket traffic. This enables Burp Scanner to now crawl sites that rely on WebSockets, including those with WebSocket-based recorded logins.

Please note that Burp Scanner does not scan the WebSocket traffic itself.

Recorded login UI editor

We've improved the editor for recorded logins. Previously, you needed to manually edit a JSON file to make changes to existing recorded logins. We have now added a See as events view in the Edit Recorded Login dialog, which displays the events in the sequence in a formatted table. From here, you can add, edit, or delete events in the sequence without manually changing the JSON file.

WebSocket match and replace rules

You can now configure match and replace rules to automatically replace parts of WebSocket messages as they pass through the Proxy. Previously, this functionality was only available for HTTP messages.

WebSocket match and replace rules may enable you to more easily bypass client-side security controls, such as HTML encoding on special characters like <, >, ", and '. Additionally, they enable you to more easily modify user permissions to gain access to hidden functionality.

Removed redundant scan checks for client-side SQL injection

Previously, Burp Scanner tested for several variants of client-side SQL injection. This is a potential vulnerability in websites that use the WebSQL Database API to create and manage databases that run in the user's browser.

WebSQL was never widely adopted and major browsers no longer support it. We've removed these scan checks as we now consider them redundant.

Quality of life improvements

We've made the following quality of life improvements:

You can now configure multiple platform authentication credentials for each destination host. Do this in the Settings dialog, under Connections > Platform authentication. This update enables you to quickly enable and disable platform authentication for different users, to more easily test access controls, for example.

We've increased the accuracy of Burp's single-packet attack. This makes it more effective at discovering race condition vulnerabilities with small race windows.

Performance improvements

We've made the following performance improvements:

We've reduced memory use, particularly for users who run a large number of extensions. Extension tabs are now only loaded when their corresponding tool tab is selected, for example when the corresponding Repeater or Proxy history tab is selected. Once loaded, the extension tabs retain their state when you switch back and forth.

We've reduced user interface lag by making the following changes:

We've fixed an issue that caused Burp to freeze when users with a large project file sorted a table column.

We've reduced the time taken to switch tabs from the Proxy history when lots of history items are selected.

We've significantly sped up access to notes, particularly when sorting by the Notes column in a large table.

Bug fixes

We have fixed the following bugs:

Hotkey highlight settings weren't automatically updating to match the previous highlight color.

The BChecks validator was failing to detect an issue with certain regex strings, resulting in incorrect validation passes.

The trailing # character was causing BCheck validation to fail incorrectly.

The crawler was failing to recognize fields called userId as valid username fields.

Browser upgrade

We have upgraded Burp's browser to Chromium 126.0.6478.57 for Windows & Mac and 126.0.6478.55 for Linux. For more information, see the Chromium release notes.
