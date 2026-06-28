# Enterprise Edition 2023.7

Source: https://portswigger.net/burp/releases/enterprise-edition-2023-7
Fetched: 2026-06-28T09:16:19.510321+00:00

This release improves how we handle database credentials and TLS certificates for Kubernetes deployments. We've also made several other improvements.

Improvements to process for deploying with Kubernetes

If you're performing a Kubernetes deployment, you can now use your values.yaml file to add a TLS certificate and database credentials. This enables you to use CI-driven scans with web servers that are configured to use a self-signed or private CA-signed certificate.

We've included a parameter to continue using your existing TLS certificate for now. For more information, see Installing the application.

Other improvements

The following changes have also been made:

You can now integrate Burp Suite Enterprise Edition with the Server, Data Center and Cloud versions of Jira 9.x.

To make it easier for you to share information with our Support team, you can now download multiple log files in a single pack. To learn more, see Downloading logs and debug packs.

In the Scans tab, the number of Scanned URLs now also includes URLs with errors.
