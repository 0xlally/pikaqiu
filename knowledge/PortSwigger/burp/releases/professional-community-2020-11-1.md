# Professional / Community 2020.11.1

Source: https://portswigger.net/burp/releases/professional-community-2020-11-1
Fetched: 2026-06-28T09:16:33.185106+00:00

This release adds the Burp Suite Navigation Recorder extension to Burp's embedded browser and fixes a minor bug in the startup process.

Burp Suite Navigation Recorder preinstalled in the embedded browser

The Burp Suite Navigation Recorder extension is now preinstalled and ready to use in Burp’s embedded browser. This means you can immediately start recording login sequences for Burp Scanner without having to perform any manual setup.

Embedded browser upgrade

Burp's embedded browser has been upgraded to Chromium version 86.0.4240.198

Bug fixes

This release also provides the following bug fixes:

Highlighting a null character no longer causes extra characters to be included in the selection by mistake.

After a failed startup, relaunching Burp and selecting an existing project no longer causes the startup to fail again.

When the mouseover decoding popup is visible in Repeater, pressing the Ctrl + Space shortcut to send the request no longer causes Burp to crash.

When entering a number range for payloads in Intruder, accidentally leaving a trailing space no longer causes the request and payload count to be set to zero.
