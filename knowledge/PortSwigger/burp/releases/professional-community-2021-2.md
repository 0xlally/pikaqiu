# Professional / Community 2021.2

Source: https://portswigger.net/burp/releases/professional-community-2021-2
Fetched: 2026-06-28T09:16:34.550593+00:00

This release provides improvements to the message inspector, non-printing character display, platform authentication controls and the embedded browser. It also provides a new vulnerability definition and several bug fixes.

New vulnerability definition: vulnerable JavaScript dependencies

Burp Scanner will now detect when a target application imports a JavaScript dependency that has a known vulnerability, such as when a library is dangerously out of date or has other issues.

Non-printing characters improvement

When viewing non-printing characters in the text editor, characters with a hexadecimal code point below 20 are displayed as "lozenges" with their hex code. Now, characters with a code point from 7F to FF are also displayed in the same way.

Per-host controls for platform authentication

Platform authentication (under "User options" and the "Connections" tab) can now be turned on or off on a per-host basis.

Message inspector improvements

There have been significant performance improvements in the message inspector. Also, users can now resize the message inspector horizontally and select multiple entries at once.

Embedded browser improvements

HTTP requests initiated by the embedded Chromium browser itself, rather than the user, are no longer sent. Also, Burp's embedded browser has been upgraded to Chromium 88.0.4324.150.

Bug fixes and minor improvements

This release also provides the following bug fixes and minor improvements:

The HTTP history message filter no longer incorrectly opens a new window when in fullscreen mode on macOS.

Streaming responses now show correctly in Burp Repeater.

Regex-based session validation no longer fails after opening an existing project file.

Activating a .burp file now opens Burp and loads the file rather than starting the Burp start-up wizard.

The "Delete bytes" context menu option has been restored to Burp Decoder.

The message editor now correctly highlights text in double quotation marks.

The colour of the "Intercept is off" button now matches nearby buttons.

Marks in check boxes are now displaying correctly in Burp extensions.

Deselecting "URL-encode these characters" is now respected for Payload Processing rules and multiple payload sets when using Cluster bomb attacks in Burp Intruder.

Burp Suite now makes use of the maximum size of messages that can be sent to Chromium DevTools, which is 100MB. This means that larger page resources can be loaded.

Burp Suite's MIME-type analysis now matches Chromium's behavior. Where multiple Content-Type headers are present in a response, Burp chooses the last one. Where there are Content-Type headers and a <meta http-equiv="content-type"> tag, Burp chooses the Content-Type headers. This change affects MIME-type filters in the Proxy and Target tabs, and the Render tab in the response viewer.

The icon for vulnerabilities with a severity of False Positive has changed from blue to green.
