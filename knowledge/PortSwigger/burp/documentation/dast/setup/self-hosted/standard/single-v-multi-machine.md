# Single vs. multi-machine architecture

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/standard/single-v-multi-machine
Fetched: 2026-06-28T09:15:33.695591+00:00

DAST

Single vs. multi-machine architecture

Last updated:

June 18, 2026

Read time:

1 Minute

The number of machines needed to run Burp Suite DAST very much depends on the scale of your intended usage.

Single machine architecture

You can run all of the components on a single machine, including the embedded database. The embedded database is designed for trials and evaluations of Burp Suite DAST. It is not intended for production use.

For production use, we recommend that you connect to an external database and use a multi-machine architecture. The diagram below shows a single-machine architecture:

Multi-machine architecture

Alternatively, you can run scans on several different machines and you can use your own external database for storage. This lets you scale the number of concurrent scans that you could potentially run

to be indefinitely large and utilize any existing database infrastructure that you have. The diagram below shows a multiple-machine architecture, with an external database and separate scanning machines:

Note that the DAST server and the web server are always deployed on a single machine.

Requirements

For specific details about the system requirements for both of these options, see System requirements for standard

instances.

Network and firewall settings

To ensure that Burp Suite DAST can work correctly, you need to configure your network to allow the various components to communicate with each other and your target applications.

The network requirements vary depending on whether you intend to use a single-machine or multi-machine architecture.

To learn more, see Configuring your network and firewall settings.

Next step - Configuring your network and firewall

CONTINUE
