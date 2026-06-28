# Restricting access to sites

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/restricting-access-to-sites
Fetched: 2026-06-28T09:15:42.180101+00:00

DAST

Restricting access to sites

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

You can use groups to restrict user access to certain parts of an organization's infrastructure. For example:

Different people have responsibility for operations, finance, and payroll applications.

Different people have access to development, staging, and production systems.

Different people handle applications in different geographical regions.

By default, groups have no restrictions on sites. However, you can configure a group to be restricted to the sites that are relevant to a group's roles. For example, you might want to let a group view scan results for everything within the "Production" folder but disallow the "HR" folder beneath that, because its scan results might contain more sensitive information.

To restrict a group's access to sites:

Log in to Burp Suite DAST as an administrator.

From the Team menu, select Groups.

Select a group from the list, or create a new group.

In the Site restrictions tab, click the folders, subfolders or sites that you want to restrict access to.

When you're happy with your choices, click Save.

Related pages

Role-based access control

Managing users locally

Managing roles locally

Managing groups locally
