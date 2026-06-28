# Professional / Community 2023.12.1.3

Source: https://portswigger.net/burp/releases/professional-community-2023-12-1-3
Fetched: 2026-06-28T09:16:41.591870+00:00

This release introduces Bambdas into Proxy > WebSockets history filter and Logger > View filter, as well as the ability to duplicate Repeater tabs multiple times. We have also enhanced the layout of Burp's Dashboard, added a Connection ID column to Logger, and improved the usability of data tables across Burp.

Advanced filtering in more tools with Bambdas

We're introducing Bambdas into more areas of Burp Suite. These Java-based code snippets enable you to customize Burp directly from the UI.

This release introduces Bambdas into two new areas of Burp:

Proxy > WebSockets history filter.

Logger > View filter.

We've also created a Bambdas GitHub repository, where you can browse submissions from community members or contribute your own Bambdas.

Keep an eye out for more Bambdas appearing across Burp in future releases!

Improved Dashboard

We've completely redesigned the Dashboard to make better use of on-screen space. You're now able to see detailed information about your scans and other tasks, without having to open additional popup windows.

To make room for all this information, we've moved the event log and the list of issues to a collapsible panel, which you access from the dock at the bottom of the screen.

Improved usability of tables in Burp

We've started rolling out major usability improvements to data tables in Burp. For most tables in Burp, in addition to sorting and filtering, you can now:

Change the order of columns.

Hide columns.

Burp remembers the changes you make to the layouts of your tables, and will apply your preferences when you create a new project, or open an existing project, on your machine.

Ability to duplicate Repeater tabs multiple times

We've added functionality that enables you to create multiple copies of a grouped Repeater tab in one go. This can be helpful if you're testing for race condition vulnerabilities as it makes the process of creating identical requests much more efficient.

Connection ID column added to Logger

We’ve added a Connection ID column to Logger, which enables you to see which requests used the same connection. This makes it easier to detect if a website’s behavior changes, based on previous requests sent down the same connection.

Other improvements

We've also made the following improvements:

We've added a Format BChecks action to the right-click menu, which can automatically adjust whitespace and indentation when writing BChecks.

Scanner now manages memory usage much more efficiently during the audit phase of browser-powered scans.

Scanner is now able to submit requests that match the Content-Type of non-standard JSON endpoints, for example, application/json-patch+json or application/*+json.

Scanner can now send arrays as query string parameters when scanning an OpenAPI schema. This enables it to find more endpoints.

Scanner is now better able to identify - and disregard - duplicate items in different areas of your application during scans. This helps to reduce the time it takes for scans to complete.

To reduce notification noise when launching Burp, the log message indicating that the Proxy is running is now recorded as a debug log item.

Bug fixes

We've fixed a bug that prevented Notes from saving when clicking Save item or Save entire history in Repeater.

Browser upgrade

We have upgraded Burp's built-in browser to 121.0.6167.85 for Mac and Linux and 121.0.6167.85/.86 for Windows. For more information, see the Chromium release notes.
