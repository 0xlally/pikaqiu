# Testing for DOM XSS with DOM Invader

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/xss/dom-xss
Fetched: 2026-06-28T09:16:00.300277+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing input validation

Cross-site scripting

Testing for DOM XSS with DOM Invader

ProfessionalCommunity Edition

Testing for DOM XSS with DOM Invader

Last updated:

June 18, 2026

Read time:

1 Minute

DOM-based XSS (DOM XSS) arises when an application contains client-side JavaScript that processes data from an untrusted source in an unsafe way, usually by writing the data back to the DOM.

DOM Invader makes it much easier for you to test applications for DOM XSS. DOM Invader injects a unique string into different sources, and then shows you the sinks that your input flows into. It also shows you the surrounding context. This replaces the need to manually follow the flow through complex JavaScript, which could have thousands of lines of code.

To learn more about sources and sinks, see DOM-based vulnerabilities.

Note

DOM Invader is pre-installed in Burp's browser. It's disabled by default as some of its features may interfere with your other testing activities.

Before you start

Enable DOM Invader. For more information, see Enabling DOM Invader.

Steps

You can follow the processes below using the lab DOM XSS in document.write sink using source location.search.

Use DOM Invader to inject a canary into the client-side JavaScript:

Use Burp's browser to visit your target website.

Right-click the browser window and select Inspect.

Select the DOM Invader tab and click Copy canary.

Inject the canary into a potential source.

Identify any controllable sinks from the list in the DOM view.

Examine the Value column to determine the XSS context.

Input a string into the source that takes into account the XSS context, to see if you can exploit the vulnerability.

Related pages

Testing for DOM XSS

DOM Invader
