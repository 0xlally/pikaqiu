# Managing SCIM users and groups

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/scim/managing-scim
Fetched: 2026-06-28T09:15:42.975137+00:00

DAST

Managing SCIM users and groups

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

Users and groups that are pushed to Burp Suite DAST via SCIM are labeled as such throughout the web UI. You manage these users and groups in a slightly different way to local users that were created directly in Burp Suite DAST.

You can also combine SAML with SCIM. This provides greater transparency because it enables you to view key details about your users and groups from Burp Suite DAST.

Assigning permissions to SCIM users

Just like local users, SCIM users inherit their permissions from the groups they belong to. They can be members of both SCIM groups, and groups that you have created in Burp Suite DAST.

Assigning permissions to SCIM groups

Before you can use SCIM to configure user groups, you need to set up an LDAP or SAML connection for single sign-on (SSO):

Self-hosted Configuring LDAP.

Configuring SAML.

You cannot modify which users belong to a SCIM group from within Burp Suite DAST. However, you can assign roles and site restrictions to them just like you would for a local group.

Removing a SCIM user

You cannot remove or disable a SCIM user from within Burp Suite DAST. Instead, you need to remove their assignment in your identity provider's admin console.

Note for Okta users

Even if you delete a user in Okta, this user will be disabled but still visible in Burp Suite DAST. This is due to the way Okta sends data about deleted users to connected applications. In order to completely remove these users, you need to remove your SCIM integration from the Burp Suite DAST settings.

Related pages

Managing users locally

Managing roles locally

Managing groups locally
