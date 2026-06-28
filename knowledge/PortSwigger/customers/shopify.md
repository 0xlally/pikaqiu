# Customer case study

Source: https://portswigger.net/customers/shopify
Fetched: 2026-06-28T09:17:04.051626+00:00

Customer case study

Shopify

Automating web security testing at scale with Burp Suite DAST.

Introduction

As an all-in-one commerce platform, Shopify enables anyone to start, run, and grow a business anywhere. In total, over 1,700,000 businesses - in 175 countries - have collectively made more than $277 billion USD in sales using Shopify.

Shopify enables third parties to develop apps for its platform - allowing the addition of features and functionality. Thousands of such apps are now available in the Shopify App Store - and this growth has led to an increasing need for security testing. In order to scale its testing processes, Shopify has implemented automated scanning with Burp Suite DAST. This allows it to deliver effective security at scale.

Leanne Shapton is an application security engineer at Shopify.

Key benefits

Leanne identified a number of key benefits that Shopify gains by using Burp Suite DAST:

Burp Suite DAST enables Shopify to automate dynamic web application security testing across thousands of partner applications.

Burp Suite DAST can find common web security vulnerabilities like cross-site request forgery (CSRF) and cross-site scripting (XSS).

Shopify's AppSec team was already familiar with using Burp Suite Professional for manual security testing, so automating with Burp Suite DAST was a natural progression.

"Burp Suite DAST just met our needs the most."

How is Shopify using Burp Suite DAST?

In the case of third-party applications, a major part of Shopify's testing regime involves checking for common web security vulnerabilities such as CSRF and XSS. Shopify carries out such testing as a matter of course for all partner applications.

As its AppSec testing needs have grown, Shopify has moved away from a manual security testing model, toward increased automation when reviewing partner applications. When it comes to automating vulnerability checks like the ones above, Shopify chose a cloud-based implementation of Burp Suite DAST.

Shopify's AppSec team uses its own custom Ruby application to carry out a number of security tests (such as SSL validation, HMAC verifications, port scanning, etc.) - and Burp Suite DAST works within this infrastructure. So, when an automated third-party application security review is started, Shopify's application also initializes a Burp Suite DAST scan.

" ... Burp Suite DAST will then start scanning the app and come back to us and raise any potential common web security vulnerabilities."

Why did Shopify choose Burp Suite DAST over other automated web vulnerability scanners?

Shopify's Application Security team is continually adapting to meet new challenges, and it uses forward-thinking strategies like bug bounty programs to ensure that those challenges are met.

When it came to selecting a web vulnerability scanner to use in its automated third party application security reviews, they tested multiple products - including Burp Suite DAST. Following their tests, Shopify found that Burp Suite DAST met its needs the most. Shopify also benefits from the fact that most of its AppSec engineers were existing users of Burp Suite Professional (having used it for manual testing) - meaning that they were already familiar with the Burp Suite ecosystem.

Because third party Shopify applications are written and hosted by developers outside Shopify, Shopify cannot utilize a static (SAST) approach (where a scanner reviews application source code). Burp Suite DAST's dynamic (DAST)-based approach instead views an application from the outside (just as an attacker would), and can be very effective in this situation.

See Leanne discuss Shopify's use of Burp Suite DAST, in a PortSwigger/HackerOne webinar.

For more information on the scanning technologies used in Burp Suite software, please see our Burp Scanner page.

" ... most of my team right now is most familiar with Burp, so it's what we knew."

About Burp Suite DAST

Burp Suite DAST is the enterprise-enabled web vulnerability scanner that lets you scan it all. Secure your whole web portfolio, catch critical bugs before code gets shipped, and unleash AppSec's expertise to supercharge engineering.

Product Overview

Find out more

Features

Find out more

Resources

Find out more

Get started for free

Begin your fully-featured trial of Burp Suite DAST

Indefinitely scalable

Unlimited users

Free technical support

Try for free
