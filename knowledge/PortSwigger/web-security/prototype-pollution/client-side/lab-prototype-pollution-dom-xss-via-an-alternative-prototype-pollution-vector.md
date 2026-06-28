# Lab: DOM XSS via an alternative prototype pollution vector

Source: https://portswigger.net/web-security/prototype-pollution/client-side/lab-prototype-pollution-dom-xss-via-an-alternative-prototype-pollution-vector
Fetched: 2026-06-28T09:17:58.457115+00:00

Web Security Academy

Prototype pollution

Client-side vulnerabilities

Lab

Lab: DOM XSS via an alternative prototype pollution vector

This lab is vulnerable to DOM XSS via client-side prototype pollution. To solve the lab:

Find a source that you can use to add arbitrary properties to the global Object.prototype.

Identify a gadget property that allows you to execute arbitrary JavaScript.

Combine these to call alert().

You can solve this lab manually in your browser, or use DOM Invader to help you.

Hint

Pay attention to the XSS context. You need to adjust your payload slightly to ensure that the JavaScript syntax remains valid following your injection.

Manual solution

Find a prototype pollution source

In your browser, try polluting Object.prototype by injecting an arbitrary property via the query string:

/?__proto__[foo]=bar

Open the browser DevTools panel and go to the Console tab.

Enter Object.prototype.

Study the properties of the returned object and observe that your injected foo property has not been added.

Back in the query string, try using an alternative prototype pollution vector:

/?__proto__.foo=bar

In the console, enter Object.prototype again. Notice that it now has its own foo property with the value bar. You've successfully found a prototype pollution source.

Identify a gadget

In the browser DevTools panel, go to the Sources tab.

Study the JavaScript files that are loaded by the target site and look for any DOM XSS sinks.

Notice that there is an eval() sink in searchLoggerAlternative.js.

Notice that the manager.sequence property is passed to eval(), but this isn't defined by default.

Craft an exploit

Using the prototype pollution source you identified earlier, try injecting an arbitrary sequence property containing an XSS proof-of-concept payload:

/?__proto__.sequence=alert(1)

Observe that the payload doesn't execute.

In the browser DevTools panel, go to the Console tab. Observe that you have triggered an error.

Click the link at the top of the stack trace to jump to the line where eval() is called.

Click the line number to add a breakpoint to this line, then refresh the page.

Hover the mouse over the manager.sequence reference and observe that its value is alert(1)1. This indicates that we have successfully passed our payload into the sink, but a numeric 1 character is being appended to it, resulting in invalid JavaScript syntax.

Click the line number again to remove the breakpoint, then click the play icon at the top of the browser window to resume code execution.

Add trailing minus character to the payload to fix up the final JavaScript syntax:

/?__proto__.sequence=alert(1)-

Observe that the alert(1) is called and the lab is solved.

DOM Invader solution

Load the lab in Burp's built-in browser.

Enable DOM Invader and enable the prototype pollution option.

Open the browser DevTools panel and go to the DOM Invader tab and reload the page.

Observe that DOM Invader has identified a prototype pollution vector in the search property i.e. the query string.

Click Scan for gadgets. A new tab opens in which DOM Invader begins scanning for gadgets using the selected source.

When the scan is complete, open the DevTools panel in the same tab as the scan, then go to the DOM Invader tab.

Observe that DOM Invader has successfully accessed the eval() sink via the sequence gadget.

Click Exploit. Observe that DOM Invader's auto-generated proof-of-concept doesn't trigger an alert().

Go back to the previous browser tab and look at the eval() sink again in DOM Invader. Notice that following the closing canary string, a numeric 1 character has been appended to the payload.

Click Exploit again. In the new tab that loads, append a minus character (-) to the URL and reload the page.

Observe that the alert(1) is called and the lab is solved.

Community solutions

Emanuele Picariello

Find prototype pollution vulnerabilities using Burp Suite

Try for free
