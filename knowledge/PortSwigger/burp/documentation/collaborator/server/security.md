# Burp Collaborator data security

Source: https://portswigger.net/burp/documentation/collaborator/server/security
Fetched: 2026-06-28T09:15:31.401983+00:00

Support Center

Documentation

Burp Collaborator

Server

Data security

DASTProfessional

Burp Collaborator data security

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Collaborator is designed with a strong emphasis on data security:

The Collaborator server stores minimal information about each interaction and discards interaction details after they've been retrieved.

Only the instance of Burp that generated a payload can receive its resulting interactions, due to the data retrieval process.

Data storage

In most cases, the Collaborator server simply records that an interaction was received. The interaction is given a random identifier.

The Collaborator server doesn't store:

The HTTP request sent from Burp to the target application.

Information that could identify the vulnerability.

Data that could be used to identify any individual Burp user. For example, an account name, or license key.

Note

Occasionally, the Collaborator server receives some application-specific data. For example, the contents of an email generated through a user registration form.

The Collaborator server also has the following storage precautions to protect against unauthorized access to its data:

Details of interactions are typically retrieved shortly after they occur. They are then discarded by the server.

Details of old interactions that haven't been retrieved are discarded after a fixed interval.

For the private Collaborator server, details of interactions are stored in ephemeral process memory.

For the public Collaborator server, details of interactions are encrypted, then stored in a Redis database. A user

secret and a master secret are required to decrypt this data.

There is no function for an administrator to view interaction details.

Data retrieval

Only the instance of Burp that generates a given payload can retrieve the details of resulting interactions. This is implemented in the following process:

Each instance of Burp generates a random secret.

Each Collaborator payload includes a random identifier that is derived from a one-way hash (cryptographic checksum) of the secret.

Any interactions with the Collaborator server include the identifier. For example, in the subdomain of a DNS lookup, or the Host header of an HTTP request.

The secret is only ever sent by Burp to the Collaborator server, to poll for details of the resulting interactions. This is done using HTTPS, unless you override this in the Collaborator settings.

When the Collaborator server receives a polling request, it performs the one-way hash of the submitted secret. It then retrieves the details of any interactions with identifiers that are derived from that hash.

Collaborator-based email addresses

If you're using the public Collaborator server, we do not recommend registering for websites using a Collaborator-based email address.

If the Collaborator server receives a single message containing identifiers from two clients, this message is available to both clients. This means that if you register on a website using an email address on the public Collaborator server, and the website places attacker-controlled data in an email to you, the attacker may be able to retrieve that email via their own client.

You can prevent this by using a private Collaborator server with a secured polling interface.
