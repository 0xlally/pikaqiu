# Configuring your private Collaborator server

Source: https://portswigger.net/burp/documentation/collaborator/server/private/configuring
Fetched: 2026-06-28T09:15:31.370077+00:00

Support Center

Documentation

Burp Collaborator

Server

Deploying a private server

Configuring your private server

DASTProfessional

Configuring your private Collaborator server

Last updated:

June 18, 2026

Read time:

6 Minutes

You can configure many options for your private Collaborator server in the configuration file. For example, you can use the configuration file to:

Configure TLS certificates.

Add a polling interface.

Use CNAME settings.

Truncate interaction messages.

Collect usage metrics.

Log interaction information.

Add custom HTTP content.

Add custom DNS records.

Note

The configurations that are described on this page are examples. You can adapt them to suit your needs. If you need any further details or have any questions please contact our Support team.

Configure TLS certificates

You need to use a wildcard TLS certificate for your domain name to make TLS connections to the Collaborator server.

If you don't configure a TLS certificate in the configuration file, then a self-signed certificate is automatically generated for you. This is generally sufficient in the following situations:

You can install the certificate as trusted on the target server.

The target application does not validate TLS certificates.

To configure the domain on the self-signed wildcard certificate, use the following configuration:

"ssl": {

"hostname": "burpcollaborator.example.com"

}

Configuring a valid TLS certificate

If you have purchased a valid wildcard TLS certificate for your domain, you can obtain the certificate from your Certificate Authority (CA), and install it in your Collaborator server.

Note

If you are using certificates signed by an internal CA, then you will need to make sure that Java's trust store has the right certificates.

You also need to update your configuration file to load the certificate. Two example configurations are outlined below:

OpenSSL

Use this configuration when OpenSSL generates the Certificate Signing Request and the CA provides the certificate and intermediate certificate:

"ssl": {

"certificateFiles": [

"keys/burpcollaborator.example.com.key.pkcs8",

"keys/burpcollaborator.example.com.crt",

"keys/intermediate.crt"

]

}

Make sure you specify the configuration in the correct order: private key, certificate, intermediate certificate(s). You can view this configuration in our example configuration file.

You also need to convert the keys from the SSLeay format to PKCS8. Use the following OpenSSL command:

openssl pkcs8 -topk8 -inform PEM -in keys/burpcollaborator.example.com.key -outform PEM -out keys/burpcollaborator.example.com.key.pkcs8 -nocrypt

Java keytool

Use this configuration when the Java keytool generates the Certificate Signing Request, and you import the certificate into the Java keystore of the server:

