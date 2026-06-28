# Professional / Community 2020.9

Source: https://portswigger.net/burp/releases/professional-community-2020-9
Fetched: 2026-06-28T09:16:34.000397+00:00

This release provides some improvements to the HTTP message editor UI.

HTTP message editor toolbar

On the "Raw" tab, the various options you have for analyzing the HTTP message are now contained in a toolbar at the top of each request or response. From the toolbar, you can now:

Alternate between the prettified, raw, or rendered HTML views where available

Toggle whether non-printing characters are displayed as "lozenges" within the message

Access a range of context-specific actions for the message from the new "Actions" menu

HTTP message editor layout options

In the upper-right corner of the message editor, you can now choose from three different layouts that determine how the request and response are arranged in the panel.

You can choose from the following options:

Horizontal layout: The request and response are arranged side-by-side.

Vertical layout: The request and response are stacked one on top of the other.

Combined view: Either the request or response will fill the message editor panel. You can alternate between the two using the corresponding tabs.

These new layout options are available in various locations throughout Burp Suite, including the Target site map and Proxy history.

Other improvements

The embedded browser has been upgraded to Chromium 85.0.4183.83.
