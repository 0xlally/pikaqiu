# DOM-based JavaScript injection

Source: https://portswigger.net/web-security/dom-based/javascript-injection
Fetched: 2026-06-28T09:17:49.133729+00:00

Web Security Academy

DOM-based

JavaScript injection

DOM-based JavaScript injection

In this section, we'll talk about DOM-based JavaScript-injection vulnerabilities, discuss how they can impact the victim, and suggest ways to reduce your exposure to JavaScript-injection vulnerabilities.

What is DOM-based JavaScript injection?

DOM-based JavaScript-injection vulnerabilities arise when a script executes attacker-controllable data as JavaScript. An attacker may be able to use the vulnerability to construct a URL that, if visited by another user, will cause arbitrary JavaScript supplied by the attacker to execute in the context of the user's browser session.

Users can be induced to visit the attacker's malicious URL in various ways, similar to the usual attack-delivery vectors for reflected cross-site scripting vulnerabilities. For more information, please refer to our page on DOM XSS.

What is the impact of a DOM-based JavaScript-injection attack?

The attacker-supplied code can perform a wide variety of actions, such as stealing the victim's session token or login credentials, performing arbitrary actions on the victim's behalf, or even logging their keystrokes.

Which sinks can lead to DOM-based JavaScript-injection vulnerabilities?

The following are some of the main sinks that can lead to DOM-based JavaScript-injection vulnerabilities:

eval()

Function()

setTimeout()

setInterval()

setImmediate()

execCommand()

execScript()

msSetImmediate()

range.createContextualFragment()

crypto.generateCRMFRequest()

How to prevent DOM-based JavaScript-injection vulnerabilities

In addition to the general measures described on the DOM-based vulnerabilities page, you should avoid allowing data from any untrusted source to be executed as JavaScript.

Find DOM-based vulnerabilities using Burp Suite

Try for free
