# Enterprise Edition 2024.4

Source: https://portswigger.net/burp/releases/enterprise-edition-2024-4
Fetched: 2026-06-28T09:16:20.260094+00:00

This release improves support for cipher suites and increases HTTP header sizes for SAML. We've also fixed some bugs.

Improvements

We've made the following improvements:

We've enhanced system compatibility by adding support for all modern cipher suites. This makes sure that secure data exchanges align with current security protocols.

We've increased the size limit for HTTP

header fields. This improves the handling of large SAML messages, to improve SSO integration.

Bug fixes

We've fixed the following bugs:

Fixed a bug in automated Trello integrations that triggered repetitive emails.

Fixed an issue with Jira integration that prevented projects being retrieved when users didn't have the right permissions.

Fixed an issue where a corrupt Burp JAR file was inadvertently used by the agent. The validation checks now make sure that only properly formatted files are used.

Fixed an issue that was causing truncation of diagnostic data in Burp scan logs.

Updated the PostgreSQL JDBC driver to preemptively address a vulnerability.

Note for Jira Server users

As of February 15, 2024, Atlassian has officially discontinued support for Jira Server. Please note that we can now offer only limited assistance with issues related to Jira Server integrations. For more information on Jira Server's discontinuation, see Atlassian's website.
