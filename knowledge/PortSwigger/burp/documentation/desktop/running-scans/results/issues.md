# Issues

Source: https://portswigger.net/burp/documentation/desktop/running-scans/results/issues
Fetched: 2026-06-28T09:15:53.879922+00:00

Support Center

Documentation

Desktop editions

Running scans

Viewing scan and live task results

Issues

Professional

Issues

Last updated:

June 18, 2026

Read time:

3 Minutes

Burp enables you to track potential vulnerabilities, whether automatically detected by Burp Scanner or manually detected during your penetration testing workflow.

All issues are recorded in your project file, along with key information to help you resolve or manually investigate the issue.

For more information on how to manually create issues in Burp Suite Professional, see Manually creating issues for reports.

You can choose to view either a task-specific list of issues, which contains issues found by an individual task, or a project-level list containing entries for all issues found across all tasks in your project.

To view the project-level issues list:

Go to the Dashboard tab.

From the bottom dock, select All issues.

To view a task-specific issues list:

Go to the Dashboard tab.

From the Tasks list, select the relevant task.

In the main panel, go to the Issues tab.

From here, you can:

Monitor scan results.

Review new issues as they are reported.

Assign confidence and severity levels to issues.

Report and delete issues.

Each item in the Issues table contains the following details:

Time - The time that the issue was found.

Source - The task that found the issue.

Issue type - The issue type.

Host - The host server for the issue.

Path - Where applicable, the URL path to the issue location.

Insertion point - Where applicable, the type of insertion point used in the request that found the issue.

Severity - High, medium, low, or information.

Confidence - Tentative, firm, or certain.

Comment - Any user-applied comment. Double-click this field to add a comment.

You can customize and sort the table, and copy column data to your clipboard. For more information, see Customizing Burp's tables.

Note

Each issue is only recorded the first time it is found.

Analyzing issue activity

To filter the Issues table, use the buttons at the top of the tab. You can filter using the following conditions:

Severity.

Confidence.

Type of check, selected from the following:

BChecks.

Scan checks.

Extensions.

Manually generated.

To filter the issues by a specific term, use the Search bar.

Select an issue to view further information on it in the panel below the table. The following tabs are available:

Advisory - A summary of the issue. This contains a description of the issue and remediation advice.

Request - This tab is displayed if the issue was triggered by a request payload. It highlights the payload that triggered the issue.

Response - This tab is displayed if the issue was reflected in a response. It highlights the issue location.

Path to issue - This tab is displayed if the issue was triggered by a request payload. It displays the actions taken by Burp Scanner that led to the request being sent.

Managing issues

Right-click an issue to perform further actions:

Add comment - Add a comment to the item.

Highlight - Apply a highlight color to the item.

Set severity - Reassign the issue's severity level. You can flag the issue as a false positive.

Set confidence - Reassign the issue's confidence level.

Delete issue - Delete selected issues from the table.

Report selected issues - Generate a report of selected issues. For more information, see Reporting scan results.

If you reassign the severity or confidence level, or capture additional evidence for the issue, then the issue is displayed with its updated details. To restore the original details, right-click an issue and select Restore original value from the context menu.

Related pages

Auditing - Gives detailed information on the

auditing process, including issue types.

Target scope - Gives detailed

information on how to set a target scope.
