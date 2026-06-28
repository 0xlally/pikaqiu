# Professional 1.5.13

Source: https://portswigger.net/burp/releases/professional-1-5-13
Fetched: 2026-06-28T09:16:25.382956+00:00

This release includes fixes for the following issues:

A bug where repeating an Intruder attack using null payloads may generate no attack requests.

A bug where the default save location for automatic updates to Burp may contain URL-encoded characters, resulting in an invalid file path.

An issue where the CSRF PoC generator output using the cross-domain XHR technique fails to work on current versions of the Chrome browser.

Burp's behavior in quitting immediately without warning on OS X when Command+Q is pressed.

Poor performance saving and restoring state in v1.5.12.
