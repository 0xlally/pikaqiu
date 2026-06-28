# Active scan check worked example

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/custom-scan-checks/creating/active-worked-example
Fetched: 2026-06-28T09:15:46.054241+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Custom scan checks

Creating custom scan checks

Active scan check example

Professional

Active scan check worked example

Last updated:

June 18, 2026

Read time:

4 Minutes

You can extend Burp Scanner by writing your own scan checks. A custom scan check can report new security issues that Burp doesn't detect natively.

In this worked example, we'll use Java to write an active custom scan check. Active checks send additional, modified requests to probe for vulnerabilities. Use these to detect issues that only appear when requests are manipulated, such as:

SQL injection.

Server-side template injection.

Command injection.

Related pages

Custom scan checks writing guide.

Creating custom scan checks.

Testing custom scan checks.

For instructions on creating BCheck-based custom scan checks, see BCheck definitions.

To view examples of custom scan checks that have been created by our researchers and the community, see our

Bambdas GitHub repository - Custom scan checks.

This example sends two follow-up requests with a forged Origin header. It reports an issue if the server reflects the header in Access-Control-Allow-Origin. The issue severity is raised if Access-Control-Allow-Credentials: true is also present, and a note is created if Vary: Origin is missing:

if (!requestResponse.hasResponse())

{

return AuditResult.auditResult();

}

var evilHttps = "https://"

+ api().utilities().randomUtils().randomString(6) + "."

+ api().utilities().randomUtils().randomString(3);

var evilHttp = "http://"

+ api().utilities().randomUtils().randomString(6) + "."

+ api().utilities().randomUtils().randomString(3);

for (var origin : new String[]{evilHttps, evilHttp}) {

var rr = http.sendRequest(

requestResponse.request()

.withRemovedHeader("Origin")

.withAddedHeader("Origin", origin)

);

if (!rr.hasResponse())

{

continue;

}

var headers = rr.response().headers().toString().toLowerCase();

var creds = headers.contains("access-control-allow-credentials: true");

var reflect = headers.contains("access-control-allow-origin: " + origin.toLowerCase());

var vary = headers.contains("vary: origin");

if (reflect) {

var severity = creds ? AuditIssueSeverity.HIGH : AuditIssueSeverity.MEDIUM;

var note = vary ? "" : " (missing Vary: Origin)";

return AuditResult.auditResult(

AuditIssue.auditIssue(

"CORS: arbitrary origin reflection" + note,

"Reflected Origin: " + origin + "; credentials=" + creds,

"Use strict allowlist; include Vary: Origin.",

rr.request().url(),

severity,

AuditIssueConfidence.FIRM,

"",

"",

severity,

rr

)

);

}

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

hasResponse checks whether a response was received.

If no response is received, AuditResult.auditResult() returns an empty result, and no issue is reported.

Step 2: Create random origins

var evilHttps = "https://"

+ api().utilities().randomUtils().randomString(6) + "."

+ api().utilities().randomUtils().randomString(3);

var evilHttp = "http://"

+ api().utilities().randomUtils().randomString(6) + "."

+ api().utilities().randomUtils().randomString(3);

This creates two random domains to avoid caching artefacts and ensure the application can't allowlist them.

Breakdown of the code

randomUtils().randomString(n) creates short random labels, such as q1w2e3.

Both https and http will be tested, as some servers handle them differently.

Step 3: Loop through each origin

for (var origin : new String[]{evilHttps, evilHttp})

This runs the following block of code twice, once for each randomly generated origin.

Breakdown of the code

new String[]{evilHttps, evilHttp} creates a new array containing the two fake origins.

for (var origin : ...) is a for-each loop that assigns each origin in turn.

Step 4: Send the modified requests

var rr = http.sendRequest(

requestResponse.request()

.withRemovedHeader("Origin")

.withAddedHeader("Origin", origin)

);

This sends the request twice, each time with a forged Origin header. If the server doesn't respond, the loop continues to the next origin.

Breakdown of the code

requestResponse.request() gets the HTTP request object.

withRemovedHeader("Origin") removes the original Origin header.

withAddedHeader("Origin", origin) appends the Origin header with the fake value to the request.

http.sendRequest(...) sends the modified request and returns a new request-response object (rr).

if (!rr.hasResponse()) checks to see if the server replied.

continue skips the rest of the loop and proceeds to the next origin if there was no response.

Step 5: Inspect the response headers

var headers = rr.response().headers().toString().toLowerCase();

var creds = headers.contains("access-control-allow-credentials: true");

var reflect = headers.contains("access-control-allow-origin: " + origin.toLowerCase());

var vary = headers.contains("vary: origin");

This examines the response headers to see how the server handled the forged Origin header.

Breakdown of the code

rr.response().headers retrieves all response headers.

toString().toLowerCase() converts the headers into a single lowercase string, so you can search case-insensitively.

reflect is true if the server repeats the forged origin in Access-Control-Allow-Origin.

creds is true if the response also includes Access-Control-Allow-Credentials: true.

vary is true if the response includes Vary: Origin.

Step 6: Return an issue if the origin is reflected

if (reflect) {

var severity = creds ? AuditIssueSeverity.HIGH : AuditIssueSeverity.MEDIUM;

var note = vary ? "" : " (missing Vary: Origin)";

return AuditResult.auditResult(

AuditIssue.auditIssue(

"CORS: arbitrary origin reflection" + note,

"Reflected Origin: " + origin + "; credentials=" + creds,

"Use strict allowlist; include Vary: Origin.",

rr.request().url(),

severity,

AuditIssueConfidence.FIRM,

"",

"",

severity,

rr

)

);

}

This creates variables that determine the severity of the finding based on whether the server allows credentials, and adds a note if the Vary: Origin header is missing. It then wraps the issue variables into an AuditIssue and returns an AuditResult containing that issue.

Breakdown of the code

if (reflect) checks whether the server reflected the random origin in Access-Control-Allow-Origin.

creds ? AuditIssueSeverity.HIGH : AuditIssueSeverity.MEDIUM sets the severity to HIGH if credentials are allowed, otherwise MEDIUM.

var note = vary ? "" : " (missing Vary: Origin)" adds a warning note when the Vary: Origin header is absent.

AuditIssue.auditIssue(...) builds the vulnerability report. For a breakdown of the elements that make up an auditIssue, see Reporting results.

Step 7: Return no issue when the header is present

return AuditResult.auditResult();

If the check didn't detect a reflection or exited early in Step 1, it returns an empty result so no issue is reported.
