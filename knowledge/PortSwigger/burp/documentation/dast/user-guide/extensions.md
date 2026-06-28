# Extensions in Burp Suite DAST

Source: https://portswigger.net/burp/documentation/dast/user-guide/extensions
Fetched: 2026-06-28T09:15:36.184684+00:00

DAST

Extensions in Burp Suite DAST

Last updated:

June 18, 2026

Read time:

1 Minute

You can add extensions to Burp Suite DAST to implement custom scan behaviors and capabilities.

There are three different types of extension:

BChecks - BChecks are custom scan checks that you can create and import. Burp Suite DAST runs these checks in addition to its built-in scanning routine, helping you to target

your scans and make your testing workflow as efficient as possible. You can download BChecks from the BChecks GitHub repository.

BApps - BApps are community-written extensions that we have reviewed against a set of quality guidelines. You can download approved BApps for free from our BApp Store. BApps that are compatible with Burp Suite DAST have a DAST tag.

Custom extensions - Custom extensions are any extensions that you have not downloaded from the BApp Store.

When you add extensions to Burp Suite DAST, they are uploaded to your Extension library.

Users can then apply extensions from this central repository on a site-by-site basis for them to be used during scans.

Extension library

The Extension library is a collection of all extensions that you have made available to your users.

To access the Extension library, from the settings menu , select Extensions.

The Extension library is split into three tabs, one for managing BChecks, one for managing BApps, and one for managing your custom extensions. From here, you can:

Add new extensions.

Manage your existing extensions.
