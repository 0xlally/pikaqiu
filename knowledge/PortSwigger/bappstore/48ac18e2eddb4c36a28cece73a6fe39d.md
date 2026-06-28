# AWS Cognito

Source: https://portswigger.net/bappstore/48ac18e2eddb4c36a28cece73a6fe39d
Fetched: 2026-06-28T09:14:43.211778+00:00

Support Center

BApp Store

AWS Cognito

Professional

AWS Cognito

Download BApp

This extension helps identify key information from requests to AWS Cognito, provides several passive scan checks, and suggests HTTP request templates for exploiting several known vulnerabilities.

Features:

Proxy History: Adding comments to Burp Proxy History to reflect the Cognito Method found in "X-Amz-Target: AWSCognitoIdentityProviderService.RevokeToken"

Passive Scan Issues:

Log URLs observed matching "^cognito-(?:identity|idp)(?:-fips)?.[^\.]+.amazonaws.com$"

Log Identity Pool IDs observed in requests and suggestions for exploiting it

Log Client IDs observed in requests

Log custom user attributes found in the "idToken" or "GetUser" response

Log "InitiateAuth" requests and suggest request templates for "SignUp" and "UpdateUserAttributes"

Log "AWSCognitoIdentityService.GetCredentialsForIdentity" requests containing temporary credentials

Author

Author

Nick Coblentz

Version

Version

0.1.7

Rating

Rating

Popularity

Popularity

Last updated

Last updated

13 December 2023

Estimated system impact

Estimated system impact

Overall impact:

Empty

Memory

Empty

CPU

Empty

General

Empty

Scanner

Empty

You can install BApps directly within Burp, via the BApp Store feature in the Burp Extender tool. You can also download them from here, for offline installation into Burp.

You can view the source code for all BApp Store extensions on our

GitHub page.

Follow

@BApp_Store on Twitter to receive notifications of all BApp releases and updates.

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.

Go back to

BappStore

Note:

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.
