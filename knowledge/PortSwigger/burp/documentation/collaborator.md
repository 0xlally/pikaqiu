# Burp Collaborator

Source: https://portswigger.net/burp/documentation/collaborator
Fetched: 2026-06-28T09:15:31.094472+00:00

Support Center

Documentation

Burp Collaborator

DASTProfessional

Burp Collaborator

Last updated:

June 18, 2026

Read time:

1 Minute

Burp Collaborator is a network service that enables you to detect invisible vulnerabilities. These are vulnerabilities that don't:

Trigger error messages.

Cause differences in application output.

Cause detectable time delays.

Burp Collaborator uses its own server to identify invisible vulnerabilities, as part of Out-of-band Application Security Testing (OAST). The general process is as follows:

Burp sends Collaborator payloads in a request to the target application. These are subdomains of the Collaborator server's domain. When certain vulnerabilities occur, the target application may use the injected payload to interact with the Collaborator server.

Burp polls the server, to see whether interactions have occurred.

Burp Collaborator is used in both Burp Suite Professional and Burp Suite DAST:

Burp Scanner automates the Collaborator process as part of various scan checks. Scanner reports on issues identified in this process.

Some extensions and custom scan checks use automated Collaborator functionality.

In Burp Suite Professional, you can use Burp Collaborator to manually test for vulnerabilities.

Related pages

Typical uses for Burp Collaborator.

Burp Collaborator server.

Deploying a private Burp Collaborator server.

Using Collaborator in checks.
