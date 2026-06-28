# Authenticated scanning

Source: https://portswigger.net/burp/documentation/scanner/authenticated-scanning
Fetched: 2026-06-28T09:16:09.812312+00:00

Support Center

Documentation

Scanner

Authenticated scanning

DASTProfessional

Authenticated scanning

Last updated:

June 18, 2026

Read time:

1 Minute

When crawling a target application, Burp Scanner attempts to cover as much of the application's attack surface as possible. Authenticated scanning enables Burp to crawl privileged content that requires a login to access, such as user dashboards and admin panels.

Burp Scanner can authenticate with target applications in two ways:

Login credentials are simple username and password pairs. They are intended for sites that use a single-step login mechanism.

Recorded login sequences are user-defined sequences of instructions. They are intended for sites that use complex login mechanisms such as Single Sign-On. You can record login sequences manually, or use Burp AI to record them automatically.

You can only use one authentication method per scan. If you enter both login credentials and a recorded login sequence, Burp Scanner ignores the provided login credentials.

In this section

Login credentials

Identifying login and registration forms

Recorded login sequences

Best practice for recording login sequences

Recording login sequences

Troubleshooting recorded login sequences
