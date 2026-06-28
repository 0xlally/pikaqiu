# Professional / Community 2025.4.2

Source: https://portswigger.net/burp/releases/professional-community-2025-4-2
Fetched: 2026-06-28T09:16:52.332495+00:00

This release introduces a number of user interface improvements, including a new browser icon in the toolbar. It also includes a Montoya API update to enable direct import of Bambda scripts into the Bambda library.

User interface improvements

We've made the following improvements to Burp's user interface:

We've added a browser icon to the toolbar, making it easier to start browsing as soon as you open Burp.

We've removed the Search and Settings text labels from the toolbar, giving it a cleaner look.

We've moved the icon from within the Inspector panel to the bottom of the side panel.

We've removed the protocol from Site map entries and added different icons to represent HTTP and HTTPS.

Montoya API update for writing extensions

You can now import Bambda scripts directly into your Bambda library using the Montoya API. This makes it quicker and easier to access and reuse your custom scripts.

Paste domains directly as requests

You can now right-click and paste a plain domain, like ginandjuice.shop, using the Paste host / URL as request context menu option. Burp will automatically create a request to the root of the domain using HTTPS, so there's no need to type out the full URL.

Bug fixes

We fixed the following bugs:

Requests sent to audit from certain tools were included without any insertion points.

You were unable to save a copy of a temporary project after running an Intruder attack with a pre-configured word list.

Browser upgrade

We've upgraded Burp's browser to Chromium 136.0.7103.49 for Windows & Mac and 136.0.7103.59 for Linux. For more information, see the Chromium release notes.
