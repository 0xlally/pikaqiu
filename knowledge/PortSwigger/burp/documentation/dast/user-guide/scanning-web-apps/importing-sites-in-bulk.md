# Importing sites in bulk

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-web-apps/importing-sites-in-bulk
Fetched: 2026-06-28T09:15:41.296799+00:00

DAST

Importing sites in bulk

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

Burp Suite DAST's bulk site upload feature makes it easier for you to add large numbers of sites to the system.

Note

Your scanning machines must be able to access the sites you want to scan. For information on allowing access, see Configuring your environment network and firewall settings.

When uploading sites in bulk, you first need to prepare a CSV template with the site information, which you can then upload to Burp Suite DAST. To help you, we provide a sample template that you can edit.

Note

Bulk upload is only available for web app sites.

Preparing the import CSV file

To prepare the upload CSV file:

Click Sites in the menu bar to display the site tree.

Click Import sites. A dialog box is displayed.

Click Download CSV template to save the sites-template.csv file to your browser's default download location.

Open the sites-template.csv file in a spreadsheet or text editor.

Add your sites to the template in the same format as the example.

Delete the first three rows of the file (i.e. the rows containing the field titles, the instruction text, and the sample site).

Save the file in .csv format.

Uploading the CSV file

To upload the CSV file:

Click Sites in the menu bar to display the site tree.

Click Import sites. A dialog box is displayed.

Click Choose file to and select the file you want to upload.

Click Continue.

From the Add sites to existing folder drop-down menu, select the folder that you want to add the sites to.

Click Import.

Burp Suite DAST imports the sites in the file and adds them to the selected folder.

Related pages

Adding new sites - explains how to add new sites individually.

Editing existing sites.
