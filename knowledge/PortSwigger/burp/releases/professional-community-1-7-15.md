# Professional / Community 1.7.15

Source: https://portswigger.net/burp/releases/professional-community-1-7-15
Fetched: 2026-06-28T09:16:31.301325+00:00

This release includes the most frequently requested feature of all time: custom wordlists in the Content Discovery feature.

It also massively improves the accuracy of detection of valid vs. not-found responses in the Content Discovery engine. We believe that this is now approaching 100% accuracy in terms of both false positives and false negatives. If anyone encounters a site where the Content Discovery function is not completely accurate, please let us know the details and we will investigate.

A number of other enhancements and fixes have been made:

Further to the security issues that were fixed in 1.7.14, some additional hardening has been performed of in-browser actions and the CSRF PoC generator, to prevent some conceivable attacks involving excessive amounts of socially engineered user actions on a malicious site.

A bug that caused the Burp Comparer progress bar to intermittently hang has been fixed.

The SMTP service of the Burp Collaborator server has been modified to reject emails without a valid interaction ID. This effectively prevents the Collaborator wrongly appearing to be an open mail relay, which caused failure reports by naive security scans.

A bug that was introduced in 1.7.14, which prevented Repeater requests from being issued when a tab other than the "Raw" tab was selected, has been fixed.
