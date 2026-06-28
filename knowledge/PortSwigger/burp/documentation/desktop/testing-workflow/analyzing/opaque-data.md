# Analyzing opaque data with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/analyzing/opaque-data
Fetched: 2026-06-28T09:15:57.586385+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Analyzing the attack surface

Analyzing opaque data

ProfessionalCommunity Edition

Analyzing opaque data with Burp Suite

Last updated:

June 18, 2026

Read time:

1 Minute

Applications often transmit opaque data that isn't human-readable. Often, this is because the data is encoded or encrypted. For example, session-handling mechanisms often include opaque tokens, such as session tokens or anti-CSRF tokens. When opaque data is transmitted, the server-side application checks the integrity of the data, and may decrypt or decode it to process its plaintext value.

Burp Suite provides a number of features that can help you work with opaque data more easily. For example, you can use Burp to decode data or to edit the data contents.

Tutorials in this section

Decoding opaque data with Burp Suite

Identifying which parts of a token impact the response with Burp Suite
