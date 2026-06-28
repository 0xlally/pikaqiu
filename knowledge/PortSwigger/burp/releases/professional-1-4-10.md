# Professional 1.4.10

Source: https://portswigger.net/burp/releases/professional-1-4-10
Fetched: 2026-06-28T09:16:24.149393+00:00

Burp now fully supports JSON requests. These are properly handled by Intruder and Scanner, for automatic placement of attack insertion points, and syntax is correctly colorized in the message viewer:

The Scanner engine now includes options to change parameter locations when scanning. If set, Burp will still scan each parameter in its original location, but will additionally move the parameter within the request and test it again. This can be highly effective when an application performs some filtering on parameters in a particular location (e.g. the query string) but reads the value of a specific named parameter from anywhere in the request. The new options are off by default because they result in many more scan requests being generated:

There are several new scan checks: frameable responses (Clickjacking), HTML5 cross-origin resource sharing, user agent-dependent responses, disabling of browser XSS filter.

Various existing scan checks have been improved (XSS, SQL injection, file path traversal, etc.). To help you fine-tune the focus of each scan, you can now configure whether the SQL injection checks should include attacks that are specific to different database types:
