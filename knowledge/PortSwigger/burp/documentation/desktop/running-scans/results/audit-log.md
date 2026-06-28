# Audit log

Source: https://portswigger.net/burp/documentation/desktop/running-scans/results/audit-log
Fetched: 2026-06-28T09:15:53.857386+00:00

Support Center

Documentation

Desktop editions

Running scans

Viewing scan and live task results

Audit log

Professional

Audit log

Last updated:

June 18, 2026

Read time:

3 Minutes

The audit log is a list of key issue events that occurred during the audit phase of a scan or task. For example, these events could include:

When Burp finds a new issue.

When Burp discovers more evidence for a known issue.

When Burp discovers that an issue is no longer present, and removes it from the Issues list.

To view the audit log for a task:

Go to the Dashboard tab.

From the Tasks list, select the relevant task.

In the main panel, go to the Audit log tab.

Viewing audit activity

The audit log enables you to:

Monitor audit progress.

View details of deferred interactions with the Burp Collaborator server.

Assign confidence and severity levels to issues.

Report issues.

Each item in the table contains the following details:

# - An index number for the item.

Time - The time that the issue was found.

Source - The task that found the issue.

Action - The action that was performed. For example, finding an issue, removing an issue, or adding evidence.

Issue type - The issue type.

Host - The host server for the issue.

Path - Where applicable, the URL path to the issue location.

Insertion point - Where applicable, the type of insertion point used in the request that found the issue.

Severity - High, medium, low, or information.

Confidence - Tentative, firm, or certain.

Comment - Any user-applied comment. Double-click this field to add a comment.

You can customize and sort the table, and copy column data to your clipboard. For more information, see Customizing Burp's tables.

Analyzing audit log activity

To filter the Audit log table, use the buttons at the top of the tab. You can filter using the following conditions:

Severity

Confidence

The type of check used, selected from the following:

BChecks

Scan checks

Extensions

To filter entries by a specific term, use the Search bar.

Select a log entry to view further information on it in the panel below the table. The following tabs are available:

Advisory - A summary of the relevant issue. This contains a description of the issue and remediation advice.

Request - This tab is displayed if the entry was created as a result of a request payload. It highlights the payload that triggered the issue.

Response - This tab is displayed if the entry was created as a result of a response. It highlights the issue location.

Path to issue - This tab is displayed if the entry was created as a result of a request payload. It displays the actions taken by Burp Scanner that led to the request being sent.

Managing audit log items

Right-click a log entry to perform further actions:

Add comment - Add a comment to the item.

Highlight - Apply a highlight color to the item.

Set severity - Reassign an issue's severity level. You can flag the issue as a false positive.

Set confidence - Reassign an issue's confidence level.

Report selected issues - Generate a report of selected issues. For more information, see Reporting scan results.

If you reassign an issue's severity or confidence level, or capture additional evidence for it, then the issue is displayed with its updated details. To restore the original severity or confidence, right-click an issue and select Restore original value from the context menu.

Related pages

Auditing - Gives detailed information on the

auditing process, including issue types.

Target scope - Gives detailed

information on how to set a target scope.
