# Configuring authentication for web apps

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-web-apps/configure-authentication
Fetched: 2026-06-28T09:15:41.244268+00:00

DAST

Configuring authentication for web apps

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

Adding authentication credentials for web app sites enables Burp Scanner to discover and audit content that is only accessible to authenticated users.

You can add the following types of authentication credentials:

Site login details

Platform authentication details

Note

This page explains how to configure web app authentication. For information on how to configure API authentication, see Adding new APIs.

Configuring login details

Adding login credentials for a web app site enables Burp Scanner to discover and audit content that is only accessible to authenticated users.

There are two types of login credential that you can add in Burp Suite DAST:

Username and password pairs are intended for web apps that use a basic, single-step login mechanism.

Recorded login sequences are intended for web apps that use more complex login mechanisms, such as Single Sign-On, TOTP MFA, or WebAuthn. You can create recorded login sequences manually, or record them using Burp AI.

You can only use one of the available login mechanisms per site.

Related pages

Adding usernames and passwords

Adding recorded login sequences

Managing steps in a recorded login

Configuring TOTP MFA

WebAuthn passkeys in recorded logins

Configuring platform authentication details

Adding credentials for NTLM and HTTP Basic authentication enables Burp Scanner to automatically authenticate to destination web servers at the platform level.

Related pages

Configuring platform authentication
