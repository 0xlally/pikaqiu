# Unattended installation of Burp Suite DAST

Source: https://portswigger.net/burp/documentation/dast/user-guide/reference/unattended-installation
Fetched: 2026-06-28T09:15:40.042939+00:00

DAST

Unattended installation of Burp Suite DAST

Last updated:

June 18, 2026

Read time:

6 Minutes

You can install Burp Suite DAST via the installation wizard or you can perform an unattended / silent installation via the command line.

When installing silently, the required input passes in a varfile. This is much more efficient when installing on multiple machines. The easiest way to prepare the varfile is to perform a manual installation on a single machine. This generates a varfile that already contains the required parameters. You can reuse this file to perform future unattended installations.

Note

You only need one license for each instance of Burp Suite DAST. Dedicated scanning machines connected to your DAST server do not need their own license.

If you want to deploy additional Burp Suite DAST servers (for example, for testing in staging or development), you must purchase a separate license for each one. Data is not shared between servers, and each is a separate instance.

If you have any questions about your licensing requirements, please contact our customer support team at hello@portswigger.net.

This page contains the following sections:

Performing an unattended installation with Linux.

Performing an unattended installation with Windows.

A guide to the varfile fields.

Note

Once the unattended installation is complete, you need to manually create the admin user. If you use an external database, you also need to manually configure the database. The sections below include instructions for these steps.

Performing an unattended installation with Linux

This section explains how to perform an unattended installation with Linux.

Perform an unattended installation of the DAST server

To perform an unattended installation of the DAST server, you need to add some values that are not stored by the installer into the response.varfile. You can then pass the edited file to the installer from the command line.

Generate a response.varfile for DAST server deployment

Perform a manual installation using the same options that you want to use for your unattended installations. This generates the response.varfile in the .install4j subdirectory of your installation directory.

Note

If you have already deployed a DAST server, you can just copy the existing response.varfile.

The default installation directory is /opt/burpsuite_enterprise/.install4j.

Example response.varfile

The following is an example of a response.varfile.

# install4j response file for Burp Suite DAST 2022.11-11262

beuser=burpsuite

beuserandgroup=burpsuite\:burpsuite

dataDirectory=/var/lib/BurpSuiteEnterpriseEdition

dbType=postgres

escapedDataDir=/var/lib/BurpSuiteEnterpriseEdition

escapedInstallationDir=/opt/burpsuite_enterprise

jreHome=/opt/burpsuite_enterprise/jre

logsDirectory=/var/log/BurpSuiteEnterpriseEdition

platformScriptSuffix=sh

sys.adminRights$Boolean=true

sys.adminRightsUiRootUnix$Boolean=true

sys.component.agent$Boolean=false

sys.component.db$Boolean=false

sys.component.enterprise$Boolean=true

sys.component.web$Boolean=true

sys.installationDir=/opt/burpsuite_enterprise

sys.languageId=en

sys.programGroupDisabled$Boolean=true

webserver_port$Integer=8443

Note

Earlier versions of Burp Suite DAST required you to enter additional parameters regarding the database and admin user into the varfile. This is no longer necessary, as this information is now entered during the initial setup process.

Perform an unattended DAST server deployment using the response.varfile

Use Terminal to enter the following command:

sudo sh burpsuite_enterprise_linux_v2022_5.sh -q -varfile response.varfile

-q runs the installer in unattended mode.

-varfile enables you to specify a response file.

Configure the application

Once the DAST server is installed, you need to create an admin user. If you're using an external database, you also need to configure the database. To configure these details:

To access the configuration page, visit https://localhost:<port> in your browser. Replace <port> with the port specified in the varfile.

Follow the instructions to configure the application.

Performing an unattended installation for scanning machines

To perform an unattended installation for a scanning machine, you can simply copy a response.varfile from an existing scanning machine installation and pass it to the installer from the command line.

Generate a response.varfile for scanning machine deployment

Perform a manual installation using the same options that you want to use for your unattended installations. This generates the response.varfile in the .install4j subdirectory of your installation directory.

Note

If you have already deployed a scanning machine, you can just copy the existing response.varfile.

The default installation directory is /opt/burpsuite_enterprise/.install4j.

Example response.varfile

The following is an example of a response.varfile.

# install4j response file for Burp Suite DAST 2022.11-11262

beuser=burpsuite

beuserandgroup=burpsuite\:burpsuite

dataDirectory=/var/lib/BurpSuiteEnterpriseEdition

dbType=postgres

enterprise_server_address=x.x.x.x

escapedDataDir=/var/lib/BurpSuiteEnterpriseEdition

escapedInstallationDir=/opt/burpsuite_enterprise

jreHome=/opt/burpsuite_enterprise/jre

logsDirectory=/var/log/BurpSuiteEnterpriseEdition

platformScriptSuffix=sh

sys.adminRights$Boolean=true

sys.adminRightsUiRootUnix$Boolean=true

sys.component.agent$Boolean=true

sys.component.db$Boolean=false

sys.component.enterprise$Boolean=false

sys.component.web$Boolean=false

sys.installationDir=/opt/burpsuite_enterprise

sys.languageId=en

sys.programGroupDisabled$Boolean=true

Perform an unattended scanning machine deployment using the response.varfile

Use Terminal to enter the following command:

sudo sh burpsuite_enterprise_linux_v2022_5.sh -q -varfile response.varfile

-q runs the installer in unattended mode.

-varfile allows you to specify a response file.

