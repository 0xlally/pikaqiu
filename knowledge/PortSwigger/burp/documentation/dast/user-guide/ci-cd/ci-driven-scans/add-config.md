# Adding a configuration file to a CI-driven scan

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/ci-driven-scans/add-config
Fetched: 2026-06-28T09:15:35.008017+00:00

DAST

Adding a configuration file to a CI-driven scan

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

This section explains how to add a configuration file to the container for a CI-driven scan. The configuration file enables you to use more advanced features, such as application logins or custom scan configurations.

To learn how to create a configuration file and download a template, see Creating a configuration file for a CI-driven scan.

The instructions on this page are suitable for all platforms. For examples for specific platforms, please see:

Jenkins

TeamCity

GitHub Actions

To add a configuration file to your CI-driven scan:

Create your configuration file, see Creating a configuration file for a CI-driven scan.

Save the configuration file as burp_config.yml in the root of the working directory.

Use the following command to run a scan:

docker run --rm --pull=always \

-u $(id -u) -v $(pwd):$(pwd) -w $(pwd) \

public.ecr.aws/portswigger/enterprise-scan-container:latest

Note

The above command mounts your current directory into the scan container, and sets it as the working directory for the container.

The scan container looks for the configuration file burp_config.yml in the root of its working directory.
