# Lab: SQL injection vulnerability allowing login bypass

Source: https://portswigger.net/web-security/sql-injection/lab-login-bypass
Fetched: 2026-06-28T09:18:03.619527+00:00

Web Security Academy

SQL injection

Lab

Lab: SQL injection vulnerability allowing login bypass

This lab contains a SQL injection vulnerability in the login function.

To solve the lab, perform a SQL injection attack that logs in to the application as the administrator user.

Solution

Use Burp Suite to intercept and modify the login request.

Modify the username parameter, giving it the value: administrator'--

Community solutions

Rana Khalil

z3nsh3ll

Michael Sommer

Find SQL injection vulnerabilities using Burp Suite

Try for free
