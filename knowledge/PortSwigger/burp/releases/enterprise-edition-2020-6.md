# Enterprise Edition 2020.6

Source: https://portswigger.net/burp/releases/enterprise-edition-2020-6
Fetched: 2026-06-28T09:16:16.739009+00:00

This release provides major usability improvements and adds support for single sign-on. We are also pleased to announce a beta release for the cloud-native Burp Suite Enterprise Edition on both AWS and Azure.

UI improvements

Over the next few months, we're working on improving the usability of Burp Suite Enterprise Edition by upgrading the UI. This release includes the first set of these changes:

The header menu has been redesigned to make it much easier to navigate. You can now jump straight to the most commonly used parts of the application with a single click.

The pages for creating, editing, and viewing both sites and scans have been redesigned to make them much more intuitive.

The overall look-and-feel of some screens has been updated. These changes will be rolled out across other parts of the application in upcoming releases.

Single sign-on

You can now configure an LDAP connection between Burp Suite Enterprise Edition and your Active Directory. This enables you to manage your Burp Suite Enterprise Edition users centrally using single sign-on, just like you might already do with other applications.

Once you configure the connection, you simply create user groups in Burp Suite Enterprise Edition that correspond to the groups in your Active Directory. Users can then log in using their existing credentials. User permissions within the application are controlled on the group level, removing the need to create and manage dedicated users for Burp Suite Enterprise Edition.

For more information, please refer to the product documentation.

Bug fixes

We have also implemented several minor bug fixes and performance improvements.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
