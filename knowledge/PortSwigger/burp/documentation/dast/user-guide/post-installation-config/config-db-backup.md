# Configuring database backups

Source: https://portswigger.net/burp/documentation/dast/user-guide/post-installation-config/config-db-backup
Fetched: 2026-06-28T09:15:38.793872+00:00

DAST

Configuring database backups

Last updated:

June 18, 2026

Read time:

1 Minute

Self-hosted

If you use the bundled H2 database, you can control your database backup settings from within Burp Suite DAST as follows:

Log in to Burp Suite DAST.

From the settings menu , select Database backup.

To change the location for your saved backup files, edit the Location of backups field.

To change the number of backup files to retain, edit the Number of backups to store field.

If necessary, set how often you want the backups to repeat.

To backup your database manually, click Backup now.

Note

If you use an external database, your database administrator manages your backup settings outside of Burp Suite DAST.
