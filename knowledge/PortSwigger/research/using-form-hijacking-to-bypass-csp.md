# Using form hijacking to bypass CSP

Source: https://portswigger.net/research/using-form-hijacking-to-bypass-csp
Fetched: 2026-06-28T09:17:31.871210+00:00

Using form hijacking to bypass CSP

Gareth Heyes

Researcher

@garethheyes

Published: Tuesday, 5 March 2024 at 14:55 UTC

Updated: Tuesday, 5 March 2024 at 14:55 UTC

In this post we'll show you how to bypass CSP by using an often overlooked technique that can enable password theft in a seemingly secure configuration.

What is form hijacking?

Form hijacking isn't really a widely known technique; the idea is you have a HTML injection vulnerability that is protected by CSP. Then you use the HTML injection to inject your own form action by using the formaction attribute or injecting your own form to send data to the attackers server. Over eager password managers will also help fill in credentials with injected input elements making the attack pretty serious.

Real world examples

We found a

real world example of this on Infosec Mastodon

where they used a fork of Mastodon that didn't filter HTML correctly. An attacker could then use form hijacking to send credentials to their server after Chrome's password manager had automatically filled them in. The end result was a user would see a post in Infosec Mastodon, click what looked like part of the interface but actually would send the user's credentials to an attacker's server.

That was over a year ago and then...we got an excellent report submitted by

Johan Carlsson

to our very own bug bounty program.

In the report he showed how we allowlisted some Google script resources and he could use that to bypass CSP by injecting AngularJS. After we fixed that he also pointed out that we didn't protect against form hijacking! Thankfully, this was just a bypass of our CSP as we didn't have a HTML injection vulnerability but it was good to receive a report that hardened our security so we gave him a $1,500 bounty.

Why does it happen?

The form-action directive was specified in version 2 of CSP. Unfortunately, default-src does not cover form actions. This means if you overlook this directive then your CSP will be vulnerable to form hijacking and this is exactly what happened in the case of the Infosec Mastodon and even our own site. Therefore this post was meant to spread awareness of this issue and hopefully harden many CSP's out there.

Scanning your CSP

We've recently released some new passive scan checks for CSP issues in Burp. These checks will find issues like form hijacking, allowlisted resources, untrusted script execution, untrusted style execution, malformed syntax, clickjacking and non-enforced CSP. I'll go through each one so you can understand how to fix these issues if you encounter them.

Form hijacking

If you don't use form actions on your site (which is pretty common these days in modern apps) you can specify the directive with the 'none' keyword, this is the safest configuration since an attacker won't be able to post forms to an external location. If your site requires "same site" form actions then you can use the 'self' keyword.  Lastly if you want to allow an external location you can specify a URL but bear in mind that an attacker will be able to post to that location too if they find a HTML injection vulnerability. Examples of each configuration are given below:

Content-Security-Policy: form-action 'none'

Content-Security-Policy: form-action 'self'

Content-Security-Policy: form-action https://portswigger.net

Allowlisted resources

It's bad practice to use allowlisted URLs because they can be used to for

script gadgets

. This scan check will look at the script directives and see if any domains are allowlisted. To fix this you are advised to use a secure random nonce to protect your scripts:

Content-Security-Policy: script-src 'nonce-RANDOM';

Untrusted script execution

This issue points out when you use 'unsafe-inline' in your script directives. As the name suggests this opens your policy up to cross site scripting attacks because you can inject an inline script tag. It also covers when the policy allows wildcard domains, data: URLs, unsafe-eval and weak nonce randomisation. Secure random nonces are the best way to resolve this issue:

Content-Security-Policy: script-src 'nonce-RANDOM';

Untrusted style execution

Style based injections can often have a significant impact if there is sensitive information or tokens on the page. This issue points out if you use 'unsafe-inline' in conjunction with style based directives. Any wildcard domains, data: URLs and weak nonce randomisation will also be reported. To fix this again use nonces in your style directives:

Content-Security-Policy: style-src 'nonce-RANDOM';

Malformed syntax

When CSP encounters some malformed syntax it will ignore the value or maybe even the directive. This scan check looks for malformed CSP syntax and reports any directives or values that do not conform to the specification. We ran a scan on a large number of sites and found lots of common mistakes that this scan check will help iron out. When some invalid syntax is found the directive or value will be displayed in the issue detail. To fix this you should consult the CSP specification and ensure the syntax is correct.

Clickjacking

This check will check X-Frame-Options and the frame-ancesters directive in CSP and inform you if your application allows it to be framed. X-Frame-Options is now deprecated so we recommend you use the frame-ancestors directive to mitigate clickjacking attacks like this:

Content-Security-Policy: frame-ancestors 'none';

Non-enforced CSP

Burp will also inform you if your policy is in report only mode, this means the policy won't be enforced but will log the results. This is often used to transition to an enforced policy but can often be overlooked by mistake. It will also report an issue on a per site basis if CSP does not exist to encourage developers to deploy one.

In the wild

Whilst testing Burp we scanned our bug bounty pipeline and found lots of common mistakes that developers make when deploying CSP. We are going to highlight some of them below to help you avoid them.

Incorrect protocol

Some web sites forget the colon quite a lot when deploying.

Content-Security-Policy: script-src 'self' https

It should be:

Content-Security-Policy: script-src 'self' https:

You should avoid doing this of course because an attacker would be able to inject a script resource from any domain with TLS provided the target site is vulnerable to XSS.

Missing semicolon

It's quite common to forget to include a semicolon. This can result in the directive name being used as a value which would mean the policy wouldn't enforce this directive!

This is incorrect:

frame-ancestors 'self' https://example.com default-src 'none'

It should be:

frame-ancestors 'self' https://example.com; default-src 'none'

Incorrect value

In CSP all special directive values are quoted. It's quite common to see values not quoted and also illegal values like the following:

Content-Security-Policy: frame-ancestors DENY

There is no DENY value in the frame-ancestors directive value. It should be:

Content-Security-Policy: frame-ancestors 'none'

None quoted hashes or nonces

A lot of sites also forget to include quotes around hashes or nonces. I think this is quite common because traditionally special values are quoted whereas non keywords are not. So it's quite understandable that they get confused:

This is incorrect:

Content-Security-Policy: script-src sha512-BASE64HASH

It should be:

Content-Security-Policy: script-src 'sha512-BASE64HASH'

Burp release

We hope that this post spreads awareness of form hijacking and common CSP mistakes. If you want to scan your own site for these issues you can get Burp on the early adopter channel. Happy hunting!

csp

Burp Suite

Form Hijacking

Back to all articles

Related Research

Repeater Strike: manual testing, amplified

15 July 2025

Repeater Strike: manual testing, amplified

Document My Pentest: you hack, the AI writes it up!

23 April 2025

Document My Pentest: you hack, the AI writes it up!

Shadow Repeater

AI-enhanced manual testing

20 February 2025

Shadow Repeater

AI-enhanced manual testing

Bypassing CSP via DOM clobbering

05 June 2023

Bypassing CSP via DOM clobbering
