# Managing scripts in your Bambda library

Source: https://portswigger.net/burp/documentation/desktop/extend-burp/bambdas/managing
Fetched: 2026-06-28T09:15:46.284195+00:00

Support Center

Documentation

Desktop editions

Extending Burp

Bambdas

Managing scripts

ProfessionalCommunity Edition

Managing scripts in your Bambda library

Last updated:

June 18, 2026

Read time:

2 Minutes

You can store and manage scripts in the Extensions > Bambda library tab. This enables you to organize your scripts for easy reuse across your Burp projects. To add scripts to the library either create and save your own or import them from our GitHub repository.

Scripts are listed in a table with the following information:

Name - The name of the script.

Function - The task that the script is designed to perform. For example, View filter or Custom column.

Location - The tool in Burp that the script is intended to be used in. For example, HTTP history or Logger.

Last modified - The time and date that the script was most recently saved to the library.

You can filter the table contents as follows:

Search the table - Click Search and enter an expression.

Filter the table - Click the Filter settings bar to open the Bambda library filter window. You can filter by

Function and Location.

Related pages

To learn about actions you can take to quickly edit the filter settings, see Managing the filter settings.

You can customize and sort the table, and copy column data to your clipboard. For more information, see Customizing Burp's tables.

Importing scripts

You can import script files that have been shared with you or downloaded from our Bambdas GitHub repository. For information on how to do this and how to keep your imported scripts up-to-date, see Importing scripts into your Bambda library.

Warning

Bambda scripts can run arbitrary code. For security reasons, please be cautious when using scripts from unverified sources.

Creating scripts

You can create scripts directly from the Bambda library. For more information, see Creating scripts.

Exporting scripts

To share scripts with others, select scripts in the Bambda library, then click . They're exported as .bambda files.

Each file includes a unique ID, name, function, and location as metadata. Burp uses the unique ID to recognize and match scripts. It is important to preserve the unique ID when sharing your script, as this ensures consistency and prevents conflicts if the script is reimported.

Related pages

For more information about how the unique ID is used when re-importing scripts, see Importing scripts - Updating your scripts.

You can share your scripts with the community by adding them to our ever-growing Bambdas GitHub repository. For more information, see Submitting scripts to our GitHub repository.

Managing scripts

You can perform the following actions on the scripts in your library:

Edit - Select the script that you want to edit, then click .

Copy - Select the script that you want to copy, then click .

Delete - Select the script that you want to delete, then click .

Note

If a script in your Bambda library defines a scan check function, any edits you make to that script are also reflected in your custom scan checks library, under

Extensions > Custom scan checks.
