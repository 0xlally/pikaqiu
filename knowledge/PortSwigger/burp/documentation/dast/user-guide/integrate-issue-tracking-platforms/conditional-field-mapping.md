# Conditional field mapping

Source: https://portswigger.net/burp/documentation/dast/user-guide/integrate-issue-tracking-platforms/conditional-field-mapping
Fetched: 2026-06-28T09:15:36.497513+00:00

DAST

Conditional field mapping

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

You can use multiple rules to map different values to Jira custom fields based on the severity and confidence of issues. This enables you to

automatically assign different priorities, team assignments, or labels depending on how critical the issues are.

Note

Make sure your severity and confidence criteria don't overlap between rules. If they do, Burp

Suite DAST will prevent some rules from creating tickets.

Setting up conditional mapping

To create conditional field mapping:

Click Settings and select Integrations.

Find the Jira tile and click Edit.

Under Raise tickets automatically, click Add rule.

Create your first rule:

Enter a descriptive Rule name, such as Critical issues - High confidence.

Select the Severity and Confidence levels for the rule.

Choose your target sites and click Next.

Set the Ticket configuration and click Next.

Set the custom field values for this combination of severity and confidence, and click Save.

Click Add rule to create additional rules, for different combinations of severity and confidence.

Related pages

Raising Jira tickets automatically

Raising Jira tickets manually
