# Kubernetes scanning resources overview

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/kubernetes/resource-overview
Fetched: 2026-06-28T09:15:32.985702+00:00

DAST

Kubernetes scanning resources overview

Last updated:

June 18, 2026

Read time:

2 Minutes

If you deploy Burp Suite DAST to Kubernetes, all of your scans run on a single, scalable pool of resources.

Note

In this documentation, the term "auto-scaling" refers to both:

Burp Suite DAST automatically creating and deleting resources to handle scan jobs.

The Kubernetes cluster automatically increasing and decreasing the number of nodes as demand changes.

You need to use both types of auto-scaling to obtain the full benefits of a Kubernetes instance.

This section does not cover configuring the Kubernetes cluster to automatically scale its own computing resource. For information on how to configure compute power auto-scaling, check your cloud provider's documentation.

How does scanning work on Kubernetes?

When running on Kubernetes, Burp Suite DAST automatically creates enough scan resources to cope with the number of concurrent scans that you need to run at any given time. These resources are scaled back down once they are no longer needed.

Auto-scaling means you can always run as many concurrent scans as your license covers. It also helps to reduce maintenance and cloud infrastructure costs because you do not need to maintain physical or virtual machines to run your scans and you only need to pay for the scan resources that you are using at any given time.

Note

Kubernetes instances support auto-scaling scanning resources only. You cannot run a fixed scanning machine setup on Kubernetes.

Configuring scanning resources

To manage scanning resources:

From the settings menu select Scanning resources.

Under Kubernetes scan containers, click View scans in progress.

From here, you can:

Set a limit on the number of concurrent scans you want to run. This is separate from the number of concurrent scans that your license potentially allows.

View any active scans.

Suspend scanning altogether.

Related pages

Deploying Burp Suite DAST to Kubernetes.

Managing Kubernetes scanning resources.

Next step - Support scope

CONTINUE
