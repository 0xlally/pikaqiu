# Configuring your network and firewall settings (Standard)

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/standard/network-firewall-config
Fetched: 2026-06-28T09:15:33.457084+00:00

DAST

Configuring your network and firewall settings (Standard)

Last updated:

June 18, 2026

Read time:

2 Minutes

To ensure that Burp Suite DAST is able to function correctly, you may need to configure your firewall to allow the various components to communicate with each other and the public web. We support IPv4 and IPv6.

Warning

For security reasons, make sure that your scanning machines can only reach systems that you intend to scan. Failure to do so may result in unintended user access to internal functionality.

Configuring a single-machine architecture

If you want to run Burp Suite DAST on a single machine, you need to make sure that the following connections are allowed:

Allow your users and API clients to access the web server. By default, they should use port 8080 or port 8443, but you can choose a different port during the installation process.

To activate your license and enable automatic software updates, allow the DAST server to access portswigger.net on port 443.

If necessary, configure a network proxy to reach the public web.

To allow email notifications, give the DAST server access to your SMTP server. To find the correct port number for your email service, refer to your email service provider.

Allow the machine to access websites that you want to scan on the relevant ports, via a proxy server if necessary.

To gain the full benefit of Burp Collaborator's out-of-band vulnerability detection technology, allow the machine to access

*.burpcollaborator.net and *.oastify.com on ports 80 and 443.

In addition, the target application must be able to access *.burpcollaborator.net and *.oastify.com on ports 80 and 443.

Configuring a multi-system architecture

Configure the connections as follows:

Allow your users and API clients to access the web server. By default, they should use port 8080 or port 8443, but you can choose a different port during the installation process.

To activate your license and perform automatic software updates, allow the DAST server to access portswigger.net on port 443.

If necessary, configure a network proxy to reach the public web.

Allow your scanning machines to access the DAST server machine on port 8072.

Allow the DAST server to access portswigger.net throughout the scanning machine installation process. This is necessary to activate the scanning machine license.

Allow your scanning machines to access the websites that you want to scan on the relevant ports.

If you use the embedded database, allow any external scanning machines to access the DAST server machine on port 9092.

If you use an external database, allow the DAST server and any external scanning machines to have access to the database service on the configured host and port.

Note

We recommend that you create a dedicated DMZ network to host the machines that Burp Suite DAST is deployed on. However, this isn't mandatory.

Next step - System requirements for standard instances

CONTINUE
