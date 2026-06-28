# Professional / Community 2021.10

Source: https://portswigger.net/burp/releases/professional-community-2021-10
Fetched: 2026-06-28T09:16:34.339469+00:00

This release provides several updates to DOM Invader, line wrapping in Burp's message editor, and some bug fixes.

DOM Invader improvements

We have made a number of minor improvements to DOM Invader:

The DOM Invader icon will now show the number of items DOM Invader has flagged.

If any interesting items are found by DOM Invader (e.g. an eval sink), then the DOM Invader icon badge will now turn red.

The number of items will now be shown in the DevTools panel.

There is now a DOM Invader tab in DevTools, which contains both the Messages and DOM views - these replace the Augmented DOM and Postmessage tabs from previous versions.

Performance has been improved - by ensuring that DOM Invader is only injecting messages which haven't previously been injected.

DOM Invader now has a refreshed UI.

Line wrapping in message editor

As requested by a number of users, we have added support for line wrapping in Burp's message editor. This makes it easier to work with messages that contain lengthy strings, such as authorization tokens.

Line wrapping is enabled by default in both the Pretty and Raw views, but you can toggle it on and off using the button above each message.

Security fix

We have updated Burp's browser to Chromium version 95.0.4638.69, which fixes a number of high severity bugs.

Other improvements

Base64url encoding is now supported in the Inspector.

Bug fixes

This release also contains several minor bug fixes.
