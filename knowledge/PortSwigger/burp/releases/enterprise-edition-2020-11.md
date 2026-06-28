# Enterprise Edition 2020.11

Source: https://portswigger.net/burp/releases/enterprise-edition-2020-11
Fetched: 2026-06-28T09:16:16.581278+00:00

This release provides a new application logins option that will enable scans to handle single sign-on and other complex login mechanisms. Please note that this upgrade includes some major changes to the GraphQL API as a result.

Recorded login sequences

When adding application logins to a site, instead of simply adding basic sets of user credentials, you now have the option to upload recorded login sequences instead. A recorded login sequence is essentially a script that tells Burp Scanner exactly how to log in to the site. This enables it to handle more complex login mechanisms, including single sign-on.

To generate this script, you use our dedicated Chrome extension to record your browser interactions while you perform the login sequence manually. You then upload this script to the relevant site in Burp Suite Enterprise Edition. When scans of this site begin an authenticated crawl, Burp Scanner will start a new session in its embedded browser and use this script to replicate your actions, performing the full login sequence from scratch.

For more information, please refer to the documentation.

API scanning

Burp Scanner is now able to scan both JSON and YAML-based APIs for vulnerabilities. By default, the crawler attempts to parse any API definitions that it encounters to identify potential endpoints, along with their supported methods and parameters. Based on the endpoints that it discovers, Burp Scanner is then able to derive new locations to crawl and audit.

You can also explicitly provide the URL of an API definition in the list of included URLs for a site.

Please note that this initial release only supports scanning of a fairly limited range of REST APIs. For a full list of the prerequisites and limitations, please refer to the Burp Scanner documentation. We plan to further develop this feature and gradually add support for a wider range of APIs in future releases.

GraphQL API updates

In order to implement the new functionality for uploading recorded login sequences, we've had to make some changes to the GraphQL API. These changes may require you to refactor your existing integrations before they will work with this version of Burp Suite Enterprise Edition.

Generally speaking, the entities related to application logins have now been split in two. This is to create the distinction between sets of basic login credentials and recorded login sequences.

The full list of changes is as follows:

The type ApplicationLogin is now obsolete. This has been replaced by two new types, LoginCredential and RecordedLogin.

The new type ApplicationLogins has been added. This provides two fields, login_credentials and recorded_logins, which contain a list of LoginCredential and RecordedLogin objects respectively.

Fields that used to contain a list of the obsolete ApplicationLogin objects now contain a single object of the new type ApplicationLogins. This affects the following fields:

The site_application_logins and schedule_item_application_logins fields of Scan objects

The application_logins field of Site objects

The following mutations are now obsolete:

create_site_application_login

update_site_application_login

delete_site_application_login

These have been replaced by the following new mutations:

create_site_login_credential

create_site_recorded_login

update_site_login_credential

delete_site_login_credential

delete_site_recorded_login

Please note that you can add either LoginCredential or RecordedLogin objects to a Site, but not both. Querying the application_logins field for a Site will return a single ApplicationLogins object for which only one of the login_credentials and recorded_logins fields will contain data.

Improved logging

We have improved the logging of certain processes, which should make it easier to troubleshoot any problems that arise. For example, there is now much greater transparency in the log entries when backing up your database. When errors occur with Jira, the log now also provides much more detail about what the problem is.

When a scan check is abandoned due to memory allocation issues, this is now indicated in the scan results, the list of scans, and the downloadable reports. Previously, this would only be mentioned in the event log, which meant that it was easy to miss.

Bug fixes

This release also provides the following bug fixes:

The installer now works for users with an external database.

The database migration scripts no longer fail when migrating a PostgreSQL or MySQL database on Azure.

When the Enterprise server is connected to your SMTP server but cannot connect to portswigger.net, you no longer receive an excessive number of emails about this issue.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
