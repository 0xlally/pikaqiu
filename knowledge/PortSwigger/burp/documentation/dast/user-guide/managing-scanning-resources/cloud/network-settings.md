# Network and firewall settings for self-hosted scanning machines

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-scanning-resources/cloud/network-settings
Fetched: 2026-06-28T09:15:37.186279+00:00

DAST

Network and firewall settings for self-hosted scanning machines

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

You need to configure your network and firewall to allow your self-hosted scanning machines to communicate with your Cloud instance of Burp Suite DAST:

Allow your scanning machines to have outbound access to the Dashboard IPs listed on the PortSwigger IP ranges page.

Enable outbound access from the scanning machine to *.oastify.com on port 443

Note

These instructions only apply to Cloud instances of Burp Suite DAST. If you're looking for network and firewall settings for a self-hosted instance of Burp Suite DAST, see:

Configuring your environment network and firewall settings - Standard

Configuring your environment network and firewall settings - Kubernetes

Related pages

System requirements

Setting up a self-hosted scanning machine for a Cloud instance
