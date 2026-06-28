# Bypassing DOMPurify again with mutation XSS

Source: https://portswigger.net/research/bypassing-dompurify-again-with-mutation-xss
Fetched: 2026-06-28T09:17:21.617677+00:00

Bypassing DOMPurify again with mutation XSS

Gareth Heyes

Researcher

@garethheyes

Published: Wednesday, 7 October 2020 at 14:17 UTC

Updated: Wednesday, 7 October 2020 at 15:02 UTC

After seeing Michał Bentkowski's DOMPurify bypass and the resulting patch, I was inspired to try and crack the patched version myself. Looking at his vector I saw he used style with math based tags to confuse the HTML parser and bypass DOMPurify. I wondered if we could take it a step further and create mXSS. DOMPurify's patch for Michal's finding worked by looking for potential mutation inside text nodes but crucially didn't take into account comments. I injected a comment and a HTML img tag with a title attribute, then I encoded the closing HTML comment and a further image that contained a XSS vector:

<math><mtext><table><mglyph><style><!--</style><img title="--&gt;&lt;img src=1 onerror=alert(1)&gt;">

This bypassed DOMPurify! The following graphic explains how this was possible:

This vector only worked in Chrome, so I was about to tweet this but then right before the tweet was scheduled to go out I found an mXSS in Firefox! For some reason a normal HTML comment wouldn't work to cause mutation in Firefox. However, if you change the comment to a CDATA tag it works fine:

<math><mtext><table><mglyph><style><![CDATA[</style><img title="]]&gt;&lt;/mglyph&gt;&lt;img&Tab;src=1&Tab;onerror=alert(1)&gt;">

The main difference between this and the Chrome one is CDATA tag and the required closing mglyph tag. I use the entity &Tab; to prove the mutation is actually happening and is not just attribute injection. It's worth noting that this Firefox vector was found after DOMPurify was patched. If you'd like to play with the vectors yourself then you can use our mXSS tool:

Chrome mXSS vector

Firefox mXSS vector

Update...

When I first tried the Firefox vector the HTML comment didn't work. I tried it again after I published the post and it worked. Maybe when I originally tried I had a different vector. Anyway this will work in Firefox too:

<math><mtext><table><mglyph><style><!--</style><img title="--&gt;&lt;/mglyph&gt;&lt;img&Tab;src=1&Tab;onerror=alert(1)&gt;">

I disclosed the Chrome vector to Cure53 and it was patched in DOMPurify version 2.1. However this mutation remains in both browsers, and may come in useful when attempting to bypass a HTML filter.

Happy hunting.

XSS

mXSS

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
