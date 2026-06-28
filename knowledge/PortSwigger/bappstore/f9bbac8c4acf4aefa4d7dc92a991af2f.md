# Autorize

Source: https://portswigger.net/bappstore/f9bbac8c4acf4aefa4d7dc92a991af2f
Fetched: 2026-06-28T09:15:05.067025+00:00

Support Center

BApp Store

Autorize

Professional

Community

Autorize

Download BApp

Autorize is an automatic authorization and authentication enforcement detection extension that identifies access

control vulnerabilities in web applications. It monitors traffic from a high-privileged user, automatically replays

those requests with low-privileged or unauthenticated credentials, and analyzes responses to detect authorization

bypasses and authentication weaknesses.

Features

Automatic detection of authorization and authentication enforcement issues by replaying requests with different

privilege levels

Support for multiple low-privileged users with independent enforcement detection and match/replace rules

Configurable enforcement detection using status codes, response headers, body content, regex patterns, and

response length

Flexible interception filters based on scope, URL patterns, HTTP methods, request/response headers and body

content

Visual status indicators showing whether authorization is bypassed, enforced, or requires manual configuration

HTML and CSV export for reporting

Usage

Navigate to the Autorize tab and open the Configuration section

Add low-privileged user credentials by specifying authorization headers or cookies that will be injected into

replayed requests

Optionally configure enforcement detectors to define custom rules for identifying when authorization is properly

enforced

Set up interception filters to control which requests should be tested (e.g., scope-only, URL patterns, HTTP

methods)

Browse the application as a high-privileged user. The extension

automatically repeats every request with the session of the low privileged user and detects authorization

vulnerabilities.

Review the results table where each request shows enforcement status: Bypassed (red), Enforced (green), or

uncertain (yellow)

Select any entry to compare the original response with the modified low-privileged and unauthenticated responses

For uncertain results, configure enforcement detectors with specific patterns that indicate proper authorization

enforcement

Author

Author

Barak Tawily, AppSec Labs

Version

Version

1.9.4

Rating

Rating

Popularity

Popularity

Last updated

Last updated

24 February 2026

Estimated system impact

Estimated system impact

Overall impact:

Low

Memory

Low

CPU

Low

General

Low

Scanner

Low

You can install BApps directly within Burp, via the BApp Store feature in the Burp Extender tool. You can also download them from here, for offline installation into Burp.

You can view the source code for all BApp Store extensions on our

GitHub page.

Follow

@BApp_Store on Twitter to receive notifications of all BApp releases and updates.

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.

Go back to

BappStore

Note:

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.
