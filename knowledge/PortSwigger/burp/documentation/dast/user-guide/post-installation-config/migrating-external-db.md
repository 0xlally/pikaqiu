# Migrating to an external database

Source: https://portswigger.net/burp/documentation/dast/user-guide/post-installation-config/migrating-external-db
Fetched: 2026-06-28T09:15:38.994819+00:00

DAST

Migrating to an external database

Last updated:

June 18, 2026

Read time:

3 Minutes

Self-hosted

If you are using Burp Suite DAST's bundled H2 database, you can migrate to an external one at any time.

The migration process involves the following phases:

Preparing for the migration

Migrating your data

Restarting the Burp Suite DAST services

Note

The database_transfer tool only migrates data from Burp Suite DAST's embedded H2 database to a supported external database. It cannot migrate data from one external database to another.

For a list of supported external databases, see System requirements for your external database.

Preparing for the migration

Set up your new database. Keep a note of the credentials that you create.

Stop all scans.

On each scanning machine, stop the burpsuiteenterpriseedition_agent services.

Perform a backup of the bundled database. You can do this from the Burp Suite DAST web UI in the database backup settings.

On the DAST server, stop the burpsuiteenterpriseedition_enterpriseserver and burpsuiteenterpriseedition_webserver services.

Create a copy of the enterprise-server.config file, in case you need to revert to using the original database.

Prerequisite steps for Oracle databases

To migrate to an Oracle database, you need to perform some additional steps before you begin transferring your data.

On the machine on which you installed the DAST server and web server:

Download the required driver (ojdbc8.jar) from the Oracle website.

Copy the downloaded file to the following locations:

<installation-directory>/databaseTransferTool/<version>/lib/ojdbc8.jar

<installation-directory>/enterpriseServer/<version>/lib/ojdbc8.jar

<installation-directory>/webServer/<version>/lib/ojdbc8.jar

To make sure that the drivers are installed as part of any future updates, create the following empty marker files:

<installation-directory>/enterpriseServer/.oracle

<installation-directory>/webServer/.oracle

Make sure that the ownership and permissions of the newly created files match those of the other files in their respective directories. This should mean that the files are readable by all users.

You also need to perform the following steps on each of your scanning machines. This applies to both internal scanning machines and external scanning machines:

Install the driver by adding the downloaded ojdbc8.jar file to the following location:

<installation-directory>/enterpriseAgent/<version>/lib/ojdbc8.jar

Create an empty marker file in the following location:

<installation-directory>/enterpriseAgent/.oracle

Make sure that the permissions for the marker file match the other files in the directory.

When these steps are complete on all of your machines, you can proceed with the rest of the migration process.

Migrating your data

Restart your database server.

On the DAST server machine, open a command prompt.

From the installation directory, run database_transfer as either the burpsuite user or root. If you don't have the database_transfer tool, see Running the database transfer command manually.

Provide the JDBC URL and credentials for the new external database.

If you don't have the database_transfer tool, or the command fails with an error message, see Running the database transfer command manually.

Data is transferred table by table and progress is reported in the console. Once the migration is complete, a summary of the rows transferred per table is reported. The enterprise-server.config file is updated with the new database connection details.

Running the database transfer command manually

For most users, the database_transfer tool is automatically installed as part of the main Burp Suite DAST installation process. However, if your first version of Burp Suite DAST was 2023.9 or earlier, you may not have the tool or it may fail to run. In this case, you need to run the database transfer command manually:

From a command prompt, navigate to your Burp Suite DAST installation directory.

Enter the following command, replacing the variables with the appropriate values:

sudo ./jre/bin/java -cp "databaseTransferTool/<version>/lib/*" net.portswigger.enterprise.database.transfer.DatabaseTransferMain <installation-directory> <data-directory>/data

Key

<version> is the version number of your current Burp Suite DAST installation, for example, 2020.6.

<installation-directory> is the directory where Burp Suite DAST is installed.

<data-directory> is the directory where your Burp Suite DAST data is stored. You specified this directory during the installation process.

The resulting command would look something like this:

cd /opt/burpsuite_enterprise/

sudo ./jre/bin/java -cp "databaseTransferTool/2020.6/lib/*" net.portswigger.enterprise.database.transfer.DatabaseTransferMain /opt/burpsuite_enterprise/ /var/lib/BurpSuiteEnterpriseEdition/data

Restarting the Burp Suite DAST services

On the DAST server machine, restart the burpsuiteenterpriseedition_enterpriseserver and burpsuiteenterpriseedition_webserver services.

On each of your scanning machines, restart the burpsuiteenterpriseedition_agent services.
