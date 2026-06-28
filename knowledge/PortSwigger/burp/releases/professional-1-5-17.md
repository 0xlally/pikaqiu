# Professional 1.5.17

Source: https://portswigger.net/burp/releases/professional-1-5-17
Fetched: 2026-06-28T09:16:25.822189+00:00

This release includes a number of enhancements and bugfixes:

There is a new "copy as curl command" function on context menus. This function constructs a curl command that generates the selected request, and copies the command to the clipboard.

The Extender tool has a new option to specify a folder from which Burp will load library JAR files for use by Java extensions.

The IBurpExtenderCallbacks interface has several new methods:

Methods to list and remove extension-provided resources such as event listeners, resource factories, etc.

Methods to print a line of output to the extension's stdout or stderr streams.

The numbers payload generator in Intruder has been enhanced to cope with numbers of arbitrary size and precision, and is no longer subject to the constraints of Java's native integer or floating point arithmetic. It is possible configure and launch attacks that will result in arbitrarily many payloads. If the number of payloads exceeds 2^31 then Burp will report the number as "unknown" but the attack will still proceed in the expected way (even though actually completing the attack is not feasible).

There is a new hotkeyable action to forward the request currently showing in the Proxy intercept view and force interception of the response. This action is not assigned a hotkey by default.

The save and restore state functions can now include the configuration options for the Extender tool.

The extensibility API to retrieve the contents of the site map now auto-generates GET requests for items in the site map that have not yet been requested.

A bug in the session handling action to update the value of a named parameter, where multiple parameters with the same name were not updated, has been fixed.

A bug in Intruder that caused some valid custom iterator configurations to fail has been fixed.

A bug in the invocation of extension-provided custom Scanner checks, where an exception thrown by an extension could cause Burp's scanning thread to die, has been fixed.

A bug in the CSRF PoC generator where pure GET requests are not properly handled has been fixed. (Of course, a pure GET request is itself deliverable cross-domain using only its own URL, but Burp now gives the option of delivering the request via a form submission if required.)
