# Professional / Community 2026.1

Source: https://portswigger.net/burp/releases/professional-community-2026-1
Fetched: 2026-06-28T09:16:56.024561+00:00

This release introduces the Discover tab, faster table navigation with command palette, smarter SQLi detection, SPNEGO support for NTLM, plus other improvements, a Java update, and a browser upgrade.

Explore Burp with the new Discover tab

We've replaced the old Learn tab with Discover, a curated starting point to help you explore Burp Suite's full potential. Discover highlights key features, workflows, and learning resources based on your edition, helping you to get the most from the tools available to you.

Whether you're just getting started, fine-tuning a seasoned workflow, or augmenting your skills with Burp AI, there's always something new to explore in Burp.

Faster table navigation with the command palette

You can now jump to specific locations in most tables across Burp Suite using the command palette. We've added three new commands:

Go to top: takes you to the first row of the selected table

Go to bottom: takes you to the final row of the selected table

Go to entry: takes you to a specific row based on the entry ID

These make it quicker and easier to navigate large tables without scrolling, losing your place, or fiddling with filters.

Smarter time-based SQL injection detection

Burp Scanner now filters out false positives caused by web application firewalls (WAFs) delaying suspicious payloads. This improves accuracy in detecting genuine time-based SQL injection in these scenarios.

Support for NTLM authentication via SPNEGO

Burp can now be configured to use SPNEGO encoding for NTLM tokens.

Java update

We've updated Burp's Java version to Java 25.0.1.

Browser upgrade

We've upgraded Burp's browser to Chromium 143.0.7499.193 for Windows & Mac and 143.0.7499.192 for Linux. For more information, see the Chromium release notes.
