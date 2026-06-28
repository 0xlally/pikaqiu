# Testing for prototype pollution with DOM Invader

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/prototype-pollution
Fetched: 2026-06-28T09:15:59.947488+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing input validation

Testing for prototype pollution with DOM Invader

ProfessionalCommunity Edition

Testing for prototype pollution with DOM Invader

Last updated:

June 18, 2026

Read time:

2 Minutes

Prototype pollution is a JavaScript vulnerability. It enables an attacker to add arbitrary properties to global object prototypes, which may then be inherited by user-defined objects. This enables attackers to control object properties that would otherwise be inaccessible.

You can test for client-side prototype pollution vulnerabilities using DOM Invader. DOM Invader can automatically detect prototype pollution sources and scan for gadgets that you can use to craft an exploit. It can use the prototype pollution sources it discovers to pollute the Object.prototype as a proof of concept.

Before you start

Enable DOM Invader. For more information, see Enabling DOM Invader.

Steps

You can follow along with this process in the DOM XSS via client-side prototype pollution Web Security Academy lab.

Enabling prototype pollution detection in DOM Invader

In the upper-right corner of Burp's browser, click the Burp Suite logo and select the DOM Invader tab. The Settings menu is displayed.

Toggle the DOM Invader switch so that DOM Invader is on.

Click Attack types and toggle the switch so that Prototype pollution is on.

Click Reload to reload the browser and make your changes take effect.

Finding potential sources for prototype pollution

Right-click in the browser window and select Inspect to open the devtools panel.

Click the DOM Invader tab.

Browse around your target site to identify potential sources for prototype pollution. DOM Invader displays any sources found in the Sources list.

Testing sources manually

While on the page in which the source was found, expand the Sources list and click Test. DOM Invader opens the same page in a new browser tab.

From the new tab, open the devtools panel and select the Console tab.

Expand the Object node to display the Object.prototype.

Confirm that the Object.prototype output now contains a property called testproperty.

Create a new object in the console using the command let myObject = {};.

Use the command console.log(myObject.testproperty); to view the new object. Confirm that this new object has inherited testproperty.

Creating a proof of concept exploit

Select the source from the Sources list and click Scan for gadgets. DOM Invader opens a new tab and starts scanning.

Once the scan has finished, right-click in the new tab's browser window and select Inspect to open the devtools panel.

Click the DOM invader tab and check the contents of the Sinks list. These are sinks that DOM Invader was able to access via the identified gadgets.

Click Exploit next to a sink to test the sink with a proof-of-concept exploit. DOM Invader opens a new window in which it attempts to call the alert() function. If it is able to call the function, then an exploitable prototype pollution vulnerability is confirmed.

Related pages

DOM Invader - Gives further information on how to use DOM Invader.

DOM-based vulnerabilities - Explains what the DOM is and how insecure processing of DOM data can introduce vulnerabilities.
