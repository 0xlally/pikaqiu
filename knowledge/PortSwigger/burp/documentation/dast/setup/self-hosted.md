# Setting up a self-hosted instance

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted
Fetched: 2026-06-28T09:15:32.245662+00:00

DAST

Setting up a self-hosted instance

Last updated:

June 18, 2026

Read time:

1 Minute

In this section, you can find detailed instructions on how to set up a self-hosted instance of Burp Suite DAST. You have several methods of deploying a self-hosted instance. We've provided a dedicated guide for each of them.

Note

If you haven't already, we recommend that you read our guide on Planning to deploy Burp Suite DAST before you start. This gives you an overview of the process to help you understand what decisions you need to make, identify any additional stakeholders that you may need to involve, and estimate the timeframe before you get started.

Standard - use a standard installer to deploy Burp Suite DAST, either to your own on-premise infrastructure or cloud-based services in AWS, Azure, Google Cloud Platform, and so on. Depending on the scale and scanning requirements of your organization, you can deploy a standard instance to a single machine or use a multi-machine architecture. For more information, see the Standard setup guide.

Kubernetes - use a Helm chart to deploy Burp Suite DAST to your Kubernetes cluster. When running on Kubernetes, Burp Suite DAST scales the amount of compute resources dedicated to scanning automatically. For more information, see the Kubernetes setup guide

CI-driven scans with no dashboard - run scans from a container in your CI/CD environment and consume the results directly in your CI/CD platform. There's no need to host or manage a Burp Suite DAST server and dashboard. For more information, see CI-driven scans with no dashboard setup guide.
