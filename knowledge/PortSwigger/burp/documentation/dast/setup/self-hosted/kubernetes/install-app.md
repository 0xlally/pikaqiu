# Installing the application (Kubernetes)

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/kubernetes/install-app
Fetched: 2026-06-28T09:15:32.990672+00:00

DAST

Installing the application (Kubernetes)

Last updated:

June 18, 2026

Read time:

5 Minutes

Burp Suite DAST uses Helm to manage installation and configuration. In order to install the application you first need to download its Helm chart.

Downloading the Helm chart

The Burp Suite DAST Helm chart is a deployment descriptor for Kubernetes that, when run, configures Burp Suite DAST in a "ready-to-run" state. It is designed to work with any Kubernetes cluster that meets the prerequisites for Burp Suite DAST.

You can get the Helm chart from two places:

From the PortSwigger Releases page. Click here to display details of the most recent Kubernetes release of Burp Suite DAST, and then click Download.

Once the chart is downloaded, unpack it into a directory of your choice. Note that you will need the name of this directory when running commands against the chart.

From the Burp Suite DAST Helm chart GitHub repository.

Note

While it is technically possible to customize the Helm chart, please note that we are unable to offer support on this process. For more information on Kubernetes support, see Support scope for Kubernetes instances.

Providing custom values for the Helm chart

The provided values.yaml file contains the default values that will be passed to the Helm chart when you run it. You can modify this file to customize these values. Please contact our support team if you need any additional guidance.

Note for Oracle users

If you want to use an Oracle database, you need to manually enable Oracle support by modifying the provided values.yaml file as follows:

support

oracle: true

Adding a TLS certificate

A TLS certificate makes sure your connection to Burp Suite DAST is secure. You can use the values.yaml file to add a TLS certificate.

The TLS certificate must have the following properties:

Use a PKCS#12 certificate with a .p12 file extension. The .pfx format is not supported.

The certificate must have a passphrase.

The certificate must include a Subject Alternative Name (SAN).

To add a TLS certificate:

Use the following command to create a Kubernetes secret that contains your TLS certificate. The secret needs to contain the certificate, and the passphrase:

kubectl -n <namespace> create secret generic bsee-web-server-https --from-file=certificate=<your certificate name>.p12 --from-literal=passphrase=<your passphrase>

In the values.yaml file, set the values for services.webServer as follows:

Set useDeprecatedHttpConfigFromDatabase to false.

Set useHttps to true.

Set a value for the httpsPort (the default is 8443).

Enter the name and key for the secrets for the certificate and the passphrase.

Note

If you later decide to switch between an HTTPS and an HTTP connection, you need to set useHttps to false, and perform a Helm upgrade.

Configuring TLS cipher suites

You can configure the enabled TLS cipher suites to meet your own security requirements, or to comply with specific standards.

Note

This configuration controls cipher suites for external communication with Burp Suite DAST only. You cannot configure the cipher suites used internally between Burp Suite DAST components.

To configure the enabled TLS cipher suites, set the environment variable BSEE_TLS_CIPHER_SUITES as follows:

DEFAULT: Use secure TLS 1.2 and TLS 1.3 cipher suites only.

TLS1.3: Use secure TLS 1.3 cipher suites only.

FIPS-140-2: Use the cipher suites that are compatible with TLS 1.2 and TLS 1.3, and are considered secure by FIPS-140-2.

If you want to create a custom configuration, you can list more than one cipher suite in the environment variable. For example, you can combine a preset with some additional cipher suites:

BSEE_TLS_CIPHER_SUITES=FIPS-140-2,TLS_DHE_DSS_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_AES_256_CBC_SHA

You can see the full list of the ciphers we currently support in the enterpriseServer log. For more information, see Support pack.

Configuring the database details

Before you attempt to connect to your database, please make sure that you have configured it to work with Burp Suite DAST. For details of how to do this, see Setting up the external database.

In the values.yaml file, set the values for database within the quote marks, as follows:

Set url to the JDBC URL of your database. The format for the URL changes depending on the type of database you want to use. For more information on JDBC URLs in Burp Suite DAST, see Database connection URL format.

Set enterpriseServerUsername for the user that you want DAST server to use to connect to the database.

Additionally, if your database requires a different format for the username when connecting externally (for example, user-name@server-name), set enterpriseServerConnectionUsername to the connection username.

Set enterpriseServerPassword to the password for the DAST server database connection.

Set scanningResourceUsername to the username of the scanning machine database user.

Additionally, if your database requires a different format for the username when connecting externally (for example, user-name@server-name), set scanningResourceConnectionUsername for the scanning machine database user.

Set scanningResourcePassword to the password of the scanning machine database user.

Using the Helm chart

After downloading the Helm chart, to deploy Burp Suite DAST, first make sure that you have created the namespace that you want to use. This is the same namespace that you used for your PersistentVolumeClaim.

Next, run the following command:

helm install -n <namespace> <deployment name> <name of directory containing the chart>

For example, to use a chart located in enterprise-helm-folder to deploy Burp Suite DAST to a deployment called bsee-deployment with a namespace of bsee-namespace, you would run:

helm install -n bsee-namespace bsee-deployment enterprise-helm-folder

Extracting the web server IP address

Once the installation process is complete, you need to extract your Burp Suite DAST external IP address to access the application. If you've used our template, the address of the webserver console is displayed after successful deployment. Otherwise run the following command to find the address:

kubectl get services -n <namespace>

This command displays details of all services in the namespace, including their external IP address. The external IP of the web server service is the IP you need to access Burp Suite DAST.

Note

If you've used your own Ingress controller, you need to use your own configured address.

Installing using a pre-existing values file

You may have previously had a Kubernetes instance of Burp Suite DAST with a customized values file. If so, you need to use the same values file for your new instance. You can specify the values file to use when you run the install command.

To specify a values file, add the -f <values file name> argument to the install command. For example:

helm install -n bsee-namespace bsee-deployment enterprise-helm-folder -f my-values-file

Warning

There are potential security implications to leaving Burp Suite DAST in an unconfigured state. We recommend completing the rest of the configuration as soon as possible.

Next step - Create the admin user

CONTINUE
