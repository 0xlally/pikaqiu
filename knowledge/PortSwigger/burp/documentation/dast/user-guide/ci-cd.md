# Integrating with CI/CD platforms

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd
Fetched: 2026-06-28T09:15:35.021715+00:00

DAST

Integrating with CI/CD platforms

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

You can use Burp Suite DAST to run CI-driven scans on your CI/CD platform. We also have documents for our legacy solution that used plugins.

CI-driven scans

CI-driven scans enable you to run Burp Scanner from a Docker container in your CI/CD environment. This is an easy way to integrate Burp Suite DAST with your CI/CD platform. It requires you to set up a Burp Suite DAST server.

The scan results are saved as a JUnit or Burp XML file. You can view the results of your scans in your CI/CD environment, or in the Burp Suite DAST dashboard.

You can run this option on any platform that supports Docker containers, including Jenkins, TeamCity, and GitHub Actions.

For more information, see Integrating CI-driven scans.

Note

You can apply custom extensions, BChecks, and BApps to CI-driven scans. For more information, see Using custom extensions, BChecks, and BApps with CI-driven scans.

CI/CD plugins (legacy)

Our legacy solution was to provide plugins for both Jenkins and TeamCity. We still provide documentation for these plugins for now, to support existing users. This method triggers a scan to run in the Burp Suite DAST environment. This is more complex to set up.

For more information, see Using plugins for CI/CD platform integration.
