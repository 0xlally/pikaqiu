# Professional / Community 2025.10

Source: https://portswigger.net/burp/releases/professional-community-2025-10
Fetched: 2026-06-28T09:16:50.409139+00:00

This release introduces smarter HTTP history filtering, a number of updates to the Montoya API, improvements to the site map UI, and the ability to bulk copy column data from a range of tables in Burp.

Updates for developing powerful extensions and scripts

We've made several updates to help you extend Burp with your own extensions and Bambda scripts.

We've added a setting to auto-reload extensions when their files change. This removes the need to reload them manually during development. For more information, see Reloading your extension.

We've also added the following new capabilities to the Montoya API:

You can now use the RankingUtils interface to analyze responses and rank them by how anomalous they are. This helps your extensions quickly identify unusual traffic patterns.

You can now access message IDs in the Proxy > HTTP history. This enables you to use scripts to filter requests and responses by ID. For more information on using scripts, see Filtering the HTTP history with scripts.

When adding a custom settings panel to your extension, you can now specify descriptions for individual fields within settings. This enables you to help users understand each option more clearly.

You can now use the CompressionUtils interface to both compress and decompress data using the inflate format.

Extensions can now reuse HTTP/1 connections.

Smarter HTTP history filtering to cut through the noise

We've made several improvements to help you focus on more meaningful traffic in the HTTP history.

We've updated the default filter to hide less relevant items like binary files and static assets, so you can concentrate on more interesting traffic. In addition, Burp now excludes more low-value MIME types by default.

You can also now toggle between the filtered and full HTTP history views without losing your current filter settings. This helps you quickly check for anything you've missed, then return to a focused workflow with one click.

A more readable site map

We've improved how requests are shown in the site map. All HTTP methods are now shown for each endpoint and are color-coded for ease of identification. This makes it easier to distinguish between different requests to the same URL, which is particularly useful when working with REST APIs.

You can also switch between split and tab views more easily, using a new toggle in the top-right corner.

Simpler data export from Burp tables

You can now copy column data from a range of Burp tables, straight to your clipboard. Simply right-click the column header, then select Copy column. This makes it easy to export interesting data in bulk for use in external analysis tools and reports.

Quality of life improvements

We've made the following quality of life improvements:

The selected text length now shows in both decimal and hex next to the text editor search bar. This is helpful for precision tasks like request smuggling.

We now check that you select the correct standalone JAR file when setting up your Python environment. This prevents setup mistakes that previously blocked Python extensions from loading.

Performance improvements

We've significantly improved performance when filtering table items by file extension.

Bug fixes

We fixed the following bugs:

An issue where column widths in the Proxy > HTTP history table weren't preserved when using custom columns.

An issue that let you save custom actions with syntax errors using a hotkey. These actions would later fail without warning.

Java update

We've updated Burp's Java version to Java 24.0.2.
