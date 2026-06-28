# Enterprise Edition 2025.2

Source: https://portswigger.net/burp/releases/enterprise-edition-2025-2
Fetched: 2026-06-28T09:16:22.561630+00:00

This release enables you to import API requests from Postman Collections. We also improved the distribution of scans between self-hosted scanning machines, and we fixed some bugs.

Support for Postman Collections

You can now import API requests from Postman Collections into Burp Suite Enterprise Edition. If you already use Postman to manage your API requests, this allows you to seamlessly import and scan your APIs for vulnerabilities. For more information, see Scanning APIs.

Bug fixes

We fixed the following bugs:

If you only had View team permission, you would be shown sites that weren't relevant to the group that you were viewing.

We increased the timeout for scanning resources, to prevent scans from failing to dispatch on slower networks.

When configuring LDAP SSO, entering a missing password now correctly re-enables the Check Connection button.
