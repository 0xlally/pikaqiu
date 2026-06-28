# Lab: Low-level logic flaw

Source: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-low-level
Fetched: 2026-06-28T09:17:56.003267+00:00

Web Security Academy

Business logic vulnerabilities

Examples

Lab

Lab: Low-level logic flaw

This lab doesn't adequately validate user input. You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price. To solve the lab, buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter

Hint

You will need to use Burp Intruder (or Turbo Intruder) to solve this lab.

To make sure the price increases in predictable increments, we recommend configuring your attack to only send one request at a time. In Burp Intruder, you can do this from the resource pool settings using the Maximum concurrent requests option.

Solution

With Burp running, log in and attempt to buy the leather jacket. The order is rejected because you don't have enough store credit. In the proxy history, study the order process. Send the POST /cart request to Burp Repeater.

In Burp Repeater, notice that you can only add a 2-digit quantity with each request. Send the request to Burp Intruder.

Go to Intruder and set the quantity parameter to 99.

In the Payloads side panel, select the payload type Null payloads. Under Payload configuration, select

Continue indefinitely. Start the attack.

While the attack is running, go to your cart. Keep refreshing the page every so often and monitor the total price. Eventually, notice that the price suddenly switches to a large negative integer and starts counting up towards 0. The price has exceeded the maximum value permitted for an integer in the back-end programming language (2,147,483,647). As a result, the value has looped back around to the minimum possible value (-2,147,483,648).

Clear your cart. In the next few steps, we'll try to add enough units so that the price loops back around and settles between $0 and the $100 of your remaining store credit. This is not mathematically possible using only the leather jacket. Note that the price of the jacket is stored in cents (133700).

Create the same Intruder attack again, but this time under Payload configuration, choose to generate exactly 323 payloads.

Click Resource pool to open the Resource pool tab. Add the attack to a resource pool with the

Maximum concurrent requests set to 1. Start the attack.

When the Intruder attack finishes, go to the POST /cart request in Burp Repeater and send a single request for 47 jackets. The total price of the order should now be -$1221.96.

Use Burp Repeater to add a suitable quantity of another item to your cart so that the total falls between $0 and $100.

Place the order to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find business logic vulnerabilities using Burp Suite

Try for free
