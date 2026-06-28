# Setup guide: CI-driven scans with no dashboard

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/ci-driven-no-dashboard
Fetched: 2026-06-28T09:15:32.077990+00:00

DAST

Setup guide: CI-driven scans with no dashboard

Last updated:

June 18, 2026

Read time:

1 Minute

You can integrate Burp Scanner into your CI/CD pipeline really easily, without the need to set up a DAST server. This is ideal if you only want to run CI-driven scans, and you don't need to use the features of Burp Suite DAST's dashboard.

This option enables you to run Burp Scanner from a Docker container in your CI/CD platform. You can view the results of your scans directly in your CI/CD platform, where they're saved as a JUnit or Burp XML file.

Configuring your scans is straightforward. You can use a configuration file to define:

Start URLs, and the scope of your scan

The scan configuration

Site login details

The configuration file is in YAML format, and includes comments to make it easy to use.

Related pages

Running a basic CI-driven scan with no dashboard

Configuring CI-driven scans with no dashboard

Example integrations for CI-driven scans with no dashboard

Next step - Running your first CI-driven scan with no dashboard

CONTINUE
