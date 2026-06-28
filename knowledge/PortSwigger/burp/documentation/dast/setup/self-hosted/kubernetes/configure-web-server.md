# Configuring your web server (Kubernetes)

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/kubernetes/configure-web-server
Fetched: 2026-06-28T09:15:32.655452+00:00

DAST

Configuring your web server (Kubernetes)

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

Use the Helm chart to set the web server port that the ingress will send traffic to. The external port used by the ingress may be different. The Web server URL needs to use the external port.

Enabling TLS

By default the web server is configured to use HTTPS with a temporary self-signed certificate. We recommend that you update the TLS certificate with your own.

The TLS certificate must have the following properties:

Use a PKCS#12 certificate with a .p12 file extension. The .pfx format is not supported.

The certificate must have a password.

The certificate must include a Subject Alternative Name (SAN).

To add a TLS certificate:

Use the following command to create a Kubernetes secret that contains your TLS certificate. The secret needs to contain the certificate, and the passphrase:

kubectl -n <namespace> create secret generic bsee-web-server-https --from-file=certificate=<your certificate name>.p12 --from-literal=passphrase=<your passphrase>

In the values.yaml file, set the values for services.webServer as follows:

Set useDeprecatedHttpConfigFromDatabase to false.

Set useHttps to true.

Set a value for the httpsPort (the default is 8443).

Enter the name and key for the secrets for the certificate and the passphrase. For example:

httpsCertificateSecret:

name: bsee-web-server-https

key: certificate

httpsPassphraseSecret:

name: bsee-web-server-https

key: passphrase

Restart your deployment to apply the changes.

Note

If you later decide to switch from an HTTPS to an HTTP connection, you need to set useHttps to false, and perform a Helm upgrade.

If necessary, you can configure an HTTP proxy server to allow you to connect to the public internet.

Next step - Continue learning about Burp Suite DAST

CONTINUE
