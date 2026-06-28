# Lab: Broken brute-force protection, multiple credentials per request

Source: https://portswigger.net/web-security/authentication/password-based/lab-broken-brute-force-protection-multiple-credentials-per-request
Fetched: 2026-06-28T09:17:41.284377+00:00

Web Security Academy

Authentication vulnerabilities

Password-based

Lab

Lab: Broken brute-force protection, multiple credentials per request

This lab is vulnerable due to a logic flaw in its brute-force protection. To solve the lab, brute-force Carlos's password, then access his account page.

Victim's username: carlos

Candidate passwords

Solution

With Burp running, investigate the login page. Notice that the POST /login request submits the login credentials in JSON format. Send this request to Burp Repeater.

In Burp Repeater, replace the single string value of the password with an array of strings containing all of the candidate passwords. For example:

"username" : "carlos",

"password" : [

"123456",

"password",

"qwerty"

...

]

Send the request. This will return a 302 response.

Right-click on this request and select Show response in browser. Copy the URL and load it in the browser. The page loads and you are logged in as carlos.

Click My account to access Carlos's account page and solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find vulnerabilities in your authentication using Burp Suite

Try for free
