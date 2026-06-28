# Lab: Weak isolation on dual-use endpoint

Source: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-weak-isolation-on-dual-use-endpoint
Fetched: 2026-06-28T09:17:57.217922+00:00

Web Security Academy

Business logic vulnerabilities

Examples

Lab

Lab: Weak isolation on dual-use endpoint

This lab makes a flawed assumption about the user's privilege level based on their input. As a result, you can exploit the logic of its account management features to gain access to arbitrary users' accounts. To solve the lab, access the administrator account and delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

Solution

With Burp running, log in and access your account page.

Change your password.

Study the POST /my-account/change-password request in Burp Repeater.

Notice that if you remove the current-password parameter entirely, you are able to successfully change your password without providing your current one.

Observe that the user whose password is changed is determined by the username parameter. Set username=administrator and send the request again.

Log out and notice that you can now successfully log in as the administrator using the password you just set.

Go to the admin panel and delete carlos to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find business logic vulnerabilities using Burp Suite

Try for free
