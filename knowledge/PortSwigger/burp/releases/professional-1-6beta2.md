# Professional 1.6beta2

Source: https://portswigger.net/burp/releases/professional-1-6beta2
Fetched: 2026-06-28T09:16:28.263611+00:00

This release fixes a number of bugs:

A bug in v1.6beta that caused some saved state files to be corrupted has been fixed. The majority of problematic state files that were generated with the previous version should be loadable in this release.

A bug in the HTTP message viewer which caused parts of a message not to be displayed in certain situations has been fixed.

A bug arising on certain platforms (e.g. some OS X retina machines), in which the HTTP message viewer displays the cursor in the wrong position, has been addressed. Since this was a platform-specific problem, and we weren't able to reproduce the bug on all reported configurations, we welcome feedback as to whether any further instances of this problem are remaining.

Problems affecting Proxy SSL negotiation on Java 8 have been addressed. Burp is not yet officially supported on this platform, pending further testing, but we welcome feedback about any further problems that arise on Java 8.

Some XSS edge cases relating to URL-encoding of specific payload characters, which were being missed by Burp, are now detected properly.

A bug in the Intruder custom iterator payload type, which caused it not to generate the expected payloads in certain conditions, has been fixed.

The opt-out checkbox for reporting of anonymous performance feedback, which previously appeared only on an options panel, has been added to the EULA acceptance dialog.
