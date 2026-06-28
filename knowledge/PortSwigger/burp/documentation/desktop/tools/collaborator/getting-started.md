# Getting started with Burp Collaborator

Source: https://portswigger.net/burp/documentation/desktop/tools/collaborator/getting-started
Fetched: 2026-06-28T09:16:02.089780+00:00

Support Center

Documentation

Desktop editions

Tools

Collaborator

Getting started

Professional

Getting started with Burp Collaborator

Last updated:

June 18, 2026

Read time:

2 Minutes

In this tutorial, you will learn how to manually use Burp Collaborator. You will test whether you can induce a target site to make a request to an arbitrary server that could potentially be controlled by an attacker.

Step 1: Access the lab

Open Burp's browser, and use it to access the following URL:

https://portswigger.net/web-security/ssrf/blind/lab-out-of-band-detection

Click Access the lab and log in to your PortSwigger account if prompted. This opens your own instance of a deliberately vulnerable shopping website.

Step 2: Browse the target site

In the browser, explore the site by clicking on a couple of the product pages.

Step 3: Send an interesting request to Repeater

In Burp, go to the Proxy > HTTP history tab.

Right-click a GET /product?productId=[...] request and select Send to Repeater.

Step 4: Inject a Collaborator payload into the request

Go to the Repeater tab. Highlight the URL in the Referer header, right-click, and select Insert Collaborator payload. This replaces the Referer URL with a URL that points to the Collaborator server, for example:

204119i326shak9tnk6k36z8jlahj74r.oastify.com

Send the request.

Note

The Collaborator server domain name may change, as we periodically add new domain names. For more information, see Generating payloads.

Step 5: Poll for interactions

Go to the Collaborator tab. Collaborator polls for interactions every 60 seconds, so you may see some interactions listed already. If not, click Poll now. Interactions received as a result of your Collaborator payloads are displayed. This confirms that the target site made a request to the arbitrary server.

In this case, you see both HTTP and DNS interactions. Click on an interaction to view more details.

Summary

Congratulations, you have now successfully:

Generated a Collaborator payload.

Inserted a Collaborator payload in a request.

Induced the application to send a request to your Collaborator subdomain, and identified this by polling the server for interactions.

You now know how to use Burp Collaborator to manually generate a proof of concept for invisible vulnerabilities, in this case, blind SSRF.

What next?

This tutorial is just an initial proof of concept. To learn how you can exploit this kind of behavior in the wild, check out the Web Security Academy, in particular:

Blind SSRF.

Blind SQL injection.

For an overview of some common uses of Burp Collaborator, see Typical uses for Burp Collaborator.
