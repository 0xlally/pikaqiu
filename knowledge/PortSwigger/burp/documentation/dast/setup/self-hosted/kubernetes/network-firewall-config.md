# Configuring your environment network and firewall settings (Kubernetes)

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/kubernetes/network-firewall-config
Fetched: 2026-06-28T09:15:32.819055+00:00

DAST

Configuring your environment network and firewall settings (Kubernetes)

Last updated:

June 18, 2026

Read time:

1 Minute

To ensure that Burp Suite DAST is able to function correctly, you may need to configure your firewall to allow the various components to communicate with each other and the public web. We support IPv4 and IPv6.

Warning

For security reasons, make sure that your Kubernetes cluster can only reach systems that you intend to scan. Failure to do so may result in unintended user access to internal functionality.

Configuring your instance

Configure the connections as follows:

Allow your users and API clients to access the web server on the configured port.

Note

You can't change the web server port on a Kubernetes instance as your external port should be configured as part of your ingress solution.

To activate your license and perform automatic software updates, allow the DAST server to access portswigger.net on port 443. If necessary, configure a network proxy to reach the public web.

Allow your Kubernetes cluster to access the websites that you want to scan on the relevant ports.

Allow the Kubernetes cluster to have access to the database service on the configured host and port.

Next step - Kubernetes system requirements

CONTINUE
