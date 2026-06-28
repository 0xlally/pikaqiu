# Enterprise Edition 2020.10

Source: https://portswigger.net/burp/releases/enterprise-edition-2020-10
Fetched: 2026-06-28T09:16:16.041061+00:00

This release further improves Burp Suite Enterprise Edition's support for single sign-on by enabling SAML integration. It also provides major improvements to the AWS deployment process.

SAML integration

Burp Suite Enterprise Edition now supports SAML-based single sign-on. This is particularly useful for managing user authentication for cloud-based deployments.

You can integrate SAML SSO using any identity provider (IdP), but the following ones have been fully tested:

Active Directory Federation Services (ADFS)

Okta

Azure Active Directory

To configure the connection to your preferred SAML IdP, log in to Burp Suite Enterprise Edition as an administrator, select "Single sign-on" from the settings menu, then open the "SAML connection" tab.

For more detailed information, please refer to the accompanying documentation.

Other improvements

This release also provides the following improvements:

When marking all issues of the same type as false positives, you can now choose to limit this to the current scan only.

Empty placeholder pages have been improved. In each case, you will now be informed why the page is empty and prompted to perform the relevant actions to populate it with data.

Sites and folders are now displayed in alphabetical order in the site tree.

Performance has been improved when running scans that use a large number of scan configurations.

Bug Fixes

We have also provided the following bug fixes:

Reinstalling Burp Suite Enterprise Edition for use with an existing database no longer causes issues.

You can now successfully run the installer over an existing installation, for example, to fix any missing libraries.

When the API key is generated for a new API user, long domain names no longer cause the URL to exceed the boundaries of the text field.

The option for creating Jira sub-tasks has been removed to avoid invalid issue type errors. Creating sub-tasks is not supported by the Jira API.

You can now update the port for your web server's HTTPS URL without having to upload a new certificate.

We have made minor corrections to the GraphQL API reference documentation.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
