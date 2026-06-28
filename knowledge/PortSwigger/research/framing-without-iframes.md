# Framing without iframes

Source: https://portswigger.net/research/framing-without-iframes
Fetched: 2026-06-28T09:17:25.605592+00:00

Framing without iframes

Gareth Heyes

Researcher

@garethheyes

Published: Wednesday, 27 July 2022 at 14:57 UTC

Updated: Wednesday, 27 July 2022 at 14:57 UTC

Whilst testing for XSS vectors, we found some new ways of framing a web site that don't use the iframe element. Naturally, we've updated our XSS cheat sheet to document them. We discovered that Chrome allows you to use param tags to change the URL of an object tag much like an iframe:

<object width=1000 height=1000 type=text/html><param name=url value="https://portswigger-labs.net">

<object width=1000 height=1000 type=text/html><param name=code value="https://portswigger-labs.net">

<object width=1000 height=1000 type=text/html><param name=movie value="https://portswigger-labs.net">

<object width=1000 height=1000 type=text/html><param name=src value="https://portswigger-labs.net">

In addition Chrome & webkit allow you to use the "code" attribute in an embed tag to reference an external URL:

<embed code=https://portswigger-labs.net width=500 height=500 type=text/html>

We tried exploiting these features for XSS but unfortunately JavaScript URLs don't work and although URLs with a data: protocol work they all execute from a null origin making them useless for XSS. Still, new ways of framing are always useful to chain other attacks or maybe even bypass CSP.

Firefox and tabindex

In other XSS news it was reported to us that Firefox now exhibits the same behaviour as Chrome when it comes to the tabindex attributes. This makes events such as onfocus fire automatically on Firefox, when previously they didn't. Hurray for attack surface expansion! The cheat sheet has now been updated to reflect this change.

Search interface

Finally, we had a request for a search interface for the XSS cheat sheet, this would make it easier to find vectors when a WAF is filtering certain attributes or tags. So we've added one that allows you to search tags, events, and the code, using regular expressions.

XSS cheat sheet

XSS

iframes

Back to all articles

Related Research

Cookie Chaos: How to bypass __Host and __Secure cookie prefixes

03 September 2025

Cookie Chaos: How to bypass __Host and __Secure cookie prefixes

Stealing HttpOnly cookies with the cookie sandwich technique

22 January 2025

Stealing HttpOnly cookies with the cookie sandwich technique

Bypassing WAFs with the phantom $Version cookie

04 December 2024

Bypassing WAFs with the phantom $Version cookie

Concealing payloads in URL credentials

23 October 2024

Concealing payloads in URL credentials
