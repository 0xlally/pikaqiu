# Modifying HTTP requests with Burp Proxy

Source: https://portswigger.net/burp/documentation/desktop/getting-started/modifying-http-requests
Fetched: 2026-06-28T09:15:51.268184+00:00

Support Center

Documentation

Desktop editions

Getting started

Modifying requests in Burp Proxy

ProfessionalCommunity Edition

Modifying HTTP requests with Burp Proxy

Last updated:

June 18, 2026

Read time:

3 Minutes

In this tutorial, you'll learn how to modify intercepted requests in Burp Proxy. This enables you to manipulate these requests in ways that the website isn't expecting, in order to see how it responds.

Using one of our deliberately vulnerable websites, known as "labs", you'll see how this can help you identify and exploit real vulnerabilities.

Web Security Academy

To follow along, you'll need an account on portswigger.net. If you don't have one already, registration is free and it grants you full access to the Web Security Academy.

Step 1: Access the vulnerable website in Burp's browser

In Burp, go to the Proxy > Intercept tab and make sure interception is switched off.

Launch Burp's browser and use it to visit the following URL:

https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-excessive-trust-in-client-side-controls

When the page loads, click Access the lab. If prompted, log in to your portswigger.net account. After a few seconds, you will see your own instance of a fake shopping website.

Step 2: Log in to your shopping account

On the shopping website, click My account and log in using the following credentials:

Username: wiener

Password: peter

Notice that you have just $100 of store credit.

Step 3: Find something to buy

Click Home to go back to the home page. Select the option to view the product details for the Lightweight "l33t" leather jacket.

Step 4: Study the add to cart function

In Burp, go to the Proxy > Intercept tab and switch interception on. In the browser, add the leather jacket to your cart to intercept the resulting

POST /cart request.

Note

You may see more than one request on the Proxy > Intercept tab if the browser is doing something else in the background. In this case, select the POST /cart request.

Study the intercepted request and notice that there is a parameter in the body called price, which matches the price of the item in cents.

Step 5: Modify the request

Change the value of the price parameter to 1 and click Forward > Forward all to send the modified request to the server, along with any other intercepted requests.

Switch interception off again so that any subsequent requests can pass through Burp Proxy uninterrupted.

Step 6: Exploit the vulnerability

In Burp's browser, click the basket icon in the upper-right corner to view your cart. Notice that the jacket has been added for just one cent.

Note

There is no way to modify the price via the web interface. You were only able to make this change thanks to Burp Proxy.

Click the Place order button to purchase the jacket for an extremely reasonable price.

Congratulations, you've also just solved your first Web Security Academy lab! You've also learned how to intercept, review, and manipulate HTTP traffic using Burp Proxy.

Next step - Setting the target scope

CONTINUE

In this tutorial

Downloading and installing Burp Suite.

Intercepting HTTP traffic with Burp Proxy.

Modifying requests in Burp Proxy.

Setting the target scope.

Manually reissuing requests with Burp Repeater.

Running your first scan.

Generating a report.

What next?
