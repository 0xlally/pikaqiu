# Managing Jira ticket duplication

Source: https://portswigger.net/burp/documentation/dast/user-guide/integrate-issue-tracking-platforms/managing-jira-ticket-duplication
Fetched: 2026-06-28T09:15:36.754282+00:00

DAST

Managing Jira ticket duplication

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

When you create automatic Jira ticket rules, it's useful to understand how Burp Suite DAST manages ticket duplication.

Burp Suite DAST tracks issues over time and classifies them as new, regressed, repeated, or resolved. Jira tickets are raised automatically based on the following logic:

New issues:

A new ticket is always raised for issues that have not been seen before on the current site.

Repeated or regressed issues:

If the automatic rule hasn't already raised a ticket for the issue, it raises a new ticket.

If the automatic rule has already raised a ticket for the issue, it doesn't raise a duplicate ticket. Instead, it creates a link to the original ticket in the Linked tickets column.

Burp Suite DAST manages tickets for each Jira project separately. This means that if two automatic rules try to generate tickets for the same issue in the same project, only one ticket is raised. If two or more automatic rules raise the same issues in different Jira projects, a ticket will be raised in each.

Related pages

Raising Jira tickets automatically

Raising Jira tickets manually
