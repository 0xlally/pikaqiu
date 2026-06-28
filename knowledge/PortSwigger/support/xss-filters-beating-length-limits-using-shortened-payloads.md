# XSS Filters: Beating Length Limits Using Shortened Payloads

Source: https://portswigger.net/support/xss-filters-beating-length-limits-using-shortened-payloads
Fetched: 2026-06-28T09:17:37.444932+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

XSS Filters: Beating Length Limits Using Shortened Payloads

The most obvious method when attempting to beat a filter that truncates your input to a fixed maximum length is to shorten your attack payload by using JavaScript APIs with the shortest possible length and removing characters that are usually included but are strictly unnecessary.

Another technique to shorten the length of your payload is to use the window.name window property. This technique effectively allows you to 'bootstrap' a much larger JavaScript payload. An attacker can exploit the behavior of window.name by using any website under his control to store a large JavaScript payload.

The example uses a version of the "Magical Code Injection Rainbow" taken from OWASP's Broken Web Application Project. Find out how to download, install and use this project.

Using the XSS vulnerability on the target site, the attacker's payload can be executed using:

eval(window.name)

This can be shortened further to:

eval(name)

We have used example.com to demonstrate the basic mechanics of this technique.

The payload is inserted in to the window.name attribute of the site under the control of the attacker.

When the victim uses the same browser tab to view the vulnerable website, the payload will remain accessible via window.name.

In practice, this technique is most likely exploited through the use of a hidden iframe which sets the payload from the attacker's site and then automatically redirects the iframed window to the vulnerable page on the target site.
