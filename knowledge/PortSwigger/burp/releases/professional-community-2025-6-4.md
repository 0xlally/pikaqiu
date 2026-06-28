# Professional / Community 2025.6.4

Source: https://portswigger.net/burp/releases/professional-community-2025-6-4
Fetched: 2026-06-28T09:16:54.287650+00:00

This release introduces automated modification of messages in Burp Repeater using custom actions. It also adds a toggle for quickly switching between tab views, simplifies extension settings management, and includes numerous quality of life improvements.

Modify messages in Repeater with custom actions

You can now use custom actions to automate modifications to requests and responses in Burp Repeater. This helps you streamline manual testing by building Repeater functionality that fits your workflow.

For example, you can now do the following:

Modify and resend requests, then automatically update the responses.

Decode or encode data directly in the message editor for faster analysis.

Annotate responses for quicker comparison or analysis.

Custom actions are quick to write and easy to use. To start writing them, check out our Custom actions reference guide. For information about how to use them, see Custom actions.

If you'd like to share your custom actions with the community, see Submitting Bambdas to our GitHub repository.

Easily switch between tab views

To make it easier to switch between tab views, we've added a toggle button in the top-right corner of Burp Repeater, Collaborator, and Intruder:

Click to show tabs in a single row.

Click to show tabs across multiple rows.

Add extension setting panels without writing UI code

You can now add custom panels to the Settings dialog using a built-in panel builder - no UI code required. This makes it easier to add settings to your extension.

The builder supports text and number fields, checkboxes, and drop-down menus. You can choose to save settings to the user data or current project file, or not persist them at all.

To get started, see Adding a settings panel to your Burp extension.

Improved integration for writing scan checks in extensions

The Montoya API now gives you more control over scan checks. You can now configure checks on a per-request and per-host basis, instead of just per-insertion point. This makes it easier to control when scan checks run and reduce unnecessary requests.

In addition, issuing requests from custom checks previously used a generic http object that bypassed Burp Scanner’s configuration. As a result, scans defaulted to standard settings. Now, the http object passed into your scan checks is fully integrated with Burp Scanner, ensuring all configured scan settings are applied.

Quality of life updates

We've made the following quality of life improvements:

You can now run shell commands more easily in custom actions and extensions, using utilities().shellUtils().execute(). You can set a timeout and choose how it's handled, enabling you to automate more complex tasks with external tools. For more information, see Running shell commands.

You can now export Organizer data as CSV files. This makes it easier to save and share your work outside of Burp.

Burp now adds a placeholder status line to responses that have no headers, including HTTP/0.9 responses. This makes them visible in Burp's message editor.

Burp now detects GraphQL in any request types, not just POST and GET requests.

You can now Select all when creating a Repeater tab group, making it easier to group all your existing tabs.

WebSocket connections created using the Montoya API now automatically respond to PING frames with PONGs. This avoids connections unexpectedly being closed.

Bug fixes

We've fixed a bug that prevented the Cut function from working in the HTTP filter Bambda editor.

Browser upgrade

We've upgraded Burp's browser to Chromium 138.0.7204.100/.101 for Windows & Mac, and 138.0.7204.100 for Linux. For more information, see the Chromium release notes.
