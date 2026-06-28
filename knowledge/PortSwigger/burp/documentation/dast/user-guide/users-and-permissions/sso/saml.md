# Configuring SAML single sign-on for Burp Suite DAST

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/saml
Fetched: 2026-06-28T09:15:42.502597+00:00

DAST

Configuring SAML single sign-on for Burp Suite DAST

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

Burp Suite DAST supports SAML-based single sign-on (SSO). This allows users to log in with their existing credentials.

Note

You can also integrate SCIM in combination with SAML. This enables you to create, update, and delete users and groups via SCIM and use SAML exclusively for authentication.

Combining SCIM and SAML enables you to view key details about your users and groups from Burp Suite DAST.

Before you configure Burp Suite DAST to use SAML, you need to enable HTTPS on your web server. Refer to Configuring your web server and follow the instructions to enable TLS.

Make sure your web server URL includes protocol and port information. The relying party trust information is dependent on your web server URL.

We've fully tested SAML integration with the following identity providers:

Active Directory Federation Services (ADFS)

Okta

Entra ID (formerly Azure AD)

Related pages

Configuring SAML SSO with ADFS.

Enabling Burp Suite DAST to access your ADFS groups.

Configuring SAML SSO with Okta.

Enabling Burp Suite DAST to access your Okta groups.

Configuring SAML SSO with Entra ID.

Enabling Burp Suite DAST to access your Entra ID groups.

Configuring single logout
