# Lab: DOM XSS using web messages and JSON.parse

Source: https://portswigger.net/web-security/dom-based/controlling-the-web-message-source/lab-dom-xss-using-web-messages-and-json-parse
Fetched: 2026-06-28T09:17:48.252411+00:00

Web Security Academy

DOM-based

Controlling the web message source

Lab

Lab: DOM XSS using web messages and JSON.parse

This lab uses web messaging and parses the message as JSON. To solve the lab, construct an HTML page on the exploit server that exploits this vulnerability and calls the print() function.

Solution

Notice that the home page contains an event listener that listens for a web message. This event listener expects a string that is parsed using JSON.parse(). In the JavaScript, we can see that the event listener expects a type property and that the load-channel case of the switch statement changes the iframe src attribute.

Go to the exploit server and add the following iframe to the body, remembering to replace YOUR-LAB-ID with your lab ID:

<iframe src=https://YOUR-LAB-ID.web-security-academy.net/ onload='this.contentWindow.postMessage("{\"type\":\"load-channel\",\"url\":\"javascript:print()\"}","*")'>

Store the exploit and deliver it to the victim.

When the iframe we constructed loads, the postMessage() method sends a web message to the home page with the type load-channel. The event listener receives the message and parses it using JSON.parse() before sending it to the switch.

The switch triggers the load-channel case, which assigns the url property of the message to the src attribute of the ACMEplayer.element iframe. However, in this case, the url property of the message actually contains our JavaScript payload.

As the second argument specifies that any targetOrigin is allowed for the web message, and the event handler does not contain any form of origin check, the payload is set as the src of the ACMEplayer.element iframe. The print() function is called when the victim loads the page in their browser.

Community solutions

Michael Sommer (no audio)

Find DOM-based vulnerabilities using Burp Suite

Try for free
