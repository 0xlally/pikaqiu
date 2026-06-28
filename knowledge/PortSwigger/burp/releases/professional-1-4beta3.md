# Professional 1.4beta3

Source: https://portswigger.net/burp/releases/professional-1-4beta3
Fetched: 2026-06-28T09:16:24.412282+00:00

This release fixes a few bugs, and also adds some further features to enhance the new functionality added in v1.4:

There is a new tracer function for troubleshooting the session handling configuration. This shows you all of the steps performed when Burp applies session handling rules to a request, allowing you to see exactly how requests are being updated and issued. You can access the session handling tracer via options / sessions / view sessions tracer:

There is a new session handling action, to execute a post-request macro. This action issues the request that is currently being processed, and then executes a further macro (request sequence). Optionally, you can configure Burp to update parameters in the first macro request with values taken from the response to the current request, to handle anti-CSRF tokens, etc. Also, you can configure whether the invoking tool should receive the response from the current request, or the response from the final macro request. You can use this feature to perform testing on an request that is part way through a multi-stage process, and ensure that the rest of the process is completed in the normal way. This can be useful to identify some bugs like XSS and SQL injection, where the relevant input is supplied at one stage of a process, and is processed in a vulnerable way at a later stage of the process.

The auto-matching of parameter values between macro requests and responses now works for URL-encoded parameters. Further, there is a default-on option to URL-encode any problematic characters in parameter values that are updated by the session handler.

When you are performing a site map comparison that involves re-requesting a site map in the current session context, the comparison wizard displays the new site map while it is in the process of being re-requested. This enables you to inspect responses within the re-requested map to ensure that your session context is still valid and your session handling configuration is working in the way you intend.
