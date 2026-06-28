# Managing groups locally

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/managing-groups
Fetched: 2026-06-28T09:15:41.702584+00:00

DAST

Managing groups locally

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

Groups allow you to map users to their relevant roles. This enables you to assign the permissions for a chosen set of roles to all the users in the group. Users in the group inherit the permissions that are defined in the assigned roles, subject to any restrictions on sites.

Each user can belong to multiple groups. They inherit the roles and permissions from all the groups that they belong to.

You can also use groups to restrict users to certain parts of the site tree.

This section explains how to manage groups locally in Burp Suite DAST. Alternatively, you can use SSO or SCIM to manage groups. For more information, see Managing SCIM users and groups.

Creating a new group

To create a new group:

Log in to Burp Suite DAST as an administrator.

From the Team menu, select Groups.

Click New group.

Enter a Group name.

In the Roles tab, select the roles that you want to assign to the group.

In the Users tab, select the users that you want to assign to the group.

Click Save.

Editing a group

You can edit a group as follows:

Log in to Burp Suite DAST as an administrator.

From the Team menu, select Groups.

From the list, click the group that you want to edit.

Use the Roles and Users tabs to edit the group settings.

When you're finished, click Save.

Restricting access to sites

You can use groups to restrict user access to certain sites. For further information, refer to Restricting access to sites.

Deleting a group

You can only delete custom groups. You can't delete built-in groups. To delete a group:

Log in to Burp Suite DAST as an administrator.

From the Team menu, select Groups.

Find the row for the group that you want to delete, and click .

At the prompt, click Delete.

Related pages

Role-based access control

Managing users locally

Managing roles locally
