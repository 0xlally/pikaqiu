# Integrating a CI-driven scan with GitHub Actions

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/ci-driven-scans/example-integrations/integrate-github
Fetched: 2026-06-28T09:15:34.806037+00:00

DAST

Integrating a CI-driven scan with GitHub Actions

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

You can integrate a CI-driven scan with GitHub Actions. This enables you to use Burp Scanner to run scans as a stage in your existing CI/CD pipeline, and fail builds that meet your issue threshold.

To learn how to do this, see the readme file for our GitHub Action (opens in a new tab):

GitHub Action for CI-driven scans

You can configure your scan using a configuration file. This enables you to use application logins, and custom scan configurations. To learn more, see Creating a configuration file for a CI-driven scan.

Related pages

Adding a configuration file to a CI-driven scan

System requirements for CI-driven scans
