# Lab: Authentication bypass via flawed state machine

Source: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-authentication-bypass-via-flawed-state-machine
Fetched: 2026-06-28T09:17:55.454851+00:00

Web Security Academy

Business logic vulnerabilities

Examples

Lab

Lab: Authentication bypass via flawed state machine

This lab makes flawed assumptions about the sequence of events in the login process. To solve the lab, exploit this flaw to bypass the lab's authentication, access the admin interface, and delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

Solution

With Burp running, complete the login process and notice that you need to select your role before you are taken to the home page.

Use the content discovery tool to identify the /admin path.

Try browsing to /admin directly from the role selection page and observe that this doesn't work.

Log out and then go back to the login page. In Burp, turn on proxy intercept then log in.

Forward the POST /login request. The next request is GET /role-selector. Drop this request and then browse to the lab's home page. Observe that your role has defaulted to the administrator role and you have access to the admin panel.

Delete carlos to solve the lab.

Community solutions

Michael Sommer

Find business logic vulnerabilities using Burp Suite

Try for free
