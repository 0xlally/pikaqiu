# Configuring your web server (Standard)

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/standard/configure-web-server
Fetched: 2026-06-28T09:15:33.495704+00:00

DAST

Configuring your web server (Standard)

Last updated:

June 18, 2026

Read time:

2 Minutes

After installation, we recommend setting up the web server URL. This is necessary to use many of the features of Burp Suite DAST. For example, the web server URL is used to generate links sent by email from the server, such as password reset emails.

To configure the web server, do the following:

From the settings menu , select Network.

Enter the Web server URL.

The first time you log in as an admin user, add your web server URL in the format https://your-web-server-IP:8443 or the fully qualified domain name of the machine on which you installed the web server.

The default port number is 8443. To use HTTPS, you also need to upload your TLS certificate.

Note

For standard instances, you can change these settings later if necessary. If you change some of the settings, you need to wait for the web server to restart. When the web server restarts, change the URL in the browser, and log in again.

You cannot change web server ports for a Kubernetes instance, as your external port should be configured as part of your ingress solution setup.

Enabling TLS

For Kubernetes instances, and standard instances with an external database, the web server is configured to use HTTPS with a temporary self-signed certificate by default. We recommend that you update the TLS certificate with your own.

The TLS certificate must have the following properties:

Use a PKCS#12 certificate with a .p12 file extension. The .pfx format is not supported.

The certificate must have a password.

The certificate must include a Subject Alternative Name (SAN).

To upload your TLS certificate:

Select the Use TLS switch.

When prompted, upload the TLS certificate.

Enter the password for the certificate file.

If you have already set the web server URL, change the scheme to HTTPS.

Note

Make sure the certificate has a .p12 file extension. The .pfx format is not supported.

If you have extra infrastructure in front of the DAST server, such as a load balancer, additional configuration may be required.

If necessary, you can configure an HTTP proxy server to allow you to connect to the public internet.

Next step - Deploying additional scanning machines

CONTINUE
