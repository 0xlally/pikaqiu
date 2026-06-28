# Recorded login sequences

Source: https://portswigger.net/burp/documentation/scanner/authenticated-scanning/recorded-login-sequences
Fetched: 2026-06-28T09:16:10.118531+00:00

Support Center

Documentation

Scanner

Authenticated scanning

Recorded login sequences

DASTProfessional

Recorded login sequences

Last updated:

June 18, 2026

Read time:

2 Minutes

When configuring application logins for a scan, you can import a recorded login sequence rather than supplying basic user credentials. A recorded login sequence is a set of instructions that tell Burp Scanner how to log in to the website.

Recorded login sequences enable Burp to handle complex authentication mechanisms, including:

Single sign-on.

Multi-step logins in which the username and password are not entered in the same form.

Login forms that contain, for example, extra fields or checkboxes.

TOTP multi-factor authentication.

WebAuthn.

Note

When running a recorded login sequence, Burp Scanner can temporarily follow any out-of-scope links that are necessary to perform the login sequence. However, these locations are not crawled or audited as part of the scan.

Recorded login sequences are especially useful if you are using Burp Suite DAST to automate scanning across a large application portfolio. In this case, you may be able to record an application's login sequence once and re-use it multiple times.

Using recorded login sequences

You can record login sequences in two ways:

Manually: To record login sequences manually, use the Login Recorder for Burp Suite. This Chrome extension captures your interactions with the website while you perform the login sequence. It then generates a JSON-based "script" that you can import into Burp Suite Professional or Burp Suite DAST.

Using Burp AI: You can use Burp AI to record login sequences autonomously, saving time and reducing the chance of human error. For more information on how to do this in Burp Suite Professional, see Generating recorded login sequences using AI. For more information on how to do this in Burp Suite DAST, see Using Burp AI to record login sequences.

Note

We recommend that you read the Best practice for recording login sequences documentation before attempting to record a login sequence. This page contains advice that should help you to record login sequences that work first time.

Related pages

Best practice for recording login sequences.

Recording login sequences.

Troubleshooting recorded login sequences.
