# Testing for asynchronous OS command injection vulnerabilities with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/command-injection/asynchronous
Fetched: 2026-06-28T09:15:59.508384+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing input validation

OS command injection

Testing for asynchronous OS command injection vulnerabilities

Professional

Testing for asynchronous OS command injection vulnerabilities with Burp Suite

Last updated:

June 18, 2026

Read time:

2 Minutes

Asynchronous OS command injection vulnerabilities occur when an application is vulnerable to command injection, but the command is executed asynchronously. This means that it has no noticeable impact on the application's response.

Burp Collaborator can help you to test for asynchronous command injection vulnerabilities. You can use Burp to inject a command that triggers an out-of-band network interaction with the Burp Collaborator server. Burp monitors the Collaborator server to identify whether an out-of-band interaction occurs, and therefore whether the command was executed.

Steps

You can follow this process using the lab Blind OS command injection with out-of-band interaction.

In Proxy > HTTP history, identify a request that you want to investigate.

Right-click the request and select Send to Repeater.

Change a parameter's value to a proof-of-concept payload. The payload should use the nslookup command to cause a DNS

lookup for a Collaborator subdomain. To insert a Collaborator subdomain into the payload, right-click and select

Insert Collaborator payload.

Click Send.

Go to the Collaborator tab and click Poll now. Any interactions with the Collaborator server are listed in the table.

If an interaction occurs, this indicates that the command was successfully injected.

Repeat Steps 3 and 4 to test additional parameters that look like they may be used in shell commands.

Note

The command may be executed after a delay. The Collaborator tab flashes when an interaction occurs. Make sure that you continue to check the Collaborator tab to identify any delayed interactions.

Related pages

Academy: OS command injection

Burp Collaborator

Burp Repeater
