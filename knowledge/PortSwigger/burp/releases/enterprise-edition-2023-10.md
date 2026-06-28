# Enterprise Edition 2023.10

Source: https://portswigger.net/burp/releases/enterprise-edition-2023-10
Fetched: 2026-06-28T09:16:18.454006+00:00

This release introduces new configuration options for CI-driven scans, including the ability to specify upstream proxies and specify platform authentication information. We have also made some changes to the Kubernetes Helm chart and fixed some minor bugs.

New configuration options for CI-driven scans

We have added some new features to the YAML file used to configure CI-driven scans and CI-driven scans with no dashboard. You can now specify the following details in the file:

A list of additional request headers and cookies.

Platform authentication information.

Details of any proxy servers between the CI-driven scan container and the Burp Suite Enterprise Edition server.

Details of any proxy servers between the CI-driven scan container and the scan target.

User action auditing

We have added CI-driven scan activity to Burp Suite Enterprise Edition's user action auditing. When a CI-driven scan is started or cancelled, the system now records the user that performed that action.

Public Helm chart GitHub repository

You can now obtain the Burp Suite Enterprise Edition Kubernetes Helm chart from our Helm chart GitHub repository.

You can still download the chart directly if required.

Kubernetes secure private registry support

You can now pull container images from a secure private registry when deploying Burp Suite Enterprise Edition to Kubernetes.

Although the Helm chart already has an optional parameter enabling you to override the container registry from which the Burp Suite Enterprise Edition images are pulled, it did not previously enable you to to connect to container registries that require authentication. You can now connect to a secure registry by specifying it in the imagePullSecrets value of the values.yaml file.

Burp Scanner upgrade

This release also upgrades Burp Scanner to version 2023.10.2.5, which provides the following improvements:

Reduces the time it takes to wait for a page to stabilize, which has decreased the overall load time of pages.

Improves handling of self-closing popups while scanning using a recorder login sequence.

When a scan finishes, Burp Scanner now polls the Collaborator server for new interactions every minute for the first 10 minutes. After this, it reverts to the default interval of once every 10 minutes. This means you no longer have to wait as long for Burp Scanner to report out-of-band interactions that are triggered almost instantly.

Upgrades the browser used for scanning to Chromium 119.0.6045.123 for Mac and Linux and 119.0.6045.123/.124 for Windows. For more information, see the Chromium release notes.

Fixes a bug whereby the crawler would stop enumerating potential GraphQL endpoints for some responses.

Fixes a bug that interfered with scanning of GraphQL introspection requests.

Bug fixes

We have also fixed the following bugs:

An issue with adding roles to SCIM groups in which errors were being reported on a hidden tab.

An issue whereby scan and connection check logs were not being cleaned up after 10 days as expected on Kubernetes deployments.

An issue whereby custom scan configurations were correctly saved but not displayed as such in the UI.

An issue with permissions whereby users with any restrictions on creating sites were not able to import sites using a CSV file. These users can now import sites into any folders they have permissions to create sites in.

An issue with permissions whereby users with any restrictions on creating sites were not able to create folders. These users can now create subfolders of any folder they have access to.

An issue whereby editing a site was causing it to revert to the default scanning pool, irrespective of any other scanning pools selected.
