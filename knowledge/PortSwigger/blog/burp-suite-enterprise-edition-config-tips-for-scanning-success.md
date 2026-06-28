# Burp Suite Enterprise Edition: config tips for scanning success

Source: https://portswigger.net/blog/burp-suite-enterprise-edition-config-tips-for-scanning-success
Fetched: 2026-06-28T09:15:09.315386+00:00

Burp Suite Enterprise Edition: config tips for scanning success

Matt Atkinson |

Wednesday, 27 April 2022 at 14:01 UTC

Burp Suite Enterprise Edition is the dynamic web vulnerability scanner that can help you to secure your whole portfolio. To help you achieve that, this article contains some advice on how to optimize your dynamic scanning for a range of requirements.

Increase scanning performance

Ensure Burp Scanner has access to the resources it needs

By its nature, dynamic (DAST) scanning can be resource-intensive. Sometimes, new users mistakenly try to run scans on under-specced machines - or with the wrong setup - which can impede, or even halt Burp Scanner's progress. To avoid this, we recommend that you:

Review our minimum system requirements documentation.

Review our networking and firewall configuration documentation.

More generally, you may also find it useful to review our documentation on working with Burp Suite Enterprise Edition.

Tip: Burp Suite Enterprise Edition's built-in scan configurations can also assist in reducing scan durations. This is something to try adjusting, if you're seeing longer than expected scan times.

Optimize signal to noise ratio

Minimize false positives by adjusting your scan configurations

While dynamic (DAST) scanning generally produces low amounts of false positives, Burp Scanner can (as with any automated tool) occasionally flag issues that turn out to be false. If you want to further improve your signal to noise ratio, you may find the following useful:

Try applying the Minimize false positives scan configuration from the built-in library. See our scan configurations documentation for details of how to do this. You may also find it helpful to check your global false positive settings.

Review our documentation on handling false positives.

Extend scan coverage

Fine-tune Burp Scanner for its target application

Web applications vary greatly in their design and complexity. Fortunately, Burp Scanner includes a range of settings allowing you to prepare it for almost any situation - including complex login sequences and heavily stateful functionality. To extend Burp Scanner's coverage, you may find the following useful:

Try applying some of the scan configurations from the built-in library - such as the Most complete crawl strategy, and / or Thorough audit coverage. See our scan configurations documentation for details of how to do this.

Review our documentation on adding application logins to a site (which also covers recorded login sequences).

Review our documentation on browser-powered scanning - especially if scanning an application which makes heavy use of JavaScript.

We're here to help

We hope that this article has been useful. Of course, if you're experiencing a problem that can't be solved using any of the suggestions here, then we'll be happy to help. Please contact PortSwigger Technical Support (if possible, including copies of the logs mentioned in our troubleshooting guide), to help us support you.

Matt Atkinson

@mattatkinson42

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.
