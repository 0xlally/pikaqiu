# Example Collaborator-based check

Source: https://portswigger.net/burp/documentation/scanner/bchecks/worked-examples/collaborator
Fetched: 2026-06-28T09:16:10.537905+00:00

Support Center

Documentation

Scanner

BCheck definitions

Worked examples

Example Collaborator-based check

DASTProfessional

Example Collaborator-based check

Last updated:

June 18, 2026

Read time:

2 Minutes

This BCheck enables Burp Scanner to use Burp Collaborator to check for SSRF.

The check works by sending a request containing a Burp Collaborator interaction ID in the Referer header. Burp Scanner reports an SSRF issue if Burp Collaborator receives any interactions as a result of this request.

metadata:

language: v2-beta

name: "Request-level collaborator-based check"

description: "Blind SSRF with out-of-band detection"

author: "Carlos Montoya"

given request then

send request:

headers:

"Referer": {generate_collaborator_address()}

if http interactions then

report issue:

severity: high

confidence: firm

detail: "This site fetches arbitrary URLs specified in the Referer header."

remediation: "Ensure that the site does not directly request URLS from the Referer header."

end if

Step 1: Add metadata

metadata:

language: v2-beta

name: "Request-level collaborator-based check"

description: "Blind SSRF with out-of-band detection"

author: "Carlos Montoya"

The definition starts with a metadata block. For more information on available metadata properties, see the reference documentation.

Step 2: Configure the request

given request then

send request:

headers:

"Referer": {generate_collaborator_address()}

The next step is to configure the request that Burp Scanner sends.

The example code means that for each request Burp Scanner audits it sends a second request containing a Burp Collaborator interaction ID in the Referer header. The {generate_collaborator_address()} reserved variable causes Burp Collaborator to generate and insert a new interaction ID into the request.

Step 3: Analyze the results

if http interactions then

report issue:

severity: high

confidence: firm

detail: "This site fetches arbitrary URLs specified in the Referer header."

remediation: "Ensure that the site does not directly request URLS from the Referer header."

end if

The final step in the check is to see whether Burp Collaborator has received any interactions as a result of the request.

This if statement uses the http interactions conditional. If the request results in the Collaborator server receiving a HTTP interaction, then the condition is true and Burp Scanner raises an issue with high severity and a confidence level of firm.

Test this BCheck

You can test out this BCheck on the Blind SSRF with out-of-band detection Web Security Academy lab. The check solves the lab outright.

Related pages

BCheck definition reference.
