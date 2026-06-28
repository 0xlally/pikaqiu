# Lab: Insufficient workflow validation

Source: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-insufficient-workflow-validation
Fetched: 2026-06-28T09:17:55.987271+00:00

Web Security Academy

Business logic vulnerabilities

Examples

Lab

Lab: Insufficient workflow validation

This lab makes flawed assumptions about the sequence of events in the purchasing workflow. To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter

Solution

With Burp running, log in and buy any item that you can afford with your store credit.

Study the proxy history. Observe that when you place an order, the POST /cart/checkout request redirects you to an order confirmation page. Send GET /cart/order-confirmation?order-confirmation=true to Burp Repeater.

Add the leather jacket to your basket.

In Burp Repeater, resend the order confirmation request. Observe that the order is completed without the cost being deducted from your store credit and the lab is solved.

Community solutions

Rana Khalil

Michael Sommer

Find business logic vulnerabilities using Burp Suite

Try for free
