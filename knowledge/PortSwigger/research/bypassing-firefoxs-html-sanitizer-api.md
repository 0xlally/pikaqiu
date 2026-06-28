# Bypassing Firefox's HTML Sanitizer API

Source: https://portswigger.net/research/bypassing-firefoxs-html-sanitizer-api
Fetched: 2026-06-28T09:17:21.730016+00:00

Bypassing Firefox's HTML Sanitizer API

Gareth Heyes

Researcher

@garethheyes

Published: Wednesday, 29 June 2022 at 14:00 UTC

Updated: Monday, 4 July 2022 at 07:46 UTC

The HTML Sanitizer is a great new API that allows web developers to filter untrusted HTML natively in the browser rather than use a JavaScript library such as DOM Purify. Microsoft created a similar API called toStaticHTML in 2008 for Internet Explorer but it was riddled with holes and wasn't widely adopted or standardised. Hopefully the Sanitizer will have more success.

The advantages of using a native browser feature are obvious; if the browser is used to filter HTML then it can use its own parsers to ensure the untrusted HTML is filtered consistently.

However, there can be a disagreement in what the Sanitizer thinks is safe compared to the actual reality of the filtered HTML. One such example is with SVG "use" elements; we've shown in the past that "use" elements can be used to execute arbitrary JavaScript by using data URLs.

The Sanitizer prevents these attacks by blocking SVG imports using both data URLs and relative URLs. However, it allowed SVG imports from absolute URLs, provided they were the same origin. This means if the target site allowed a file upload of an SVG file and protected it by forcing a download using Content-Disposition: attachment, it would still be possible to execute arbitrary JavaScript.

<svg><use href="//portswigger-labs.net/use_element/upload.php#x"/></svg>

Proof of concept

Here's the result of the untrusted HTML being filtered incorrectly by the Sanitizer:

Input:

<svg><use href="//portswigger-labs.net/use_element/upload.php#x" />

Output:

<div><svg><use href="//portswigger-labs.net/use_element/upload.php#x"></use></svg></div>

Conclusion

Browser APIs for sanitizing HTML are a good idea as the browser is in a better position to filter the HTML correctly however this doesn't mean they are a foolproof mechanism to prevent malicious HTML from sneaking past. As with any filter, a feature like this requires a large amount of testing to ensure correct filtering of malicious HTML.

Note

Please note this is an experimental API and isn't widely supported yet.

Timeline

2022-02-25 09:42 PST - Reported bug to Mozilla

2022-04-29 15:03 PDT - Fixed

2022-06-28  - Firefox 102.0 released

2022-06-29 15:00 PM GMT - Published this post

XSS

filter

firefox

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
