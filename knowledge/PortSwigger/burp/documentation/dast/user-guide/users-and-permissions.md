# Managing users and permissions

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions
Fetched: 2026-06-28T09:15:41.509143+00:00

DAST

Managing users and permissions

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

Burp Suite DAST uses role-based access control to manage permissions for your users. For more information, see Role-based access control.

You can add users to Burp Suite DAST locally, or using single sign-on (SSO).

Note

Even if you want to manage user authentication with your existing SSO solution, we recommend that you create a backup local admin user.

Managing users locally

You can add and manage your users individually through the Burp Suite DAST dashboard. You can do this for all your users, or you can combine it with your SSO solution. For more information, see Adding local users.

Using SSO

Burp Suite DAST supports authentication via the LDAP and SAML SSO standards. You can also create and remove users via SCIM. For more information, see Enabling SSO.

Warning

Be cautious when creating users and assigning permissions. Users may be able to access and exploit internal systems if your infrastructure isn't sufficiently secured. To mitigate this risk, it's crucial to limit the creation of new users and assign permissions carefully.

Related pages

Role-based access control

Adding local users

Enabling SSO

Managing users locally

Managing roles locally

Managing groups locally

Restricting access to sites

Resetting your admin password
