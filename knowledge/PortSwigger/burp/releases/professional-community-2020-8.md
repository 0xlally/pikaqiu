# Professional / Community 2020.8

Source: https://portswigger.net/burp/releases/professional-community-2020-8
Fetched: 2026-06-28T09:16:33.792531+00:00

This release provides an upgrade to the web cache poisoning scan checks as well as several other minor improvements and bug fixes.

New web cache poisoning scan checks

Burp Scanner can now identify a variety of recently discovered cache poisoning issues. These checks are based on the techniques documented by James Kettle in his presentation "Web Cache Entanglement: Novel Pathways to Poisoning" at BlackHat USA 2020. For more information about web cache poisoning, please see the following links:

Practical Web Cache Poisoning whitepaper

Web Cache Entanglement whitepaper

Learn about web cache poisoning on the Web Security Academy

Other improvements

We have improved the performance of Burp Intruder when using HTTP/2.

We have reduced the amount of noise from the embedded browser by disabling Chromium's random DNS checks during startup.

Bug fixes

Closing the first tab in the embedded browser no longer causes the whole browser window to close.

You can now launch the embedded browser on Kali Linux even as a non-root user
