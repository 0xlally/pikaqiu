# Professional / Community 2023.2.3

Source: https://portswigger.net/burp/releases/professional-community-2023-2-3
Fetched: 2026-06-28T09:16:42.306102+00:00

This release provides improved support for WebSocket functionality in the Montoya API, as well as a number of minor improvements and bug fixes.

Montoya API WebSocket support

We have improved Montoya API support for WebSockets. This enables you to create extensions that interact more effectively with WebSockets. You can now:

Create WebSockets.

Create WebSocket message editors.

Retrieve WebSocket messages from the Proxy history. This enables you to search the messages for interesting content.

Send binary messages on both proxied and non-proxied WebSockets. This enables you to interact with services that process binary messages.

Add comments and highlights to proxied WebSocket messages.

Minor improvements

We have made a number of minor improvements, including:

We have added an entry for the Support HTTP/2 setting to the proxy listeners table.

We have updated the proxy listener to automatically restart when the Support HTTP/2 setting is changed.

When you reopen the Settings dialog your previous search is now displayed, so that you can quickly be in context.

Bug fixes

We have fixed a number of minor bugs:

Checkboxes now scale correctly when you modify the font size.

We have fixed a bug whereby if you generated a tab with a Burp extension, the tab did not display correctly.

We have fixed a bug whereby responses were erroneously marked as edited when using extensions in Montoya-compatible builds of Burp.

We have fixed a bug whereby the Hackvertor tab was not displaying correctly in the message editor when using the Hackvertor BApp.

We have fixed a bug whereby Intruder attack results windows sometimes displayed requests and responses from multiple Intruder attacks that were launched from the same tab. Each window now only displays requests and responses relating to the originating attack.

Browser update

This release upgrades Burp's browser to Chromium 111.0.5563.64/65. This upgrade contains a critical security fix, as well as several high-severity fixes.

Note for Windows Server 2012 and Windows 7/8/8.1 users

Due to a recent Chrome upgrade, Burp Scanner is no longer compatible with the Windows Server 2012 and Windows 7/8/8.1 operating systems. For more information, see the related Chrome announcement.
