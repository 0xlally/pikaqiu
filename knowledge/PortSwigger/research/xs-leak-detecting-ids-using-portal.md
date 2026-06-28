# XS-Leak: Detecting IDs using Portal

Source: https://portswigger.net/research/xs-leak-detecting-ids-using-portal
Fetched: 2026-06-28T09:17:33.613383+00:00

XS-Leak: Detecting IDs using Portal

Gareth Heyes

Researcher

@garethheyes

Published: Thursday, 14 November 2019 at 15:58 UTC

Updated: Tuesday, 8 September 2020 at 12:26 UTC

Following up on my XS-Leak research I thought it would be cool to detect applications by identifying distinctive tag IDs on a web application. The problem is that our technique relies on framing the target website, and many web applications such as phpMyAdmin have the X-Frame-Options header.

Chrome has experimental support for the portal tag which is like an iframe but doesn't allow user interaction, and more importantly doesn't take into account the X-Frame-Options header! Michał Bentkowski did some research in this area. Although the portal element doesn't allow user interaction, it does allow focus events, I can use this to bypass the X-Frame-Options header and see if the portal gets focus and therefore identify the application. In order for this to work you need to enable portals in Chrome by going to about:flags, search for Portal and then enable the experiment. The proof of concept is pretty simple, I just have a onblur event and a portal element that contains a phpMyAdmin specific ID in the hash, this will then only focus when that ID exists. The code looks like this:

<body onblur="alert('phpMyAdmin detected!')"><portal src="https://demo.phpmyadmin.net/master-config/index.php?route=/server/databases#text_create_db"></portal></body>

Proof of concept

Some readers may be feeling smug because they have disabled JavaScript, so then I thought about doing the same thing without JavaScript. CSS has a :focus selector and a :not selector which you can use to simulate a blur event. Using the :not selector with :focus you can then make a request or show a specific element. In this case I show "phpMyAdmin detected", but I could easily use an image to trigger a cross-domain request instead:

<style>

.hidden {

display: none;

}

.x:focus {

background-color:#000;

}

.x:not(:focus) {

background-color:red;

}

.x:not(:focus) + div {

display: block;

}

</style>

<input class="x" autofocus>

<div class="hidden">phpMyAdmin detected</div>

<portal src="https://demo.phpmyadmin.net/master-config/index.php?route=/server/databases#text_create_db">

</iframe>

The :not selector is combined with the adjacent sibling selector (+) which will show the div element adjacent to the input element when the input element loses focus.

Proof of concept

XS-Leak

XS-Leaks

Portal

Back to all articles

Related Research

XS-Leak: Leaking IDs using focus

08 October 2019

XS-Leak: Leaking IDs using focus
