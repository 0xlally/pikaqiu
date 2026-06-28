# Enterprise Edition 2025.1.1

Source: https://portswigger.net/burp/releases/enterprise-edition-2025-1-1
Fetched: 2026-06-28T09:16:20.995799+00:00

This release fixes a bug that was introduced in Enterprise Edition 2025.1. The bug prevented certain users from creating sites. 2025.1 was withdrawn while we fixed the bug. 2025.1.1 also includes all the changes that were introduced in 2025.1.

Enterprise Edition 2025.1

Enterprise Edition 2025.1 enables you to bulk-schedule scans for sites and folders. We've also added support for dynamic authorization for API scans, and enabled you to configure TLS cipher suites to meet specific security requirements. In addition, we now support IPv6 networks for self-hosted instances, and we fixed some security issues and bugs.

Bulk-scheduling sites and folders

You can now select multiple sites and folders, and schedule recurring scans for all of them at once. This makes it easier to manage scans if you have a large portfolio of sites.

When you schedule a recurring scan for a folder, you create a scan for each of the sites in the folder.

If you remove a site from the folder, you remove the scheduled scan from the site.

If you add a site to the folder, you add the scheduled scan to the site.

For more information, see Creating scans.

Dynamic authorization API keys and custom tokens

Dynamic tokens expire after a set time, and have to be refreshed. You can now configure Burp Suite Enterprise Edition to fetch refreshed API keys and custom tokens automatically. This enables you to scan assets which use this type of enhanced security.

For more information, see Configuring API authentication.

Configuring TLS cipher suites

If you use a self-hosted instance of Burp Suite Enterprise Edition, you can now configure TLS cipher suites to meet your own security requirements, or to comply with specific standards. You can use an environment variable to select which groups of cipher suites you want to enable, or create your own combinations of cipher suites.

For more information, see Configuring TLS cipher suites - self-hosted, or Configuring TLS cipher suites - Kubernetes.

Support for IPv6 networks

You can now configure self-hosted instances of Burp Suite Enterprise Edition on IPv6 networks.

Security fixes

We made the following security changes:

(CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:L/I:L/A:L) 4.8 Medium

Privilege escalation due to lack of file permissions verification during software installation in Windows systems.

Prior to Burp Enterprise installation, a local attacker with low privileges could create malicious directories to have control over sensitive files.

(CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N) 3.3 Low

Hardcoded credentials used as the Java keystores password in both Windows and Linux systems.

(CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N) 2.5 Low

Improper session termination that could be leveraged for persisted session hijacking if the victim’s session token is previously leaked.

Bug fixes

The search filter now works correctly, when you use it to assign sites to a scanning pool.