"ssl": {

"keystore": {

"path": "myKeystore.jks",

"password": "myPassword"

}

Note

You may need to prove domain ownership to obtain a valid certificate. To do this, use the custom

HTTP and

custom DNS configuration options.

Add a polling interface

By default, the Collaborator server handles both interaction events and polling requests on the same network interface:

Interaction events - When a target application initiates an interaction with the Collaborator server. For example, a DNS lookup or an HTTP request.

Polling requests - When Burp asks the Collaborator server whether any interaction events have occurred due to the Collaborator payloads.

You can configure the server to serve polling requests on a different interface. This enables you to work around firewall restrictions, or control access to the polling function at the network level.

To configure a separate polling interface, add a polling field to your configuration file. For example:

"polling": {

"publicAddress": "<External_IP>"

},

You can fully customize the polling interface, for example to configure ports or a TLS certificate. If you don't include an option, the options in the eventCapture field are used.

You can use a single TLS certificate for both the interaction and polling interfaces. To do this, repeat the ssl configuration under both eventCapture and

polling in your configuration file. The Collaborator server's DNS service directs polling requests to the correct interface.

You can view a configuration for a polling interface with customized ports in our example configuration file.

Note

Collaborator automatically prepends polling. to the server domain when it performs polling requests.

Use CNAME settings

You can configure the Collaborator server to use CNAME settings. To do this, add the following sections to the event and polling interfaces:

"eventCapture": {

"canonicalName": "<FQDN>"

},

"polling": {

"canonicalName": "<FQDN>"

}

Note

If CNAME settings are used, the CNAME record will be returned if the label in the domain matches, regardless of the DNS query type.

Truncate interaction messages

You can configure the Collaborator server to restrict the size of stored interaction messages. This reduces the load on the Collaborator server. It may be useful if you have a large team concurrently using Collaborator. Smaller teams or single testers are unlikely to find it helpful, as their load on the server is already low.

Use the following configuration to truncate SMTP and HTTP messages. The limit is set in bytes:

"interactionLimits": {

"http": 8192,

"smtp": 8192

},

You can view this configuration in our example configuration file.

Collect usage metrics

You can configure Burp Collaborator to collect usage metrics on the performance and load of the server. This enables you to check that the Collaborator machine is sufficiently powerful.

You can access metrics data via the Collaborator server's polling interface. You can control access with a shared secret URL path and a client IP address whitelist. The data does not include any information about specific interaction events or polling requests.

The following configuration collects usage metrics on the 21.10.23.0/24 network at https://10.20.0.159/jnaicmez8/metrics:

"metrics": {

"path": "jnaicmez8",

"addressWhitelist": [

"21.10.23.0/24"

]

},

You can view this configuration in our example configuration file.

Log interaction information

You can configure Collaborator to log exceptions and other information to standard output. To do this, use the logLevel field in your configuration file. The available values are:

OFF - Nothing is logged.

ERROR - Unexpected exceptions are logged.

INFO - Information about configuration and services is logged at startup. This is the default value. You can view this configuration in our example configuration file.

DEBUG - Details of Collaborator interactions and polling are logged, including source IP address and interaction IDs. Note that this might disclose sensitive information in the log output.

Add custom HTTP content

You can define custom URLs for your Collaborator server that point to bespoke content. This enables you to, for example:

Point to an index page that identifies your organization and the purpose of the service.

Host files at arbitrary URLs. For example, in order to validate TLS certificate requests, a CA might ask you to host a file at a specific URL to prove that you own the domain. Hosting custom robots.txt and crossdomain.xml files is also supported.

To define custom URLs:

Add the array customHttpContent to the top level of the configuration file.

In the array, create an object for each URL.

For each object, specify the following properties:

path - The path from which this resource can be accessed on your Collaborator server.

contentType - The MIME type of the resource.

base64Content - The actual content that you want to host at this URL, encoded using Base64.

Note

By default, most URLs on your private Collaborator server point to a generic page that provides basic information about Burp Collaborator.

Example configuration

The following configuration sets a custom index page to the root path and adds a readme file at /info/readme.txt:

"customHttpContent": [

{

"path": "/",

"contentType": "text/html",

"base64Content": "PCFkb2N0eXBlIGh0bWw+Cgo8aHRtbCBsYW5nPSJlbiI+CjxoZWFkPgogIDxtZXRhIGNoYXJzZXQ9InV0Zi04Ij4KICA8dGl0bGU+RXhhbXBsZSBQYWdlPC90aXRsZT4KCiAgPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSJjc3MvbXlzdHlsZXNoZWV0LmNzcyI+CjwvaGVhZD4KPGJvZHk+CjxoMT5XZWxjb21lIHRvIG15IGV4YW1wbGUgcGFnZTwvaDE+CjxwPlRoYW5rcyBmb3IgdmlzaXRpbmcgbXkgZXhhbXBsZSBwYWdlLjwvcD4KPC9ib2R5Pgo8L2h0bWw+"

},

{

"path": "/info/readme.txt",

"contentType": "text/plain",

"base64Content": "VGhpcyBpcyB0aGUgcmVhZG1lIGZpbGUgZm9yIG15IGNvbGxhYm9yYXRvciBzZXJ2ZXIu"

}

]

You can view this configuration in our example configuration file.

Add custom DNS records

You can add multiple custom TXT records and a single CNAME record. This enables the Collaborator server to respond to DNS challenges as part of domain validation.

Example configuration

If you add this configuration for burpcollaborator.example.com, then TXT type queries to the name server for

_acme-challenge.burpcollaborator.example.com would receive a response of 275fe5b909adb10e41c78066e9485f7d.

The following fields are included:

label - the subdomain being queried.

record - the value that the server responds with.

type - the type of record, either TXT or CNAME.

ttl - the time for the record in seconds. It is optional.

"customDnsRecords": [

{

"label": "_acme-challenge",

"record": "275fe5b909adb10e41c78066e9485f7d",

"type": "TXT",

"ttl": 60

},

{

"label": "queried_subdomain",

"record": "reponse",

"type": "TXT"

},

{

"label": "queried_subdomain",

"record": "response",

"type": "CNAME"

}

]

You can view this configuration in our example configuration file.
