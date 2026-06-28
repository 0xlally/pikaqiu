# Configuring an HTTP proxy server

Source: https://portswigger.net/burp/documentation/dast/user-guide/post-installation-config/configure-http-proxy-server
Fetched: 2026-06-28T09:15:38.944215+00:00

DAST

Configuring an HTTP proxy server

Last updated:

June 18, 2026

Read time:

2 Minutes

Self-hosted

If your organization does not allow you to connect to the public internet directly, you can configure a network proxy that the DAST server can use to reach external domains, such as portswigger.net.

To activate your license and perform automatic software updates, the DAST server needs access to portswigger.net on port 443. For the best experience give the server permanent access, rather than just for the initial installation.

From the settings menu , select Network.

Scroll down to HTTP proxy server and select Use an HTTP proxy server.

Enter the Host and Port for your proxy server.

If your proxy server requires a login:

Select Authenticated.

Enter a valid username and password.

To use the proxy server for connecting to an SMTP server, select Use proxy to connect to email server.

To bypass the proxy for specific hosts, enter them in No proxy for. Click the icon to add additional entries. This is useful for internal hosts that are not reachable through your proxy.

You can add the following types of entry:

An exact hostname, for example internal.example.com.

A wildcard that matches all subdomains of a domain, for example *.example.com. This matches subdomains such as api.example.com and a.b.example.com, but not example.com. You can only use the * wildcard at the start of an entry, immediately followed by a dot.

An IP address, for example 192.168.0.10 or 2001:db8::1. Wildcards and CIDR ranges are not supported for IP addresses.

Note

You can only use an unauthenticated proxy to connect to an SMTP server. For more information, see configure a connection to your SMTP server.

Related pages

Planning to deploy Burp Suite DAST
