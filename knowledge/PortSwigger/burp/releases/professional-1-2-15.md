# Professional 1.2.15

Source: https://portswigger.net/burp/releases/professional-1-2-15
Fetched: 2026-06-28T09:16:22.750050+00:00

1. Burp Scanner now checks for a few new issues:

XML external entity injection

Server-side XML / SOAP injection

Vulnerable Flash cross-domain policies

2. IBurpExtenderCallbacks gets a new method:

public IScanIssue[] getScanIssues(String urlPrefix);

This method returns all of the current scan issues for URLs matching the specified literal prefix. The prefix can be null to match all issues.

3. Previously, Burp Scanner could be configured to skip server-side injection checks for specific parameters. This feature is useful to avoid wasting time testing built-in platform parameters that are unlikely to contain vulnerabilities like SQL injection. Client-side issues like XSS are still checked for because this involves hardly any overhead.

Now, you can also configure Burp Scanner to skip absolutely all tests for specific parameters. This is useful if you know that a parameter is not used by the application, or if changing its value causes problems like session termination:

4. Various bugfixes.
