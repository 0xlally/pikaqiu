# Integrating CI-driven scans

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/ci-driven-scans
Fetched: 2026-06-28T09:15:34.823708+00:00

DAST

Integrating CI-driven scans

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

You can integrate CI-driven scans into your CI/CD pipeline. This enables Burp Scanner to run from a Docker container, and report results back to your Burp Suite DAST server. CI-driven scans make it easy to scan sites and applications before they enter production.

What are CI-driven scans?

When a CI-driven scan is initiated, an instance of Burp Scanner is created inside a Docker container. This instance of Burp Scanner runs a local scan on a specified URL, defined by an environment variable in your pipeline script. Once the scan has finished, the instance of Burp Scanner sends the results to your Burp Suite DAST server in JUnit XML format.

Note

We provide full setup walkthroughs for Jenkins, TeamCity, and GitHub Actions. However, you can use our generic setup instructions to fully integrate with any CI platform, including CircleCI, Bamboo, and Azure DevOps.

Configuring your scan

CI-driven scans are configured using a YAML file. This file defines:

Start URLs

The scope of your scan

The scan configuration

Site login details

You can also use the YAML file to apply custom extensions, BChecks, and BApps to your scans. For more information, see Using custom extensions, BChecks, and BApps with CI-driven scans.

Viewing your scan results

You can view your scan results in a number of ways:

In your CI/CD environment

By viewing the JUnit XML file directly

In the web interface for Burp Suite DAST

Related pages

System requirements for CI-driven scans

Getting started with CI-driven scans

Creating a configuration file for a CI-driven scan

Adding a configuration file to a CI-driven scan

Integration walkthroughs
