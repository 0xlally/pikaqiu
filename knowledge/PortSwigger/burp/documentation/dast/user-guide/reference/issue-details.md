# Issue details

Source: https://portswigger.net/burp/documentation/dast/user-guide/reference/issue-details
Fetched: 2026-06-28T09:15:39.064222+00:00

DAST

Issue details

Last updated:

June 18, 2026

Read time:

2 Minutes

When you view the details of a particular issue, the Issues window displays several tabs. Depending on the type of issue, the tabs displayed change. However, the Advisory tab is always present.

Advisory tab

This tab shows key information about the issue:

The Severity of the issue.

The Confidence that the issue is present.

The host and URL path where the issue was found.

The Advisory tab shows whether the issue was found by an extension.

The collapsible headings contain more detailed information about the issue. Note that only headings that apply to the particular issue are shown:

Issue description.

Issue detail.

Issue background.

Issue remediation.

References.

Vulnerability classifications.

Request and response tabs

The Request and Response tabs show a snippet of the HTTP requests and responses in which the issue was found. There might only be one request and one response, or there might be a series of interconnected requests and responses that lead to the issue.

To help you to analyze the issue, key parts of each request and response are highlighted in red. These include payloads injected by the scanner and the string or regex in the response that confirms the vulnerability.

Dynamic analysis

For DOM-based vulnerabilities, the Dynamic analysis tab shows the results of Burp Scanner's dynamic analysis of JavaScript on the site using an embedded headless browser. It loads HTTP responses into the browser, injects payloads into the DOM at locations that are potentially controllable by an attacker, and executes the JavaScript within the response.

Burp Scanner also interacts with the page by creating mouse events to achieve as much code coverage as possible. It monitors dangerous sinks that could be used to perform an attack in order to identify any injected payloads that reach them.

The tab shows:

The values that were injected into a given source.

The values that subsequently reached a sink.

A stack trace at both the source and sink are also included.

Wherever possible, the dynamic analysis also generates a proof of concept that you can use to reproduce the issue manually.

Related pages

Viewing issue details.
