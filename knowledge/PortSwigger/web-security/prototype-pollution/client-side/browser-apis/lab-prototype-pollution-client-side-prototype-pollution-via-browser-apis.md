# Lab: Client-side prototype pollution via browser APIs

Source: https://portswigger.net/web-security/prototype-pollution/client-side/browser-apis/lab-prototype-pollution-client-side-prototype-pollution-via-browser-apis
Fetched: 2026-06-28T09:17:58.304441+00:00

Web Security Academy

Prototype pollution

Client-side vulnerabilities

Browser APIs

Lab

Lab: Client-side prototype pollution via browser APIs

This lab is vulnerable to DOM XSS via client-side prototype pollution. The website's developers have noticed a potential gadget and attempted to patch it. However, you can bypass the measures they've taken.

To solve the lab:

Find a source that you can use to add arbitrary properties to the global Object.prototype.

Identify a gadget property that allows you to execute arbitrary JavaScript.

Combine these to call alert().

You can solve this lab manually in your browser, or use DOM Invader to help you.

This lab is based on real-world vulnerabilities discovered by PortSwigger Research. For more details, check out Widespread prototype pollution gadgets by Gareth Heyes.

Manual solution

Find a prototype pollution source

In your browser, try polluting Object.prototype by injecting an arbitrary property via the query string:

/?__proto__[foo]=bar

Open the browser DevTools panel and go to the Console tab.

Enter Object.prototype.

Study the properties of the returned object and observe that your injected foo property has been added. You've successfully found a prototype pollution source.

Identify a gadget

In the browser DevTools panel, go to the Sources tab.

Study the JavaScript files that are loaded by the target site and look for any DOM XSS sinks.

In searchLoggerConfigurable.js, notice that if the config object has a transport_url property, this is used to dynamically append a script to the DOM.

Observe that a transport_url property is defined for the config object, so this doesn't appear to be vulnerable.

Observe that the next line uses the Object.defineProperty() method to make the transport_url unwritable and unconfigurable. However, notice that it doesn't define a value property.

Craft an exploit

Using the prototype pollution source you identified earlier, try injecting an arbitrary value property:

/?__proto__[value]=foo

In the browser DevTools panel, go to the Elements tab and study the HTML content of the page. Observe that a <script> element has been rendered on the page, with the src attribute foo.

Modify the payload in the URL to inject an XSS proof-of-concept. For example, you can use a data: URL as follows:

/?__proto__[value]=data:,alert(1);

Observe that the alert(1) is called and the lab is solved.

DOM Invader solution

Load the lab in Burp's built-in browser.

Enable DOM Invader and enable the prototype pollution option.

Open the browser DevTools panel, go to the DOM Invader tab, then reload the page.

Observe that DOM Invader has identified two prototype pollution vectors in the search property i.e. the query string.

Click Scan for gadgets. A new tab opens in which DOM Invader begins scanning for gadgets using the selected source.

When the scan is complete, open the DevTools panel in the same tab as the scan, then go to the DOM Invader tab.

Observe that DOM Invader has successfully accessed the script.src sink via the value gadget.

Click Exploit. DOM Invader automatically generates a proof-of-concept exploit and calls alert(1).

Community solutions

Emanuele Picariello

Find prototype pollution vulnerabilities using Burp Suite

Try for free
