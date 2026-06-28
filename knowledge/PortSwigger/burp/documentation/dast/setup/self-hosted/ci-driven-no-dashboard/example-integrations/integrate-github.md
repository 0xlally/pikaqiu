# Integrating a CI-driven scan with no dashboard with GitHub Actions

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/ci-driven-no-dashboard/example-integrations/integrate-github
Fetched: 2026-06-28T09:15:32.256454+00:00

DAST

Integrating a CI-driven scan with no dashboard with GitHub Actions

Last updated:

June 18, 2026

Read time:

1 Minute

You can integrate a no-dashboard scan with GitHub Actions. This enables you to use Burp Scanner to run scans as a stage in your existing CI/CD pipeline, and fail builds that meet your issue threshold.

To learn how to do this, see the readme file for our GitHub Action (opens in a new tab):

GitHub Action for CI-driven scans

You can configure your scan using a configuration file. This enables you to use application logins, and custom scan configurations. To learn more, see Creating a configuration file for a CI-driven scan with no dashboard.
