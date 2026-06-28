# Setting up a suitable Kubernetes cluster

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/kubernetes/set-up-k8s
Fetched: 2026-06-28T09:15:33.042220+00:00

DAST

Setting up a suitable Kubernetes cluster

Last updated:

June 18, 2026

Read time:

1 Minute

Before you deploy Burp Suite DAST to Kubernetes, make sure your cluster meets the system requirements. For more information, see System requirements for Kubernetes instances

Warning

For security reasons, make sure you set your cluster up in a way that prevents your scanning resources from accessing any network systems or functionality that you don't intend to scan.

Using the reference template

We have made an Amazon Web Services reference template available on our public GitHub repo for customers who do not yet have a Kubernetes cluster that meets the Burp Suite DAST prerequisites. You can use this template to build out a suitable Kubernetes cluster and Postgres database.

While the provided reference template uses Amazon Web Services (AWS), Kubernetes instances of Burp Suite DAST can run on any suitable compute platform.

The reference template is intended as an example way of working rather than a strict configuration process. As such, you may want to fork it to your own repository and customize it to best meet your needs.

Note

While we offer full support for Kubernetes instances of Burp Suite DAST, we are unable to offer support on your underlying Kubernetes infrastructure. This includes using and customizing any reference templates. For more information, see Support scope for Kubernetes instances.

Next step - Install the application

CONTINUE
