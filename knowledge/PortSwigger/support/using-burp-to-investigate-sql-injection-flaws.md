# Using Burp to Investigate SQL Injection Flaws

Source: https://portswigger.net/support/using-burp-to-investigate-sql-injection-flaws
Fetched: 2026-06-28T09:17:36.380596+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Investigate SQL Injection Flaws

When you have detected a potential SQL injection vulnerability you may wish to investigate further.

In this example we will demonstrate how to investigate SQL injection flaws using Burp Suite. This tutorial uses an exercise from the "WebGoat" training tool taken from OWASP's Broken Web Application Project. Find out how to download, install and use this project.

Ensure the Proxy "Intercept" is on.

Now send a request to the server, in this example by clicking the "Go" button.

The request will be captured in the Proxy "Intercept" tab.

Right click anywhere on the request to bring up the context menu and click "Send to Repeater".

Note: You can also send requests to the Repeater via the context menu in any location where HTTP requests are shown, such as the site map or Proxy history.

Go to the "Repeater" tab.

Here we can input various payloads in to the input field of a web application.

We can test various inputs by editing the values of appropriate parameters in the "Raw" or "Params" tabs.

In this example we are attempting to reveal the credit card details held by the application.

Smith' OR '1' = '1 is an attempt to alter the query logic and reveal all the user information held in the table.

The response can be viewed in the "Response" panel of the Repeater tool.

Responses that warrant further investigation or confirmation can be viewed in your browser.

Click "Show response in browser".

Paste the URL in to the browser to view the response there.

In this example the attack has yielded the credit card details of all users.

Related articles:

What is Burp Proxy?

Using Burp Repeater

Using Burp to Test For SQL Injection Flaws

Using Burp to Exploit SQL Injection Vulnerabilities: The UNION Operator

Using Burp to Detect SQL-specific Parameter Manipulation Flaws

Using Burp to Detect Blind SQL Injection Bugs

Using Burp to Exploit Bind SQL Injection Bugs
