# Configuring SAML SSO with Okta

Source: https://portswigger.net/burp/documentation/dast/user-guide/users-and-permissions/sso/saml/okta
Fetched: 2026-06-28T09:15:42.852060+00:00

DAST

Configuring SAML SSO with Okta

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

This section explains how to configure SAML SSO using Okta as your identity provider. You may also need to refer to the Okta documentation.

Before you start

Make sure your web server URL includes protocol and port information. For more information, see Configuring your web server.

Note

The relying party trust information is dependent on your web server URL.

Step 1: Add Burp Suite DAST to your trusted applications

To add Burp Suite DAST to your trusted applications:

Log in to Burp Suite DAST as an administrator.

From the settings menu , select Integrations.

On the SAML tile, click Configure. Notice that you can copy the Relying party trust identifier, the Relying party service URL, and the Relying party single logout URL.

In Okta, go to the dashboard and sign in as an administrator.

Create a new app integration using SAML 2.0.

When you create the new integration, paste the Relying party service URL into the Single sign-on URL field.

Select the Use this for Recipient URL and Destination URL tick box.

Paste the Relying party trust identifier into the Audience URI field.

Step 2: Add a Group Attribute Statement

Add a Group Attribute Statement in Okta as follows:

In the Name field, enter http://schemas.xmlsoap.org/claims/Group.

Leave the Name format as Unspecified.

Set the Filter to Matches regex, and enter .*.

Step 3: Obtain key details from Okta

To configure Burp Suite DAST, you need to obtain the following Sign On information from Okta's SAML 2.0 settings page:

The Sign on URL. Burp Suite DAST sends users to this URL when they choose to log in using SAML.

The Issuer URL. This is the URL that is sent as the Issuer value in SAML responses.

The Signing Certificate. Burp Suite DAST uses this to verify that the SAML response was genuinely issued by Okta. Download this and keep it for the next step.

Step 4: Enter the key details in Burp Suite DAST

To enter the key details in Burp Suite DAST:

In Burp Suite DAST, make sure that you're still on the SAML page.

In Company details, enter your company name.

In SAML configuration, enter the following information:

In the Identity provider Entity ID field, enter the Issuer URL from Okta.

In the Identity provider SSO URL field, enter the Sign on URL from Okta.

Open the Signing Certificate that you downloaded from Okta in a text editor, and copy the certificate. Paste the certificate into the Identity provider token signing public certificate field.

Click Save.

Step 5: Test your configuration

Once the connection is established, we recommend that you test your configuration:

Log out of Burp Suite DAST and Okta.

Go to Burp Suite DAST, and notice that a new login panel is added to the login page. It has the same name as the Name field that you set in Okta.

Click Login in the new panel, and sign in with your Okta username and password.

If the configuration was successful, you will now be logged into Burp Suite DAST. However, you won't yet have permission to do anything.

Managing groups

You can now configure how you manage your groups:

You can push the groups from your identity provider using SCIM. For more information, see Configuring SCIM.

Alternatively, you can duplicate your Okta groups in Burp Suite DAST, and manage them locally. For more information, see Enabling Burp Suite DAST to access your Okta groups.
