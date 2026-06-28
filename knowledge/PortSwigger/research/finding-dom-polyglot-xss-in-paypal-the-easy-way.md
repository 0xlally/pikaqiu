# Finding DOM Polyglot XSS in PayPal the Easy Way

Source: https://portswigger.net/research/finding-dom-polyglot-xss-in-paypal-the-easy-way
Fetched: 2026-06-28T09:17:25.201791+00:00

Finding DOM Polyglot XSS in PayPal the Easy Way

Gareth Heyes

Researcher

@garethheyes

Published: Wednesday, 30 June 2021 at 16:47 UTC

Updated: Wednesday, 7 September 2022 at 09:04 UTC

Introduction

Finding DOM XSS can be tricky when it's buried in thousands of lines of code. We recently developed DOM Invader to help tackle this using a combined dynamic+manual approach to vulnerability discovery, and promptly found an interesting polyglot DOM XSS affecting PayPal. In this post, we'll take you through the discovery journey, and also show how to use unintended script gadgets to bypass an allow list based CSP.

First, we used Burp's embedded browser to navigate the site and inject the canary to see which sources and sinks were used on each of the pages. When we encountered some interesting sinks, we would then send probes of characters such as <>'" along with the canary and inspect the sink to see if they were allowed. It didn't take us long to find a page that was reflecting our probes in an insecure way. Normally this would be difficult as the reflection is invisible, but with DOM Invader it was easy.

As you can see in the screenshot above our canary is being reflected inside an id attribute. If we send a double quote we can see how the value reaches the sink. But when sending a double quote, the screen goes blank. However, if we escape the double quote, then the site will not break and we can see it reaches the sink:

In HTML, backslash has no effect on the double quote - so we appear to have an XSS vulnerability. We need to confirm this though by injecting other characters which will cause JavaScript to execute. After multiple probes at this vulnerability, we noticed that the value injected had to be a valid CSS selector. So we came up with the following vector:

burpdomxss input[value='\">\<iframe srcdoc=&lt;script&gt;alert(document.domain)&llt;/script&gt;>\"']

This didn't work initially because of the CSP - but when we disabled this in Burp, we got the alert. We then reported this to PayPal on HackerOne, along with the instructions to disable CSP. To our surprise, we got the response from a HackerOne triager that:

After review, there doesn’t seem to be any security risk and/or security impact as a result of the behavior you are describing.

So apparently you need a CSP bypass to report XSS on PayPal assets. We didn't agree with this assessment and other companies like Google will reward you for XSS without a CSP bypass. But this is PortSwigger, and we don't stop there. We then began to look for ways to bypass PayPal's policy.

Bypassing CSP on PayPal

First we studied the CSP and noticed a few weak parts. In the script-src directive they were allowing certain domains like *.paypalobjects.com and *.paypal.com. They also included the 'unsafe-eval' directive which would allow the use of eval, the Function constructor and other JavaScript execution sinks:

base-uri 'self' https://*.paypal.com; connect-src 'self' https://*.paypal.com https://*.paypalobjects.com https://*.google-analytics.com https://nexus.ensighten.com https://*.algolianet.com https://*.algolia.net https://insights.algolia.io https://*.qualtrics.com; default-src 'self' https://*.paypal.com https://*.paypalobjects.com; form-action 'self' https://*.paypal.com; frame-src 'self' https://*.paypal.com https://*.paypalobjects.com https://www.youtube-nocookie.com https://*.qualtrics.com https://*.paypal-support.com; img-src 'self' https: data:; object-src 'none'; script-src 'nonce-RGYH2N1hP59U4+QwLcOaI5GgHbP19yxg1MEmKXc883wiDeAj' 'self' https://*.paypal.com https://*.paypalobjects.com 'unsafe-inline' 'unsafe-eval'; style-src 'self' block-all-mixed-content;; report-uri https://www.paypal.com/csplog/api/log/csp

Looking at the policy, the allow list and 'unsafe-eval' were probably the best targets to bypass the CSP. So we added those domains in the Burp Suite scope. You can use regexes in the scope which is super handy. Our scope looked like this:

^(?:.*[.]paypal(?:objects)?.com)$

Burp allows you to pick specific protocols in the scope - and because the policy had the 'block-all-mixed-content' directive, we only selected the HTTPS protocol.

