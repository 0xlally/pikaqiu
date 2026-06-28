# Enterprise Edition 2023.9

Source: https://portswigger.net/burp/releases/enterprise-edition-2023-9
Fetched: 2026-06-28T09:16:19.554743+00:00

This release enables you to include login details when you bulk-import sites. We've also increased the character limit for custom headers and cookies.

Configuring login details for bulk site imports

You can now include login details for sites when using the bulk import CSV template. To enable this, we've added three new columns:

Labels

Usernames

Passwords

For more information about importing sites in bulk, see Importing sites in bulk.

Other improvements

We've increased the number of characters that you can add to custom headers and cookies to 8192 characters. This enables you to use much longer JWTs, for example.

Bug fixes

We've fixed the following bugs:

If you delete a start URL from a site with multiple start URLs, the list of start URLs is now updated correctly.

Users with some site restrictions can now create new sites, using the New site button.

When you add or delete extensions for your sites, they now save correctly.

The database transfer tool is now installed as part of the Burp Suite Enterprise Edition installation process.

For Kubernetes deployments, if you modify the network settings they now save correctly.
