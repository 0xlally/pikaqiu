# Lab: Client-side prototype pollution in third-party libraries

Source: https://portswigger.net/web-security/prototype-pollution/client-side/lab-prototype-pollution-client-side-prototype-pollution-in-third-party-libraries
Fetched: 2026-06-28T09:17:58.412580+00:00

Web Security Academy

Prototype pollution

Client-side vulnerabilities

Lab

Lab: Client-side prototype pollution in third-party libraries

This lab is vulnerable to DOM XSS via client-side prototype pollution. This is due to a gadget in a third-party library, which is easy to miss due to the minified source code. Although it's technically possible to solve this lab manually, we recommend using DOM Invader as this will save you a considerable amount of time and effort.

To solve the lab:

Use DOM Invader to identify a prototype pollution and a gadget for DOM XSS.

Use the provided exploit server to deliver a payload to the victim that calls alert(document.cookie) in their browser.

This lab is based on real-world vulnerabilities discovered by PortSwigger Research. For more details, check out Widespread prototype pollution gadgets by Gareth Heyes.

Solution

Load the lab in Burp's built-in browser.

Enable DOM Invader and enable the prototype pollution option.

Open the browser DevTools panel, go to the DOM Invader tab, then reload the page.

Observe that DOM Invader has identified two prototype pollution vectors in the hash property i.e. the URL fragment string.

Click Scan for gadgets. A new tab opens in which DOM Invader begins scanning for gadgets using the selected source.

When the scan is complete, open the DevTools panel in the same tab as the scan, then go to the DOM Invader tab.

Observe that DOM Invader has successfully accessed the setTimeout() sink via the hitCallback gadget.

Click Exploit. DOM Invader automatically generates a proof-of-concept exploit and calls alert(1).

Disable DOM Invader.

In the browser, go to the lab's exploit server.

In the Body section, craft an exploit that will navigate the victim to a malicious URL as follows:

<script>

location="https://YOUR-LAB-ID.web-security-academy.net/#__proto__[hitCallback]=alert%28document.cookie%29"

</script>

Test the exploit on yourself, making sure that you're navigated to the lab's home page and that the alert(document.cookie) payload is triggered.

Go back to the exploit server and deliver the exploit to the victim to solve the lab.

Community solutions

Emanuele Picariello

Find prototype pollution vulnerabilities using Burp Suite

Try for free
