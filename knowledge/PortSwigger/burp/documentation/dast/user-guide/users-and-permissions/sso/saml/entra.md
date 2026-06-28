# Configuring SAML SSO with Entra ID

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/saml/entra
Fetched: 2026-06-28T09:15:42.686277+00:00

DAST

Configuring SAML SSO with Entra ID

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

This section explains how to configure SAML SSO using Entra ID (formerly Azure AD) as your identity provider. You may also need to refer to the Entra ID documentation.

Before you start

Make sure your web server URL includes protocol and port information. For more information, see Configuring your web server.

Note

The relying party trust information is dependent on your web server URL.

Step 1: Configure your Entra ID Enterprise Application

To add Burp Suite DAST to your Entra ID Enterprise Applications:

Log in to Burp Suite DAST as an administrator.

From the settings menu , select Integrations.

On the SAML tile, click Configure. Notice that you can copy both the Relying party trust identifier and the Relying party service URL.

In Entra ID, go to Basic SAML Configuration.

Paste the Relying party service URL into the Reply URL (Assertion Consumer Service URL) field.

Paste the Relying party trust identifier into the Identifier (Entity ID) field.

Step 2: Import key details from Entra ID

To configure Burp Suite DAST, you need to import some key details from Entra ID (formerly Azure AD):

In Entra ID, go to the SAML Signing Certificate page.

Download the Federation Metadata XML file.

In Burp Suite DAST, make sure that you're still on the SAML page.

In Company details, enter your company name.

In SAML configuration, click Import metadata.

Click Choose file and select the Federation metadata XML file.

Click Save.

Step 3: Test your configuration

Once the connection is successfully established, we recommend that you test your configuration by logging in to Burp Suite DAST. If the configuration was successful, you will see a message that you have logged in, but you don't yet have permission to do anything.

Managing groups

You can now configure how you manage your groups:

You can push the groups from your identity provider using SCIM. For more information, see Configuring SCIM.

Alternatively, you can duplicate your Entra ID groups in Burp Suite DAST, and manage them locally. For more information, see Enabling Burp Suite DAST to access your Entra ID groups
