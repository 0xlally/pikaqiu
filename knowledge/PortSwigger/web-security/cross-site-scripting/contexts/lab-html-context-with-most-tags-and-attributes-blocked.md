# Lab: Reflected XSS into HTML context with most tags and attributes blocked

Source: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-most-tags-and-attributes-blocked
Fetched: 2026-06-28T09:17:46.143760+00:00

Web Security Academy

Cross-site scripting

Contexts

Lab

Lab: Reflected XSS into HTML context with most tags and attributes blocked

This lab contains a reflected XSS vulnerability in the search functionality but uses a web application firewall (WAF) to protect against common XSS vectors.

To solve the lab, perform a cross-site scripting attack that bypasses the WAF and calls the print() function.

Note

Your solution must not require any user interaction. Manually causing print() to be called in your own browser will not solve the lab.

Solution

Inject a standard XSS vector, such as:

<img src=1 onerror=print()>

Observe that this gets blocked. In the next few steps, we'll use use Burp Intruder to test which tags and attributes are being blocked.

Open Burp's browser and use the search function in the lab. Send the resulting request to Burp Intruder.

In Burp Intruder, replace the value of the search term with: <>

Place the cursor between the angle brackets and click Add § to create a payload position. The value of the search term should now look like: <§§>

Visit the XSS cheat sheet and click Copy

tags to clipboard.

In the Payloads side panel, under Payload configuration, click Paste to paste the list of tags into the payloads list. Click Start attack.

When the attack is finished, review the results. Note that most payloads caused a 400 response, but the body payload caused a 200 response.

Go back to Burp Intruder and replace your search term with:

<body%20=1>

Place the cursor before the = character and click Add § to create a payload position. The value of the search term should now look like: <body%20§§=1>

Visit the XSS cheat sheet and click

Copy events to clipboard.

In the Payloads side panel, under Payload configuration, click Clear to remove the previous payloads. Then click Paste to paste the list of attributes into the payloads list. Click Start attack.

When the attack is finished, review the results. Note that most payloads caused a 400 response, but the onresize payload caused a 200 response.

Go to the exploit server and paste the following code, replacing YOUR-LAB-ID with your lab ID:

<iframe src="https://YOUR-LAB-ID.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'>

Click Store and Deliver exploit to victim.

Community solutions

z3nsh3ll

Michael Sommer

Find XSS vulnerabilities using Burp Suite

Try for free
