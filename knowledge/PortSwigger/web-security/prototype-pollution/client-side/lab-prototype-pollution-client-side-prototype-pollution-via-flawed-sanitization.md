# Lab: Client-side prototype pollution via flawed sanitization

Source: https://portswigger.net/web-security/prototype-pollution/client-side/lab-prototype-pollution-client-side-prototype-pollution-via-flawed-sanitization
Fetched: 2026-06-28T09:17:58.762084+00:00

Web Security Academy

Prototype pollution

Client-side vulnerabilities

Lab

Lab: Client-side prototype pollution via flawed sanitization

This lab is vulnerable to DOM XSS via client-side prototype pollution. Although the developers have implemented measures to prevent prototype pollution, these can be easily bypassed.

To solve the lab:

Find a source that you can use to add arbitrary properties to the global Object.prototype.

Identify a gadget property that allows you to execute arbitrary JavaScript.

Combine these to call alert().

Solution

Find a prototype pollution source

In your browser, try polluting Object.prototype by injecting an arbitrary property via the query string:

/?__proto__.foo=bar

Open the browser DevTools panel and go to the Console tab.

Enter Object.prototype.

Study the properties of the returned object and observe that your injected foo property has not been added.

Try alternative prototype pollution vectors. For example:

/?__proto__[foo]=bar

/?constructor.prototype.foo=bar

Observe that in each instance, Object.prototype is not modified.

Go to the Sources tab and study the JavaScript files that are loaded by the target site. Notice that deparamSanitized.js uses the sanitizeKey() function defined in searchLoggerFiltered.js to strip potentially dangerous property keys based on a blocklist. However, it does not apply this filter recursively.

Back in the URL, try injecting one of the blocked keys in such a way that the dangerous key remains following the sanitization process. For example:

/?__pro__proto__to__[foo]=bar

/?__pro__proto__to__.foo=bar

/?constconstructorructor[protoprototypetype][foo]=bar

/?constconstructorructor.protoprototypetype.foo=bar

In the console, enter Object.prototype again. Notice that it now has its own foo property with the value bar. You've successfully found a prototype pollution source and bypassed the website's key sanitization.

Identify a gadget

Study the JavaScript files again and notice that searchLogger.js dynamically appends a script to the DOM using the config object's transport_url property if present.

Notice that no transport_url property is set for the config object. This is a potential gadget.

Craft an exploit

Using the prototype pollution source you identified earlier, try injecting an arbitrary transport_url property:

/?__pro__proto__to__[transport_url]=foo

In the browser DevTools panel, go to the Elements tab and study the HTML content of the page. Observe that a <script> element has been rendered on the page, with the src attribute foo.

Modify the payload in the URL to inject an XSS proof-of-concept. For example, you can use a data: URL as follows:

/?__pro__proto__to__[transport_url]=data:,alert(1);

Observe that the alert(1) is called and the lab is solved.

Community solutions

Emanuele Picariello

Find prototype pollution vulnerabilities using Burp Suite

Try for free
