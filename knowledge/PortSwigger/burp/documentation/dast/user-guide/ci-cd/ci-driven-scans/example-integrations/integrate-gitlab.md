# Integrating a CI-driven scan with GitLab

Source: https://portswigger.net/burp/documentation/dast/user-guide/ci-cd/ci-driven-scans/example-integrations/integrate-gitlab
Fetched: 2026-06-28T09:15:35.392009+00:00

DAST

Integrating a CI-driven scan with GitLab

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

This page contains instructions to integrate a CI-driven scan with GitLab. This enables you to use Burp Scanner to run scans as a stage in your existing CI/CD pipeline, and fail builds if issue thresholds are met.

You configure the scan by defining a set of simple parameters in a YAML file. To learn how to do this, see Creating a configuration file for a CI-driven scan.

These instructions have been tested with GitLab version 17.1.

Before you start

You need to complete the following steps before you start:

Deploy Burp Suite DAST. See Setting up Burp Suite DAST.

Create an API user in the CI-driven scan initiator group, and save the API key. See Creating API users.

Save the YAML configuration file for your CI-driven scan. See Creating a configuration file for a CI-driven scan.

GitLab agent requirements

To integrate a CI-driven scan with GitLab, your GitLab agent must have Docker installed.

You do not need to install any plugins other than the GitLab defaults.

For information on the machine specification required to run a CI-driven scan, see System requirements for CI-driven scans.

Configuring the GitLab pipeline

Navigate to your project in GitLab.

Select Code > Repository.

Above the file list, use the drop-down to select the branch you want to commit to.

In the drop-down to the right of this, select the file you want to use. If you don't already have a script in the branch, choose New file.

(Optional) Creating a starter pipeline YAML file

If you don't already have a YAML configuration file, you can use the following example script.

The script uses pipeline secrets for the Enterprise URL and API key:

pipeline:

image: docker:latest

stage: test

services:

- docker:dind

script:

- docker run --rm

-u $(id -u) -v $(pwd):$(pwd):rw -w $(pwd)

-e BURP_CONFIG_FILE_PATH=$(pwd)/burp-config.yml

-e BURP_REPORT_FILE_PATH=$(pwd)/burp_junit_report.xml

-e BURP_ENTERPRISE_API_KEY=$BURP_ENTERPRISE_API_KEY

-e BURP_ENTERPRISE_SERVER_URL=$BURP_ENTERPRISE_SERVER_URL

public.ecr.aws/portswigger/enterprise-scan-container:latest

artifacts:

when: always

paths:

- burp_junit_report.xml

reports:

junit: burp_junit_report.xml

To learn more about creating and editing the configuration file, see Creating a configuration file for a CI-driven scan.

Running the GitLab pipeline

To run the GitLab pipeline:

In your project dashboard, select Build > Pipelines.

Select Run pipeline.

In the Run for branch name or tag field, select the branch or tag to run the pipeline for.

Enter any CI/CD variables required for the pipeline to run. You can set specific variables to have their values prefilled in the form.

Select Run pipeline.

The pipeline now runs the jobs according to its configuration.

Viewing scan results in GitLab

When your scan has completed, you can view the results of your scan:

In your project dashboard, select Build > Pipelines.

Select a pipeline to open its details page.

Select the Tests tab.

Remediation advice and evidence

Click View details in the Tests tab of the report to find remediation advice and evidence for security issues identified by Burp Scanner. This section includes:

Links to relevant parts of the Web Security Academy, providing further details about web security vulnerabilities.

Requests sent by Burp Scanner to produce the issue, as well as the response sent by the application.
