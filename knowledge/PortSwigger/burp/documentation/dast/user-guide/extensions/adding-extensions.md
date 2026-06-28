# Adding extensions to Burp Suite DAST

Source: https://portswigger.net/burp/documentation/dast/user-guide/extensions/adding-extensions
Fetched: 2026-06-28T09:15:36.534791+00:00

DAST

Adding extensions to Burp Suite DAST

Last updated:

June 18, 2026

Read time:

3 Minutes

When you add extensions to Burp Suite DAST, they are uploaded to your Extension library.

Users can then apply extensions from this central repository on a site-by-site basis for them to be used during scans.

Prerequisite permissions for adding extensions

Only users with the Manage extensions permission can add extensions to the library. Initially, this is only assigned to the built-in Administrator role.

Warning

Be careful when granting this permission to additional users. During a scan, extensions run on your scanning machine with the permissions of the burpsuite OS user. Therefore, there is a potential security risk if someone inadvertently uploads a fake extension created by a malicious third party.

Adding BApps to Burp Suite DAST

To add a BApp:

Download the BApp from the BApp Store. Make sure that it is compatible with Burp Suite DAST - you can filter the store to make this easier.

Log in to Burp Suite DAST as a user with permission to manage extensions.

From the settings menu , select Extensions to open the Extension library.

On the BApp extensions tab, click Upload BApp.

Select the .bapp file that you downloaded from the BApp Store.

The extension is now in your Extension library. Your users can apply the extension to specific sites to use it during scans.

Adding custom extensions to Burp Suite DAST

If you're proficient in Java, you can create your own custom extensions for Burp Suite DAST. Learn more about Creating Burp

extensions.

Requirements for extensions

To use an extension with Burp Suite DAST, it needs to meet the following conditions:

The extension is written in Java 21 or lower.

The extension doesn't require user interaction, or the use of the user interface.

The extension doesn't use features that are exclusive to Burp Suite Professional or Community Edition, such as Repeater, Intruder, or Proxy.

Adding a custom extension

To add a custom extension:

Log in to Burp Suite DAST as a user with permission to manage extensions.

From the settings menu , select Extensions to open the Extension library.

On the Custom extensions tab, click Upload extension.

Select the JAR file for the extension.

Enter a name and description for the extension, then click Add.

The extension is now in your Extension library.

Your users can apply the extension to specific sites to use it during scans.

Adding BChecks to Burp Suite DAST

You can download BChecks created by PortSwigger, and by the Burp Suite community, from the BChecks GitHub repository.

If you have access to Burp Suite Professional, you can also create your own custom scan checks, enabling you to target your scans and make your testing workflow as efficient as possible.

For more information, see Creating custom scan checks.

To add a BCheck:

Log in to Burp Suite DAST as a user with permission to manage extensions.

From the settings menu , select Extensions to go to the Extension library.

On the BChecks tab, click Upload BCheck.

Select the BCheck you want to upload.

Files that you want to import should be in plain text format with a .bcheck extension.

The extension is now in your Extension library. Your users can apply the extension to specific sites to use it during scans.
