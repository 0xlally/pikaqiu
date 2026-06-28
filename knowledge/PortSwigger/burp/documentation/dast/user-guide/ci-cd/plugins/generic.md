# Integrating with other CI/CD platforms

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/plugins/generic
Fetched: 2026-06-28T09:15:35.557521+00:00

DAST

Integrating with other CI/CD platforms

Last updated:

June 18, 2026

Read time:

1 Minute

Although we provide plugins for Jenkins and TeamCity, you can integrate Burp Suite DAST with most other CI/CD platforms using our generic, platform-agnostic driver. The functionality is similar, but instead of using a UI to control your settings, you have to pass them into a build step as command line parameters.

Note

The CI/CD driver allows you to configure both site-driven scans and Burp scans. This is determined by whether the --site-id parameter is present in the command that triggers the scan. If you're unsure which option is right for you, please refer to the following page for more information: Integration types

In this section

Configuring a site-driven scan with the generic CI/CD driver

Configuring a Burp scan with the generic CI/CD driver

Parameter reference for the generic CI/CD driver

Optional settings

Overriding the default scan configurations from your CI/CD system

Ignoring issues
