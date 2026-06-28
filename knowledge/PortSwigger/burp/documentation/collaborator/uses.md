# Typical uses for Burp Collaborator

Source: https://portswigger.net/burp/documentation/collaborator/uses
Fetched: 2026-06-28T09:15:31.693501+00:00

Support Center

Documentation

Burp Collaborator

Uses

DASTProfessional

Typical uses for Burp Collaborator

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Collaborator can be used to detect a wide range of out-of-band vulnerabilities. Some common use cases are described below:

External service interaction.

Out-of-band resource load.

Blind SQL injection.

Blind cross-site scripting.

External service interaction

Burp Collaborator can induce and detect a typical external service interaction as follows:

When the application receives a payload from Burp Collaborator, it performs a DNS lookup on the payload URL, then performs an HTTP request.

The Collaborator server receives the DNS lookup and HTTP request.

Burp polls the Collaborator server for payload interactions.

Burp reports the external service interaction, including the full interaction messages.

You can detect some types of service vulnerabilities by analyzing the details of the service interaction with a collaborating instance of that service. For example, mail header injection can be detected in this way.

Note

The ability to induce an external service interaction doesn't always indicate a vulnerability. You need to determine whether this is intended behavior. For more information about external service interaction vulnerabilities, see the

External service interaction issues in Vulnerabilities detected by Burp Scanner.

Out-of-band resource load

This is when an application can be induced to load content from an external source and include it in its own response.

To detect this vulnerability, the Collaborator server returns specific data in its responses to the application's interactions. Burp then analyzes the application's in-band response for the data.

Related pages

For more information, see the Out-of-band resource load issue in Vulnerabilities detected by Burp Scanner.

Blind SQL injection

This is when an application is vulnerable to SQL injection, but its HTTP responses don't contain the results of the relevant SQL query or the details of any database errors.

To detect this vulnerability, Burp sends injection-based payloads that trigger an external interaction when the injection is successful.

The following example uses an Oracle-specific API to trigger an interaction when injected into a SQL statement.

Related pages

For more information, see the Web Security Academy documentation on Blind SQL injection.

Blind cross-site scripting

The Collaborator server can notify Burp of deferred interactions that occur asynchronously when the relevant in-band payload is submitted to the target. This enables the detection of various stored vulnerabilities, such as second-order SQL injection and blind XSS.

In the example below:

Burp sends a stored XSS payload that triggers a Collaborator interaction if it is rendered to a user.

An admin user views the payload later. Their browser performs the interaction.

Burp polls the Collaborator server. Burp receives details of the interaction and reports the stored XSS vulnerability.
