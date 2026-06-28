# Professional / Community 2024.3.1.3

Source: https://portswigger.net/burp/releases/professional-community-2024-3-1-3
Fetched: 2026-06-28T09:16:46.898240+00:00

This release introduces custom Bambda columns, global Collaborator settings, and streamlined headers. We've also made other improvements and bug fixes.

Custom table columns with Bambdas

We have introduced a feature that enables you to add custom columns to the HTTP history, WebSockets history, and Logger tables using Bambdas. With these custom columns, you can display additional details about the items in your tables for a more tailored analysis based on your specific focus.

Please note that this feature is available in Burp Suite Professional only.

Burp Collaborator server settings override

We've added the Burp Collaborator server as user settings. This means that instead of configuring the Collaborator server for each project individually, you can now set it once and have it apply across all Burp installations on your machine. If you need to customize the Collaborator server for a specific project, you can still do so by turning on the Override options for this project only toggle.

Hide uninteresting headers in Pretty tab

The Pretty tab of the message editor now has an option to hide headers such as Sec-Ch-Ua, Accept-Language, and Upgrade-Insecure-Requests, helping to declutter the view and focus on more relevant information.

Other improvements

We've upgraded the Bambda Java version to 21.

Scanner's crawl paths view now includes the Rendered DOM, offering a clearer insight into the final page structure after dynamic changes.

You can now identify endpoints that Burp won't scan due to unsupported features in your API specification, helping to clarify the scope of API scans and reduce confusion about missing endpoints.

Bug fixes

Fixed an issue where changes to Burp Collaborator project settings weren't retained in the project file.

Fixed an issue where hiding uninteresting headers caused display issues when highlighting message text.

Fixed an issue preventing tabs created by extensions from appearing in Burp Suite search results.

Fixed an issue causing Target > Site map to not always update to show the correct request/response.

Fixed an issue with slow load times in the Crawl paths view, resulting in significantly reduced wait times.

Fixed a performance issue in Burp Scanner, enabling more efficient processing of large responses.

Browser upgrade

We've upgraded Burp's built-in browser to 124.0.6367.60

for Linux & Windows and 124.0.6367.61

for MacOS. For more information, see the Chromium release notes.
