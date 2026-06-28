# Managing CA certificates

Source: https://portswigger.net/burp/documentation/desktop/tools/proxy/manage-certificates
Fetched: 2026-06-28T09:16:06.757894+00:00

Support Center

Documentation

Desktop editions

Tools

Burp Proxy

Managing CA certificates

ProfessionalCommunity Edition

Managing CA certificates

Last updated:

June 18, 2026

Read time:

2 Minutes

Each installation of Burp generates its own CA certificate that Proxy listeners use to negotiate TLS connections. This section explains how to export, import, and create CA certificates.

Note

You only need to manage CA certificates in the following cases:

You want to use an external browser, instead of Burp's browser. For the vast majority of users, this isn't necessary.

You want to test certain types of network devices or applications.

Exporting and importing the CA certificate

You can export your installation-specific CA certificate for use in other tools or other instances of Burp, and import a certificate to use in the current instance of Burp:

From the Proxy tab, select Proxy Settings.

Go to the Proxy listeners field and click the Import / export CA certificate button.

Configure the Export or Import settings. Click Next.

Enter the file details, and keystore password if necessary. Click Next.

At the prompt, click Close.

Note

You should not disclose the private key for your certificate to any untrusted party. A malicious attacker in possession of your certificate and key may be able to intercept your browser's HTTPS traffic even when you are not using Burp.

To regenerate a CA certificate:

From the Proxy tab, select Proxy settings.

Go to the Proxy listeners field and click the Regenerate CA certificate button.

At the prompt, click Yes.

Restart Burp for the change to take effect.

Install the new certificate in your browser.

Creating a custom CA certificate

You can use OpenSSL to create a CA certificate with your own details:

Enter the following OpenSSL command to create a self-signed certificate with an unencrypted 2048-bit RSA key, which is valid for 730 days:

openssl req -x509 -days 730 -nodes -newkey rsa:2048 -outform der -keyout server.key -out ca.der

Enter the following OpenSSL command to convert the key from PEM to DER:

openssl rsa -in server.key -inform pem -out server.key.der -outform der

Enter the following OpenSSL command to convert the key to a PKCS8 that contains the key:

openssl pkcs8 -topk8 -in server.key.der -inform der -out server.key.pkcs8.der -outform der -nocrypt

Click the Import / export CA certificate button in Burp, and select Certificate and private key in DER format.

Select ca.der as the certificate file, and server.key.pkcs8.der as the key file.

Burp loads the custom CA certificate and uses it to generate per-host certificates.
