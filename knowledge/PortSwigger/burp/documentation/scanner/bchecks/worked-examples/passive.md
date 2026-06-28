# Example passive check

Source: https://portswigger.net/burp/documentation/scanner/bchecks/worked-examples/passive
Fetched: 2026-06-28T09:16:10.663668+00:00

Support Center

Documentation

Scanner

BCheck definitions

Worked examples

Example passive check

DASTProfessional

Example passive check

Last updated:

June 18, 2026

Read time:

2 Minutes

This check enables Burp Scanner to identify responses that disclose an AWS Access Key ID. It is an example of a passive check (that is, a check that inspects traffic passing through Burp without sending any additional requests).

Specifically, the check examines each response for the regular expression AKIA[0-9A-Z]{16}. If Burp Scanner finds a matching expression, it returns an issue indicating that the AWS key information has been disclosed.

metadata:

language: v2-beta

name: "Response-level (passive) check"

description: "Checks responses for leaked AWS Access Key IDs"

tags: "passive"

given response then

if {latest.response} matches "AKIA[0-9A-Z]{16}" then

report issue:

severity: high

confidence: firm

detail: "Leaked AWS Access Key ID."

remediation: "Replace your keys and ensure keys are no longer revealed."

end if

Note

Although this worked example identifies AWS key IDs, you could create a check that identifies any form of disclosed information by modifying the matches pattern.

Step 1: Add metadata

metadata:

language: v2-beta

name: "Response-level (passive) check"

description: "Checks responses for leaked AWS Access Key IDs"

tags: "passive"

The definition starts with a metadata block. For more information on available metadata properties, see the reference documentation.

Step 2: Add a string for the check to match

given response then

if {latest.response} matches "AKIA[0-9A-Z]{16}" then

This example checks each response received using an if statement. The statement checks for the regex string AKIA[0-9A-Z]{16}. This is the format that AWS key information would likely be presented in in a response.

Step 3: Report the issue

report issue:

severity: high

confidence: firm

detail: "Leaked AWS Access Key ID."

remediation: "Replace your keys and ensure keys are no longer revealed."

If Burp Scanner finds a response containing AWS key information, then it reports an issue with a confidence level of firm and provides some simple remediation advice.

Test this BCheck

You can use a similar passive scan check to solve the Information disclosure in error messages Web Security Academy lab. Can you rewrite this BCheck to find the Apache Struts version number in the lab?

Related pages

BCheck definition reference.
