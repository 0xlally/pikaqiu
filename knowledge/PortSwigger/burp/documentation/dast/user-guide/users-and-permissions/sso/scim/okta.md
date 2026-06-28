# Integrating SCIM using Okta

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/scim/okta
Fetched: 2026-06-28T09:15:43.010661+00:00

DAST

Integrating SCIM using Okta

Last updated:

June 18, 2026

Read time:

4 Minutes

Cloud

Self-hosted

In this section, we'll guide you through the process of integrating SCIM with Burp Suite DAST using Okta as your identity provider (IdP).

Prerequisites

Your users and groups are set up in Okta.

You have already created a custom app integration for Burp Suite DAST in Okta and completed the SAML configuration.

If you want to integrate SCIM without setting up SAML, use Okta's pre-built SCIM 2.0 Test App (Header Auth) app integration from the app catalog instead. Note that in this case, some of the steps described here may vary.

Get your SCIM URL and API token

First, you need to get the SCIM URL and API token for Okta to use to communicate with Burp Suite DAST. The process for doing this differs slightly depending whether you're using a Cloud or self-hosted instance.

Log in to Burp Suite DAST as an administrator.

From the settings menu, select Integrations.

On the SCIM tile, click Configure.

Get your SCIM URL:

Cloud Your SCIM URL is automatically generated and displayed on screen for you to copy.

Self-hosted The base URL takes the following format:

https://<host>:<port>/scim/v2

The host is usually the same domain name or IP address as in the Burp Suite DAST web server URL. However, this may differ depending on your network infrastructure. Enter the port that you want to use for the SCIM URL. This should be a different port than the one you use for the web server URL so that you can configure separate firewall rules for this connection.

Get your API key:

Cloud Click Generate API token.

Self-hosted Click Save & generate API token.

When prompted, copy and save the new API token somewhere secure.

Note

If you lose your API token, you can generate a new one by clicking Regenerate API token in the upper-right corner of the SCIM settings page.

Upload a TLS certificate

Self-hosted

Okta only supports SCIM over HTTPS. This means that you need to enable TLS by uploading a PKCS#12 certificate. Make sure that the certificate has the .p12 file extension. Certificates in .pfx format are not supported.

To upload a TLS certificate:

From the settings menu , select Integrations.

On the SCIM tile, click Edit.

In Configure SCIM, activate Use TLS.

Click Upload certificate.

When prompted, click Choose file and select the certificate.

Enter the certificate password.

Click Save.

Configure the connection in Okta

Once you've got your SCIM URL and generated an API token in Burp Suite DAST, configure the connection from Okta as follows:

Enable SCIM provisioning

Log in to Okta.

Go to Applications and select the app integration that you created for Burp Suite DAST.

Go to the General tab.

In the App Settings section, click Edit.

Under Provisioning, select the Enable SCIM provisioning checkbox.

Save your changes.

Enter the connection details

In Okta, select the app integration that you created for Burp Suite DAST.

Go to the Provisioning tab.

From the Settings menu on the left, select Integration.

In the SCIM Connection panel, click Edit.

In the SCIM connector base URL field, enter your SCIM URL.

In the Unique identifier field for users field, enter userName.

Under Supported provisioning actions, select only the following options:

Push New Users.

Push Profile Updates.

Push Groups.

Under Authentication mode, select HTTP header.

In the Authorization field, enter the API token that you copied from Burp Suite DAST.

To confirm that the connection is working correctly, click Test Connector Configuration.

Save your changes.

Configure the provisioning to app settings

In Okta, select the app integration that you created for Burp Suite DAST.

Go to the Provisioning tab.

From the Settings menu on the left, select To App.

In the Provisioning To App section, click Edit.

Use the checkboxes to enable the following settings:

Create Users.

Update User Attributes.

Deactivate Users.

If you're not using SAML, enable and configure the Sync Password setting.

Save your changes.

Push your Okta users and groups to Burp Suite DAST

To push your users and groups to Burp Suite DAST, do the following steps.

To push users:

In Okta, select the app integration that you created for Burp Suite DAST.

Go to the Assignments tab.

Decide how to assign your users:

To assign individual users, click Assign > Assign to People.

To assign all users from a particular group to the application, click Assign > Assign to Groups.

Warning

Assigning groups to the app integration pushes all users belonging to that group to Burp Suite DAST. However, it does not push the actual group. To avoid synchronization issues, we recommend that you create a separate group in Okta which you only use to bulk-assign users to Burp Suite DAST.

To push groups:

Warning

Do not push the group you created for bulk-assigning users to Burp Suite DAST.

In Okta, select the app integration that you created for Burp Suite DAST.

Go to the Push Groups tab.

Click Push Groups > Find Group By Name and select the relevant group.

You may need to wait a short while for the users or groups to become available in Burp Suite DAST. Any changes you make in Okta sync automatically. Note that users do not have access to any functionality unless you assign them to a group with the relevant roles in Burp Suite DAST.

Related pages

Managing users locally

Managing roles locally

Managing groups locally
