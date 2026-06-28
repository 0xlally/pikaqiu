# Testing for OS command injection vulnerabilities

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/command-injection/testing
Fetched: 2026-06-28T09:16:00.063238+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing input validation

OS command injection

Testing for command injection vulnerabilities

ProfessionalCommunity Edition

Testing for OS command injection vulnerabilities

Last updated:

June 18, 2026

Read time:

2 Minutes

OS command injection is a vulnerability that enables an attacker to execute arbitrary operating system (OS) commands on the server that is running an application. This can fully compromise the application and its data.

You can use Burp to test for OS command injection vulnerabilities:

Professional Use Burp Scanner to automatically flag potential OS command injection vulnerabilities.

Use Burp Repeater to manually test for OS command injection vulnerabilities.

Steps

You can follow this process using the lab OS command injection, simple case.

Scanning for command injection vulnerabilities

If you're using Burp Suite Professional, you can use Burp Scanner to test for command injection vulnerabilities:

Identify a request that you want to investigate.

In Proxy > HTTP history, right-click the request and select Do active scan. Burp Scanner audits the request.

Review the Issues tab on the Dashboard to identify any OS command injection issues that Burp Scanner flags.

Manually testing for command injection vulnerabilities

You can use Burp Repeater to manually test for command injection vulnerabilities. This process also enables you to closely investigate any issues that Burp Scanner has identified:

In Proxy > HTTP history, right-click the request that you want to investigate and select

Send to Repeater.

Go to the Repeater tab.

Change the parameter that you want to test to an OS command injection proof-of-concept attack. For example, you can

use the 1|whoami command. If it executes, it determines the name of the current user.

Review the response to determine whether the command has been executed.

If necessary, modify the command, then resend the request. Repeat this process until your command executes.

Repeat Steps 3 to 5 for each parameter in the request.

Related pages

Academy: OS command injection

Burp Scanner

Burp Repeater
