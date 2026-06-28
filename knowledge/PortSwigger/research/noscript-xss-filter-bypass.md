# Noscript XSS filter bypass

Source: https://portswigger.net/research/noscript-xss-filter-bypass
Fetched: 2026-06-28T09:17:27.784063+00:00

Noscript XSS filter bypass

Gareth Heyes

Researcher

@garethheyes

Published: Tuesday, 28 July 2015 at 13:47 UTC

Updated: Friday, 14 June 2019 at 12:00 UTC

I thought I'd take a look at the Noscript's XSS filter and see if I could come up with a bypass. The filter is pretty impressive, it was tough to find one. I noticed that it allows function calls to user defined functions such as a, so a vector of ',a(1),' would work fine. This isn't exploitable since you need a function on the page that does something dangerous with the arguments but it gave me a clue how to get round the filter. It was time to fire up Hackvertor and have a look which methods might have been forgotten.

I inspected an object literal and found __defineSetter__. This would work on window since every object has the method. Define setter allows you to set a property with the first argument and the function you want to call in the second argument.

Because __defineSetter__ is a method of the window object you do not need to specify window when calling it. I tried an injection of ',__defineSetter__('x',alert),x=1,' and it worked perfectly bypassing Noscript's XSS filter check in script context. The output of the page would look like this:

<script>x = '',__defineSetter__('x',alert),x=1,'';</script>

Define setter is called on window with a property of x, alert is then called when an assignment of x occurs with an argument of 1.

You can also call arbitrary code by changing the alert to eval and the assignment to name. Using name as the assignment allows you to send a payload across domains using the window.name property. Usually you use an iframe with a name attribute of the payload you wish to execute then reuse that payload using the "name" property in the injected site. An example of that is below:

<iframe name=alert(1) src="//somedomain?x=',__defineSetter__('x',eval),x=name,'"></iframe>

The filter has now been patched and the vector no longer works.

Visit our Web Security Academy to learn more about cross-site scripting (XSS)

Back to all articles

Related Research

05 February 2026

06 January 2026

The Fragile Lock:

Novel Bypasses For SAML Authentication

10 December 2025

The Fragile Lock:

Novel Bypasses For SAML Authentication

Introducing HTTP Anomaly Rank

11 November 2025

Introducing HTTP Anomaly Rank
