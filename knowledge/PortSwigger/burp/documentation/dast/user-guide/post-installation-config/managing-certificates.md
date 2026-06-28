# Managing certificates for outbound connections

Source: https://portswigger.net/burp/documentation/dast/user-guide/post-installation-config/managing-certificates
Fetched: 2026-06-28T09:15:38.923356+00:00

DAST

Managing certificates for outbound connections

Last updated:

June 18, 2026

Read time:

1 Minute

Self-hosted

You can add or remove certificates so that Burp Suite DAST knows which external systems to trust. For example, you can add certificates for email or Jira servers, or to allow updates from PortSwigger.

You can also upload certificates for an internal certificate authority, or individually self-signed certificates.

Note

Only upload certificates from trusted sources.

Certificates for inbound traffic are managed separately, refer to Enabling TLS.

To manage your certificates for outbound connections:

Log in to Burp Suite DAST as an administrator.

From the settings menu , select Network.

Scroll down to Manage certificates.

To add a certificate, click Upload certificate.

To remove a certificate, click .
