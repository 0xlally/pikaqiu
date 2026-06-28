# Getting started with CI-driven scans

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/ci-driven-scans/getting-started
Fetched: 2026-06-28T09:15:35.574243+00:00

DAST

Getting started with CI-driven scans

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

You can integrate CI-driven scans with any CI/CD platform that supports containers. This enables you to use Burp Scanner to run scans as a stage in your existing CI/CD pipeline.

Use this guide to quickly integrate a CI-driven scan with your chosen CI/CD platform. These instructions enable you to run a scan with the default scan configuration against a single URL, using a shell script.

Before you start

Before you start, you need to perform the following steps:

Deploy Burp Suite DAST.

Create an API user in the CI-driven scan initiator group, and save the API key. See Creating API users.

System requirements

For information on the machine specification required to run a CI-driven scan, see the System requirements for CI-driven scans.

Running a scan

To run a CI-driven scan, include the following Docker run command in your pipeline script:

docker run --rm --pull=always \

-u $(id -u) -v $(pwd):$(pwd) -w $(pwd) \

-e BURP_ENTERPRISE_SERVER_URL=https://ent-server.com \

-e BURP_ENTERPRISE_API_KEY=XXXXxxxxXXXXxxxx \

-e BURP_START_URL=https://ginandjuice.shop \

-e BURP_CORRELATION_ID=my_vulnerable_website \

public.ecr.aws/portswigger/enterprise-scan-container:latest

You need to input the correct values for the environment variables in the command:

BURP_ENTERPRISE_SERVER_URL: This is the URL of your DAST server.

BURP_ENTERPRISE_API_KEY: This is the API key that you copied when you created an API user.

BURP_START_URL: This is the URL of the website you want Burp Scanner to scan.

BURP_CORRELATION_ID: This is optional. You only need to input a correlation ID if you want to view the scan results on the Burp Suite DAST web interface. Burp Suite DAST saves the results in a new site with the same name as the correlation ID. You can use a text string up to 64 characters long.

Note

If you want to get an idea of how Burp Scanner works and how the results are displayed, you may want to scan our deliberately vulnerable website, https://vulnerable-website.com.

You can also apply custom extensions, BChecks, and BApps to CI-driven scans. For more information, see Using custom extensions, BChecks, and BApps with CI-driven scans.

Warning

For security reasons, only use custom extensions, BChecks, and BApps that you trust.

Setting the public key certificate

Self-hosted

If your DAST server uses a self-signed TLS certificate, you need to provide the full public certificate chain to the Docker container via the BURP_ENTERPRISE_SERVER_TLS_CERTIFICATE environment variable.

Make sure your certificate file contains the full public certificate chain and is accessible from the location where you run the docker run command. Then pass it in as follows:

-e BURP_ENTERPRISE_SERVER_TLS_CERTIFICATE="$(cat self-signed-cert.pem)"

Alternatively, you can include your TLS certificate with the configuration file. For more information, see Creating a configuration file for a CI-driven scan.

Scan results

The results from Burp Scanner are available as a JUnit XML file when a scan is complete. The file is saved as burp_junit_report.xml in the working directory of the container for your CI-driven scan.

Remediation advice

The results from Burp Scanner include remediation advice for any security issues they find. This advice includes links to relevant sections of the free Web Security Academy resource, which provide further detail on web security vulnerabilities.

Evidence

The results from Burp Scanner include evidence for any security issues found. This evidence includes the request sent by Burp Scanner to produce the issue, as well as the response sent by the application.

Configuring CI-driven scans

To use more advanced features, such as custom scan configurations or application logins with CI-driven scans, you need to create a configuration file.

CI-driven scan configuration files work with any CI platform that supports containers.

More information

Generic configuration instructions for all platforms

CI-driven scan integration examples

To help you integrate and configure CI-driven scans with some of the most popular CI platforms, we've created some platform-specific integration guides.

More information

CI-driven scan integration examples
