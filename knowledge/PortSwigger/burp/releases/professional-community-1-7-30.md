# Professional / Community 1.7.30

Source: https://portswigger.net/burp/releases/professional-community-1-7-30
Fetched: 2026-06-28T09:16:31.894975+00:00

This release adds new granular configuration of scan issues:

You can select issues by scan type, and active issues are now subdivided into light, medium, and intrusive, based on the nature of the scanning activity involved in finding them.

You can also select individual issues. Whereas previously, you could select broad areas of scanning activity (such as "server-side code injection"), you can now select each issue individually ("PHP code injection", "Perl code injection", etc.).

If you select individual issues, you can also select the detection methods that are used for some types of issues, using the context menu:

This gives you highly granular control of the checks that are performed by Burp Scanner, and lets you create customized configurations for all kinds of specific purposes.

There are various other minor enhancements:

A "cancel" button is now shown during long-running filter updates.

There is a new option at Project options / SSL / SSL Negotiation to disable SSL session resume.

The "Copy as curl command" function no longer ignores any request headers. In older versions of curl, attempting to set some headers was ignored, but this is no longer the case.

A bug that caused automatically added SSL pass through entries not to appear in the UI config has been fixed.
