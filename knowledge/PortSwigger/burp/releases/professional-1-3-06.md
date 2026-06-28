# Professional 1.3.06

Source: https://portswigger.net/burp/releases/professional-1-3-06
Fetched: 2026-06-28T09:16:23.417573+00:00

This release adds various enhancements to the Scanner engine to further improve its ability to find vulnerabilities and avoid false positives. Most of the improvements affect the core detection logic for XSS and SQL injection.

Aside from the better performance, the only noticeable difference in the UI is a new Scanner option to follow redirects. If enabled, this lets the Scanner follow redirects where necessary to identify certain vulnerabilities (for example echoed input or a database error message which is only displayed when a redirect is followed).

Because some applications issue redirects to third-party URLs which include parameter values that you have submitted, Burp protects you against inadvertently attacking third-party applications, by not following just any redirection which is received. If the request being scanned is within the defined target scope (i.e. you are using target scope to control what gets scanned), then Burp will only follow redirects that are within that scope. If the request being scanned is not in scope (i.e. you have manually initiated a scan of an out-of-scope request), Burp will only follow redirects which (a) are to the same host/port as the request being scanned; and (b) are not explicitly covered by a scope exclusion rule (e.g. "logout.aspx").
