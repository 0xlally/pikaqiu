# Configuring SAML SSO with ADFS

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/saml/adfs
Fetched: 2026-06-28T09:15:42.689895+00:00

DAST

Configuring SAML SSO with ADFS

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

This section explains how to configure SAML SSO using Active Directory Federation Services (ADFS) as your identity provider. You may also need to refer to the ADFS documentation.

Before you start

Make sure your web server URL includes protocol and port information. For more information, see Configuring your web server.

Note

The relying party trust information is dependent on your web server URL.

Step 1: Add Burp Suite DAST to your trusted applications

To add Burp Suite DAST to your trusted applications:

Log in to Burp Suite DAST as an administrator.

From the settings menu , select Integrations.

On the SAML tile, click Configure. Notice that you can copy both the Relying party trust identifier and the Relying party service URL.

In ADFS, run the Add Relying Party Trust wizard.

Paste the Relying party service URL into the Relying party SAML 2.0 SSO Service URL field.

Paste the Relying party trust identifier into the Relying party trust identifier field.

Step 2: Obtain key details from ADFS

To configure Burp Suite DAST, you need to obtain the following key details from ADFS:

The Entity ID. This is the URL that is sent as the Issuer value in SAML responses.

The SSO URL. Burp Suite DAST sends users to this URL when they choose to log in using SAML.

The token-signing certificate. Burp Suite DAST uses this to verify that the SAML response was genuinely issued by ADFS.

For more information on how to find these, see the ADFS documentation.

Step 3: Enter the key details in Burp Suite DAST

To enter the key details in Burp Suite DAST:

In Burp Suite DAST, make sure that you're still on the SAML page.

In Company details, enter your company name.

Enter the key details in the relevant fields.

Click Save.

Step 4: Test your configuration

Once the connection is successfully established, we recommend that you test your configuration by logging in to Burp Suite DAST. If the configuration was successful, you will see a message that you have logged in, but you don't yet have permission to do anything.

Managing groups

You can now configure how you manage your groups:

You can push the groups from your identity provider using SCIM. For more information, see Configuring SCIM.

Alternatively, you can duplicate your ADFS groups in Burp Suite DAST, and manage them locally. For more information, see Enabling Burp Suite DAST to access your ADFS groups
