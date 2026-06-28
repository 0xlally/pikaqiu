# Lab: Blind OS command injection with time delays

Source: https://portswigger.net/web-security/os-command-injection/lab-blind-time-delays
Fetched: 2026-06-28T09:17:57.751424+00:00

Web Security Academy

OS command injection

Lab

Lab: Blind OS command injection with time delays

This lab contains a blind OS command injection vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response.

To solve the lab, exploit the blind OS command injection vulnerability to cause a 10 second delay.

Solution

Use Burp Suite to intercept and modify the request that submits feedback.

Modify the email parameter, changing it to:

email=x||ping+-c+10+127.0.0.1||

Observe that the response takes 10 seconds to return.

Community solutions

Rana Khalil

Michael Sommer

Find OS command injection vulnerabilities using Burp Suite

Try for free
