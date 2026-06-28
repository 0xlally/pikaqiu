# Support scope for Kubernetes instances

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/kubernetes/support-scope
Fetched: 2026-06-28T09:15:33.117660+00:00

DAST

Support scope for Kubernetes instances

Last updated:

June 18, 2026

Read time:

1 Minute

This page lists what we are able to support when deploying to Kubernetes.

PortSwigger Kubernetes support scope

The following is within our support scope for Kubernetes instances:

Installation and uninstallation of the Burp Suite DAST application and its components using the supplied Helm chart to a cluster meeting the documented prerequisites, as listed on the Set up a suitable Kubernetes cluster page.

Using the Helm chart (when unmodified) and values file.

Providing guidance on how best to use the parameters contained within the Helm chart, values file, and reference infrastructure template.

Supporting the application running state post-deployment.

Not supported

We are unable to support the following:

Customization of the Helm chart (except for the values file).

Customization of any reference infrastructure templates.

Kubernetes customer responsibilities

When deploying and running Burp Suite DAST on Kubernetes, it is your responsibility to do the following:

Make sure that your Kubernetes infrastructure meets the prerequisites, as listed on the Set up a suitable Kubernetes cluster page.

Make sure that your cluster is appropriately sized.

Customize the values file according to your organization's requirements.

Customize the Helm chart, if required.

Customize the CloudFormation reference infrastructure template, if required.

Manage resource requests and limits.

Next step - Configuring your environment network and firewall settings

CONTINUE
