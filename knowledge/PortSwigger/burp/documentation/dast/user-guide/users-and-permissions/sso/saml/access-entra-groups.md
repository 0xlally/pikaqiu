# Enabling Burp Suite DAST to access your Entra ID groups

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/saml/access-entra-groups
Fetched: 2026-06-28T09:15:42.681563+00:00

DAST

Enabling Burp Suite DAST to access your Entra ID groups

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

If you're not using SCIM, you can create groups in Burp Suite DAST that have identical names to your groups in Entra ID. This enables you to duplicate and manage these groups locally.

To configure your groups in a way that Burp Suite DAST can recognize:

In the Entra ID portal, open the application that represents Burp Suite DAST.

Under Set up Single Sign-on with SAML, go to User Attributes and Claims and add a group claim.

Select the Customize the name of the group claim checkbox and enter the following values:

Name: Group

Namespace: http://schemas.xmlsoap.org/claims

The next step depends on how you manage your users:

If your Entra ID instance is backed by an on-premise installation of Active Directory, select sAMAccountName as the source attribute. Note that when you create your user groups in Burp Suite DAST, they must have the exact same name as the corresponding sAMAAccountName in your Active Directory.

If your users are managed in Entra ID, select Group ID as the source attribute. In this case, you will need to use the corresponding Group ID as the name for your user groups in Burp Suite DAST.

Adding your groups to Burp Suite DAST

The next step is to grant permissions, by matching the names of groups that you create in Burp Suite DAST with your Entra ID groups. For more information, see Configuring groups for SAML or LDAP.
