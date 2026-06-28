# Raising tickets for multiple issues

Source: https://portswigger.net/burp/documentation/dast/user-guide/work-with-scan-results/raising-tickets/raise-tickets-multiple
Fetched: 2026-06-28T09:15:43.586311+00:00

DAST

Raising tickets for multiple issues

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

You can raise tickets for several issues at once. You can also group similar issues together on one ticket, which minimizes the number of tickets that you need to manage.

To raise new tickets for multiple issues, do the following:

In Burp Suite DAST, go to Scans > Issues.

Select the checkbox for each of the issues that you want to raise a ticket for. A menu bar appears with options for raising tickets. You can only see options for the issue tracking platforms that your administrator has configured. For more information, refer to integrating issue tracking platforms.

Click the button for your preferred issue tracking platform.

Choose how you want tickets to be raised if there are several issues of the same type:

To raise a separate ticket for each issue, select For each issue.

If you want to combine all the issues of the same type into one ticket, select For each issue type.

Click Create.

Notice that icons appear in the Linked tickets column to show that the issues are linked to Jira, GitLab, or Trello.

Note

If necessary, you can repeat this process to raise tickets on a different issue tracking platform.

Linking multiple issues to an existing ticket

You can link multiple issues to an existing ticket. This allows you to have a mixture of issue types on the same ticket:

From your issue tracking platform, make a note of the ticket number that you want to link to.

In Burp Suite DAST, go to Scans > Issues.

Select the checkbox for each of the issues that you want to link to the ticket. A menu bar appears with options for raising tickets. You can only see options for the issue tracking platforms that your administrator has configured. For more information, refer to integrating issue tracking platforms.

Click the button for your preferred issue tracking platform.

Select Link to existing ticket.

Enter the ticket number, and click Link.

Managing linked tickets

The Linked tickets tab provides an overview of all the tickets that are linked to issues found by the selected scan. You can manage your linked tickets using the following actions:

To see more information about a ticket, expand the entry in the Type column. You can view a list of the issues that are linked to the ticket. You can also see the ticket status and priority.

To view the ticket on the issue tracking platform, click the ticket ID in the Link column.

To unlink an issue, click the unlink symbol in the Actions column.

To unlink multiple tickets, select the checkboxes and click Unlink.
