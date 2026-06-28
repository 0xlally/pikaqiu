# Enterprise Edition 2022.1

Source: https://portswigger.net/burp/releases/enterprise-edition-2022-1
Fetched: 2026-06-28T09:16:19.231930+00:00

This release provides a number of minor improvements and bug fixes. For example:

You are now warned via the scan log if the assigned agent machine has insufficient resources available to run a scan. This should help you avoid overloading your machines with too many concurrent scans, which could result in poor performance or cause scans to fail.

We have fixed a bug that prevented bulk site imports from a CSV file working as expected.

We have fixed a bug that prevented you from using self-signed certificates for connecting to an SMTP server using TLS.

Cloud deployment links

There are no AWS CloudFormation or Azure Resource Manager templates for this release. We will shortly be providing an improved, much simpler deployment method and recommend waiting for this instead.
