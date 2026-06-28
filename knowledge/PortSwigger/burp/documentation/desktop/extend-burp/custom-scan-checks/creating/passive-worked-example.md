# Passive scan check worked example

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/custom-scan-checks/creating/passive-worked-example
Fetched: 2026-06-28T09:15:46.404719+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Custom scan checks

Creating custom scan checks

Passive scan check example

Professional

Passive scan check worked example

Last updated:

June 18, 2026

Read time:

4 Minutes

You can extend Burp Scanner by writing your own scan checks. A custom scan check can report new security issues that Burp doesn't detect natively.

In this worked example, we'll use Java to write a passive custom scan check. Passive checks analyze traffic without modifying or sending any new requests. Use these to detect vulnerabilities that are visible directly in responses, such as:

Missing security headers.

Leaked server information in error messages.

Insecure cookies or forms configurations.

Related pages

Custom scan checks writing guide.

Creating custom scan checks.

Testing custom scan checks.

For instructions on creating BCheck-based custom scan checks, see BCheck definitions.

To view examples of custom scan checks that have been created by our researchers and the community, see our

Bambdas GitHub repository - Custom scan checks.

This example reports an issue when a response doesn't include a Content-Security-Policy header. It is intended to run once for every request in the scan:

if (!requestResponse.hasResponse()) {

return AuditResult.auditResult();

}

if (!requestResponse.response().hasHeader("Content-Security-Policy")) {

var issueTitle = "Content Security Policy header missing";

var issueDetail = "The response does not include a Content-Security-Policy header. Without this header the browser cannot enforce a restrictive policy for scripts, styles, images and other resources, increasing exposure to XSS, click-jacking and content-injection attacks.";

var remediation = "Add a suitable Content-Security-Policy header, for example: Content-Security-Policy: default-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'none';";

var background = "Content Security Policy (CSP) is an HTTP response header that tells the browser which sources are permitted for each resource type. A correctly configured CSP helps mitigate XSS and other code-injection flaws by limiting the origins from which content can be loaded.";

var remediationBackground = "Create a baseline policy in report-only mode, review violation reports, then switch to enforcement. Start with default-src 'self' and add only the sources that the application legitimately requires.";

return AuditResult.auditResult(

AuditIssue.auditIssue(

issueTitle,

issueDetail,

remediation,

requestResponse.request().url(),

AuditIssueSeverity.LOW,

AuditIssueConfidence.FIRM,

background,

remediationBackground,

AuditIssueSeverity.LOW,

requestResponse

)

);

}

return AuditResult.auditResult();

Step 1: Make sure there's a response

if (!requestResponse.hasResponse())

{

return AuditResult.auditResult();

}

Before doing anything, the check confirms there's a response to work with. It exits cleanly if a response doesn't exist.

Breakdown of the code

requestResponse represents the request/response pair that Burp passes to your script.

hasResponse checks if a response was received.

If no response is received, AuditResult.auditResult() returns an empty result, meaning that no issue is reported.

Step 2: Check for the CSP header

if (!requestResponse.response().hasHeader("Content-Security-Policy")) {

// Build and return an issue

}

This checks if the response sets a Content-Security-Policy header. If the header is missing, the code will continue to build an issue.

Breakdown of the code

requestResponse.response() gets the HTTP response object.

hasHeader looks for a specific header in a case-insensitive way.

Step 3: Build the issue variables

var issueTitle = "Content Security Policy header missing";

var issueDetail = "The response does not include a Content-Security-Policy header. Without this header the browser cannot enforce a restrictive policy for scripts, styles, images and other resources, increasing exposure to XSS, click-jacking and content-injection attacks.";

var remediation = "Add a suitable Content-Security-Policy header, for example: Content-Security-Policy: default-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'none';";

var background = "Content Security Policy (CSP) is an HTTP response header that tells the browser which sources are permitted for each resource type. A correctly configured CSP helps mitigate XSS and other code-injection flaws by limiting the origins from which content can be loaded.";

var remediationBackground = "Create a baseline policy in report-only mode, review violation reports, then switch to enforcement. Start with default-src 'self' and add only the sources that the application legitimately requires."

These variables define what appears in the reported issue.

Breakdown of the code

issueTitle is the issue name.

issueDetail explains the risk and impact of a missing CSP.

remediation gives a safe baseline header example.

background adds context about this security mechanism.

remediationBackground adds guidance for rolling out a CSP safely.

Step 4: Return an issue if no CSP header is present

return AuditResult.auditResult(

AuditIssue.auditIssue(

issueTitle,

issueDetail,

remediation,

requestResponse.request().url(),

AuditIssueSeverity.LOW,

AuditIssueConfidence.FIRM,

background,

remediationBackground,

AuditIssueSeverity.LOW,

requestResponse

)

);

This wraps the issue variables into an AuditIssue and returns an AuditResult containing that issue. When the check reports a finding, users can view it in the All issues panel (accessible from the bottom dock) or from the Issues tab for the relevant task on the Dashboard.

Breakdown of the code

request().url() links the issue to the base URL where it was identified.

AuditIssueSeverity.LOW sets the severity of the finding.

AuditIssueConfidence.FIRM indicates a high level of confidence in the result.

requestResponse provides Burp with the request and response to display.

Step 5: Return an empty result when the header is present

return AuditResult.auditResult();

If the Content-Security-Policy header exists, or the script exited early in Step 1, this returns an empty result so no issue is reported.
