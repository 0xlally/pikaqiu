# Integrating SCIM using OneLogin

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/scim/onelogin
Fetched: 2026-06-28T09:15:43.230216+00:00

DAST

Integrating SCIM using OneLogin

Last updated:

June 18, 2026

Read time:

4 Minutes

Cloud

Self-hosted

In this section, we'll guide you through the process of integrating SCIM with Burp Suite DAST using OneLogin as your identity provider (IdP).

Prerequisites

You already have your users set up in OneLogin.

If you want to use SCIM in conjunction with SAML, you have already created a SCIM Provisioner with SAML (SCIM v2 Core) application in OneLogin and have completed the SAML configuration.

Get your SCIM URL and API token

You need to obtain the SCIM URL and API token. OneLogin uses these to communicate with Burp Suite DAST. The process is different for obtaining these for Cloud and self-hosted instances.

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

For production use, we strongly recommend enabling TLS on the connection by uploading a PKCS#12 certificate. Note that this must have the .p12 file extension - certificates in .pfx format are not supported.

From the settings menu , select Integrations.

On the SCIM tile, click Edit.

Under Configure SCIM, activate the Use TLS toggle.

When prompted, upload your certificate and enter the certificate password.

Click Save.

Configure the connection in OneLogin

Once you've got your SCIM URL and generated an API token in Burp Suite DAST, you can use this information to configure the connection from OneLogin.

Enter the connection details

In OneLogin, select the application that you created for Burp Suite DAST.

From the left-hand navigation menu, select Configuration and scroll down to the API Connection section.

In the SCIM Base URL field, enter your SCIM URL.

In the Custom Headers field, add the following header:

Content-Type: application/scim+json

In the SCIM Bearer Token field, enter the API token that you copied from Burp Suite DAST.

In the SCIM JSON Template field, paste the following template:

{

"schemas": [

"urn:ietf:params:scim:schemas:core:2.0:User"

],

"userName": "{$parameters.scimusername}",

"name": {

"givenName": "{$user.firstname}",

"familyName": "{$user.lastname}"

},

"emails": [

{

"primary": true,

"value": "{$user.email}",

"type": "work"

}

],

"displayName": "{$user.display_name}"

}

At the top of the API Connection section, under API Status, click the button to enable the connection.

Save your changes.

Configure the parameters

In OneLogin, select the application that you created for Burp Suite DAST.

From the left-hand navigation menu, select Parameters.

Click the entry for the NameID parameter.

In the dialog that opens, change the value of this parameter to Username.

Save your changes.

Enable SCIM provisioning

Once you've successfully configured the SCIM connection between OneLogin and Burp Suite DAST, you can enable SCIM provisioning so that you can sync your users and groups.

In OneLogin, select the application that you created for Burp Suite DAST.

From the left-hand navigation menu, select Provisioning.

Under Workflow, select the Enable provisioning checkbox.

Configure the rest of the settings on this page however you like. We recommend choosing the option to delete users when they are deleted in OneLogin or their app access is removed. Otherwise, redundant users will still be visible in Burp Suite DAST.

Save your changes.

Push your OneLogin users to Burp Suite DAST

Once you have successfully configured the OneLogin integration, you can push your users so that they are available in Burp Suite DAST. To do this, just assign your users and roles to the application that you created in OneLogin.

After a while, these users will be available in Burp Suite DAST. Any changes you make to these users in OneLogin will automatically be synced. However, note that users will not have access to any functionality unless they are assigned to a group with the relevant roles in Burp Suite DAST.

Note

You can push users from OneLogin, but not groups. When using OneLogin as your IdP, you need to create and manage all of your group assignments directly in Burp Suite DAST.

Troubleshooting provisioning issues in OneLogin

To check that all of your users were provisioned successfully:

In OneLogin, select the application that you created for Burp Suite DAST.

From the left-hand navigation menu, select Users.

In the Provisioning State column, check for any users with the status Failed.

If you find any users that were not provisioned successfully, click the name of the user and in the dialog that opens, click Reset Login. This will clear the user's current provisioning state and re-attempt to provision the user.
