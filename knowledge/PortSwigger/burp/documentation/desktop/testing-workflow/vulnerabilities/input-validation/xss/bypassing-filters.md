# Bypassing XSS filters by enumerating permitted tags and attributes

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/xss/bypassing-filters
Fetched: 2026-06-28T09:16:00.000496+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing input validation

Cross-site scripting

Bypassing XSS filters

ProfessionalCommunity Edition

Bypassing XSS filters by enumerating permitted tags and attributes

Last updated:

June 18, 2026

Read time:

2 Minutes

Reflected cross-site scripting (XSS) arises when an application receives data in an HTTP request, then includes that data in its response in an unsafe way.

Applications use a range of processing and input validation methods to protect against common XSS payloads. You can use Burp Intruder to enumerate tags and attributes that are permitted by the application. This enables you to craft an XSS payload that will be executed by the application, and is a useful next step if your attempts to test using proof-of-concept payloads were not successful.

Before you start

Identify a request / response pair with reflected input. For more information, see Identifying reflected

input.

Steps

You can follow the processes below using the lab Reflected XSS into HTML context with most tags and attributes blocked.

In Proxy > HTTP history, right-click the request with a reflected input that you want to investigate. Select Send to Intruder.

Identify whether any tags are permitted:

In Intruder, replace the value of the input with: <>.

Click inside the angle brackets, then click Add § to add a payload

position.

In the Payloads side panel, under Payload configuration, add a list of tags that you want to test. For example, use the tags in the

XSS cheat sheet.

Click Start attack. The attack starts running in a new dialog. Intruder sends a request for each tag on the list.

When the attack is finished, look for any responses with a 200 status code. This indicates that the tag is permitted. If a tag is filtered out, it has a

400 status code instead.

Identify whether any attributes are permitted:

In the Intruder tab, update the payload position. Add a tag that you enumerated in the previous step, click Add § to add a payload position to test different attributes.

In the Payloads side panel, under Payload configuration, click Clear to remove the list of tags that you tested in the previous step.

Add a list of attributes that you want to test. For example, use the events listed in the XSS cheat sheet.

Click Start attack. The attack starts running in a new dialog. Intruder sends a request for each attribute on the list.

When the attack is finished, look for any responses with a 200 status code. This indicates that an attribute is permitted.

You can use the permitted tags and attributes that you identified to construct an attack string. For more information, see Testing for reflected XSS manually.

Related pages

Academy: Reflected XSS

Cross-site scripting (XSS) cheat sheet

Burp Intruder

Testing for reflected XSS manually with Burp Suite

Testing for stored XSS with Burp Suite
