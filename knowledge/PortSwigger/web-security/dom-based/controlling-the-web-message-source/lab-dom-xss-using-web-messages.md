# Lab: DOM XSS using web messages

Source: https://portswigger.net/web-security/dom-based/controlling-the-web-message-source/lab-dom-xss-using-web-messages
Fetched: 2026-06-28T09:17:48.333257+00:00

Web Security Academy

DOM-based

Controlling the web message source

Lab

Lab: DOM XSS using web messages

This lab demonstrates a simple web message vulnerability. To solve this lab, use the exploit server to post a message to the target site that causes the print() function to be called.

Solution

Notice that the home page contains an addEventListener() call that listens for a web message.

Go to the exploit server and add the following iframe to the body. Remember to add your own lab ID:

<iframe src="https://YOUR-LAB-ID.web-security-academy.net/" onload="this.contentWindow.postMessage('<img src=1 onerror=print()>','*')">

Store the exploit and deliver it to the victim.

When the iframe loads, the postMessage() method sends a web message to the home page. The event listener, which is intended to serve ads, takes the content of the web message and inserts it into the div with the ID ads. However, in this case it inserts our img tag, which contains an invalid src attribute. This throws an error, which causes the onerror event handler to execute our payload.

Community solutions

Michael Sommer (no audio)

Find DOM-based vulnerabilities using Burp Suite

Try for free
