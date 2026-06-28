# Lab: DOM XSS using web messages and a JavaScript URL

Source: https://portswigger.net/web-security/dom-based/controlling-the-web-message-source/lab-dom-xss-using-web-messages-and-a-javascript-url
Fetched: 2026-06-28T09:17:48.365021+00:00

Web Security Academy

DOM-based

Controlling the web message source

Lab

Lab: DOM XSS using web messages and a JavaScript URL

This lab demonstrates a DOM-based redirection vulnerability that is triggered by web messaging. To solve this lab, construct an HTML page on the exploit server that exploits this vulnerability and calls the print() function.

Solution

Notice that the home page contains an addEventListener() call that listens for a web message. The JavaScript contains a flawed indexOf() check that looks for the strings "http:" or "https:" anywhere within the web message. It also contains the sink location.href.

Go to the exploit server and add the following iframe to the body, remembering to replace YOUR-LAB-ID with your lab ID:

<iframe src="https://YOUR-LAB-ID.web-security-academy.net/" onload="this.contentWindow.postMessage('javascript:print()//http:','*')">

Store the exploit and deliver it to the victim.

This script sends a web message containing an arbitrary JavaScript payload, along with the string "http:". The second argument specifies that any targetOrigin is allowed for the web message.

When the iframe loads, the postMessage() method sends the JavaScript payload to the main page. The event listener spots the "http:" string and proceeds to send the payload to the location.href sink, where the print() function is called.

Find DOM-based vulnerabilities using Burp Suite

Try for free
