# Intercept HTTP traffic with Burp Proxy

Source: https://portswigger.net/burp/documentation/desktop/getting-started/intercepting-http-traffic
Fetched: 2026-06-28T09:15:54.982167+00:00

Support Center

Documentation

Desktop editions

Getting started

Intercepting HTTP traffic with Burp Proxy

ProfessionalCommunity Edition

Intercept HTTP traffic with Burp Proxy

Last updated:

June 18, 2026

Read time:

2 Minutes

In this tutorial, you'll use a live, deliberately vulnerable website to learn how to intercept requests with Burp Proxy.

Intercepting a request

Burp Proxy lets you intercept HTTP requests and responses sent between Burp's browser and the target server. This enables you to study how the website behaves when you perform different actions.

Step 1: Launch Burp's browser

Go to the Proxy > Intercept tab.

Set the intercept toggle to Intercept on.

Click Open Browser. This launches Burp's browser, which is preconfigured to work with Burp right out of the box.

Position the windows so that you can see both Burp and Burp's browser.

Step 2: Intercept a request

Using Burp's browser, try to visit https://portswigger.net and observe that the site doesn't load. Burp Proxy has intercepted the HTTP request that was issued by the browser before

it could reach the server. You can see this intercepted request on the Proxy > Intercept tab.

The request is held here so that you can study it, and even modify it, before forwarding it to the target server.

Step 3: Forward the request

Click the Forward button to send the intercepted request. Click Forward again to send any subsequent requests that are intercepted, until the page loads in Burp's browser. The

Forward button sends all the selected requests.

Step 4: Switch off interception

Due to the number of requests browsers typically send, you often won't want to intercept every single one of them. Set the intercept toggle to Intercept off.

Go back to the browser and confirm that you can now interact with the site as normal.

Step 5: View the HTTP history

In Burp, go to the Proxy > HTTP history tab. Here, you can see the history of all HTTP traffic that has passed through Burp Proxy, even while intercept was switched off.

Click on any entry in the history to view the raw HTTP request, along with the corresponding response from the server.

This lets you explore the website as normal and study the interactions between Burp's browser and the server afterward, which is more convenient in many cases.

Next step - Modifying HTTP requests with Burp Proxy

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
