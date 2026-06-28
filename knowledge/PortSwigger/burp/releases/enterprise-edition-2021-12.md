# Enterprise Edition 2021.12

Source: https://portswigger.net/burp/releases/enterprise-edition-2021-12
Fetched: 2026-06-28T09:16:17.196700+00:00

This release enables bulk actions for sites and scans, and integration with GitLab and Trello so that you can raise tickets for any vulnerabilities found by your scans.

Bulk actions for sites and scans

From the Sites and Scans pages, you can now perform common actions on multiple items at the same time. This includes:

Moving sites and folders

Deleting sites and folders

Launching quick scans

Cancelling or deleting scans

The bulk actions menu appears automatically when you select one or more items using the checkboxes to the left of the page. This can save you a significant amount of time and effort, especially when managing your site tree.

Trello and GitLab integration

You can now connect Burp Suite Enterprise Edition to both Trello and GitLab. This enables you to create Trello cards or raise GitLab issues directly from the Burp Suite Enterprise Edition web UI for any vulnerabilities identified by your scans.

For details of how to configure the integration, please refer to the documentation.

Microsoft SQL Server 2019 support

You can now use Microsoft SQL Server 2019 databases with Burp Suite Enterprise Edition. For a full list of supported database types, please refer to the documentation.

GraphQL upgrade

We have upgraded our GraphQL implementation to GraphQL Java 17.3. This provides a number of bug fixes, as well as increased protection against denial-of-service attacks.

Verbose scan log

When creating a one-off scan, you now have the option to enable verbose logging. You can then download this log from the Reporting & Logs tab.

Please note that this is primarily intended for use by our technical support team, who will occasionally ask you to activate this feature when assisting you with a problem.

Bug fixes

This release also contains several minor bug fixes, Most notably, the uninstaller has been improved to reduce the chance of issues arising when reinstalling at a later date. We have also fixed an issue that could occur when running the database transfer tool with MySQL 8 databases.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
