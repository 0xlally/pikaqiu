# Using Burp to Test Session Token Handling

Source: https://portswigger.net/support/using-burp-to-test-session-token-handling
Fetched: 2026-06-28T09:17:37.367075+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Test Session Token Handling

Regardless of how well session tokens are generated, the session mechanism of an application will be wide open to attack if those tokens are not handled carefully. For example, if tokens are disclosed to an attacker via some means, the attacker can hijack user sessions even if predicting the token is impossible.

The following tutorial demonstrates how to use Burp to test for session token handling issues.

First, ensure that Burp is correctly configured with your browser.

With intercept turned off in the Proxy "Intercept" tab, visit the web application you are testing in your browser.

Go to the Target "Scope" tab.

Ensure that the target application is included in scope.

Go to the Scanner "Live Scanning" tab.

Ensure that live passing scanning is enabled for in-scope items.

Go to the Scanner "Options" tab.

By selecting the appropriate scanning areas you can instruct Burp to scan for various session token handling issues, both actively and passively.

Walk through the application in the normal way from first access, through the login process, and then through all of the application's functionality.

A record can be kept of every URL visited in the "HTTP history" table. Pay particular attention to login functions and transitions between HTTP and HTTPS communications.

If cookies are being used as the transmission mechanism for session tokens, verify whether the "secure" flag has been set, preventing them from ever being transmitted over unencrypted connections.

In this "Gruyere" example we can see that the secure flag has not been set.

Alternatively, go to the Scanner "Results" tab.

The Scanner's passive scan function detects session token management issues such as "SSL cookie without secure flag set" and "Cookie without HttpOnly flag set".

The Scanner also provides an advisory section with Issue detail, background and remediation.

Related articles:

What is Burp Proxy?

Scanning websites with Burp Scanner

Using Burp to attack session management
