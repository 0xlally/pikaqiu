# Kubernetes architecture overview

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/kubernetes/architecture-overview
Fetched: 2026-06-28T09:15:32.575205+00:00

DAST

Kubernetes architecture overview

Last updated:

June 18, 2026

Read time:

1 Minute

The following diagram shows the core components of Burp Suite DAST and the connections between them.

DAST server

The DAST server is the main application server. It coordinates between the other components.

Web server

The web server provides the interface to users either via the web UI or one of the APIs.

Database

The Kubernetes version of Burp Suite DAST requires you to connect your own external SQL database to store all the application data. For more information, see System requirements for the external database.

Scans and scanning resources

For Kubernetes instances, your scanning resources automatically scale to cope with the number of concurrent scans that you need to run at any given time. These resources are then scaled back down again once they are no longer needed.

Read more

Managing Kubernetes scanning resources

Related pages

Kubernetes system requirements

Next step - Kubernetes scanning resources overview

CONTINUE
