# Testing for reflected XSS manually with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/xss/testing-for-reflected-xss
Fetched: 2026-06-28T09:16:00.315452+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing input validation

Cross-site scripting

Testing for reflected XSS manually

ProfessionalCommunity Edition

Testing for reflected XSS manually with Burp Suite

Last updated:

June 18, 2026

Read time:

2 Minutes

Reflected cross-site scripting (or XSS) occurs when an application receives data in an HTTP request and includes that data within the immediate response in an unsafe way.

While Burp Scanner can detect reflected XSS, you can also manually test applications for reflected XSS using Burp Repeater. Burp Repeater enables you to manipulate HTTP requests directly, making it easier to test whether reflected input is adequately sanitized or filtered server-side.

Before you start

Identify a request that reflects input. For more information, see Identifying reflected input.

Steps

You can follow along with the steps below using the Reflected XSS into HTML context with nothing encoded Web Security Academy lab.

To test for reflected XSS in Burp Repeater:

Note the location of the reflected input and the context in which the input is reflected. For example, in the lab the input is reflected inside an HTML <h1> element. This affects the potential XSS vectors you can use to construct an attack.

In the response panel, select > Auto scroll when text changes.

Change the canary to an XSS proof of concept attack. For example, you could use the alert() function by replacing the canary string with <script>alert(1)</script>.

Send the proof of concept request. Burp Repeater highlights any changes between the new and original responses.

If necessary, repeat steps 3 and 4 until you find a proof of concept that is returned in the response.

Right-click on the request in and select Show response in browser. Burp Suite displays a dialog containing a URL.

Copy and paste this URL into your browser to see if the proof of concept ran successfully.

Related pages

Academy: Cross-site scripting

Burp Repeater

Bypassing XSS filters by enumerating permitted tags and attributes
