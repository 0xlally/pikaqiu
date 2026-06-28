# Configuring single logout

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/saml/slo
Fetched: 2026-06-28T09:15:42.797721+00:00

DAST

Configuring single logout

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

Burp Suite DAST provides optional support for single logout (SLO). You can configure SLO after you configure SAML SSO.

If you enable SLO, users are automatically logged out of the identity provider when they log out of Burp Suite DAST. This prevents users from inadvertently remaining logged in to multiple applications.

To configure single logout:

Generate a new self-signed x509 certificate.

Log in to Burp Suite DAST as an administrator.

From the settings menu , select Integrations.

On the SAML tile, click Edit.

In Relying trust information, copy the Relying party single logout URL. Leave this page open.

Go to your identity provider's admin panel and edit the SAML settings for your Burp Suite DAST integration.

Paste the URL from your clipboard into the appropriate field.

Obtain the Single Logout URL from your identity provider. This may have a different name depending on your identity provider.

In Burp Suite DAST, select Use single logout.

In the Identity provider single logout URL field, enter the URL you obtained from your identity provider.

Paste your self-signed certificate in Service provider certificate.

Paste the private key for your certificate in Service provider private key.

Note

Some identity providers, such as Okta, require that Burp Suite DAST signs all the single logout messages that it generates. This is necessary to verify that they come from a trusted source. In this case, you may also need to upload the certificate that you generated to your identity provider.
