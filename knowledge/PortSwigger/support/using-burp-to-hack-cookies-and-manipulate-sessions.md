# Using Burp to Hack Cookies and Manipulate Sessions

Source: https://portswigger.net/support/using-burp-to-hack-cookies-and-manipulate-sessions
Fetched: 2026-06-28T09:17:36.476608+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Hack Cookies and Manipulate Sessions

First, ensure that Burp is correctly configured with your browser.

With intercept turned off in the Proxy "Intercept" tab, visit the login page of the application you are testing in your browser.

Log in to the application you are testing.

You can log in using the credentials user:user.

Return to Burp.

In the Proxy "Intercept" tab, ensure "Intercept is on".

Refresh the page in your browser.

The request will be captured by Burp, it can be viewed in the Proxy "Intercept" tab.

Cookies can be viewed in the cookie header.

We now need to investigate and edit each individual cookie.

Right click anywhere on the request and click "Send to Repeater".

Note: You can also send requests to Repeater via the context menu in any location where HTTP requests are shown, such as the site map or Proxy history.

Go to the Repeater tab.

The cookies in the request can be edited easily in the "Params" tab.

By removing cookies from the request we can ascertain the function of each cookie.

In this example, if the "username", "uid" and "PHPSESSID" cookies are removed, the session is ended and the user is logged out of the application.

We can use the Repeater to remove cookies and test the response from the server.

Remove and add cookies using the "Add" and "Remove" buttons and use the "Go" button to forward requests to the server.

Cookies can be edited in the Request "Params" table.

In this example we have altered the value of the "uid" cookie to 1.

Alter the value then click the "Go" button.

The response from the server can be viewed in the "Response" panel in Repeater.

The response shows that by altering the "uid" cookie we have logged in to the application as "admin".

We have used cookies to manipulate the session and access another account with elevated privileges.

Related articles:

What is Burp Proxy?

Using Burp Intruder

Using Burp Repeater

Scanning websites with Burp Scanner

Using Burp to attack session management
