# Integrating SCIM using Entra ID

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/scim/entra-id
Fetched: 2026-06-28T09:15:43.428266+00:00

DAST

Integrating SCIM using Entra ID

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

This section explains how to integrate SCIM with Burp Suite DAST using Entra ID as your identity provider.

Prerequisites

You have created an Entra ID enterprise application.

You have assigned your users and groups to the enterprise application.

You have a Microsoft Entra ID P1 or P2 license (required for group provisioning).

Make sure your firewall allows inbound access to your Burp Suite DAST instance on your chosen SCIM port, for example 8090.

Get your SCIM URL and API token

You need to obtain the SCIM URL and API token. Entra ID uses these to communicate with Burp Suite DAST.

Cloud instances

Log in to Burp Suite DAST as an administrator.

From the Settings menu, select Integrations.

On the SCIM tile, click Configure.

Copy the displayed SCIM URL.

Click Generate API token.

Save the new API token somewhere secure.

Self-hosted instances

Log in to Burp Suite DAST as an administrator.

From the Settings menu, select Integrations.

On the SCIM tile, click Configure.

Configure the SCIM port. Enter the port that you want to use for the SCIM URL. Use a different port to your web server URL, so you can configure separate firewall rules. We recommend enabling TLS (see the TLS section below for details).

Note your SCIM URL format: https://<host>:<port>/scim/v2

The host is usually the same domain name or IP address used in the Burp Suite DAST web server URL. This may differ depending on your network infrastructure.

The port is the SCIM port you configured (not the web server port).

Click Save & generate API token.

Save the new API token somewhere secure.

Note

If you lose your API token, you can generate a new one by clicking Regenerate API token in the upper-right corner of the SCIM settings page.

Upload a TLS certificate

Self-hosted

For production use, we strongly recommend enabling TLS on the connection by uploading a PKCS#12 certificate. Note that this must have the .p12 file extension - certificates in .pfx format are not supported.

From the Settings menu, select Integrations.

On the SCIM tile, click Edit.

Under Configure SCIM, select the Use TLS toggle.

When prompted, upload your certificate and enter the certificate password.

Click Save.

Configure the connection in Entra ID

Once you've got your SCIM URL and generated an API token in Burp Suite DAST, you can use this information to configure the connection from Entra ID. The SCIM URL format is https://<host>:<port>/scim/v2 where the port is the SCIM port (not the web server port).

Enter the connection details

In Entra ID, create an enterprise application.

From the left-hand navigation menu, select Provisioning.

Under Create configuration, click Connect your application.

In the Tenant URL field, enter your SCIM URL.

In the Secret token field, enter the API token.

Click Test Connection and make sure the connection was successful.

Click Create.

Enable SCIM provisioning

Once you've successfully configured the SCIM connection between Entra ID and Burp Suite DAST, you need to add users and groups, then enable SCIM provisioning so that you can sync your users and groups.

Click Manage on the left-hand side menu.

Select Users and groups.

Add users and groups as needed.

Go back to the Overview page.

Click the play button to start provisioning. The configuration status will show as enabled.

After a while, your users and groups will be available in Burp Suite DAST. Users will not have access to any functionality unless they are assigned to a group with the relevant roles in Burp Suite DAST.

Important

After users and groups are provisioned to Burp Suite DAST, you must still assign appropriate roles and permissions to the groups within Burp Suite DAST. Provisioning alone does not provide access to functionality.

For more information, see Managing users and permissions.

Note

You can only push groups from Entra ID if you have a Microsoft Entra ID P1 or P2 license.

Troubleshooting provisioning issues in Entra ID

To check that all of your users were provisioned successfully:

In Entra ID, select the Enterprise Application that you created for Burp Suite DAST.

From the left-hand navigation menu, select Provisioning.

On the Overview tab, make sure that the Configuration status is Enabled.

On the Monitoring tab, click View provisioning logs. Review the logs to assist with troubleshooting.

Related pages

Managing SCIM users and groups

Configuring SAML SSO with Entra ID
