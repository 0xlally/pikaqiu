# Testing for client-side prototype pollution

Source: https://portswigger.net/burp/documentation/desktop/tools/dom-invader/prototype-pollution
Fetched: 2026-06-28T09:16:02.553792+00:00

Support Center

Documentation

Desktop editions

Tools

DOM Invader

Testing for client-side prototype pollution

ProfessionalCommunity Edition

Testing for client-side prototype pollution

Last updated:

June 18, 2026

Read time:

3 Minutes

DOM Invader provides a number of features to help you test for client-side prototype pollution vulnerabilities. These enable you to perform the following key tasks:

Automatically detect sources for prototype pollution in the URL and any JSON objects sent via web messages. This includes detecting alternative techniques using the same source.

Generate a proof of concept by polluting the Object.prototype using any discovered sources. You can then manually verify the vulnerability via the browser console.

Scan for potential gadgets that you can use to craft an exploit.

Enabling prototype pollution

To avoid interfering with your target site's functionality, DOM Invader's prototype pollution features are disabled by default. To enable these features:

Go to the DOM Invader settings menu.

Under Attack types, toggle the switch so that Prototype pollution is on.

Click Reload to refresh the browser. This is necessary for your changes to take effect.

DOM Invader now scans for prototype pollution sources as you browse.

Detecting sources for prototype pollution

Once you enable prototype pollution, DOM Invader automatically checks the page for sources that enable you to add arbitrary properties to the Object.prototype. Any sources it identifies are displayed in the DOM view, along with some useful information and features for further testing.

In this example, DOM Invader has identified two potential techniques for polluting the Object.prototype using the location.hash source.

Manually confirming sources for prototype pollution

Once DOM Invader has identified a potential source for prototype pollution, it also helps you to manually confirm this.

To manually test whether prototype pollution is possible via this source:

From the DOM view, click the Test button next to the relevant source. DOM Invader opens a new tab in which it uses the selected source to add an arbitrary property to the Object.prototype.

In the new tab, go to the browser console. Note that DOM Invader has automatically output the Object.prototype.

Expand the nodes to confirm that this object contains a proof-of-concept testproperty.

In the console, create a new object:

let myObject = {};

Confirm that your new object has inherited testproperty via the prototype chain:

console.log(myObject.testproperty);

// Output: 'DOM_INVADER_PP_POC'

Scanning for prototype pollution gadgets

A prototype pollution source is of no use unless you also have access to a "gadget" property. This is any user-controllable property that is passed to a sink without being properly sanitized. Finding such a gadget manually is extremely tedious, but DOM Invader can automate this process.

To scan for gadgets using a particular source:

From the DOM view, click the Scan for gadgets button next to any prototype pollution source that DOM Invader has found. DOM Invader opens a new tab and starts scanning for suitable gadgets.

In the same tab, open the DOM Invader tab in the DevTools panel. Once the scan is finished, the DOM view displays any sinks that DOM Invader was able to access via the identified gadgets. In the example below, a gadget property called html was passed to the innerHTML sink.

Generating a proof-of-concept exploit

Once DOM Invader finds a gadget for prototype pollution, it is able to automatically generate a proof-of-concept by combining the source, gadget, and sink to confirm the XSS.

Simply click the Exploit button next to the discovered sink. DOM Invader opens a new window in which it successfully calls alert().

Read more

DOM Invader is highly configurable. For more information about DOM Invader's prototype pollution features and how you can fine-tune their behavior for a particular site, see Prototype pollution settings.
