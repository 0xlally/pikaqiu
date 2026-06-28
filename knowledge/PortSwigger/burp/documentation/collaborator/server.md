# Burp Collaborator server

Source: https://portswigger.net/burp/documentation/collaborator/server
Fetched: 2026-06-28T09:15:31.209176+00:00

Support Center

Documentation

Burp Collaborator

Server

DASTProfessional

Burp Collaborator server

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Collaborator provides custom implementations of various network services on a single server. The server listens for requests that are induced by Collaborator payloads.

The server has the following functionality:

It is the authoritative DNS server for its registered domains and subdomains. It answers any DNS queries

for these domains with its own IP address.

It uses a valid wildcard TLS certificate for its domain names.

It provides an HTTP/HTTPS service.

It provides an SMTP/SMTPS service.

Private or public server

You can choose to use a private or public Collaborator server. The public server is enabled by default.

You can also configure Burp to not use a Collaborator server. With this option, none of the Collaborator capabilities are available. To do this:

Professional In Burp Suite Professional, go to the Settings dialog, under Project > Collaborator. Select

Don't use Burp Collaborator. For more information, see

Collaborator settings.

DAST In Burp Suite DAST, do this under Burp Collaborator server when you create a custom scan configuration. Select None under Collaborator type. For more information, see

Create a custom scan configuration.

Public collaborator server

You can use the server provided by PortSwigger, which is shared between all users. The server is already configured - you can simply start testing.

If the public Collaborator server suffers from a service outage or degradation, then the efficacy of Collaborator-related functionality within Burp may be impaired. For this reason, PortSwigger makes no warranty about the availability or performance of this server.

Private Collaborator server

You can choose to run your own instance of the Collaborator server. This requires you to configure the server, but gives you total ownership of your data.

This is likely to appeal to penetration testing firms and in-house security teams. It's also necessary when working on a closed network with no internet access.

For information on how to set up a private Collaborator server, see Deploying a private Burp Collaborator

server.

Related pages

Burp Collaborator data security.
