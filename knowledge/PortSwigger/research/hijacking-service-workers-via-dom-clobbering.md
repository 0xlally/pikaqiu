# Hijacking service workers via DOM Clobbering

Source: https://portswigger.net/research/hijacking-service-workers-via-dom-clobbering
Fetched: 2026-06-28T09:17:26.005104+00:00

Hijacking service workers via DOM Clobbering

Gareth Heyes

Researcher

@garethheyes

Published: Tuesday, 29 November 2022 at 14:00 UTC

Updated: Monday, 5 December 2022 at 08:50 UTC

In this post, we'll briefly review how service worker hijacking works, then introduce a variant that can be triggered via DOM clobbering thanks to a quirk in document.getElementById().

Understanding service workers

Many websites use service workers (SWs) to provide caching and offline capabilities. Web pages often pass information to service workers using query parameters, as SWs don't have access to the parent page's DOM. If these parameters are handled insecurely, this can lead to malicious JavaScript execution inside the SW as noted by the "Security Study of Service Worker Cross-Site Scripting" paper. Although rare, this vulnerability has a much higher impact than typical XSS as it enables permanent client-side site takeover.

Hijacking service workers

This technique to hijack a service worker enables three key outcomes:

HTML filter evasion

Bypassing CSP

Escalating XSS

The importScripts() function lies at the heart of this vulnerability - it allows a SW to retrieve JavaScript from a different domain. In the example below an attacker can control the host query parameter, which can then lead to full control over the script that gets imported and therefore full control over the website responses.

In order to exploit these types of vulnerabilities, you need two components:

One - control over a query string parameter that is passed to the SW.

Two - an importScripts() function call inside the SW that can be influenced by the query string parameter.

index.html:

<script>

navigator.serviceWorker.register('/dom-invader/testcases/augmented-dom-import-scripts/sw.js' + location.search);

// attacker controls location.search

</script>

sw.js:

const searchParams = new URLSearchParams(location.search);

let host = searchParams.get('host');

self.importScripts(host + "/sw_extra.js");

//host can be controllable by an attacker

Using this knowledge we went hunting for bugs using Puppeteer and DOM Invader

We scanned multiple bug bounty sites and found one site using a SW inside an iframe - they were passing URL parameters to the SW from the framed document. DOM Invader immediately flagged this behaviour but, thankfully for the site they did not allow you to inject the SW from the top-level window. The code looked like this:

navigator.serviceWorker.register('https://redacted&_flasher_manifest_=https://redacted/@xconfig/flasher_classic/manifestysvoy7p7location.href')

DOM Invader generated a random token inside the location.href source which was then passed to serviceWorker.register() sink. This behaviour was then reported in the augmented DOM. We had configured DOM Invader to automatically inject the canary into all sources, but this didn't yield many results. So we decided to take another approach - what if we looked for all service worker registrations that used query parameters instead? This would identify potentially vulnerable SWs, but would require further investigation to see if they were exploitable - this led to an interesting discovery ...

Service worker clobbering

We found that a major website was using <div> elements to pass information to a SW script. They were doing this by using the innerText of a <div> element with an id of "cdnDomain":

<div style="display: none;" id="cdnDomain">example.com</div>

This is bad because if you can use DOM Clobbering to clobber the variable, you could then get control over the SW domain. In fact, this is slightly different to a normal DOM Clobbering attack since the code was using document.getElementById() and innerText. If you could inject a HTML element before the <div> element then you could control the CDN domain - this would mean you could control the contents of the SW script. This could result in full control over the website's responses whilst bypassing a HTML filter, or evading CSP and escalating a reflected XSS. Here's what the code looked like:

Later the SW register method was used passing this domain:

/sw?cdnDomain=example.com

Then the SW itself was using the domain to load some scripts:

importScripts(`${n}/versionless/workbox-v${s.e}/workbox-sw.js`)

At first we thought you would require an element before the cdnDomain div in order to exploit it, however we discovered that's not necessarily the case. You can clobber the results of a document.getElementById() call if you inject a <html> or <body> tag with the same id attribute. Here's an example:

<div style=display:none id=cdnDomain>test</div>

<p>

<html id="cdnDomain">clobbered</html>

<script>

alert(document.getElementById('cdnDomain').innerText);//clobbbered

</script>

What's also interesting is that you can hide elements from innerText, so if you inject a HTML/body tag you can use styles to hide it from innerText to prevent other text from interfering with your attack:

<div style=display:none id=cdnDomain>test</div>

<p>existing text</p>

<html id="cdnDomain">clobbered</html>

<style>

p{display:none;}

</style>

<script>

alert(document.getElementById('cdnDomain').innerText);//clobbbered

</script>

We looked at SVG too and it's possible to use the <body> tag there:

<div style=display:none id=cdnDomain>example.com</div>

<svg><body id=cdnDomain>clobbered</body></svg>

<script>

alert(document.getElementById('cdnDomain').innerText)//clobbered

</script>

You need a <foreignobject> tag in order to use the HTML tag inside SVG on both Chrome and Firefox:

<div style=display:none id=cdnDomain>example.com</div>

<svg>

<foreignobject>

<html id=cdnDomain>clobbered</html>

</foreignobject>

</svg>

<script>

alert(document.getElementById('cdnDomain').innerText)//clobbered

</script>

Clobbering document.querySelector()

The same technique can be used to clobber the results of document.querySelector(). Since this function returns the first element it can find, you clobber the class name using <html> or <body> tag.

<div class=x></div>

<body class=x>

<script>

alert(document.querySelector('.x'))

</script>

Finding service worker injection with DOM Invader

In order to find SW injection you simply need to place the canary in the query string, or configure DOM Invader to inject the canary into all sources. Then DOM Invader will show the new sink called "serviceWorker.register" if it finds a vulnerable function call:

We've created a test case which demonstrates this issue. Note that this is only flagging that the query string is being passed to the SW, further investigation is required to see if this query string is parsed and then used with something like importScripts() inside the SW.

DOM Invader can help you find SW injection by manipulating the query string. However, in more complex cases or bug chains, you might want to configure DOM Invader to only show you SW registrations and have a blank canary to see all calls to it. You can do this by going to settings and entering a blank canary, then clicking "update canary". If you only want to see SW registrations, click settings again, then the general settings cog (next to the DOM Invader is on), then scroll down and select none. Then search for serviceWorker.register and enable it, this will then show you all SW registrations. You can also use a sink callback to look for question marks in the sink value.

To find these types of vulnerabilities yourself you can use the latest release of Burp Suite, currently available on the early adopter channel. If you do give it a try, and especially if you find any instances of SW injection, please let us know - we'd love your feedback.

service workers

XSS

DOM Clobbering

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
