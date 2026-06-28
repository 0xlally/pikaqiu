# Professional 1.5.03

Source: https://portswigger.net/burp/releases/professional-1-5-03
Fetched: 2026-06-28T09:16:24.694306+00:00

This release fixes a number of bugs affecting the new extensibility:

Extensions are now automatically reloaded on startup when Burp is running in headless mode.

A bug introduced in v1.5.02 where Burp won't load a new Python extension unless the JRuby JAR file has been configured, has been fixed.

An exception that occurred when adding custom scan issues asynchronously (using IBurpExtenderCallbacks.addScanIssue()) has been fixed.

A bug where all custom scan issues were reported in the UI with High severity has been fixed.

When an IProxyListener sets one of the XXX_AND_REHOOK intercept actions, when the subsequent call to the listener occurs, the intercept action returned from IInterceptedProxyMessage.getInterceptAction() will now be the same value that was previously set (rather than defaulting back to ACTION_FOLLOW_RULES). This enables extensions to more easily re-identify messages that are being rehooked.
