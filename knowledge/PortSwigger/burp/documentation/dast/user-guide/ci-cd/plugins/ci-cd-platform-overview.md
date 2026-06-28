# Overview of CI/CD platform integration

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/plugins/ci-cd-platform-overview
Fetched: 2026-06-28T09:15:35.467387+00:00

DAST

Overview of CI/CD platform integration

Last updated:

June 18, 2026

Read time:

2 Minutes

Our legacy solution for CI/CD platform integration was to provide plugins for both Jenkins and TeamCity, as well as a generic driver for any other platform that you might use. The documentation in this section is to support users who are already using this solution. If you're looking to integrate scans in your CI/CD pipeline for the first time, please see Integrating CI-driven scans.

The legacy integration process involves adding build steps that will automatically trigger a scan, which can optionally be linked to one of your existing sites in Burp Suite DAST. This means you can work with the scan results and analyze the generated data in the web UI, just like you can with scans that you create manually. Scans can also be configured to generate HTML reports, which you can use to share the results across your organization, even with people who do not have access to Burp Suite DAST.

Integration types

Regardless of which CI/CD platform you use, you have two options for integrating Burp Suite DAST scans. You can either configure a site-driven scan or use the legacy "Burp scan" option. You select your preferred option when adding the associated build steps to your pipeline. Which one you choose affects the rest of the process, so it is important to understand the differences and decide which approach is right for you.

Read more

Integration types for CI/CD (legacy)

Detailed instructions

The exact steps required for the integration differ slightly depending on your preferred CI/CD platform. However, all the different options require you to create an API user in Burp Suite DAST first. Please refer to the relevant sections below for detailed instructions on how to perform the integration process.

In this section

Creating an API user

Integrating with Jenkins

Integrating with TeamCity

Integrating with other CI/CD platforms

Optional settings
