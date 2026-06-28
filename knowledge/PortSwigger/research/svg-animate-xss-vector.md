# SVG animate XSS vector

Source: https://portswigger.net/research/svg-animate-xss-vector
Fetched: 2026-06-28T09:17:29.595550+00:00

SVG animate XSS vector

Gareth Heyes

Researcher

@garethheyes

Published: Tuesday, 28 January 2020 at 14:54 UTC

Updated: Tuesday, 8 September 2020 at 12:22 UTC

As part of my recent research into obfuscating XSS payloads to bypass WAFs, I was looking at the SVG elements set, animate, animateTransform and animateMotion. I added a couple of known XSS vectors to the cheat sheet using those tags. Then focusing on the animate tag I found an interesting XSS vector using the values attribute. The values attribute lets you specify a number of values for an SVG animation separated by semi-colons:

<svg><animate values="1;2;3" /></svg>

I wondered if I could include a JavaScript URL in the middle of the values attribute - that might confuse a lot of WAFs looking for the JavaScript protocol. The problem was, if I didn't set a duration then the first value would always be shown and if I did set a duration then the URL would cycle through the values and therefore not always show the JavaScript URL. Looking at the SVG specification I noticed that there's a keyTimes attribute that allows you to control the pacing of the animation for each of the values. Using this with the repeatCount attribute would enable the animation to always show the JavaScript URL. Here is the final XSS vector:

<svg><animate xlink:href=#xss attributeName=href dur=5s repeatCount=indefinite keytimes=0;0;1 values="https://portswigger.net?&semi;javascript:alert(1)&semi;0" /><a id=xss><text x=20 y=20>XSS</text></a>

We have released an interactive XSS lab built around this technique in the Web Security Academy so you can try it out for yourself:

LAB

SVG animate lab

This vector will also shortly be integrated into our XSS cheat sheet. Enjoy!

Cross Site Scripting

cheatsheet

SVG

vectors

Back to all articles

Related Research

New crazy payloads in the URL Validation Bypass Cheat Sheet

29 October 2024

New crazy payloads in the URL Validation Bypass Cheat Sheet

Our favourite community contributions to the XSS cheat sheet

03 October 2022

Our favourite community contributions to the XSS cheat sheet

New XSS vectors

20 April 2022

New XSS vectors

DOM Clobbering strikes back

06 February 2020

DOM Clobbering strikes back
