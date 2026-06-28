# Professional / Community 1.7.23

Source: https://portswigger.net/burp/releases/professional-community-1-7-23
Fetched: 2026-06-28T09:16:31.600784+00:00

This release adds the capability to report a number of new scan issues:

CSS injection - reflected and stored

Link manipulation - reflected and stored

Client-side HTTP parameter pollution - reflected and stored

Form action hijacking - reflected and stored

Open redirection - stored

Burp Infiltrator for Java has been enhanced to correctly deal with some kinds of edge case bytecode that were not previously patched correctly.

Extensions written in Python and Ruby can now import libraries located in Java JARs. You can configure a location for Java libraries at Extender / Options / Java environment. This location is now used for extensions written in Python and Ruby, as well as those written in Java.

Various performance improvements and other minor enhancements have been made.
