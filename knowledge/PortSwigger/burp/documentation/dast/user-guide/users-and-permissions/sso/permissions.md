# Creating local groups for SAML or LDAP

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/permissions
Fetched: 2026-06-28T09:15:42.370694+00:00

DAST

Creating local groups for SAML or LDAP

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

If you're not using SCIM, you can duplicate your SAML or LDAP groups in Burp Suite DAST and manage them locally. You do this by creating groups in Burp Suite DAST that have identical names to your SAML or LDAP groups.

Note

You can add local users to the local groups in Burp Suite DAST. However, you won't be able to see any users that are managed by SAML or LDAP.

To create local groups for SAML or LDAP in Burp Suite DAST:

Log in to Burp Suite DAST as an administrator.

From the Team menu, select Groups.

Click New group.

Create a new group representing each of the groups of users in your Active Directory or SAML identity provider. Make sure that the groups you create have exactly the same names as the ones you send from Active Directory or your SAML identity provider.

If you manage your users directly in Entra ID (formerly Azure AD), you will need to use the Group ID instead. For more information, see Configuring SAML SSO with Entra ID.

Assign roles to your groups as required. If you do not assign any roles, users can log in but they can't access any functionality.

Apply site restrictions for each group as necessary. This limits which sites users in each group can access.

Users can now log in to Burp Suite DAST using their existing credentials. For SAML SSO, users need to click the link on the login page to authenticate themselves via your identity provider.

Related pages

Managing users locally

Managing roles locally

Managing groups locally

Restricting access to sites

Resetting your admin password
