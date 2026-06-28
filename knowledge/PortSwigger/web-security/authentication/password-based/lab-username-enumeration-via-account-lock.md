# Lab: Username enumeration via account lock

Source: https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-account-lock
Fetched: 2026-06-28T09:17:41.809770+00:00

Web Security Academy

Authentication vulnerabilities

Password-based

Lab

Lab: Username enumeration via account lock

This lab is vulnerable to username enumeration. It uses account locking, but this contains a logic flaw. To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

Candidate usernames

Candidate passwords

Solution

With Burp running, investigate the login page and submit an invalid username and password. Send the POST /login request to Burp Intruder.

Select Cluster bomb attack from the attack type drop-down menu. Add a payload position to the username parameter. Add a blank payload position to the end of the request body by clicking Add §. The result should look something like this:

username=§invalid-username§&password=example§§

In the Payloads side panel, add the list of usernames for the first payload position. For the second payload position, select the Null payloads type and choose the option to generate 5 payloads. This will effectively cause each username to be repeated 5 times. Start the attack.

In the results, notice that the responses for one of the usernames were longer than responses when using other usernames. Study the response more closely and notice that it contains a different error message: You have made too many incorrect login attempts. Make a note of this username.

Create a new Burp Intruder attack on the POST /login request, but this time select Sniper attack from the attack type drop-down menu. Set the username parameter to the username that you just identified and add a payload position to the password parameter.

Add the list of passwords to the payload set and create a grep extraction rule for the error message. Start the attack.

In the results, look at the grep extract column. Notice that there are a couple of different error messages, but one of the responses did not contain any error message. Make a note of this password.

Wait for a minute to allow the account lock to reset. Log in using the username and password that you identified and access the user account page to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find vulnerabilities in your authentication using Burp Suite

Try for free
