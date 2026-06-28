# Lab: Limit overrun race conditions

Source: https://portswigger.net/web-security/race-conditions/lab-race-conditions-limit-overrun
Fetched: 2026-06-28T09:17:59.604946+00:00

Web Security Academy

Race conditions

Lab

Lab: Limit overrun race conditions

This lab's purchasing flow contains a race condition that enables you to purchase items for an unintended price.

To solve the lab, successfully purchase a Lightweight L33t Leather Jacket.

You can log in to your account with the following credentials: wiener:peter.

For a faster and more convenient way to trigger the race condition, we recommend that you solve this lab using the Trigger race conditions custom action. This is only available in Burp Suite Professional.

Note

Solving this lab requires Burp Suite 2023.9 or higher.

Solution - Burp Suite Professional

Predict a potential collision

Log in and buy the cheapest item possible, making sure to use the provided discount code so that you can study the purchasing flow.

Consider that the shopping cart mechanism and, in particular, the restrictions that determine what you are allowed to order, are worth trying to bypass.

In Burp, from the proxy history, identify all endpoints that enable you to interact with the cart. For example, a POST /cart request adds items to the cart and a POST /cart/coupon request applies the discount code.

Try to identify any restrictions that are in place on these endpoints. For example, observe that if you try applying the discount code more than once, you receive a Coupon already applied response.

Make sure you have an item to your cart, then send the GET /cart request to Burp Repeater.

In Repeater, try sending the GET /cart request both with and without your session cookie. Confirm that without the session cookie, you can only access an empty cart. From this, you can infer that:

The state of the cart is stored server-side in your session.

Any operations on the cart are keyed on your session ID or the associated user ID.

This indicates that there is potential for a collision.

Consider that there may be a race window between when you first apply a discount code and when the database is updated to reflect that you've done this already.

Benchmark the behavior

Make sure there is no discount code currently applied to your cart.

Send the request for applying the discount code (POST /cart/coupon) to Repeater.

In Repeater, send the POST /cart/coupon request twice.

Observe that the first response confirms that the discount was successfully applied, but the second response rejects the code with the same Coupon already applied message.

Probe for clues

Remove the discount code from your cart.

In Repeater, open the Custom actions side panel.

Click New > From template, then select Trigger race condition.

Save the template to the Custom actions side panel without making any modifications.

Click beside the Trigger race condition custom action. The request is sent 20 times in parallel.

In the browser, refresh your cart and confirm that the 20% reduction has been applied more than once, resulting in a significantly cheaper order.

Prove the concept

Remove the applied codes and the arbitrary item from your cart and add the leather jacket to your cart instead.

Resend the group of POST /cart/coupon requests in parallel.

Refresh the cart and check the order total:

If the order total is still higher than your remaining store credit, remove the discount codes and repeat the attack.

If the order total is less than your remaining store credit, purchase the jacket to solve the lab.

Solution - Burp Suite Community Edition

Predicting a potential collision

Log in and buy the cheapest item possible, making sure to use the provided discount code so that you can study the purchasing flow.

Consider that the shopping cart mechanism and, in particular, the restrictions that determine what you are allowed to order, are worth trying to bypass.

In Burp, from the proxy history, identify all endpoints that enable you to interact with the cart. For example, a POST /cart request adds items to the cart and a POST /cart/coupon request applies the discount code.

Try to identify any restrictions that are in place on these endpoints. For example, observe that if you try applying the discount code more than once, you receive a Coupon already applied response.

Make sure you have an item to your cart, then send the GET /cart request to Burp Repeater.

In Repeater, try sending the GET /cart request both with and without your session cookie. Confirm that without the session cookie, you can only access an empty cart. From this, you can infer that:

The state of the cart is stored server-side in your session.

Any operations on the cart are keyed on your session ID or the associated user ID.

This indicates that there is potential for a collision.

Consider that there may be a race window between when you first apply a discount code and when the database is updated to reflect that you've done this already.

Benchmarking the behavior

Make sure there is no discount code currently applied to your cart.

Send the request for applying the discount code (POST /cart/coupon) to Repeater.

In Repeater, add the new tab to a group. For details on how to do this, see Creating a new tab group.

Right-click the grouped tab, then select Duplicate tab. Create 19 duplicate tabs. The new tabs are automatically added to the group.

Send the group of requests in sequence, using separate connections to reduce the chance of interference. For details on how to do this, see Sending requests in sequence.

Observe that the first response confirms that the discount was successfully applied, but the rest of the responses consistently reject the code with the same Coupon already applied message.

Probing for clues

Remove the discount code from your cart.

In Repeater, send the group of requests again, but this time in parallel, effectively applying the discount code multiple times at once. For details on how to do this, see Sending requests in parallel.

Study the responses and observe that multiple requests received a response indicating that the code was successfully applied. If not, remove the code from your cart and repeat the attack.

In the browser, refresh your cart and confirm that the 20% reduction has been applied more than once, resulting in a significantly cheaper order.

Proving the concept

Remove the applied codes and the arbitrary item from your cart and add the leather jacket to your cart instead.

Resend the group of POST /cart/coupon requests in parallel.

Refresh the cart and check the order total:

If the order total is still higher than your remaining store credit, remove the discount codes and repeat the attack.

If the order total is less than your remaining store credit, purchase the jacket to solve the lab.

Community solutions

Intigriti

Popo Hack

Find race condition vulnerabilities using Burp Suite

Try for free
