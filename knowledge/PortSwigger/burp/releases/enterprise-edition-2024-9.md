# Enterprise Edition 2024.9

Source: https://portswigger.net/burp/releases/enterprise-edition-2024-9
Fetched: 2026-06-28T09:16:21.304702+00:00

This release introduces two new issue management features: accepted risk marking and severity adjustment. We've also made some other improvements, and fixed some bugs.

Enhanced issue management options

We’ve added some new features to make managing your issues easier:

Accepted risk:You can now mark known issues as accepted risks when they either don't require further action, or when you have mitigating controls in place.

Edit issue severity: You can now adjust the severity rating of issues to better match your organization's risk management framework.

You can leave notes to keep track of why each decision was made.

Combined with the existing false positive option, these features enable you to manage your security issues with more accuracy and control.

Other improvements

We've made some other improvements, including:

If you manually add bearer token authentication to an API site, we no longer ask you to fill in a format field. You'll still see the format field if you manually added bearer token authentication to your site before this update.

We now validate URLs when you create an API site. If the URL isn't valid, you will not be able to save the site and you will be prompted to review the URL.

Bug fixes

We fixed the following bugs:

You can now update Burp Suite Enterprise Edition without errors if you are using API authentication and a Microsoft SQL database.

If you upload an API definition file that has a parameterized server URL, the file is now parsed correctly.
