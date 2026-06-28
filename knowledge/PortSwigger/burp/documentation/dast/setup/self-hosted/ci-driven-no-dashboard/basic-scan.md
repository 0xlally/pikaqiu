# Running a basic CI-driven scan with no dashboard

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/ci-driven-no-dashboard/basic-scan
Fetched: 2026-06-28T09:15:31.927271+00:00

DAST

Running a basic CI-driven scan with no dashboard

Last updated:

June 18, 2026

Read time:

3 Minutes

You can integrate a scan with any CI/CD platform that supports Docker containers. This enables you to use Burp Scanner to run scans as a stage in your existing CI/CD pipeline. You don't need to set up Burp Suite DAST.

If you don't need to use the features of Burp Suite DAST's dashboard, you can use this guide to quickly integrate a scan with your CI/CD platform. These instructions enable you to run a scan with the default scan configuration against a single URL, using a shell script.

Before you start

Before you start:

Log in to your user account.

To set up a scan for the first time, you need to switch your license to an API key:

Under Subscriptions > Actions, click Manage Subscription and select Switch to API key.

At the prompt, click Proceed.

Under Licenses > Downloads, click View access details.

Copy the URL and API Key.

System requirements

Make sure you meet the system requirements, in order to run scans successfully:

We recommend that you run a scan on a machine that has a minimum of 4 CPU cores and 8 GB of RAM. We also recommend that you have 30 GB of free disk space. While this should be suitable for most use cases, larger or more complex target applications may require more resources.

Your CI/CD build agent or node must be configured to run Docker containers.

The container must be able to access the DAST server URL that was supplied with your license. For more information, see your account page.

The CI/CD build agent or node where the container is running must be able to access PortSwigger's public image repository public.ecr.aws/portswigger/ as well as the target application you want to scan.

Running a scan

To run a scan, include the following docker run command in your pipeline script:

docker run --rm --pull=always \

-u $(id -u) -v $(pwd):$(pwd) -w $(pwd) \

-e BURP_ENTERPRISE_SERVER_URL=https://ent-server.com \

-e BURP_ENTERPRISE_API_KEY=XXXXxxxxXXXXxxxx \

-e BURP_START_URL=https://ginandjuice.shop \

public.ecr.aws/portswigger/enterprise-scan-container:latest

You need to input the correct values for the environment variables in the command:

BURP_ENTERPRISE_SERVER_URL: This is the URL of your DAST server. It's displayed under View access details in your PortSwigger account.

BURP_ENTERPRISE_API_KEY: This is the API key that you copied when you created an API user. It's displayed under View access details in your PortSwigger account.

BURP_START_URL: This is the URL of the website you want Burp Scanner to scan.

Scan results

The results from Burp Scanner are available as a JUnit or Burp XML file when a scan is complete. The file is saved in the working directory for your scan.

Remediation advice

The results from Burp Scanner include remediation advice for any security issues they find. This advice includes links to relevant sections of the free Web Security Academy resource, which provide further detail on web security vulnerabilities.

Evidence

The results from Burp Scanner include evidence for any security issues found. This evidence includes the request sent by Burp Scanner to produce the issue, as well as the response sent by the application.

Configuring CI-driven scans

To use more advanced features, such as custom scan configurations or application logins with CI-driven scans, you need to create a configuration file.

More information

Generic configuration instructions, for all platforms

CI-driven scan integration examples

To help you integrate and configure CI-driven scans with some of the most popular CI platforms, we've created some platform-specific integration guides.

More information

CI-driven scan integration examples

Next step - Configuring scans

CONTINUE
