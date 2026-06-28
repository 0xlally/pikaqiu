# Configuring SCIM

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/scim
Fetched: 2026-06-28T09:15:42.968545+00:00

DAST

Configuring SCIM

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

Burp Suite DAST allows you to integrate SCIM in order to simplify the process of provisioning and decommissioning users from a central identity provider (IdP). We have fully tested SCIM integrations with the following IdPs:

Okta

OneLogin

Entra ID

SCIM is typically integrated in conjunction with SAML. This means you're able to create, update, and delete users and groups via SCIM and leave SAML exclusively for handling authentication. This also provides greater transparency because it enables you to view key details about your users and groups directly from Burp Suite DAST.

You can also use SCIM to push your users, then assign groups from Burp Suite DAST.

Note

SCIM is not currently supported for self-hosted Kubernetes instances of Burp Suite DAST.

Related pages

Integrating SCIM using Okta

Integrating SCIM using OneLogin

Integrating SCIM using Entra ID

Managing SCIM users and groups
