# TLS settings

Source: https://portswigger.net/burp/documentation/desktop/settings/network/tls
Fetched: 2026-06-28T09:15:55.313449+00:00

Support Center

Documentation

Desktop editions

Settings

Network

TLS

ProfessionalCommunity Edition

TLS settings

Last updated:

June 18, 2026

Read time:

4 Minutes

The TLS settings enable you to configure:

TLS negotiation.

Client TLS certificates.

Server TLS certificates.

Custom CA certificates.

Java TLS settings.

TLS negotiation

These settings control the TLS protocols and ciphers that Burp uses when negotiating with upstream servers.

To enable upstream TLS verification, click Verify upstream TLS and select the protocols and ciphers that you want Burp to use. You can:

Use all of the protocols and ciphers that your Java installation supports.

Use the default protocols and ciphers for your Java installation.

Use custom protocols and ciphers. Select this option and then select the required protocols and ciphers.

Further options are available:

Allow unsafe renegotiation - This option may be necessary when using some client TLS certificates or attempting to work around other TLS problems.

Disable TLS session resume - This option controls whether Burp caches and reuses TLS connections between requests. Resuming sessions helps you to work more efficiently, but can cause problems in some situations.

Note

If you configure an upstream proxy with credentials, these credentials are transmitted before the encrypted tunnel is established.

The TLS negotiation settings are project settings. They apply to the current project only.

Client TLS certificates

These settings enable you to configure the client TLS certificates that Burp uses when requested to by a destination host. You can configure multiple certificates, and specify which hosts each certificate is used for.

When a host requests a client TLS certificate, Burp uses the first certificate in the list for that host.

To add a client TLS certificate, click Add to display the Client TLS Certificate dialog and then enter a destination host and certificate type.

Destination host

This is the name of the associated hosts. You can use wildcards: * matches zero or more characters, and ? matches any character except a dot.

To use a single certificate for all hosts, use * as the destination host.

Certificate type

Burp supports the following certificate types:

File (PKCS#12) - Certificates in this format must have a .p12 file extension. Select the location of the certificate file and the password for the certificate.

Hardware token or smartcard (PKCS#11) - Select the location of the PKCS#11 library file for your device from the menu. On Windows, Burp can automatically search common locations to find the library files that you have installed. You will also need to enter your PIN code and select the certificate from the available options. If you want to test applications that don't directly trust your intermediate certificate authority, you can also add an intermediate certificate.

You can also edit or reorder the list of rules if required.

The Client TLS certificate settings can apply at both user and project level. If you select Override options for this project only then the selected settings only apply to the current project.

Server TLS certificates

This information-only panel contains details of all X509 certificates received from web servers. Double-click an item in the list to display the certificate details.

The Server TLS certificates settings are project settings. They apply to the current project only.

Custom CA certificates

This panel enables you to configure additional certificate authorities that Burp trusts when validating upstream TLS connections. Double-click an item to view the full certificate details.

The Custom CA certificates configuration is a user setting. It applies to all Burp installations on your machine.

Java TLS settings

These settings enable TLS features that might be necessary to connect to certain servers. The following options are available:

Enable algorithms blocked by Java security policy - As of Java 7, the Java security policy can be used to block certain obsolete algorithms from being used in TLS negotiation. Some of these algorithms (MD2, for example) are blocked by default. However, many live web servers have TLS certificates that use these obsolete algorithms. It is not possible to connect to these servers using the default Java security policy. Enable this setting to allow Burp to use the obsolete algorithms when it connects to these servers. Restart Burp for any changes to this setting to take effect.

Disable Java SNI extension - As of Java 7, the TLS Server Name Indication (SNI) extension is implemented and enabled by default. Some misconfigured web servers that have SNI enabled send an "Unrecognized name" warning in the TLS handshake. While browsers ignore this warning, the Java implementation does not, resulting in a failed connection. Use this option to disable the Java SNI extension and connect to the servers. Restart Burp for any changes to this setting to take effect.

The Java TLS settings are user settings. They apply to all Burp installations on your machine.
