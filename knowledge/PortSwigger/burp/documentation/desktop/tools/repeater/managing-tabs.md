# Managing Burp Repeater tabs

Source: https://portswigger.net/burp/documentation/desktop/tools/repeater/managing-tabs
Fetched: 2026-06-28T09:16:07.764612+00:00

Support Center

Documentation

Desktop editions

Tools

Repeater

Managing tabs

ProfessionalCommunity Edition

Managing Burp Repeater tabs

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Repeater opens each new HTTP or WebSocket message in a new tab. This enables you to work on multiple messages at once.

You can use the controls on the tab header to create new tabs and make various changes to existing ones:

Create a request from scratch - To open a new tab, click the button. Select either HTTP or WebSocket. You can also send a request to Repeater from elsewhere in Burp to create a new tab.

Rename tabs - Double-click the tab header and enter a new name for the tab.

Duplicate tabs - Right-click a grouped tab, then select Duplicate tab. This option is only available for tabs that are part of a group. Note that each tab consumes system resources, so opening large numbers of tabs may impact performance.

Switch tab view - Use the tab view toggle in the top-right corner to choose from two different views::

Scrolling view - To view tabs in a single, scrollable row, click . To view a drop-down list of open tabs, click .

Wrapped view - To wrap tabs onto multiple rows, click .

Add a tab to a group - Right-click a tab and click Add tab to group, then select a group.

Close tabs - You can close tabs in multiple ways:

Close a single tab - Click the close icon by the tab header.

Close all tabs other than the selected tab - Right-click the tab and select Close other tabs.

Close all tabs to one side of the selected tab - Right-click the tab and select Close tabs to the left or Close tabs to the right.

Reopen the last tab you closed - Right-click any tab and select Reopen closed tab.

Note

You can send a request to Repeater from a request that is already in Repeater - a new tab is created with another instance of the same request.

Tab groups

You can use Repeater's tab group feature to group related tabs together and send groups of HTTP requests in sequence.

Related pages

For more information on grouping Repeater tabs, see Managing tab groups.

For more information on sending Repeater HTTP tabs in sequence, see Sending HTTP requests in sequence.
