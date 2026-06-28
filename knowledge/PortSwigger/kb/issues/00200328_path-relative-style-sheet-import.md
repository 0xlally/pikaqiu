# Path-relative style sheet import

Source: https://portswigger.net/kb/issues/00200328_path-relative-style-sheet-import
Fetched: 2026-06-28T09:17:07.514480+00:00

Support Center

Issue Definitions

Path-relative style sheet import

Path-relative style sheet import

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Path-relative style sheet import

Path-relative style sheet import vulnerabilities arise when the following conditions hold:

A response contains a style sheet import that uses a path-relative URL (for example, the page at "/original-path/file.php" might import "styles/main.css").

When handling requests, the application or platform tolerates superfluous path-like data following the original filename in the URL (for example, "/original-path/file.php/extra-junk/"). When superfluous data is added to the original URL, the application's response still contains a path-relative stylesheet import.

The response in condition 2 can be made to render in a browser's quirks mode, either because it has a missing or old doctype directive, or because it allows itself to be framed by a page under an attacker's control.

When a browser requests the style sheet that is imported in the response from the modified URL (using the URL "/original-path/file.php/extra-junk/styles/main.css"), the application returns something other than the CSS response that was supposed to be imported. Given the behavior described in condition 2, this will typically be the same response that was originally returned in condition 1.

An attacker has a means of manipulating some text within the response in condition 4, for example because the application stores and displays some past input, or echoes some text within the current URL.

Given the above conditions, an attacker can execute CSS injection within the browser of the target user. The attacker can construct a URL that causes the victim's browser to import as CSS a different URL than normal, containing text that the attacker can manipulate.

Being able to inject arbitrary CSS into the victim's browser may enable various attacks, including:

Executing arbitrary JavaScript using IE's expression() function.

Using CSS selectors to read parts of the HTML source, which may include sensitive data such as anti-CSRF tokens.

Capturing any sensitive data within the URL query string by making a further style sheet import to a URL on the attacker's domain, and monitoring the incoming Referer header.

Remediation: Path-relative style sheet import

The root cause of the vulnerability can be resolved by not using path-relative URLs in style sheet imports. Aside from this, attacks can also be prevented by implementing all of the following defensive measures:

Setting the HTTP response header "X-Frame-Options: deny" in all responses. One method that an attacker can use to make a page render in quirks mode is to frame it within their own page that is rendered in quirks mode. Setting this header prevents the page from being framed.

Setting a modern doctype (e.g. "<!doctype html>") in all HTML responses. This prevents the page from being rendered in quirks mode (unless it is being framed, as described above).

Setting the HTTP response header "X-Content-Type-Options: nosniff" in all responses. This prevents the browser from processing a non-CSS response as CSS, even if another page loads the response via a style sheet import.

References

Detecting and exploiting path-relative stylesheet import (PRSSI) vulnerabilities

Vulnerability classifications

CWE-16: Configuration

CAPEC-154: Resource Location Spoofing

CAPEC-468: Generic Cross-Browser Cross-Domain Theft

Typical severity

Information

Type index (hex)

0x00200328

Type index (decimal)

2097960

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Burp Scanner

This issue - and many more like it - can be found using our

web vulnerability scanner

Read more

Get Burp

Scan your web application from just $499.00

Find out more
