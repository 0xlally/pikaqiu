# Raising Jira tickets automatically

Source: https://portswigger.net/burp/documentation/dast/user-guide/integrate-issue-tracking-platforms/raising-jira-tickets-automatically
Fetched: 2026-06-28T09:15:36.548503+00:00

DAST

Raising Jira tickets automatically

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

You can raise Jira tickets automatically for issues that match the specific severity and confidence levels that you set.

Note

To avoid creating a large number of tickets, we recommend that you set high severity and confidence levels to begin with. You can add lower severities and confidence levels once you have a better understanding of how many tickets are created as a result of your scans.

From the settings menu , select Integrations and find the Jira panel. Click Edit.

Under Raise tickets automatically, click Add rule.

Enter a name for the rule. You can also add a description.

Select one or more severity levels and confidence levels that cause a ticket to be raised. Click Next.

Select all the sites that you want the rule to apply to. Click Next.

Select a project from the Project drop-down list. Start typing to search the available projects.

Select a ticket type from the Ticket type drop-down list. Start typing to search the available ticket types.

If required, select a parent from the Parent drop-down list. Start typing to search the available Jira parents.

Click Next. The Custom ticket fields tab opens.

Adding custom ticket fields

Burp Suite DAST detects if your Jira project has fields that are compulsory when you raise a ticket. The Custom ticket fields tab enables you to automatically fill these fields.

You can also add custom ticket fields that are optional.

Note

We currently support the following ticket field types:

Text strings

Numbers

Single select lists

Multi-select lists

If your project requires fields that are a different type, Burp Suite DAST won't be able to raise tickets.

To automatically fill custom ticket fields:

In the Custom ticket fields tab, enter a Jira value for each Required Jira field.

To add a Jira value to an optional custom field:

Click Add more fields.

Enter values for your Jira field and Jira value.

To add an additional custom field, click the Configure optional fields button.

Click Save.

Raising tickets for previously found issues

When you create an automatic rule, it will raise Jira tickets when you run your next scan.

You can also raise tickets for issues that were found by your most recent successful scan, that meet your new rule. Select the tick box for Raise tickets for all issues from the most recent successful scan.

The process of raising tickets for these issues begins when you click Save.

Note

If you select this option for a large number of sites, it may take some time to raise all the relevant tickets.

Duplicating rules for automatic tickets

You can duplicate the rules you've already created for raising tickets. This makes it easy to raise tickets for different projects or severities, for example.

To duplicate the rules for automatic ticket creation:

From the settings menu , select Integrations and find the Jira panel. Click Edit.

Find the ticket rules you want to duplicate, and click the options menu . Select Create a duplicate.

Enter a new name for your rule, and edit the rule as necessary.

When you finish editing the rule, click Save.

Related pages

To learn how to populate Jira tickets conditionally, based on severity and confidence, see Conditional field mapping

To learn how Burp Suite DAST manages duplicate tickets, see Managing Jira ticket duplication.

To learn how to enable users to raise Jira tickets manually, see Enable users to manually raise Jira tickets.

To learn how users can manually raise Jira tickets, see Raising Jira tickets manually.
