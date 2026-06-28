# Configuring NTLM with Burp Suite

Source: https://portswigger.net/support/configuring-ntlm-with-burp-suite
Fetched: 2026-06-28T09:17:34.240600+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Configuring NTLM with Burp Suite

Burp's Platform Authentication settings let you configure Burp to automatically carry out platform authentication to destination web servers. Different authentication types and credentials can be configured for individual hosts.

Windows Challenge/Response (NTLM) is the authentication protocol used on networks that include systems running the Windows operating system and on stand-alone systems. In this article we'll demonstrate how to configure Burp Suite with an application using NTLM authentication.

NTLM credentials are based on data obtained during the interactive logon process and consist of a domain name, a user name, and a one-way hash of the user's password.

When an application is using NTLM authentication, you will need to configure Burp Suite to automatically carry out the authentication process.

You can configure these settings at User Options > Connections > Platform Authentication.

Use the Add function to configure new credentials.

Select the correct authentication type and add the appropriate credentials.

With the credentials configured correctly, Burp automatically carries out the NTLM authentication, allowing access to the destination application web server.
