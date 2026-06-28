# Setting up the external database (Standard)

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/standard/setup-external-database
Fetched: 2026-06-28T09:15:33.850878+00:00

DAST

Setting up the external database (Standard)

Last updated:

June 18, 2026

Read time:

4 Minutes

In this section, we'll show you how to set up a database that you want to connect to Burp Suite DAST. This is relevant in the following cases:

You want to set up a standard instance of Burp Suite DAST from scratch.

You have been using Burp Suite DAST's embedded database and want to transfer your data to an external one.

Preparing the database for Burp Suite DAST involves the following high-level steps:

Connect to your database server.

Run the setup script for your database type. This creates a database and two users for Burp Suite DAST.

Save the connection URL for your database. You will need this later to connect Burp Suite DAST.

Note

For more information on external database system requirements for standard instances, see External database system

requirements.

Database setup scripts

The setup scripts below create a new database and two users: burp_enterprise and burp_agent. These are used by the DAST server and your scanning machines to connect to your database.

If you're setting up this database in order to migrate from the embedded one, you must use these exact usernames.

You should substitute the placeholder ******** strings used in the example script with your own strong passwords.

PostgreSQL

Oracle

MariaDB / MySQL

Microsoft SQL Server

Note

AWS Aurora databases are not supported.

PostgreSQL

CREATE DATABASE burp_enterprise;

CREATE USER burp_enterprise PASSWORD '********';

CREATE USER burp_agent PASSWORD '********';

GRANT ALL ON DATABASE burp_enterprise TO burp_enterprise;

\c burp_enterprise postgres

GRANT ALL ON SCHEMA public TO burp_enterprise;

Oracle

CREATE TABLESPACE burp_enterprise_tabspace;

CREATE USER burp_enterprise DEFAULT TABLESPACE burp_enterprise_tabspace QUOTA UNLIMITED ON burp_enterprise_tabspace IDENTIFIED BY ********;

GRANT CREATE PROCEDURE, CREATE SEQUENCE, CREATE SESSION, CREATE TABLE, CREATE TRIGGER, CREATE SYNONYM, CREATE PUBLIC SYNONYM, DROP PUBLIC SYNONYM TO burp_enterprise;

CREATE USER burp_agent IDENTIFIED BY ********;

GRANT CREATE SESSION to burp_agent;

MariaDB / MySQL

CREATE DATABASE burp_enterprise CHARACTER SET = 'utf8mb4' COLLATE = 'utf8mb4_unicode_ci';

CREATE USER 'burp_enterprise'@'%' IDENTIFIED BY '********';

CREATE USER 'burp_agent'@'%' IDENTIFIED BY '********';

GRANT ALL PRIVILEGES ON burp_enterprise.* TO 'burp_enterprise'@'%' WITH GRANT OPTION;

If you encounter errors when trying to install a MySQL database, please refer to the troubleshooting section below for details on how to resolve some known issues.

Microsoft SQL Server

sp_configure 'contained database authentication', 1;

RECONFIGURE;

CREATE DATABASE burp_enterprise CONTAINMENT = PARTIAL;

USE burp_enterprise;

CREATE USER burp_enterprise WITH PASSWORD = '********';

CREATE USER burp_agent WITH PASSWORD = '********';

ALTER ROLE db_owner ADD MEMBER burp_enterprise;

Authentication mode

To support password-based logins, you also need to make sure that the Windows Authentication and SQL Server Authentication option is enabled for the installation. This option is sometimes referred to as Mixed Mode Authentication.

Additional configuration for Microsoft SQL Server

Burp Suite DAST uses Microsoft's JDBC driver to connect to SQL Server databases. By default, the driver only lets you connect to databases that have a valid TLS certificate signed by a public certificate authority. Therefore, you need to install a suitable certificate on your SQL Server instance before attempting to connect to it from Burp Suite DAST. For details on how to do this, please refer to the Microsoft SQL Server documentation.

Note

As a temporary workaround, you can bypass this certificate validation by appending ;trustServerCertificate=true to the JDBC connection URL that you provide when deploying Burp Suite DAST.

For untrusted networks, we do not recommend this as a long-term solution. It potentially enables malicious third parties to intercept traffic on the connection to your database.

Database connection URL format

To connect Burp Suite DAST to your new database, you will need to provide the JDBC URL in various places. The format for this URL differs slightly depending on the database type.

PostgreSQL: jdbc:postgresql://<host>:5432/burp_enterprise

Oracle: jdbc:oracle:thin:@//<host>:1521/<instance-id>

MariaDB / MySQL: jdbc:mysql://<host&gt:3306/burp_enterprise

Microsoft SQL Server: jdbc:sqlserver://<host>:1433;databaseName=burp_enterprise

Troubleshooting for MySQL databases

This section explains how to resolve some known issues that occur when completing installation with a MySQL database.

Multiple primary keys defined

Some managed service providers have enabled the generated invisible primary keys variable by default for MySQL. For example, Azure Database for MySQL has enabled this variable for version 8.0 and above. If this variable is enabled, an invisible primary key is added to any InnoDB table that is created without an explicit primary key. This means that multiple primary keys are defined, resulting in the following exception:

liquibase.exception.MigrationFailedException: Migration failed for change set

...

liquibase.exception.DatabaseException: (conn=1645) Multiple primary key defined

To resolve the issue, disable the sql_generate_invisible_primary_key variable. Please refer to the service provider's documentation for instructions.

RSA public key is not available client side

When using the default authentication mechanism for MySQL 8, the Burp Suite DAST driver validates the public key of the database. If the key is self-signed, you the following exception is displayed:

liquibase.exception.DatabaseException: liquibase.exception.DatabaseException: java.sql.SQLTransientConnectionException: Could not connect to address=(host=127.0.0.1)(port=3306)(type=master) : RSA public key is not available client side (option serverRsaPublicKeyFile not set)

There are several options for resolving this issue:

Use a certificate signed by a well-known certification authority instead.

Distribute the public key of the self-signed certificate manually. Please see the instructions below for details on how to do this.

Disable the security feature that is raising this issue by appending the allowPublicKeyRetrieval=true parameter to the database connection URL. You should not do this unless you fully understand the security implications as this could potentially enable man-in-the-middle attacks on the connection.

Distributing the public key manually

Obtain an RSA key pair on your database server by following the steps detailed in the MySQL documentation.

Copy the .pem file containing the public key to the machine on which the Burp Suite DAST server is hosted, as well as any external scanning machines that you've deployed. The path to this file must be identical across all of your machines.

Append the serverRsaPublicKeyFile parameter to your database connection URL, pointing it to the location of the key on your machines. For example:

jdbc:mysql://mysql.dev.example.com:3306/burpenterprise?serverRsaPublicKeyFile=/home/user/public_key.pem

Next step - Prerequisites for standard installations

CONTINUE
