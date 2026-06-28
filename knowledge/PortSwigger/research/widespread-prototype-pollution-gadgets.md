# Widespread prototype pollution gadgets

Source: https://portswigger.net/research/widespread-prototype-pollution-gadgets
Fetched: 2026-06-28T09:17:32.550936+00:00

Widespread prototype pollution gadgets

Gareth Heyes

Researcher

@garethheyes

Published: Wednesday, 22 June 2022 at 13:17 UTC

Updated: Friday, 28 October 2022 at 13:04 UTC

We recently launched a new version of DOM Invader that can find Client-Side Prototype Pollution (CSPP).

If you're not already familiar with Client-Side Prototype Pollution, check out the post above. Just to recap, a successful CSPP exploit requires two components:

A way to poison the prototype, referred to as a prototype pollution source.

A way to use a poisoned prototype for an actual exploit, referred to as a prototype pollution gadget.

In this post we're going to talk about CSPP gadgets in browser APIs and how we found them in common libraries too.

Prototype pollution gadgets in browser JavaScript APIs

I was quite surprised to discover that some JavaScript APIs in the browser contain prototype pollution gadgets. Functions that accept objects as arguments can be polluted just like any other object. The fetch function is one such example. When calling fetch, there is an optional argument that accepts an object - this allows you to control headers, body parameters, etc. If a site doesn't specify one of those properties, then it's possible to use prototype pollution to control them provided there is a prototype pollution source:

Object.prototype.body = "foo=bar";

fetch('/', {method:"POST"})

Even ES5 functions such as Object.defineProperty are vulnerable - if a developer does not specify a "value" property, then prototype pollution sources can be used to overwrite properties! Consider the following example:

let myObject = {property:"Existing property value"};

Object.defineProperty(myObject,'property', {configurable:false,writable:false} );

myObject.property = 'Should fail';

alert(myObject.property);//Existing property value

If you use prototype pollution on the value property, then you can overwrite "property" even though it's been configured as not writable:

Object.prototype.value='overwritten';

let myObject = {property: "Existing property value"};

Object.defineProperty(myObject,'property', {configurable:false,writable:false});

alert(myObject.property);//overwritten!

So even though the property has been made unconfigurable and unwritable, by using a prototype pollution source we can poison the descriptor used by Object.defineProperty to overwrite the property value. This is because if you don't specify a "value" property on the descriptor then the JavaScript engine uses the Object.prototype.

Another interesting property to pollution is configurable. It's quite common for apps/sandboxes to use defineProperty without defining a configurable property in the descriptor. This is because when not included it makes the property un-configurable. Polluting configurable makes the property redefinable later this could possibly lead to a JavaScript sandbox escape since you can modify the configurability of the property.

Local storage

I later realised that localStorage/sessionStorage will also inherit from the Object.prototype which means if a site has a client-side prototype pollution vulnerability and the site uses a getter not the get() method then it's possible to control the localStorage value.

Object.prototype.foo = 'bar';

localStorage.get('foo');//not vulnerable

localStorage.foo//vulnerable and will return bar

Google analytics

Whilst testing various bug bounty sites, DOM Invader was reporting a gadget called "hitCallback" that was sent to a "setTimeout" sink. We traced this back to Google Analytics using the setTimeout sink, and discovered that "c" contains the value from the prototype pollution gadget:

this.Ja = function() {

!b.fb && c && setTimeout(c, 10)

}

DOM Invader shows the "hitCallback" gadget inside the "setTimeout" sink:

So for any website that uses this version of Google Analytics, and has a client-side prototype pollution source, it would be possible to use this gadget to gain DOM XSS on the target website. We successfully exploited this gadget on a well known game site, and others.

Google tag manager

We've seen many websites, using Google tag manager, have a resultant vulnerable gadget "sequence" that ends up in an eval sink. There is also another gadget called "event_callback" which ends up in a "setTimeout" sink. We reported these to Google but they claim it's the customer's responsibility to ship code that doesn't contain prototype pollution sources. Personally, I think they should also fix gadgets where possible as a defence in depth measure. Quite hilariously, our own Web Security Academy site has one of these gadgets but thankfully no prototype pollution source. We successfully exploited this gadget on a Wordpress domain which has now been fixed as well as a few other sites.

The Wordpress exploit looked like this:

https://es.wordpress.org/patterns/?__proto__%5Bsequence%5D=alert%28document.domain%29-

The trailing "-" is required because the value ends up in a JavaScript expression alongside an integer.

Adobe dynamic tag management

Sergey Bobrov did an excellent job of documenting various CSPP vulnerabilities. On the Github page, I noticed Adobe's dynamic tag management scripts and decided to scan them for gadgets. DOM Invader found multiple undocumented gadgets, as well as the existing documented ones. The gadget "cspNonce" was being used in an innerHTML sink, as well as "bodyHiddenStyle", this hit an innerHTML sink too but has an existing <style> block before the value was written.

There were various other gadgets in the context of script.src where you didn't have full control over the URL, but DOM Invader highlighted an interesting gadget. In the "trackingServerSecure" gadget it found, you couldn't control the protocol but could control the host - this could lead to DOM XSS:

Conclusion

When using browser APIs that allow objects in arguments, care must be taken to ensure that you don't expose gadgets that can be later exploited by CSPP. A good defence in depth measure is to use objects with a null prototype when using these APIs. If you're writing or using a JavaScript library, it would be a good idea to scan it for gadgets before deploying it.

Client-side prototype pollution

XSS

DOM Invader

Gadgets

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
