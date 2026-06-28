# Adding local users

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/adding-local-users
Fetched: 2026-06-28T09:15:41.935979+00:00

DAST

Adding local users

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

You can create users and edit permissions directly from the Burp Suite DAST dashboard. If you have a small number of users, you may want to add all of them locally.

Alternatively, you may want to create local users in addition to those managed by your single sign-on (SSO) solution. Even if you use SSO, we recommend that you create a backup local admin user.

Note

Self-hosted Before you create new users, we recommend connecting your SMTP server. This enables Burp Suite DAST to automatically send email invites to newly created users.

To create a new local user in Burp Suite DAST:

Log in to Burp Suite DAST as an administrator.

From the Team menu, select Add a new user.

In the User credentials section, enter the details for the new user.

Under Choose a login type, select Password.

To allow the user to log in immediately, select Enabled.

Select the groups that you want the user to belong to.

When you're finished, scroll down and click Save.

The new user appears in the list of users. The user should automatically receive an email invite to complete the registration process and obtain their password.

Alternatively, you can copy the link when prompted and email it to the user manually.

Creating an API user

If you need to create a user to enable integration with other software, refer to Creating API users.

Related pages

Enabling SSO

Managing users locally

Managing roles locally

Managing groups locally
