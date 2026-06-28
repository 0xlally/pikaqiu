# Lab: Flawed enforcement of business rules

Source: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-flawed-enforcement-of-business-rules
Fetched: 2026-06-28T09:17:55.655951+00:00

Web Security Academy

Business logic vulnerabilities

Examples

Lab

Lab: Flawed enforcement of business rules

This lab has a logic flaw in its purchasing workflow. To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter

Solution

Log in and notice that there is a coupon code, NEWCUST5.

At the bottom of the page, sign up to the newsletter. You receive another coupon code, SIGNUP30.

Add the leather jacket to your cart.

Go to the checkout and apply both of the coupon codes to get a discount on your order.

Try applying the codes more than once. Notice that if you enter the same code twice in a row, it is rejected because the coupon has already been applied. However, if you alternate between the two codes, you can bypass this control.

Reuse the two codes enough times to reduce your order total to less than your remaining store credit. Complete the order to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find business logic vulnerabilities using Burp Suite

Try for free
