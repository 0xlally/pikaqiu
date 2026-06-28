# Lab: High-level logic vulnerability

Source: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-high-level
Fetched: 2026-06-28T09:17:55.872231+00:00

Web Security Academy

Business logic vulnerabilities

Examples

Lab

Lab: High-level logic vulnerability

This lab doesn't adequately validate user input. You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price. To solve the lab, buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter

Solution

With Burp running, log in and add a cheap item to your cart.

In Burp, go to "Proxy" > "HTTP history" and study the corresponding HTTP messages. Notice that the quantity is determined by a parameter in the POST /cart request.

Go to the "Intercept" tab and turn on interception. Add another item to your cart and go to the intercepted POST /cart request in Burp.

Change the quantity parameter to an arbitrary integer, then forward any remaining requests. Observe that the quantity in the cart was successfully updated based on your input.

Repeat this process, but request a negative quantity this time. Check that this is successfully deducted from the cart quantity.

Request a suitable negative quantity to remove more units from the cart than it currently contains. Confirm that you have successfully forced the cart to contain a negative quantity of the product. Go to your cart and notice that the total price is now also a negative amount.

Add the leather jacket to your cart as normal. Add a suitable negative quantity of the another item to reduce the total price to less than your remaining store credit.

Place the order to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Popo Hack

Find business logic vulnerabilities using Burp Suite

Try for free
