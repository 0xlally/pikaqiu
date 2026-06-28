# Example insertion point check

Source: https://portswigger.net/burp/documentation/scanner/bchecks/worked-examples/insertion-point
Fetched: 2026-06-28T09:16:10.558703+00:00

Support Center

Documentation

Scanner

BCheck definitions

Worked examples

Example insertion point check

DASTProfessional

Example insertion point check

Last updated:

June 18, 2026

Read time:

2 Minutes

This BCheck checks for suspicious input transformation. It is an example of a check that runs once for each insertion point found during the crawl.

The check works by adding a simple mathematical calculation to the end of a request payload. If the answer to the calculation is returned in the response, then it is possible that the application is vulnerable to some form of server-side code injection.

metadata:

language: v2-beta

name: "Insertion-point-level"

description: "Inserts a calculation into each parameter to detect suspicious input transformation"

author: "Carlos Montoya"

define:

calculation="{{1337*1337}}"

answer="1787569"

given insertion point then

if not({answer} in {base.response}) then

send payload:

appending: {calculation}

if {answer} in {latest.response} then

report issue:

severity: high

confidence: tentative

detail: "The application transforms input in a way that suggests it might be vulnerable to some kind of server-side code injection."

remediation: "Manual investigation is advised."

end if

end if

Step 1: Add metadata

metadata:

language: v2-beta

name: "Insertion-point-level"

description: "Inserts a calculation into each parameter to detect suspicious input transformation"

author: "Carlos Montoya"

The definition starts with a metadata block. For more information on available metadata properties, see the reference documentation.

Step 2: Define the calculation

define:

calculation="{{1337*1337}}"

answer="1787569"

The next step is to define variables containing the mathematical calculation to be used in the check and the answer to that calculation.

Step 3: Send the request

given insertion point then

if not({answer} in {base.response}) then

send payload:

appending: {calculation}

The next step is to send the request.

Before the request is sent, Burp Scanner reduces false positives by checking that the answer to the calculation does not already appear in the base response. If it does not find a string matching the answer, Burp Scanner sends a request with the calculation appended to its payload.

Step 4: Report issues

if {answer} in {latest.response} then

report issue:

severity: high

confidence: tentative

detail: "The application transforms input in a way that suggests it might be vulnerable to some kind of server-side code injection."

remediation: "Manual investigation is advised."

The final step is to report an issue where appropriate. If the response contains the answer to the calculation then Burp Scanner knows that the application can transform input (in this case, by solving the calculation) and reports an issue with tentative confidence.

Related pages

BCheck definition reference.
