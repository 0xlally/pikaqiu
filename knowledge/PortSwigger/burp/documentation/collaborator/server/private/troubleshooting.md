# Troubleshooting

Source: https://portswigger.net/burp/documentation/collaborator/server/private/troubleshooting
Fetched: 2026-06-28T09:15:31.609422+00:00

Support Center

Documentation

Burp Collaborator

Server

Deploying a private server

Troubleshooting

DASTProfessional

Troubleshooting

Last updated:

June 18, 2026

Read time:

1 Minute

If you have problems with your Collaborator server, try the following:

Professional Run the Collaborator health check.

Check that your server domain resolves to your Collaborator server's IP address.

Collaborator health check

To access the Collaborator health check in Burp Suite Professional, go to the Collaborator page in the Settings dialog, and click Run health check.

Related pages

Burp Collaborator settings.

Server domain resolution

The health check may fail if the server domain doesn't resolve to your Collaborator server IP address. The following process can help you troubleshoot this:

Check that the NS record for your domain resolves to the expected name servers. For example:

dig burpcollaborator.example.com NS +noall +answer +short

ns1.burpcollaborator.example.com

Check that the above entry has a corresponding A/AAAA record that resolves to the Collaborator's IP addresses. For example:

dig ns1.burpcollaborator.example.com A +noall +answer +short

192.168.0.1

Check that the public IP address returns when you resolve a subdomain of the Collaborator server. For example:

dig randomsubdomain.burpcollaborator.example.com A +noall +answer +short

ns1.burpcollaborator.example.com

192.168.0.1

Check the Collaborator's logs and configuration.

Check that your DNS port is open for UDP traffic. This is port 53, unless you changed the default ports. For more information, see

Setting up the ports and firewall.
