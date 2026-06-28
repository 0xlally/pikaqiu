# Architecture overview (Standard)

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/standard/architecture-overview
Fetched: 2026-06-28T09:15:33.213091+00:00

DAST

Architecture overview (Standard)

Last updated:

June 18, 2026

Read time:

2 Minutes

The following diagram shows the core components of Burp Suite DAST and the connections between them.

DAST server

The DAST server is the main application server. It coordinates between the other components. The DAST server is always installed on the same machine as the web server.

Web server

The web server provides the interface to users either via the web UI or one of the APIs. The web server is always installed on the same machine as the DAST server.

Database

Burp Suite DAST uses a SQL database to store all the application data, including scan data. You can use one of the following options:

An embedded database that can be installed on the same machine as the DAST server and web server.

The embedded database is designed for trials and evaluations of Burp Suite DAST. It is not intended for production use.

For production use, we recommend that you use your own external database.

Your own external database. We recommend using an external database for production use.

This option enables you utilize any existing database infrastructure that you have, including database backups.

Read more

External database requirements

Setting up an external database

Services

Burp Suite DAST installs the following services on your machine:

burpsuiteenterpriseedition_agent.service

burpsuiteenterpriseedition_enterpriseserver.service

burpsuiteenterpriseedition_webserver.service

burpsuiteenterpriseedition_db.service

*

* burpsuiteenterpriseedition_db.service is only installed if you're using an embedded database rather than your own external one.

Read more

Managing services

Scans and scanning machines

For standard instances, scans run on a scanning machine. You can install the scanning component on the same machine as the server, or you can deploy external scanning machines on which your scans can run.

The number of scanning machines you need depends on how many concurrent scans your organization wants to run:

For up to five concurrent scans, we recommend a single-machine architecture. In this setup, scans run on the machine that the DAST server is installed on. This is the simplest deployment method.

For more than five concurrent scans, we recommend a multi-machine architecture.

In this setup, scans run on dedicated scanning machines, offering a more scalable solution in which you could potentially run any number of concurrent scans.

After deployment, you can group scanning machines into scanning pools, which gives you greater control over scanning resources.

Read more

Single vs. multi-machine architecture

Deploying additional scanning machines

Next step - Single vs. multi-machine architecture

CONTINUE
