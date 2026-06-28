# System requirements for your external database (Standard)

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/standard/external-database-requirements
Fetched: 2026-06-28T09:15:33.401366+00:00

DAST

System requirements for your external database (Standard)

Last updated:

June 18, 2026

Read time:

1 Minute

Burp Suite DAST requires a database to store the application data. For production use, we recommend that you connect to an external database.

The size of the database you need depends on the total number of scans your organization runs, and the volume of issues found by the Scanner.

Note

If you need help with the system requirements, please email our support team.

The following table indicates the quantity of data that you are likely to accumulate, based on the number of scans your organization has run:

Number of scans

Data storage

1,000

500 MB

10,000

5 GB

100,000

50 GB

Database size requirements

The size of your database instance depends on the number of concurrent scans that you want to run, and the type of database.

For a database instance such as AWS RDS, we recommend a minimum of 2 vCPUs and 8GB RAM, for example a db.t3.large instance.

Supported database versions

We support the following external databases. We expect newer versions from these vendors to be supported, but these are the latest that we have actively tested.

We try to support older versions as long as they are supported by the vendor.

Type

Latest version tested

MariaDB

11.2.3

Microsoft SQL server

2022 (16.0.1000.6)

MySQL

8.3.0

Oracle

23c (23.0.0.0.0)

PostgreSQL

17.4

Note

AWS Aurora databases are not supported.
