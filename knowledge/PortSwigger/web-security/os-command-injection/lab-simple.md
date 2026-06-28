# Lab: OS command injection, simple case

Source: https://portswigger.net/web-security/os-command-injection/lab-simple
Fetched: 2026-06-28T09:17:57.825772+00:00

Web Security Academy

OS command injection

Lab

Lab: OS command injection, simple case

This lab contains an OS command injection vulnerability in the product stock checker.

The application executes a shell command containing user-supplied product and store IDs, and returns the raw output from the command in its response.

To solve the lab, execute the whoami command to determine the name of the current user.

Solution

Use Burp Suite to intercept and modify a request that checks the stock level.

Modify the storeID parameter, giving it the value 1|whoami.

Observe that the response contains the name of the current user.

Community solutions

Rana Khalil

z3nsh3ll

Michael Sommer

Find OS command injection vulnerabilities using Burp Suite

Try for free
