# Enterprise Edition 2024.1

Source: https://portswigger.net/burp/releases/enterprise-edition-2024-1
Fetched: 2026-06-28T09:16:19.549092+00:00

This release introduces support for Java 21, as well as a number of bug fixes.

Support for Java 21

Burp Suite Enterprise Edition now supports Java 21, the latest Java release that has long term support. This brings performance improvements and security enhancements.

Bug fixes

We've fixed the following bugs:

You can now upload large extensions to Burp Suite Enterprise Edition. We now support uploads up to 500MB.

If you have a GitLab integration, when you delete a GitLab issue you can now unlink the issue in Enterprise.

When integrating with Jira, Burp now only shows Jira projects that you have permission to create issues for. This helps to make the integration requirements clearer.

If you have a GitLab integration, when an issue is superseded due to further evidence, then the original Jira ticket is now automatically updated to link to the later issue.
