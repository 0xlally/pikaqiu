# Professional / Community 2020.5

Source: https://portswigger.net/burp/releases/professional-community-2020-5
Fetched: 2026-06-28T09:16:33.684784+00:00

This release provides a useful new feature for the HTTP message editor, as well as several general improvements.

HTTP message editor

You can now choose to display non-printing characters as "lozenges" in the HTTP message editor. This is supported for any bytes with a hexadecimal value lower than 20, which includes tabs, line feeds, carriage returns, and null bytes.

This feature will be greatly beneficial for many use cases, including:

Spotting subtle differences between byte values in responses

Experimenting with HTTP request smuggling vulnerabilities

Studying line endings to identify potential HTTP header injection vulnerabilities

Observing how null-byte injections are handled by the server

Non-printing characters are hidden by default, but you can toggle the lozenges on and off by clicking the "\n" button at the bottom of the editor.

These non-printing characters can currently only be displayed in the message editor. For now, you have to edit bytes using Burp's hex view. However, we plan to enable you to do this directly in the message editor in the near future.

General improvements

This release also provides the following minor improvements to various areas of Burp:

The embedded Chromium browser for the experimental browser-driven scanning mode has been upgraded to version 83.

Java 14 is now supported for both Professional and Community Edition.

Burp Proxy no longer intercepts requests for SVG or font files by default.

Crawling of static content is now faster.

Bug fixes

We have also implemented several minor bug fixes, most notably:

The response received/completed times are now displayed for 401 responses.

The response time is now displayed even when the time taken was < 1ms.

"Check session is valid" session handling rules are now applied properly when session tracing is running

The content discovery tool no longer erroneously displays the "Session is not running" message.
