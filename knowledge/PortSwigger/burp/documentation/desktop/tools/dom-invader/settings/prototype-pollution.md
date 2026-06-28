# Prototype pollution settings

Source: https://portswigger.net/burp/documentation/desktop/tools/dom-invader/settings/prototype-pollution
Fetched: 2026-06-28T09:16:02.732171+00:00

Support Center

Documentation

Desktop editions

Tools

DOM Invader

Settings

Prototype pollution settings

ProfessionalCommunity Edition

Prototype pollution settings

Last updated:

June 18, 2026

Read time:

4 Minutes

You can click the cog icon next to the Prototype pollution option to access further settings for fine-tuning how DOM Invader's tests for prototype pollution vulnerabilities.

Scan for gadgets

When this setting is enabled, DOM Invader automatically scans for gadgets whenever the page loads. Although you can scan for gadgets using specific sources, this setting is a useful alternative in cases where you haven't found any sources. This enables you to ensure that your site doesn't contain any gadgets that could potentially be exploited in future.

DOM Invader automatically adjusts the rest of the prototype pollution settings. You can override these settings manually if required.

Auto-scale amount of properties per frame

By default, DOM Invader automatically scales the number of properties used per frame when scanning for prototype pollution gadgets. This helps to improve performance, but lead to gadgets being missed. For example, an injected property could cause an exception that prevents DOM Invader from testing any other gadgets within the same iframe, resulting in false negatives.

If you prefer, you can disable this setting and use the slider to set a fixed limit instead. Lowering the limit makes the scan take longer, but reduces the chance of you missing gadgets. Increasing the limit has the opposite effect.

Scan nested properties

By default, DOM Invader recursively scans properties nested within other properties. If you disable this setting, DOM Invader only scans for gadgets using the top-level properties of each object.

For example, consider the following object:

const user = {

id: 1337,

name: "carlos",

contactInfo: {

email: "carlos@ginandjuice.shop",

phone: 0161133713371

}

}

By default, DOM Invader will test all properties of this user object. If you disable this setting, both the user.contactInfo.email and user.contactInfo.phone properties will be skipped.

Query string injection

By default, DOM Invader tests for prototype pollution using parameters in the query string. You may need to disable this setting if it is preventing the site from working correctly.

Hash injection

By default, DOM Invader tests for prototype pollution using the hash or fragment part of the URL. You may need to disable this setting if it is preventing the site from working correctly.

JSON injection

By default, DOM Invader tests for prototype pollution by injecting JSON-based web messages. You may need to disable this setting if it is preventing the site from working correctly.

Verify onload

By default, DOM Invader waits for the page to finish loading before reporting on prototype pollution. This is to ensure that any identified gadgets are still present in the final DOM.

If you disable this setting, DOM Invader reports on potential gadgets as soon as it finds them. This can reduce the duration of the scan, but may result in false positives. For example, DOM Invader could identify gadgets using the constructor or __proto__ properties, which might be sanitized by the time the page has finished loading.

Remove CSP header

When this setting is enabled, DOM Invader strips the Content-Security-Policy header from all responses. This prevents the CSP from blocking potential XSS vectors, as well as iframes, which are necessary when scanning for gadgets.

Remove X-Frame-Options header

When this setting is enabled, DOM Invader strips the X-Frame-Options header from all responses. This prevents it from blocking iframes, which are necessary when scanning for gadgets.

Scan each technique in separate frame

For performance reasons, DOM Invader scans for prototype pollution in the top frame by default. However, you may encounter situations where the different techniques interfere with each other, which could cause you to miss vulnerabilities. For example, trying both __proto__ and constructor at the same time fails on some sites, even though constructor in isolation works.

When this setting is enabled, DOM Invader uses a separate iframe for each technique. Although this may have a minor performance impact, it ensures that each technique is tested independently, reducing the chance of false negatives.

Disabling prototype pollution techniques

DOM Invader uses a number of different techniques for prototype pollution. You may find that using all of these techniques at once prevents the attack from working on certain sites. For this reason, you may prefer to disable some of the techniques or use one technique at a time.

To disable prototype pollution techniques:

From the DOM Invader settings menu, under Attack types, click the cog icon next to the Prototype pollution switch.

In the dialog, click the Techniques button.

Use the switches to enable or disable the techniques as required.

Click Save and then Reload to refresh the browser. This is required in order for your changes to take effect.
