# Managing users locally

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/managing-users
Fetched: 2026-06-28T09:15:42.656658+00:00

DAST

Managing users locally

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

A user is a person who has access to Burp Suite DAST through the web interface, or a system that has access via one of the APIs.

This section explains how to create users locally in Burp Suite DAST. Alternatively, you can use SSO and SCIM to manage your users. For more information, see Managing SCIM users and groups.

Burp Suite DAST uses role-based access control. For more information, see Role-based access control.

Viewing users

Log in to Burp Suite DAST as an administrator.

From the Team menu, select All users.

To filter the list of users, click the filter buttons.

Creating a new user

You can either create local users directly in Burp Suite DAST, or configure a SCIM integration to push users from your existing identity provider (IdP). For more information, see:

Adding local users

Enabling single sign-on (SSO)

Editing users

You can edit most of the user details. However, you can't change a user's login type.

To edit an existing user:

Log in to Burp Suite DAST as an administrator.

From the Team menu, select All users.

Click the user in the list and edit their details.

When you're finished, scroll down and click Save.

Note

If you have enabled a SCIM integration, you need to manage any SCIM users and groups using your identity provider's administration console.

Suspending a user temporarily

You can temporarily suspend a user. You may want to do this if they are on extended leave, for example:

Log in to Burp Suite DAST as an administrator.

From the Team menu, select All users.

Click the user in the list.

To temporarily suspend the user, deselect Enabled.

Scroll down and click Save.

Deleting a user

To delete a user:

Log in to Burp Suite DAST as an administrator.

From the Team menu, select All users.

Find the user in the list.

In the right-hand column, click .

At the prompt, click Delete.

Related pages

Role-based access control

Adding local users

Managing roles locally

Managing groups locally
