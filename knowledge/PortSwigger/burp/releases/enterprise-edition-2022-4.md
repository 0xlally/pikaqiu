# Enterprise Edition 2022.4

Source: https://portswigger.net/burp/releases/enterprise-edition-2022-4
Fetched: 2026-06-28T09:16:17.919117+00:00

This release enables some new reporting formats relating to PCI DSS and OWASP Top 10 vulnerabilities, as well as automated ticket creation for GitLab and Trello.

Compliance reporting

Burp Suite Enterprise Edition now includes compliance reporting formats directly relating to the PCI DSS and the OWASP Top 10. This makes it easier than ever to check for relevant vulnerabilities across your whole web portfolio.

Automated ticket creation for GitLab and Trello

Burp Suite Enterprise Edition can now automatically create GitLab tickets and Trello cards for issues found during scans. When automated ticket creation is enabled, the system creates a card or ticket for any issues that are above a specified severity and confidence level.

Minor improvements and bug fixes

This release also provides a number of minor improvements and bug fixes. For example:

We have added support for MariaDB 10.6.

We have fixed an issue whereby Trello cards were being raised with visible HTML tags included in the content.

We have fixed an issue whereby the web server sometimes failed to generate a self-signed certificate when installing using an external database.