After studying the CSP, we opened the embedded browser in Burp and began browsing the site manually - in order to pick the targets which had a lot of JavaScript assets. Once we had collected a lot of proxy history, we then used Burp's superb search functionality to find older JavaScript libraries. Conveniently, Burp allows you to search only in scope items - so we checked that box - allowing us to find assets that would bypass the CSP.

We started with searches for AngularJS, as it's pretty easy to create a CSP bypass with that. There were references to Angular but not AngularJS - and the JavaScript files we tried didn't seem to load Angular or cause exceptions. So we moved on to Bootstrap and did searches in request headers and the response body. A few instances of Bootstrap came up, and we found an older version (3.4.1).

Next we looked into Bootstrap gadgets. There were a few XSS issues on GitHub, but these affected versions 3.4.0. We looked at the Bootstrap code for a while, looking for jQuery usage but were unable to find suitable gadgets.

Rather than find gadgets in libraries, we thought about PayPal gadgets. What if PayPal had some insecure JavaScript that we could exploit? This time, instead of searching for a specific library, we searched for part of a path where libraries were hosted (such as "/c979c6f780cc5b37d2dc068f15894/js/lib/"). In the search results, we noticed a file called youtube.js and immediately spotted an obvious DOM XSS hole in it:

../' +  $(this).attr("data-id") + '.jpg"...

This file was using jQuery, so all we needed to do was include jQuery and youtube.js, exploit the vulnerability, and we had a CSP bypass. Looking at the youtube.js file we saw that it used a CSS selector to find the YouTube player element:

...$(".youtube-player").each(function() {...

So we needed to inject an element with a class of "youtube-player" and a data-id attribute that contained our jQuery XSS vector. Once we had the basis of our generic PayPal CSP bypass, all we had to do was combine it with the original injection. First we injected an iframe with a srcdoc attribute. This was because we wanted to inject an external script - but because this was a DOM based vulnerability, scripts won't execute. But with srcdoc they will:

input[value='\">\<iframe srcdoc=

Notice that we need to ensure it's a valid selector by escaping double quotes, and assigning single quotes for the value part of the selector. Then we can inject our scripts, which point to jQuery and the YouTube gadget:

&lt;script/src=https://www.paypalobjects.com/web/res/28f/c979c6f780cc5b37d2dc068f15894/js/lib/jquery-2.2.4.min.js&gt;&lt;/script&gt;&lt;script/src=https://www.paypalobjects.com/web/res/28f/c979c6f780cc5b37d2dc068f15894/js/lib/youtube.js&gt;&lt;/script&gt;

Notice that we have to HTML encode the vector - because we don't want it to close the srcdoc attribute with a > character. We avoid using spaces for the same reason. Then we use the YouTube gadget to inject a script, which jQuery converts and executes. Again we need to HTML encode the vector, give it the correct class name, and use the data-id attribute to inject our vector. Notice that we use an encoded single quote to avoid the attribute from breaking. We have to double HTML encode the double quote, because the srcdoc will decode the HTML, and the data-id attribute will decode when it's rendered in the iframe - so double encoding makes sure the quote is there when it injects into the YouTube gadget. Finally, we clean up by using a single line comment to ensure the script ignores anything after the inject - finishing the CSS selector with a double quote and single quote:

<div/class=youtube-player data-id=&apos;&amp;quot;&gt;&lt;script&gt;alert(document.domain)//&apos;&gt;>\"']

The final proof of concept can be found here:

Proof of concept

Here is a screenshot of the PoC in all its glory:

This is pretty cool - a complete CSP bypass on all of PayPal - but is it needed? Well, as we've seen, jQuery is CSP's nemesis. It converts scripts, and will happily execute them with policies, using the 'unsafe-eval' directive. Looking at the original XSS hole, it appears to be a jQuery selector. We can therefore inject a script, and it will be converted by jQuery - so a separate CSP bypass isn't required. Therefore, we can simplify the injection to the following:

input[value='\">\<script>alert(1)//>\"']

Proof on concept with smaller vector

Conclusion

Allow list policies are definitely not secure - especially when you have a multitude of scripts/libraries that can be abused. Fixing XSS even when user input is typically not expected can help prevent unintentional script gadgets.

You should never rely solely on a CSP to protect you from XSS. While it's part of your defence, it's not the only barrier available. If you run a bug bounty program we recommend you fix XSS regardless of a CSP. If you don't use DOM Invader, you'll miss out on serious XSS vulnerabilities in your application.

XSS

polyglot

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
