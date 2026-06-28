# Lab: Excessive trust in client-side controls

Source: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-excessive-trust-in-client-side-controls
Fetched: 2026-06-28T09:17:55.373403+00:00

Web Security Academy

Business logic vulnerabilities

Examples

Lab

Lab: Excessive trust in client-side controls

This lab doesn't adequately validate user input. You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price. To solve the lab, buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter

Solution

With Burp running, log in and attempt to buy the leather jacket. The order is rejected because you don't have enough store credit.

In Burp, go to "Proxy" > "HTTP history" and study the order process. Notice that when you add an item to your cart, the corresponding request contains a price parameter. Send the POST /cart request to Burp Repeater.

In Burp Repeater, change the price to an arbitrary integer and send the request. Refresh the cart and confirm that the price has changed based on your input.

Repeat this process to set the price to any amount less than your available store credit.

Complete the order to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Popo Hack

Find business logic vulnerabilities using Burp Suite

Try for free
