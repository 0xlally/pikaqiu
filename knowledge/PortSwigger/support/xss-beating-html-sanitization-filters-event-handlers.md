# XSS: Beating HTML Sanitization Filters: Event Handlers

Source: https://portswigger.net/support/xss-beating-html-sanitization-filters-event-handlers
Fetched: 2026-06-28T09:17:37.862438+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

XSS: Beating HTML Sanitization Filters: Event Handlers

In cases where the script you are injecting in to resides within an event handler, rather than a full script block, you may be able to HTML-encode your quotation marks to bypass the application's sanitization and break out of the string you control. Event handlers are special JavaScript functions that perform an action based on certain events.

The example uses a version of the "Magical Code Injection Rainbow" taken from OWASP’s Broken Web Application Project. Find out how to download, install and use this project.

If you control the value *INJECT* in:

<a href="#" onClick="var a ='foo*INJECT*'">Click Me</a>

and the application is properly escaping both quotation marks and backslashes in your input, the following attack may succeed:

&apos;; alert(1);//

This results in the following response:

<a href="#" onClick="var a ='foo&apos;; alert(1);//'">Click Me</a>

The attack succeeds because browsers perform an HTML decode of the value of the onClick attribute before it is executed as JavaScript.

The fact that event handlers are HTML-decoded before being executed as JavaScript represents an important caveat to the standard recommendation of HTML-encoding user input to prevent XSS attacks.

In this syntactic context, HTML encoding is not necessarily an obstacle to an attack. The attacker himself may even use it to circumvent other defenses.
