# Testing HTTP match and replace rules

Source: https://portswigger.net/burp/documentation/desktop/tools/proxy/match-and-replace/testing
Fetched: 2026-06-28T09:16:07.093923+00:00

Support Center

Documentation

Desktop editions

Tools

Burp Proxy

Match and replace

Testing rules

ProfessionalCommunity Edition

Testing HTTP match and replace rules

Last updated:

June 18, 2026

Read time:

1 Minute

When adding or editing a HTTP match and replace rule, you can test your rule using the built-in test function. This enables you to confirm that the rule correctly matches and replaces the intended text.

To test a HTTP match and replace rule in the match/replace rule editor:

Review the sample message under Original request or Original response. Optionally, replace this sample message with the specific request or response you'd like to test the rule against.

Click Test. Burp applies the rule to the original message, creating a modified request or response.

Review the modified request or response under Auto-modified request or Auto-modified response.

Adjust the rule as necessary.

To restore the sample request or response, click .
