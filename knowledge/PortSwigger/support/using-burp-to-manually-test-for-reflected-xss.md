# Using Burp to Manually Test for Reflected XSS

Source: https://portswigger.net/support/using-burp-to-manually-test-for-reflected-xss
Fetched: 2026-06-28T09:17:36.491742+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Manually Test for Reflected XSS

Reflected cross-site scripting vulnerabilities arise when data is copied from a request and echoed in to the application’s immediate response in an unsafe way. An attacker can use the vulnerability to construct a request which, if issued by another application user, will cause JavaScript code supplied by the attacker to execute within the user's browser in the context of that user's session with the application. The attacker-supplied code can perform a wide variety of actions, such as stealing the victim's session token or login credentials, performing arbitrary actions on the victim's behalf, and logging their keystrokes.

In this tutorial we will demonstrate how to generate a proof-of-concept reflected XSS exploit. The example uses a version of "Mutillidae" taken from OWASP's Broken Web Application Project. Find out how to download, install and use this project.

First, ensure that Burp is correctly configured with your browser.

With intercept turned off in the Proxy "Intercept" tab, visit the web application you are testing in your browser.

Visit the page of the website you wish to test for XSS vulnerabilities.

Return to Burp.

In the Proxy "Intercept" tab, ensure "Intercept is on".

Enter some appropriate input in to the web application and submit the request.

The request will be captured by Burp. You can view the HTTP request in the Proxy "Intercept" tab.

You can also locate the relevant request in various Burp tabs without having to use the intercept function, e.g. requests are logged and detailed in the "HTTP history" tab within the "Proxy" tab.

Right click anywhere on the request to bring up the context menu.

Click "Send to Repeater"

Go to the "Repeater" tab.

Here we can input various XSS payloads into the input field.

We can test various inputs by editing the "Value" of the appropriate parameter in the "Raw" or "Params" tabs.

A simple payload such as <s> can often be used to check for issues.

In this example we have used a payload that attempts to perform a proof of concept pop up in our browser.

Click "Go".

We can assess whether the attack payload appears unmodified in the response. If so, the application is almost certainly vulnerable to XSS.

You can find the response quickly using the search bar at the bottom of the response panel.

The highlighted text is the result of our search.

Right click on the response to bring up the context menu.

Click "Show response in browser" to copy the URL.

You can also use "Copy URL" or "Request in browser".

In the pop up window, click "Copy".

Copy the URL in to your browser's address bar.

In this example we were able to produce a proof of concept for the vulnerability.

Related articles:

What is Burp Proxy?

Using Burp Repeater
