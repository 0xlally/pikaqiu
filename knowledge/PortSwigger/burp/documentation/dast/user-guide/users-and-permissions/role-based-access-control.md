# Role-based access control

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/role-based-access-control
Fetched: 2026-06-28T09:15:42.181749+00:00

DAST

Role-based access control

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

Burp Suite DAST uses role-based access control. Once you've added your users, you can manage their permissions using roles and groups:

A user represents a person who has access to Burp Suite DAST via the web interface, or a system that has access via one of the APIs.

A role is a set of permissions to perform specific actions, such as scheduling and deleting scans. You assign roles to groups of users.

A group is a collection of users with an assigned set of roles.

You can also restrict groups to certain sites.

You can configure groups in two different ways:

Through the Burp Suite DAST web interface.

Using SCIM. For more information, see Managing SCIM users and groups.

Vertical segregation of permissions

You can use the roles assigned to a group to provide vertical segregation of permissions. This means that different categories of users can perform different types of actions. For example, you can allow some users to initiate scans, and you can limit others so that they can only view scan results.

Horizontal segregation of permissions

You can restrict users' access to specific sites. This allows for horizontal segregation of permissions, meaning users can only perform their permitted actions on data related to their sites.

Related pages

Managing users and permissions

Adding local users

Enabling single sign-on

Managing users locally

Managing roles locally

Managing groups locally
