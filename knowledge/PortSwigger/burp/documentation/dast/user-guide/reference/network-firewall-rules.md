# Network and firewall rule reference

Source: https://portswigger.net/burp/documentation/dast/user-guide/reference/network-firewall-rules
Fetched: 2026-06-28T09:15:39.429892+00:00

DAST

Network and firewall rule reference

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

To run scans in Burp Suite DAST, you need to allow inbound and outbound network access between your sites and scanning resources. The specific network requirements vary depending on whether your instance is Cloud or self-hosted, and the type of scans you want to run.

This page lists network requirements for the various combinations of instance and scan type.

On this page

Cloud instances running scans on PortSwigger's infrastructure

Cloud instances with self-hosted scans

Cloud instances with CI-driven scans

Self-hosted instances with self-hosted scans

Self-hosted instances with CI-driven scans

Cloud instances running scans on PortSwigger's infrastructure

Cloud

Sites need:

Inbound access from the Scanner IPs listed on the PortSwigger IP ranges page.

Outbound access to *.oastify.com on ports 80 and 443.

You do not need to configure network access for scanning machines when running scans on PortSwigger's infrastructure.

Cloud instances with self-hosted scans

Cloud

Sites need:

Inbound access from your scanning machines.

Outbound access to *.oastify.com on ports 80 and 443.

Scanning machines need:

Outbound access to the sites that you want to scan on the relevant ports.

Outbound access to the Dashboard IPs listed on the PortSwigger IP ranges page.

Outbound access to *.oastify.com on port 443.

Cloud instances with CI-driven scans

Cloud

Sites need:

Inbound access from your scan containers.

Outbound access to *.oastify.com on ports 80 and 443.

Scan containers need:

Outbound access to the sites that you want to scan on the relevant ports.

Outbound access to the Dashboard IPs listed on the PortSwigger IP ranges page.

Outbound access to *.oastify.com on port 443.

Self-hosted instances with self-hosted scans

Self-hosted

Sites need:

Inbound access from your scanning machines.

Outbound access to *.oastify.com on ports 80 and 443.

Scanning machines need:

Outbound access to the sites that you want to scan on the relevant ports.

Outbound access to your DAST server on port 8072.

Outbound access to *.oastify.com on port 443.

Access to the database:

If you use the embedded database, allow any external scanning machines to access the DAST server machine on port 9092.

If you use an external database, allow the DAST server and any external scanning machines to access the database service on the configured host and port.

Note:

When connecting a new scanning machine, the Burp Suite DAST server must have access to *.portswigger.net on port 443.

Self-hosted instances with CI-driven scans

Self-hosted

Sites need:

Inbound access from your scan containers.

Outbound access to *.oastify.com on ports 80 and 443.

Scan containers need:

Outbound access to the sites that you want to scan on the relevant ports.

Outbound access to your DAST server.

Outbound access to *.oastify.com on port 443.
