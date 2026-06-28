# Configuring network and firewall settings for a site

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-your-sites/configuring-network-and-firewall-settings
Fetched: 2026-06-28T09:15:38.054935+00:00

DAST

Configuring network and firewall settings for a site

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

When you add a new site, you need to configure your network and firewall settings to enable Burp Suite DAST to scan your site effectively. This includes:

Allowing access to your site from the infrastructure on which your scans will run.

Allowing outbound connections to the public Burp Collaborator server. This enables Burp Scanner to use out-of-band application security testing (OAST) techniques to test whether an attacker could induce your site to interact with arbitrary external services. For more information, see Burp Collaborator.

The configuration depends on whether you have a Cloud or self-hosted instance of Burp Suite DAST.

For details, see the relevant section below.

Cloud instances

If you want to run scans of the site on Cloud scanning machines:

Allow inbound access to your site from the Scanner IPs listed on the PortSwigger IP ranges page.

Allow outbound access from your site to *.oastify.com on ports 80 and 443.

If you want to run scans of the site on self-hosted scanning machines:

Allow inbound access to your site from the IP addresses of your scanning machines.

Allow outbound access from your site to *.oastify.com on ports 80 and 443.

If you want to run CI-driven scans of your site:

Allow inbound access to your site from your scan containers.

Allow outbound access from your site to *.oastify.com on ports 80 and 443.

Note

These options are not mutually exclusive. You can enable all of them for your site.

Self-hosted instances

To allow your scanning machines to scan your site effectively:

Allow inbound access to your site from the IP addresses of your scanning machines.

Allow outbound access from your site to *.oastify.com on ports 80 and 443.

If you want to run CI-driven scans of your site:

Allow inbound access to your site from your CI/CD platform agents.

Allow outbound access from your site to *.oastify.com on ports 80 and 443.

Note

These options are not mutually exclusive. You can enable all of them for your site.
