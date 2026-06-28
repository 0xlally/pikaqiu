# Bypassing CSP with policy injection

Source: https://portswigger.net/research/bypassing-csp-with-policy-injection
Fetched: 2026-06-28T09:17:21.452734+00:00

Bypassing CSP with policy injection

Gareth Heyes

Researcher

@garethheyes

Published: Wednesday, 5 June 2019 at 13:10 UTC

Updated: Friday, 4 September 2020 at 14:31 UTC

Whilst testing PayPal looking for ways to bypass CSP and mixed content protection I found an interesting behaviour. PayPal was putting a GET parameter called token inside the report-uri directive of their CSP. I found that by changing the token parameter it was possible to inject directives into the policy. Most browsers simply skip over invalid CSP directives, but Edge behaves differently. If it encounters invalid syntax, Edge will drop the entire policy! I fuzzed Edge to find ways of breaking the CSP with as few characters as possible, and found you could simply use a semi-colon and an underscore. So if you loaded the following URL:

https://www.paypal.com/webapps/xoonboarding?values=etc&token=SOMETOKEN;_

You would be served this CSP header:

Content-Security-Policy: default-src 'self' https://*.paypal.com https://*.paypal.com:* https://*.paypalobjects.com 'unsafe-eval';connect-src 'self' https://*.paypal.com https://nexus.ensighten.com https://*.paypalobjects.com;frame-src 'self' https://*.paypal.com https://*.paypalobjects.com https://*.cardinalcommerce.com;script-src https://*.paypal.com https://*.paypalobjects.com 'unsafe-inline' 'unsafe-eval';style-src 'self' https://*.paypal.com https://*.paypalobjects.com 'unsafe-inline';img-src https: data:;object-src 'none'; report-uri /webapps/xoonboarding/api/log/csp?token=SOMETOKEN;_

And Edge would drop the entire policy.

To see it in action I created a simple PoC:

Edge CSP bypass using policy injection

Of course hardly anyone uses Edge, so then I thought about Chrome. Since Chrome ignores invalid directives and our injection happens at the end of the policy, I needed a way to override a directive. I found a recently proposed directive called "script-src-elem". This directive allows you to control just script blocks and was created so that you can allow event handlers but block script elements for example:

Content-Security-Policy: script-src-elem 'none'; script-src-attr 'unsafe-inline'

<script>alert("This will be blocked")</script>

<a href="#" onclick="alert('This will be allowed')">test</a>

The interesting thing about this directive is that it will overwrite existing script-src directives! So you can use it to bypass CSP provided you have policy injection. Here is a PoC that works on Chrome:

Chrome CSP bypass using policy injection

PayPal awarded me $900 for this bug which I thought was quite generous for a mitigation bypass.

Visit our Web Security Academy to learn more about cross-site scripting (XSS)

csp

Back to all articles

Related Research

Using form hijacking to bypass CSP

05 March 2024

Using form hijacking to bypass CSP

Bypassing CSP via DOM clobbering

05 June 2023

Bypassing CSP via DOM clobbering

Ambushed by AngularJS: a hidden CSP bypass in Piwik PRO

28 April 2023

Ambushed by AngularJS: a hidden CSP bypass in Piwik PRO

Stealing passwords from infosec Mastodon - without bypassing CSP

15 November 2022

Stealing passwords from infosec Mastodon - without bypassing CSP
