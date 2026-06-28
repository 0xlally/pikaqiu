# Managing services

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-services
Fetched: 2026-06-28T09:15:37.670748+00:00

DAST

Managing services

Last updated:

June 18, 2026

Read time:

2 Minutes

You may occasionally want to check if your services are running or manually stop and restart them. The process for this differs depending on whether you're using a standard or Kubernetes Burp Suite DAST instance:

For standard instances, you can list running services and choose to stop or start them. For instructions on how to do this, see Managing Burp Suite DAST services for standard instances.

For Kubernetes instances, you can restart services. For instructions on how to do this, see Restarting services for Kubernetes instances.

Managing Burp Suite DAST services for standard instances

When deploying a standard instance of Burp Suite DAST, the following services will be installed on your machine:

burpsuiteenterpriseedition_agent.service

burpsuiteenterpriseedition_enterpriseserver.service

burpsuiteenterpriseedition_webserver.service

burpsuiteenterpriseedition_db.service

Note that this final service is only installed if you're using the bundled database rather than your own external one.

You may sometimes want to manage these services. For example, if you decide to migrate from the bundled database to an external one, you will need to stop some of the services before migrating your data. This process differs slightly depending on your operating system.

List running services

To list all the Burp Suite DAST services that are currently running:

Linux: From a command prompt, enter:

sudo systemctl | grep burp

Windows: Open the built-in Services tool (Control Panel > System and Security > Services) and use the GUI to look for the relevant services in the list. Check the Status column to see if the service is currently running.

Stop running services

To stop a Burp Suite DAST service that is currently running:

Linux: From a command prompt, enter:

sudo systemctl stop <servicename>

Windows: Open the built-in Services tool (Control Panel > System and Security > Services) and use the GUI to look for the relevant services in the list. Right-click on the service and select Stop.

Start services

To start a Burp Suite DAST service that is not currently running:

Linux: From a command prompt, enter:

sudo systemctl start <servicename>

Windows: Open the built-in Services tool (Control Panel > System and Security > Services) and use the GUI to look for the relevant services in the list. Right-click on the service and select Start.

Restarting services for Kubernetes instances

The easiest way to restart services for a Kubernetes instance is to restart your deployments using the following commands:

kubectl -n <namespace> rollout restart deployment <deployment-name>-web-server

kubectl -n <namespace> rollout restart deployment <deployment-name>-enterprise-server
