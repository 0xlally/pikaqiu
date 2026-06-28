# Example configuration file

Source: https://portswigger.net/burp/documentation/collaborator/server/private/example
Fetched: 2026-06-28T09:15:31.326650+00:00

Support Center

Documentation

Burp Collaborator

Server

Deploying a private server

Example configuration file

DASTProfessional

Example configuration file

Last updated:

June 18, 2026

Read time:

5 Minutes

When you set up a private Collaborator server, you need to write a configuration file. You can refer to this example configuration file for guidance. This page also contains information on the different fields used in the configuration file.

The file uses a JSON format, with support for comments. Where IP addresses are required, you can configure a single address or list of addresses.

Related pages

For more information on the setup process, see Deploying a private Collaborator server.

For more information on how to configure options for your private server, see Configuring your

private

Collaborator server.

This example file configures:

Certificates that have been signed by a certificate authority.

Custom ports for polling.

Custom DNS records for CA signing challenges. See the customDnsRecord section. Restart the Collaborator server for any custom DNS records to take effect.

{

"serverDomain": "burpcollaborator.example.com",

"workerThreads": 10,

"interactionLimits": {

"http": 8192,

"smtp": 8192

},

"eventCapture": {

"localAddress": ["10.20.0.159", "127.0.0.1"],

"publicAddress": "10.20.0.159",

"http": {

"ports": 80

},

"https": {

"ports": 443

},

"smtp": {

"ports": [25, 587]

},

"smtps": {

"ports": 465

},

"ssl": {

"certificateFiles" : [

"keys/burpcollaborator.example.com.key.pkcs8",

"keys/burpcollaborator.example.com.crt",

"keys/intermediate.crt" ]

}

},

"polling": {

"localAddress": "127.0.0.1",

"publicAddress": "10.20.0.159",

"http": {

"port": 9090

},

"https": {

"port": 9443

},

"ssl": {

"certificateFiles": [

"keys/burpcollaborator.example.com.key.pkcs8",

"keys/burpcollaborator.example.com.crt",

"keys/intermediate.crt" ]

}

},

"metrics": {

"path": "jnaicmez8",

"addressWhitelist": ["10.10.23.0/24"]

},

"dns": {

"interfaces": [{

"name": "ns1",

"localAddress": "10.20.0.159",

"publicAddress": "98.87.76.55"

}, {

"name": "ns2",

"localAddress": "10.20.0.159",

"publicAddress": "98.87.11.00"

}],

"ports": 53

},

"logLevel": "INFO",

"customDnsRecords" : [

{

"label" : "_acme-challenge",

"type" : "TXT",

"record" : "jsd3Ew2nign7svGT",

"ttl" : 60

}

],

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

}

Configuration file fields

The following fields are used in the example configuration file:

Field

Meaning

serverDomain

The domain or subdomain that the Collaborator server controls DNS for. This is required for DNS functionality.

workerThreads

The number of threads used by the Collaborator server to process incoming requests. The default is 5.

eventCapture.localAddress

Specify the interfaces that Collaborator listens on. Otherwise, the Collaborator listens on all local interfaces for capturing interaction events.

eventCapture.publicAddress

The public IP address for capturing interaction events.

eventCapture.http.ports

The ports for listening for HTTP interaction events. You can specify multiple ports. The default is 80. Only change this if port 80 is being forwarded and port mappings are configured.

eventCapture.https.ports

The ports for listening for HTTPS interaction events. You can specify multiple ports. The default is 443. Only change this if port 443 is being forwarded.

eventCapture.smtp.ports

The ports for listening for SMTP interaction events. The defaults are 25 and 587. Only change these if they are being forwarded.

eventCapture.smtps.ports

The ports for listening for SMTPS interaction events. You can specify multiple ports. The default is 465. Only change this if port 465 is being forwarded.

eventCapture.ssl.certificateFiles

Specify certificate files to load.

polling.localAddress

The interface for polling requests. If you don't specify this, the Collaborator server uses the same network interface to capture interaction events and serve polling requests. You can choose to specify a separate polling interface.

polling.publicAddress

The public address used to serve polling requests.

polling.http.port

The port used for polling over HTTP.

polling.https.port

The port used for polling over HTTPS.

polling.ssl.certificateFiles

Specify certificate files to load.

metrics.path

The URL path from which the metrics page can be accessed. If this isn't specified, there is no metrics endpoint. You won't collect any metrics, but the Collaborator server functions as usual.

metrics.addressWhitelist

The client IP addresses that are allowed to access the metrics page. If no addresses are specified, you won't be able to access the metrics.

If a custom port is used for the polling interface this is also used in the URL for the metrics page. For example

https://burpcollaborator.example.com:9443/jnaicmez8/metrics

dns.interfaces

A list of local interfaces that listen for DNS queries. If your registrar requires that you

configure a different IP address for each authoritative name server, you can use multiple

network interfaces and configure their locations.

dns.interfaces.name

The hostname to use for the name server running on this interface. Use a different hostname for each name server.

Do not use the fully qualified domain name. This is generated automatically, by appending the value of

serverDomain to this value.

dns.interfaces.localAddress

The local address to bind to for this name server.

dns.interfaces.publicAddress

The public IP address that corresponds to the configured local address.

You typically need to use the configured hostname and public IP address in your DNS record for your domain.

dns.ports

The ports that listen for DNS queries. The default is port 53. Only change this if port 53 is being forwarded.

logLevel

The level of logging sent to standard output. The default is INFO.

customDnsRecords.label

The DNS label for the custom content.

customDnsRecords.record

The custom DNS record for the corresponding label.

customDnsRecords.type

The type of custom DNS record. You can choose TXT or CNAME.

customDnsRecords.ttl

The time to live for the record in seconds.

customHttpContent.path

The path for the custom HTTP content. You can set multiple paths.

customHttpContent.contentType

The MIME type to add to the response header for the custom content.

customHttpContent.base64content

The BASE64 encoded content is decoded for use on the HTML page.

Alternative configuration fields:

These fields aren't included in the example configuration file, but can be used in your configuration:

Field

Meaning and example

interactionLimits.http

The maximum number of bytes that are stored for each incoming HTTP interaction message. The default is 10000000.

"http" : 8192

interactionLimits.smtp

The maximum number of bytes that are stored for each incoming SMTP interaction message. There is no limit by default.

"smtp" : 8192

eventCapture.https.hostname

Generate a self-signed certificate. This is not necessary if you have a CA-signed certificate. See

Configure TLS certificates for more details.

"hostname" : "burpcollaborator.example.com"

This creates a self-signed wildcard certificate for:

*.burpcollaborator.example.com

eventCapture.ssl.keystore.path

Import a certificate into the Java keystore of the server. Use this if the certificate signing request was generated using Java keytool.

"ssl": {

"keystore": {

"path": "myKeystore.jks",

"password": "myPassword"

}

eventCapture.ssl.keystore.password

The password for the Java keystore.

eventCapture.canonicalName

The CNAME record for interaction events. Specify this as the fully qualified domain name.

"canonicalName": "<FQDN>"

polling.https.hostname

Generate a self-signed certificate. This is not necessary if you have a CA-signed certificate. See Configure TLS certificates for more details.

"hostname" : "polling"

eventCapture.ssl.keystore.path

Import a certificate into the Java keystore of the server. Use this if the certificate signing request was generated using Java keytool.

"ssl": {

"keystore": {

"path": "myKeystore.jks",

"password": "myPassword"

}

eventCapture.ssl.keystore.password

The password for the Java keystore.
