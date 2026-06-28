# Managing scanning resources for a self-hosted instance

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-scanning-resources/self-hosted
Fetched: 2026-06-28T09:15:37.472086+00:00

DAST

Managing scanning resources for a self-hosted instance

Last updated:

June 18, 2026

Read time:

2 Minutes

Self-hosted

This section explains how to manage your scanning resources if you have a self-hosted instance of Burp Suite DAST. It includes information for standard instances, and Kubernetes instances.

Standard instances

Standard instances of Burp Suite DAST use either or both of the following resources:

Scanning machines. These are dedicated physical or virtual machines that run scans. You can deploy as many scanning machines as you choose, and organize them into scanning pools for ease of management.

CI-driven scans. You can run scans in your CI/CD pipeline, from temporary scanning resources that are created in a Docker container on a CI/CD agent node.

Scanning machines

What is a scanning machine?

Deploying additional scanning machines

Managing scanning pools

Assigning scan limits

Note

You can also deploy all of Burp Suite DAST's components on a single machine, meaning that scans run on the same machine as the DAST server. While this is suitable for evaluation purposes, we do not recommend this setup in most production environments. For more information, see Single vs multi-machine architecture.

Kubernetes instances

Self-hosted

Kubernetes instances of Burp Suite DAST can use either or both of the following scanning resources:

Auto-scaling scanning resources. Rather than requiring you to configure individual scanning machines, Kubernetes instances run scans using an auto-scaling resource pool. Burp Suite DAST automatically creates scanning resources to cope with the number of concurrent scans that you need to run at any given time. The resources scale back down once they are no longer needed.

CI-driven scans. You can run scans in your CI/CD pipeline, from temporary scanning resources that are created in a Docker container on a CI/CD agent node.

Related pages

Deploying additional scanning machines

Scanning pools for self-hosted instances of Burp Suite DAST

Assigning scan limits

Managing Kubernetes scanning resources

Integrating CI-driven scans
