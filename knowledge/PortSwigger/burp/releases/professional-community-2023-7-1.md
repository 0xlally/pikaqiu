# Professional / Community 2023.7.1

Source: https://portswigger.net/burp/releases/professional-community-2023-7-1
Fetched: 2026-06-28T09:16:44.084101+00:00

This release introduces the ability to easily customize the layout of Burp Suite's top-level tabs. We've also made some other improvements and fixed a few bugs.

Customizing Burp's layout

You can now customize the layout of Burp's top-level tabs. This enables you to tweak Burp's user interface to better suit your preferences. For example, you can now:

Change the order of tabs.

Detach tabs. This enables you to open a tab, or groups of tabs, in a new window. You can open and arrange windows to suit your work style.

Hide tabs. This enables you to limit the number of tabs that you can view, to focus on particular tools and extensions that you use more frequently.

Burp remembers these preferences, so you won’t need to reorder your tabs every time you start Burp.

For more information on how you can customize Burp's layout, see our reference documentation.

Scanner improvements

We've made some improvements to Burp Scanner, including:

We have added a Status column to the Crawl Paths > Outlinks tab, giving more information on the actions that Burp Scanner took to discover each location in the crawl.

You can now replay recorded login sequences that contain shadow DOM elements.

Other improvements

We have some additional improvements, including:

We've added a setting that switches off the confirmation dialog that appears when you close Burp Suite. Find this in Settings > Suite > Burp's closing behavior.

We've configured Burp Intruder to populate number fields by default when you select a Numbers payload type.

We've standardized Burp Intruder's payload placeholders, making it simpler for you to configure payloads.

Bug fixes

We have fixed a number of minor bugs, including:

Content in extension-generated editor tabs now updates correctly.

Burp’s browser no longer erroneously sends HTTPS requests for HTTP URLs.

Burp Scanner no longer erroneously reports a Content Type Incorrectly Stated issue when scanning font files, or content types that Burp does not recognize.

Live passive audits now run any passive BChecks that have been marked as enabled.

Browser upgrade

We have upgraded Burp's built-in browser to Chromium 115.0.5790.102 for Windows, Linux and Mac.
