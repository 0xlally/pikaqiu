# Lab: DOM XSS in jQuery selector sink using a hashchange event

Source: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-selector-hash-change-event
Fetched: 2026-06-28T09:17:45.762448+00:00

Web Security Academy

Cross-site scripting

DOM-based

Lab

Lab: DOM XSS in jQuery selector sink using a hashchange event

This lab contains a DOM-based cross-site scripting vulnerability on the home page. It uses jQuery's $() selector function to auto-scroll to a given post, whose title is passed via the location.hash property.

To solve the lab, deliver an exploit to the victim that calls the print() function in their browser.

Solution

Notice the vulnerable code on the home page using Burp or the browser's DevTools.

From the lab banner, open the exploit server.

In the Body section, add the following malicious iframe:

<iframe src="https://YOUR-LAB-ID.web-security-academy.net/#" onload="this.src+='<img src=x onerror=print()>'"></iframe>

Store the exploit, then click View exploit to confirm that the print() function is called.

Go back to the exploit server and click Deliver to victim to solve the lab.

Community solutions

Jarno Timmermans

z3nsh3ll

Intigriti

Find XSS vulnerabilities using Burp Suite

Try for free
