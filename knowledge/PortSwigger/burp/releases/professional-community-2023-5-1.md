# Professional / Community 2023.5.1

Source: https://portswigger.net/burp/releases/professional-community-2023-5-1
Fetched: 2026-06-28T09:16:43.925210+00:00

This release provides some improvements to the Burp Suite Navigation Recorder extension and an upgrade for Burp's browser.

Recorded login improvements

We have made the following minor changes to the Burp Suite Navigation Recorder browser extension:

When the login sequence that you're recording uses a type of platform authentication that is not supported by the extension, such as an NTLM-based mechanism, we now warn you of this during the recording.

When recording a login sequence, you no longer need to use the browser's incognito mode. However, we strongly recommend using incognito mode whenever possible to avoid issues with stateful behavior. We implemented this change to support users who would otherwise be unable to use the extension at all due to restrictions imposed by their organization.

Browser upgrade

This release upgrades Burp's browser to Chromium 113.0.5672.126 for Mac and Linux and 113.0.5672.126/.127 for Windows. This contains a critical security patch. For more information, see the Chromium release notes.

Bug fix

We have fixed an issue with DOM Invader that prevented it from working properly with newer versions of Chromium.
