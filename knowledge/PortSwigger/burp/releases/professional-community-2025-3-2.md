# Professional / Community 2025.3.2

Source: https://portswigger.net/burp/releases/professional-community-2025-3-2
Fetched: 2026-06-28T09:16:52.219616+00:00

This release enhances the efficiency of Burp Scanner by configuring the audit phase of scans to run in parallel with the crawl phase. We've also added custom actions to Burp Repeater to data extraction and analysis, refreshed the BApp Store, and enhanced the Montoya API.

Crawl and audit now run in parallel during scans

Burp Scanner now begins auditing as soon as the first audit item is identified during the crawl. As additional items are discovered, Burp continuously reprioritizes the audit queue to ensure that the most valuable items are audited first.

This improves scan efficiency and enables earlier issue detection, especially in larger or more complex applications.

Click all pointer clickable elements

We've added a new custom crawling configuration setting that enables Burp Scanner to click all elements that are styled with a pointer cursor (for example, using cursor: pointer). This can help identify interactive elements that are not standard links or buttons.

Custom actions

We've added custom actions to Burp Repeater. These are tasks that you can apply to HTTP messages to extract and analyze data. They're powered by Bambdas, which are scripts that run directly from Burp Suite's interface.

You can use custom actions for a wide range of purposes, such as:

Analyze responses - Extract data, count elements, decode and encode message content, and check for specific content.

Retrieve additional data - Perform lookups, resolve hostnames, and fetch external data.

Resend requests - Modify headers, parameters, or body content and resend the request.

To get started with custom actions, try out our example scripts. To load these, click Add samples from the empty Custom actions side panel in Repeater.

Custom actions are only available in Burp Suite Professional.

To learn more about custom actions, see our documentation.

BApp Store UI refresh

We've refreshed the BApp Store user interface to make it easier to find, install, and manage extensions.

To help you find useful new extensions, you can now filter the BApp Store by the following categories:

Featured - Extensions that we recommend. These offer stand out functionality that we find particularly interesting.

Recently updated - Extensions that have been added or updated in the last three months.

PortSwigger created - Extensions developed by our team at PortSwigger.

We've also added options to customize the table view, so you can focus on the details that matter most.

To try it out, go to Extensions > BApp Store.

Montoya API updates for writing Bambdas and extensions

We've made the following updates to the Montoya API, improving support for writing extensions and Bambdas:

We've improved support for JSON handling. You can now add, delete, and update JSON parameters. Previously, these actions would fail silently or cause an exception.

You can now replicate the message editor's URL-encoding options, giving you more control over URL-encoding behavior.

Extensions can now register custom hotkeys for the HTTP message editor. This makes it easier to trigger extension actions directly from the editor. If a hotkey is already specified in Extensions > User interface > Hotkeys, the error console will log the conflict.

You can now retrieve Intruder payload positions using requestMarkers() in the Montoya API. This provides a way to access these positions in extensions, which were previously defined using the § payload marker. The § marker is now purely visual.

You can now set notes on Repeater tabs. This enables extensions to add notes via the context menu, or even from a custom action.

Keyboard navigation in Burp

You can now use the Tab key on your keyboard to navigate around most areas of Burp. This streamlines workflows for users who prefer keyboard navigation.

Browser upgrade

We've upgraded Burp's browser to Chromium 135.0.7049.85 for Windows & Mac and 135.0.7049.84 for Linux. For more information, see the Chromium release notes.

Bug fixes

We've fixed the following bugs:

We've fixed a bug with Intruder attacks that use the Numbers payload type. Previously, if you only set the From value, Intruder always sent 0 as the payload.

We've fixed a bug that prevented requests from appearing in the Organizer when sent from Logger.

We've fixed a bug that prevented extensions from retrieving notes in certain contexts.

We've fixed a bug that prevented extensions from setting notes on Repeater tabs.
