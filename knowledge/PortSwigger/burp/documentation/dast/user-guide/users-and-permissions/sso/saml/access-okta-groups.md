# Enabling Burp Suite DAST to access your Okta groups

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/saml/access-okta-groups
Fetched: 2026-06-28T09:15:42.912859+00:00

DAST

Enabling Burp Suite DAST to access your Okta groups

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

Self-hosted

If you're not using SCIM, you can create groups in Burp Suite DAST that have identical names to your groups in Okta. This enables you to duplicate and manage these groups locally.

To configure your Okta Group Attribute statements in a way that Burp Suite DAST can recognize:

From the Okta admin console, go to SAML settings for your Burp Suite DAST integration.

Create Group Attribute Statements with the following values:

Name: http://schemas.xmlsoap.org/claims/Group

Name format: Unspecified

Filter: Matches regex

Value: .*

The filter value determines which groups will be sent. The regex in this example makes sure that all groups are sent. If you want to limit the selection to a particular subset of groups, refer to the Okta documentation.

Adding your groups to Burp Suite DAST

The next step is to grant permissions, by matching the names of groups that you create in Burp Suite DAST with your Okta groups. For more information, see Configuring groups for SAML or LDAP.