The scanning machine fingerprint is sent to standard output (stdout).

Performing an unattended installation with Windows

This section explains how to perform an unattended installation with Windows.

Perform an unattended installation of the DAST server

To perform an unattended installation of the DAST server, you need to add some values that are not stored by the installer into the response.varfile. You can then pass the edited file to the installer from the command line.

Generate a response.varfile for DAST server deployment

Perform a manual installation using the same options that you want to use for your unattended installations. This generates the response.varfile in the .install4j subdirectory of your installation directory.

Note

If you have already deployed a DAST server, you can just copy the existing response.varfile.

The default installation directory is C:\Program Files\burpsuite_enterprise\.install4j.

The following is an example of a response.varfile.

# install4j response file for Burp Suite DAST 2022.11-11262

dataDirectory=C\:\\ProgramData\\BurpSuiteEnterpriseEdition

dbType=mssql

escapedDataDir=C\:/ProgramData/BurpSuiteEnterpriseEdition

escapedInstallationDir=C\:/Program Files/burpsuite_enterprise

jreHome=C\:\\Program Files\\burpsuite_enterprise\\jre

logsDirectory=C\:\\ProgramData\\BurpSuiteEnterpriseEdition

platformScriptSuffix=bat

sys.adminRights$Boolean=true

sys.component.agent$Boolean=false

sys.component.db$Boolean=false

sys.component.enterprise$Boolean=true

sys.component.web$Boolean=true

sys.installationDir=C\:\\Program Files\\burpsuite_enterprise

sys.languageId=en

sys.programGroupAllUsers$Boolean=true

sys.programGroupDisabled$Boolean=false

sys.programGroupName=Burp Suite DAST

webserver_port$Integer=8443

Note

Earlier versions of Burp Suite DAST required you to enter additional parameters regarding the database and admin user into the varfile. This is no longer necessary, as this information is now entered during the initial setup process.

Perform an unattended DAST server deployment using the response.varfile

Use the command prompt as an administrator to enter the following command:

"burpsuite_enterprise_windows-x64_v2022_5.exe" -q -c -varfile response.varfile

-c runs the installer in command line mode.

-q runs the installer in unattended mode.

-varfile enables you to specify a response file.

Configure the application

Once the DAST server is installed, you need to create an admin user. If you're using an external database, you also need to configure the database. To configure these details:

To access the configuration page, visit https://localhost:<port> in your browser. Replace <port> with the port specified in the varfile.

Follow the instructions to configure the application.

Performing an unattended installation for scanning machines

To perform an unattended installation for a scanning machine, you can simply copy a response.varfile from an existing scanning machine installation and pass it to the installer from the command line.

Generate a response.varfile for scanning machine deployment

Perform a manual installation using the same options that you want to use for your unattended installations. This generates the response.varfile in the .install4j subdirectory of your installation directory.

Note

If you have already deployed a scanning machine, you can just copy the existing response.varfile.

The default installation directory is C:\Program Files\burpsuite_enterprise\.install4j.

Example response.varfile

The following is an example of a response.varfile.

# install4j response file for Burp Suite DAST 2022.11-11262

dataDirectory=C\:\\ProgramData\\BurpSuiteEnterpriseEdition

dbType=mssql

enterprise_server_address=x.x.x.x

escapedDataDir=C\:/ProgramData/BurpSuiteEnterpriseEdition

escapedInstallationDir=C\:/Program Files/burpsuite_enterprise

jreHome=C\:\\Program Files\\burpsuite_enterprise\\jre

logsDirectory=C\:\\ProgramData\\BurpSuiteEnterpriseEdition

platformScriptSuffix=bat

sys.adminRights$Boolean=true

sys.component.agent$Boolean=true

sys.component.db$Boolean=false

sys.component.enterprise$Boolean=false

sys.component.web$Boolean=false

sys.installationDir=C\:\\Program Files\\burpsuite_enterprise

sys.languageId=en

sys.programGroupAllUsers$Boolean=true

sys.programGroupDisabled$Boolean=false

sys.programGroupName=Burp Suite DAST

Perform an unattended scanning machine deployment using the response.varfile

Use the command prompt as an administrator to enter the following command:

"burpsuite_enterprise_windows-x64_v2022_5.exe" -q -c -varfile response.varfile

-c runs the installer in command line mode.

-q runs the installer in unattended mode.

-varfile allows you to specify a response file.

The scanning machine fingerprint is sent to standard output (stdout).

Varfile field guide

This section describes the most relevant varfile fields.

Specifying the script type

For Linux, use platformScriptSuffix=sh.

For Windows, use platformScriptSuffix=bat.

Installing components

The following varfile fields install components:

sys.component.agent$Boolean=true - Set to true to install the scanning component.

sys.component.db$Boolean=true - Set to true to install the built-in database. Set to false if you are using your own database.

sys.component.enterprise$Boolean=true - Set to true to install the Burp DAST server.

sys.component.web$Boolean=true - Set to true to install the Burp DAST server.

Database settings

If you use the built-in database, you must specify the database backup directory:

databaseBackupsDirectory=/var/lib/BurpSuiteEnterpriseEdition

If you use your own external database, set the webserver_port field to 8443:

webserver_port$Integer=8443

To change this value after installation, edit the network settings. For more information refer to Configuring your environment network and firewall settings.

Database type fields

Built-in database: h2.

MariaDB: mariadb.

Microsoft SQL Server: mssql.

MySQL: mysql.

Oracle: oracle.

PostgreSQL: postgres.
