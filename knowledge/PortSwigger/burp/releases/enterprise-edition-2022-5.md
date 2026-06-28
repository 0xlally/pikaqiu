# Enterprise Edition 2022.5

Source: https://portswigger.net/burp/releases/enterprise-edition-2022-5
Fetched: 2026-06-28T09:16:17.686202+00:00

This release enables you to raise tickets for multiple issues at once and provides a security patch. In addition, we've simplified the way that you manage scan configurations.

Raise tickets for multiple issues

You can now raise tickets for multiple issues at the same time in Jira, GitLab and Trello. You can create a separate ticket for each issue, or combine issues of the same type into one ticket.

Changes to how scan configurations are managed

You now manage scan configurations exclusively on the site level. You can no longer override the site's configuration when scheduling a scan. This simplifies the process and ensures that the data you use to track your security posture remains accurate. Previously, users could inadvertently distort your trend analysis data by scheduling one-off scans with a completely different configuration.

We still support any existing scan configurations that were set at the scan level. However, we recommend that you migrate these to the site level as soon as possible.

Other improvements

This release also provides a number of other improvements:

Users running scans in the cloud can enable verbose debugging. This allows more detailed logs to be sent to the PortSwigger support team.

Scan reports now include reasons for scan failures.

To reduce the need to manage disk space manually, old versions of the scanner are cleaned up after seven days. The latest version is not deleted.

This release upgrades the JRE to version 11.0.15. This provides several security patches.

Security patch

We have fixed a bug related to site restrictions. If a high-privileged user restricted another user's access to specific sites, and then subsequently deleted all of these sites, then the low-privileged user gained access to all configured sites. This was identified during internal testing.

Bug fixes

We've fixed some bugs. For example:

You can now change the web server port when using an HTTP web server configuration.

You can delete sites if you're running an SQL server.

The Scan again button works for users with the 'Scan initiator' role.

You can select sites in nested folders in the scanning pool.
