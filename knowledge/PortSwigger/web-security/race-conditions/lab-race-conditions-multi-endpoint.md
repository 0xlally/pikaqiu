# Lab: Multi-endpoint race conditions

Source: https://portswigger.net/web-security/race-conditions/lab-race-conditions-multi-endpoint
Fetched: 2026-06-28T09:17:59.618147+00:00

Web Security Academy

Race conditions

Lab

Lab: Multi-endpoint race conditions

This lab's purchasing flow contains a race condition that enables you to purchase items for an unintended price.

To solve the lab, successfully purchase a Lightweight L33t Leather Jacket.

You can log into your account with the following credentials: wiener:peter.

Note

Solving this lab requires Burp Suite 2023.9 or higher.

Tip

When experimenting, we recommend purchasing the gift card as you can later redeem this to avoid running out of store credit.

Solution

Predict a potential collision

Log in and purchase a gift card so you can study the purchasing flow.

Consider that the shopping cart mechanism and, in particular, the restrictions that determine what you are allowed to order, are worth trying to bypass.

From the proxy history, identify all endpoints that enable you to interact with the cart. For example, a POST /cart request adds items to the cart and a POST /cart/checkout request submits your order.

Add another gift card to your cart, then send the GET /cart request to Burp Repeater.

In Repeater, try sending the GET /cart request both with and without your session cookie. Confirm that without the session cookie, you can only access an empty cart. From this, you can infer that:

The state of the cart is stored server-side in your session.

Any operations on the cart are keyed on your session ID or the associated user ID.

This indicates that there is potential for a collision.

Notice that submitting and receiving confirmation of a successful order takes place over a single request/response cycle.

Consider that there may be a race window between when your order is validated and when it is confirmed. This could enable you to add more items to the order after the server checks whether you have enough store credit.

Benchmark the behavior

Send both the POST /cart and POST /cart/checkout request to Burp Repeater.

In Repeater, add the two tabs to a new group. For details on how to do this, see Creating a new tab group

Send the two requests in sequence over a single connection a few times. Notice from the response times that the first request consistently takes significantly longer than the second one. For details on how to do this, see Sending requests in sequence.

Add a GET request for the homepage to the start of your tab group.

Send all three requests in sequence over a single connection. Observe that the first request still takes longer, but by "warming" the connection in this way, the second and third requests are now completed within a much smaller window.

Deduce that this delay is caused by the back-end network architecture rather than the respective processing time of the each endpoint. Therefore, it is not likely to interfere with your attack.

Remove the GET request for the homepage from your tab group.

Make sure you have a single gift card in your cart.

In Repeater, modify the POST /cart request in your tab group so that the productId parameter is set to 1, that is, the ID of the Lightweight L33t Leather Jacket.

Send the requests in sequence again.

Observe that the order is rejected due to insufficient funds, as you would expect.

Prove the concept

Remove the jacket from your cart and add another gift card.

In Repeater, try sending the requests again, but this time in parallel. For details on how to do this, see Sending requests in parallel.

Look at the response to the POST /cart/checkout request:

If you received the same "insufficient funds" response, remove the jacket from your cart and repeat the attack. This may take several attempts.

If you received a 200 response, check whether you successfully purchased the leather jacket. If so, the lab is solved.

Community solutions

Intigriti

Popo Hack

Find race condition vulnerabilities using Burp Suite

Try for free
