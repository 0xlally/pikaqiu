# Planning to deploy Burp Suite DAST

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/planning
Fetched: 2026-06-28T09:15:33.130060+00:00

DAST

Planning to deploy Burp Suite DAST

Last updated:

June 18, 2026

Read time:

4 Minutes

To ensure that your deployment of Burp Suite DAST runs smoothly, you should take some time to prepare before beginning the process. This gives you an overview of the process to help you understand what decisions you need to make, identify any additional stakeholders that you may need to involve, and estimate the timeframe before you get started. We recommend that you account for approximately one month of planning time before attempting to deploy Burp Suite DAST.

On this page

Decide on your subscription.

Choose a deployment method.

Choose your preferred architecture.

Plan your database setup.

Review the system requirements.

Plan your network and firewall setup.

Prepare your organization.

Decide on your subscription

We provide flexible licensing models for Burp Suite DAST to meet various requirements.

For more information, get in touch through our enquiry form so our team can help you find the right subscription.

Choose a deployment method

You have several methods of deploying a self-hosted instance. We've provided a dedicated guide for each of them.

Standard - use a standard installer to deploy Burp Suite DAST, either to your own on-premise infrastructure or cloud-based services in AWS, Azure, Google Cloud Platform, and so on. Depending on the scale and scanning requirements of your organization, you can deploy a standard instance to a single machine or use a multi-machine architecture. For more information, see the Standard setup guide.

Kubernetes - use a Helm chart to deploy Burp Suite DAST to your Kubernetes cluster. When running on Kubernetes, Burp Suite DAST scales the amount of compute resources dedicated to scanning automatically. We recommend this option only if your organization has previous experience with Kubernetes. While we offer full support for your Burp Suite DAST instance, we are unable to offer support on your underlying Kubernetes infrastructure. For more information, see the Kubernetes setup guide.

CI-driven scans with no dashboard - run scans from a container in your CI/CD environment and consume the results directly in your CI/CD platform. There's no need to host or manage a Burp Suite DAST server and dashboard. For more information, see CI-driven scans with no dashboard setup guide.

Choose your preferred architecture

When using the standard, installer-based method, you can either deploy all of Burp Suite DAST's components to a single machine, or use a multi-machine architecture with dedicated scanning machines and an external database.

The number of machines you need depends on how many concurrent scans you intend to run:

For up to five concurrent scans, we recommend a single-machine setup. In this case, scans run on the same machine as the DAST server.

For more than five concurrent scans, we recommend a multi-machine setup. In this case, scans run on dedicated scanning machines to spread the load.

Note

You can deploy as many scanning machines as you need. The number of concurrent scans you can run on each scanning machine depends on your system specification. For more information, see System requirements.

Plan your database setup

Burp Suite DAST includes an optional H2 database, making it easy for you to evaluate the product or run trials without having to set up a database connection. However, for production use, we recommend that you connect to an external database.

You must use the database script provided to set up any external database you want to use before installing Burp Suite DAST.

Related pages

External database system requirements (standard).

Setting up an external database (standard).

External database system requirements (Kubernetes).

Setting up an external database (Kubernetes).

Review the system requirements

Whichever architecture you choose, you should ensure that the machines you intend to use meet the system requirements.

Related pages

Burp Suite DAST system requirements.

Plan your network and firewall setup

To ensure that Burp Suite DAST can work correctly, you need to configure your network to allow the various components to communicate with each other and your target applications. The network requirements vary depending on whether you intend to use a single or multi-machine architecture.

Note that the DAST server must be able to connect to portswigger.net on port 443 in order to activate your license and complete the installation process. If you are not able to connect to the public internet, you may need to configure an HTTP proxy server.

Related pages

Configuring your environment network and firewall settings (standard).

Configuring your environment network and firewall settings (Kubernetes).

Configuring an HTTP proxy server.

Prepare your organization

As well as making technical decisions, we recommend that you consider any factors within your organization that may cause delays when attempting to install Burp Suite DAST.

For example, you should ensure that:

You have accounted for any internal compliance and security procedures.

You have appropriate IT resource available.

You have accounted for the time needed to authorize and provision any required infrastructure.
