# Professional / Community 2024.1.1.4

Source: https://portswigger.net/burp/releases/professional-community-2024-1-1-4
Fetched: 2026-06-28T09:16:45.171672+00:00

This release introduces the new Insertion points panel in Burp Scanner, enhancing visibility into the attack surface coverage. Major usability improvements come to Intruder and Proxy data tables, with customizable layouts. Native ARM64 builds for Windows are now available for better performance on ARM64 devices. Other notable improvements include easier access to the search feature, custom keyboard shortcuts for macOS, reintroduced Scope sub-tab in the Target tab, updated dashboard notifications, and enhanced GraphQL tab functionalities. The update also includes a performance improvement and fixes several bugs.

Insertion points panel

We've introduced an Insertion points panel in Burp Scanner's Audit items tab. This new panel lists all the insertion points for a request, which can help you understand how much attack surface the scanner is covering.

The panel organizes the insertion points into a tree view, and categorizes them into three main types: Detected (those identified from the base request), Moved (those identified after existing parameters within the request were moved), and Added (those identified after new parameters were added to the request). It also identifies nested insertion points (encoded insertion points that reveal additional insertion points when decoded), and displays these hierarchically. The panel also displays the status of each insertion point, such as Pending, Audited, or Skipped, to reflect the action taken by the scanner based on the scan configuration and the behavior of the insertion point.

Improved usability of tables in Burp Suite

We've continued our rollout of major usability improvements to include Intruder and Proxy data tables. In addition to sorting and filtering, you can now:

Change the order of columns.

Hide columns.

Burp remembers the changes you make to the layouts of your tables, and will apply your preferences when you create a new project, or open an existing project, on your machine.

Native Windows ARM64 builds

We're introducing native ARM64 builds for Windows, optimized for better performance on ARM64 devices. You can download the new builds directly from our website, and if you are using the x64 version on ARM machines with auto-updates turned on, you will automatically upgrade to the ARM64 version in future updates.

Performance improvements

We're working on a number of performance improvements for Burp Suite Professional. In this release, we've reduced the number of browsers that Burp Scanner creates during the audit phase, which lowers demand on system resources while maintaining scan speed.

Other improvements

In Burp Suite Professional, we have added a new search icon to the tab bar to help make the search feature easier to access. This change does not affect Burp Suite Community Edition.

We've reintroduced the Target > Scope tab to help make it easier to access. It's also still accessible via the settings menu.

We've updated the dashboard to ensure any applied filters now influence which notifications appear in the bottom dock tabs. This means irrelevant notifications will no longer be shown.

We've adjusted the sensitivity of the event log so that messages that always occur at startup, like the 'proxy is running' notification, are now logged at debug level.

We've enhanced the 'Update ready to install' notification to include a short description of new features, with a link to detailed release notes.

We've added syntax highlighting and automatic indentation for queries in the GraphQL tab, making it easier to read, write, and edit queries.

We've added a Start response timer column to the HTTP history table. This enables you to monitor how long it takes for responses to start.

Bug fixes

We've fixed several bugs, including:

The drag sensitivity on tabs was too high, leading to accidental detachment of tabs into separate windows.

RequestOptions in the Montoya API was not working as expected.

Adding items to the scope using the Montoya API was not working as expected.

WOFF2 content types were being incorrectly identified, resulting in erroneous 'Content Type Incorrectly Stated' vulnerabilities.

Notes and highlights were sometimes being lost when closing a project file.

Browser upgrade

We've upgraded Burp's built-in browser to 121.0.6167.160 for Mac and Linux and 121.0.6167.160/161 for Windows. For more information, see the Chromium release notes.
