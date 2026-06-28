# XSS Filters: Beating Length Limits Using DOM-based Techniques

Source: https://portswigger.net/support/xss-filters-beating-length-limits-using-dom-based-techniques
Fetched: 2026-06-28T09:17:37.551152+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

XSS Filters: Beating Length Limits Using DOM-based Techniques

A highly effective technique in some situations where you encounter a length limit filter is to "convert" a reflected XSS flaw into a DOM-based vulnerability. The example below demonstrates how this technique can be used to beat a length restriction on the message parameter that is copied in to the returned page of an application.

The example uses a version of the "Magical Code Injection Rainbow" taken from OWASP’s Broken Web Application Project. Find out how to download, install and use this project.

Having located a reflected XSS vulnerability and identified a length restriction, you can inject the following 45-byte script, which evaluates the fragment string in the current URL:

<script>eval(location.hash.slice(1)</script>

By injecting this script into the parameter that is vulnerable to reflected XSS, you can effectively induce a DOM-based XSS vulnerability in the resulting page.

This allows the attacker to execute a second script located within the fragment string, which is outside the control of the application's filters and may be arbitrarily long.

In this example we have used the IE browser.

To execute this attack in another browser you may need to URL decode the message within the payload.
