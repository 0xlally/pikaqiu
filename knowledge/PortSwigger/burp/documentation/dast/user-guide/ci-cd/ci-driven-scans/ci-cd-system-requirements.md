# System requirements for CI-driven scans

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/ci-driven-scans/ci-cd-system-requirements
Fetched: 2026-06-28T09:15:34.932860+00:00

DAST

System requirements for CI-driven scans

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

In order to run scans successfully, make sure that your infrastructure meets the following requirements:

We recommend that you run a CI-driven scan on a machine that has a minimum of 4 CPU cores and 8 GB of RAM. We also recommend that you have 30 GB of free disk space. While this should be suitable for most use cases, larger or more complex target applications may require more resources.

Your CI/CD build agent or node must be configured to run Docker containers.

The CI/CD build agent or node where the container is running must be able to access PortSwigger's public image repository public.ecr.aws/portswigger/, as well as the target application you want to scan.

Network and firewall configuration

To run CI-driven scans, you need to perform some network and firewall configuration. There are different configuration requirements for Cloud and self-hosted instances of Burp Suite DAST.

Cloud

To run CI-driven scans on a Cloud instance, enable the following:

Outbound access from your scanning containers to the Dashboard IPs listed on the PortSwigger IP ranges page.

Outbound access from your scan containers to *.oastify.com on port 443.

Self-hosted

To run CI-driven scans on a self-hosted instance, enable the following:

Outbound access from your scan containers to your DAST server.

Outbound access from your scan containers to *.oastify.com on port 443.
