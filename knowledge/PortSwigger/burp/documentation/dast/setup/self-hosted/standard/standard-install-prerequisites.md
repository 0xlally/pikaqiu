# Prerequisites for a standard installation

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/standard/standard-install-prerequisites
Fetched: 2026-06-28T09:15:33.984374+00:00

DAST

Prerequisites for a standard installation

Last updated:

June 18, 2026

Read time:

3 Minutes

You will need to provide some technical details when installing Burp Suite DAST. To make the installation process as smooth as possible, we recommend you have these details to hand before you begin installing.

Note

Burp Suite DAST offers multiple subscription and deployment options. We strongly recommend that your organization takes some time to decide on the best deployment method and system architecture to use,

and that you review the system requirements for standard instances, before attempting to install.

If you have not yet done so, see Preparing to deploy Burp Suite DAST.

Port

For standard instances, you need to specify a port that users and API clients can use to access the application.

By default, Burp Suite DAST uses port 8080 (HTTP) or 8443 (HTTPS). During the installation process, you can change this to any port that meets the following requirements:

The port must be available for use on the machine that you want to install the DAST server on.

The operating system user must be allowed to bind to the port. On Linux, low-privileged users are unable to bind to some well-known port numbers (such as 80 or 433).

If you want to use a low port number, you should configure port redirection at the OS level.

TLS certificate

Burp Suite DAST supports Transport Layer Security (TLS) communication with the web server front end. Configuring TLS is optional, but recommended for production use.

You can choose whether to enable TLS as part of the initial configuration once you have installed the application. You will need to provide a TLS certificate that meets the following requirements:

The certificate must be in PKCS#12 format with a .p12 file extension. The .pfx format is not supported.

The certificate must have a password.

The certificate must include a Subject Alternative Name (SAN).

Related pages

Configuring your web server

Installation location

You will need to specify separate directories for the Burp Suite DAST application itself, its logs, and its data during installation.

System user

For Linux installations, you will need to decide whether you want to use an existing operating system user to run the Burp Suite DAST services, or create a new user during installation.

By default Burp Suite DAST creates a new user called burpsuite to run processes under.

Scanning machine requirements

In order to run more than five concurrent scans, you will need to deploy separate dedicated scanning machines in addition to the Burp Suite DAST server machine.

The number of scanning machines you need to deploy is determined by the number of concurrent scans your organization intends to run.

For more information, see the system requirements.

Related pages

Single vs. multi-machine architecture

Deploying additional scanning machines

System requirements

Database setup script

Burp Suite DAST includes an embedded H2 database, making it easy for you to evaluate the product or run trials. However, for production use, we recommend that you connect to an external database.

You must use the database script provided to set up any external database you want to use up before installing Burp Suite DAST.

Next step - Installing Burp Suite DAST

CONTINUE
