# Using Burp's "Request in Browser" Function to Test for Access Control Issues

Source: https://portswigger.net/support/using-burp-suites-request-in-browser-function-to-test-for-access-control-issues
Fetched: 2026-06-28T09:17:35.771287+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp's "Request in Browser" Function to Test for Access Control Issues

Comparing the application's contents when accessed in different user contexts sometimes requires each page to be tested individually, to confirm whether access controls are being applied. One way to perform this testing manually is to walk through a process several times in your browser and use your proxy to switch the session token supplied in different requests to that of a less-privileged user.

However, you can often dramatically speed up this process by using the "Request in browser" feature of Burp Suite. This tutorial demonstrates the use of this function on a version of a WordPress web application. The version of WordPress we are using is taken from OWASP’s Broken Web Application Project. Find out how to download, install and use this project.

First, ensure that Burp is correctly configured with your browser.

With intercept turned off in the Proxy "Intercept" tab, visit the login page of the application you are testing in your browser.

Login using the higher privileged account, in this example using the credentials admin : admin.

Walk through the process or area of the application you are testing.

The request/response will be captured in Burp's Site map and Proxy history.

Log out of the application and log in using the lower-privileged account (or none at all).

Locate the area you are testing in Burp's Site map or HTTP history.

Right click on the entry to bring up the context menu.

Click "Request in browser", then "In current session".

The "Request in browser" pop up window allows you to copy the URL of the required page.

Click the "Copy" button.

Post the URL in to your browser to attempt to access the individual page your are testing.

In this example we are denied access to the page. It would appear that appropriate access controls are in place for this class of user.

Related articles:

What is Burp Proxy?

Using Burp's site map

Burp Proxy history
