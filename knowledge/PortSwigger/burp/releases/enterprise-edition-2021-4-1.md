# Enterprise Edition 2021.4.1

Source: https://portswigger.net/burp/releases/enterprise-edition-2021-4-1
Fetched: 2026-06-28T09:16:17.223559+00:00

This release provides the ability to arrange your agent machines and target sites into pools, to better organize your scanning resources. It also includes significant improvements to the user interface and navigation such as a new scan results page design. The release also fixes several bugs.

Agent machine pools

Agent machines and sites are now organized into agent machine pools. All agent machines and all sites are assigned to one and only one agent machine pool. Unless you specify otherwise, all agent machines and sites will be assigned to the same default pool. An agent will only scan a site if the site belongs to the same agent machine pool as the agent's machine.

Agent machine pools support the "agent affinity" concept and are useful if you have a need to limit which agent machines can scan certain sites. Agent machine pools stop the problem of a scan failing because the relevant machine is busy elsewhere, or an assigned agent being unable to access a restricted site for a scan. Sample uses for agent machine pools are:

Keeping the agent machines and sites for one geographic area together.

Allocating the resources of one team.

Scanning sites with restricted access.

Reserving agent machines for specific purposes, such as a CI/CD pipeline or ad-hoc scanning.

UI and navigation improvements

We have improved the user interface and experience throughout Burp Suite Enterprise Edition. These improvements include:

We have improved the way we present scan results, to make access for information quicker and to make understanding the results easier. These changes include a set of tabs to show scan details and a site tree view for scanned sites. See here for the details of the changes.

We have added a new wizard to make integration with Jira easier.

The interface is now more consistent across Teams pages.

We added a page to the help center that directs uses to key category pages of documentation.

We improved navigation throughout Burp Suite Enterprise Edition.

New user permission for viewing site login details

We have created a new user permission for viewing login details (credentials and/or recorded login sequences) associated with sites. This permission is not assigned to any user by default.

Bug fixes

This release also includes several bug fixes, including:

Migrations to MS-SQL databases no longer fail when the username includes a backslash character.

When performing an offline update under Windows, you are now correctly redirected to the updated software.

Scans no longer incorrectly report scan failure when the scan path contains 4-byte unicode characters.

LDAP connections no longer fail when there are Cyrillic characters in the user name.

Filters for the schedule_items query in GraphQL are now enums rather than strings. See more details here.

Requesting issue type descriptions through GraphQL now correctly returns the description and remediation.

Database transfers to databases with custom names now work correctly.

Deleting users who have defined custom scan configurations no longer causes errors.

Users with site restrictions creating sites within folders they don't have permission to view can now correctly see the created site without having to log out and back in again.

Performing a GraphQL query of a site's parent ID via a schedule item in a scan no longer returns an incorrect value.

A browser crashing during a browser-powered scan no longer causes an error message and the scan results to be unavailable.

New to release 2021.4.1

This release provides the following bug fix:

When upgrading from a previous version of Burp Suite Enterprise Edition and using an MS-SQL database, agent machine pool assignments now work correctly, and the site tree loads without errors.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
