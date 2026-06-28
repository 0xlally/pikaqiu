# Configuring LDAP single sign-on for Burp Suite DAST

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/ldap
Fetched: 2026-06-28T09:15:42.352222+00:00

DAST

Configuring LDAP single sign-on for Burp Suite DAST

Last updated:

June 18, 2026

Read time:

2 Minutes

Self-hosted

If you have a self-hosted instance of Burp Suite DAST, you can configure LDAP-based single sign-on (SSO). This enables your users to log in with their existing Active Directory credentials.

To configure the LDAP connection between Burp Suite DAST and your Active Directory server:

Log in to Burp Suite DAST as an administrator.

From the settings menu , select Integrations.

On the LDAP tile, click Configure.

Under Connection details, select LDAP or LDAPS. We recommend using LDAPS wherever possible.

In the Server field, enter the IP address or hostname of your Active Directory server.

Note

The port updates automatically. By default, LDAP uses port 389 and LDAPS uses port 636.

Under Service account details, enter the username and password for a valid Active Directory service account. This is used to query your Active Directory when authenticating users.

Specify the base distinguished name from which Burp Suite DAST should search for users. All the users that you want to manage must be children of this base distinguished name.

Select a Login method. This determines whether users log in with their UserPrincipalName or their sAMAccountName.

When you are happy with your entries, click Check Connection.

To use a self-signed certificate for LDAPS, upload the root certificate when prompted if necessary.

Testing your configuration

Once the connection is successfully established, you can test your configuration by logging in to Burp Suite DAST. If the configuration was successful, you will see a message that you have logged in, but you don't yet have permission to do anything.

You can now configure user groups and permissions for your users. For more information, see Configuring groups for SAML or LDAP.
