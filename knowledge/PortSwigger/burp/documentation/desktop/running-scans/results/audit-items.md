# Audit items

Source: https://portswigger.net/burp/documentation/desktop/running-scans/results/audit-items
Fetched: 2026-06-28T09:15:53.919742+00:00

Support Center

Documentation

Desktop editions

Running scans

Viewing scan and live task results

Audit items

Professional

Audit items

Last updated:

June 18, 2026

Read time:

3 Minutes

For each task, the Audit items tab contains a list of items audited by Burp Scanner. It is populated as the audit runs, enabling you to monitor the progress of individual audit items. This enables you to diagnose problems with the audit, for example due to network errors or large numbers of insertion points. You can then change the scan configuration to optimize your audit.

You can view the following details about each item:

# - The item's index number.

Host - The destination host.

URL - The destination URL.

Status - Indicates whether the audit is in progress or complete.

Passive phases, Active phases, JavaScript phases - The audit phase indicators.

Issues - The number of issues identified for the item. These are categorized by severity.

Requests - The number of requests made while auditing the item. This is not necessarily a linear function of the number of insertion points.

Errors - The number of network errors encountered.

Insertion points - The number of insertion points created for the item.

Scanned insertion points - The number of insertion points that have been either fully audited or lightly audited.

Start time, End time - The start and end time of the audit.

Comment - Any user-applied comment. Double-click this field to add a comment.

You can sort and customize the table, and copy column data to your clipboard. For more information, see Customizing

Burp's tables.

Click on an item to view the following information in the panels below the table:

The base request.

A list of all insertion points. Click Insertion points to replace this panel with the base response.

Related pages

Viewing insertion points

Right-click an item to perform various actions as part of your workflow:

Show details - View the base request and response in a new window, as well as the Inspector panel. You can also double-click an item to open this window.

View insertion points - View a list of insertion points for the request in a panel below the table.

Cancel - Stop auditing the item. There may be a short delay while any pending requests are completed.

Audit again - Duplicate the item and add it to the end of the list.

Add comment - Add a comment to the item. You can also double-click the comment cell.

Highlight - Apply a highlight to the item. You can also use the drop-down menu in the index cell.

Send to ... - Send the item's base request to other Burp tools.

Audit phase indicators

Burp Scanner runs through the following phases when auditing content:

Passive phases

Burp Scanner has two passive phases:

Phase 1 - Identify passive issues.

Phase 2 - Consolidate issues that exist at different locations in the application. Burp then reports on the issues.

Active phases

Burp Scanner has five active phases:

Phase 1 - Test each insertion point for first-order vulnerabilities.

Phase 2 - Send data to each insertion point. The data is designed to detect stored input behaviors.

Phase 3 - Re-fetch application responses to detect stored input behaviors.

Phase 4 - Test the stored input paths for second-order vulnerabilities.

Phase 5 - Send a Collaborator payload to each insertion point. The payload is designed to detect blind stored XSS vulnerabilities.

JavaScript phases

Burp Scanner has three JavaScript phases:

Phase 1 - Analyze JavaScript to detect self-contained DOM-based issues.

Phase 2 - Analyze reflection of input into JavaScript code to detect reflected DOM-based issues.

Phase 3 - Analyze stored input in JavaScript code to detect stored DOM-based issues.

Related pages

Auditing - Gives detailed information on the auditing process, including the audit phases.

Dashboard
