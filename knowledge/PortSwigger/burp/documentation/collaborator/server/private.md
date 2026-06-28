# Deploying a private Burp Collaborator server

Source: https://portswigger.net/burp/documentation/collaborator/server/private
Fetched: 2026-06-28T09:15:31.648089+00:00

Support Center

Documentation

Burp Collaborator

Server

Deploying a private server

DASTProfessional

Deploying a private Burp Collaborator server

Last updated:

June 18, 2026

Read time:

7 Minutes

Follow the steps on this page to set up your own private instance of the Collaborator server. This may be useful in the following situations:

For large penetration testing firms and in-house security teams.

When working on a closed network with no internet access. This means the public Collaborator server can't be used. The basic setup is often sufficient to support a single tester or small team in this situation.

General setup

To launch a Collaborator server instance that supports all Collaborator functionality, you need to:

Set up a Collaborator domain and DNS records.

Set up the ports and firewall for your Collaborator server.

Set up your host server resources.

Write the configuration file.

Launch the Collaborator server and tell Burp where to find the server.

Professional Once you have completed these steps, we recommend that you run the Collaborator health check.

Setting up the domain and DNS records

To access full Collaborator-related functionality, you need to obtain a domain and configure Collaborator to use the domain. The Collaborator server then runs a DNS service for your domain.

Note

Alternatively, you can configure the Collaborator server to use an IP address instead of a domain. However, this is less effective at detecting vulnerabilities, as any Collaborator-related functionality that relies on DNS resolution is not available.

To obtain the domain or subdomain for the Collaborator server to use, you could:

Purchase a dedicated domain, such as example.com.

Use a subdomain of a domain you already own, such as burpcollaborator.example.com.

If your installation is restricted to an internal network, use a dedicated internal domain.

To configure the Collaborator server to use the domain, you need to:

Specify the domain in the serverDomain field of your configuration file.

Set the Collaborator server as authoritative for the specified domain. This makes sure that queries for the domain are resolved by the server.

You can generally set the Collaborator server as authoritative on your domain registrar's web interface. Speak to your domain provider for assistance. You also need to:

Set up the DNS configuration. This is based on your domain registrar, but you must always have the following entries:

An A or AAAA record for the Collaborator subdomain that points to the external IP of the interactions interface.

An NS record for the Collaborator subdomain that points to the Collaborator name server. For example, ns1.burpcollaborator.example.com.

An A or AAAA record for the Collaborator name server.

If your domain registrar requires each configured DNS server to reside on its own IP address, then you might need to configure two public IP addresses. Make sure you specify both of these in your configuration file.

Note

You can't edit the host file of the target server to avoid the use of the Collaborator DNS service. Host files do not support wildcards and so can't be used to route queries with randomly generated subdomains.

Setting up the ports and firewall

By default, Burp Collaborator server listens on the following ports:

DNS: UDP port 53.

HTTP: TCP port 80.

HTTPS: TCP port 443.

SMTP: TCP ports 25 and 587.

SMTPS: TCP port 465.

To make sure the server operates correctly, you need to:

Stop any other processes that are using these ports. The server fails to start if it can't bind to the ports it needs to run its services.

Configure your firewall to:

Allow inbound communication from any network on these ports.

Allow the applications that you are testing, and their DNS servers, to access the Collaborator server.

On Unix-based systems, you may need to run the server with root privileges.

Changing the ports

You may wish to change the ports from their defaults if you're using a different server, or if you are on a Unix-based system and want to run the Collaborator server as a non-root user.

To change the ports, edit the ports value in the eventCapture and dns fields of your configuration file. You can enter a single port value or multiple values. You can also do this in the polling field if you've

configured a separate polling interface.

You also need to:

Specify the chosen ports. Use the format burpcollaborator.example.com:9443 to add a location for the HTTP or HTTPS port, depending on your polling connection:

Professional In Burp Suite Professional, do this under Project > Collaborator in the Settings dialog. Select Use a private Collaborator server, then add the polling location.

DAST In Burp Suite DAST, do this under the Burp Collaborator server settings when you create a custom scan configuration. Set the Collaborator type to private, then add the polling location.

Configure your operating system to map the original ports to the custom ports.

You may also need to configure mappings for TCP and UDP connections.

Setting up your server resources

You need to make two key decisions when you set up the Collaborator server:

Whether to run the server on a physical or cloud-based machine.

The memory size of your server - you need enough memory to store interaction data. For more information on Collaborator data storage, see Burp Collaborator server.

Controlling memory usage

To control how much memory your computer assigns to the Collaborator server, you can configure the JVM's memory handling and garbage collection. To do this, add the

--collaborator-server argument to the command line when you launch the Burp Suite JAR. For example:

On a desktop machine, with a small number of expected users:

sudo java -Xms10m -Xmx200m -XX:GCTimeRatio=19 -jar /path/to/file.jar --collaborator-server

This command allows the heap to fluctuate between 10 and 200MB. The JVM spends 5% of its time in garbage collection, which uses less memory.

On a dedicated machine, with a larger number of users:

sudo java -Xmx3g -Xms3g -jar /path/to/file.jar --collaborator-server

This command fixes the size of the heap to the amount of physical memory available. It leaves 1GB for the operating system, JVM, and other running processes.

On a dedicated machine with more that 4GB of physical memory, and a large number of users:

sudo java -Xmx12g -Xms12g -XX:+UseG1GC -jar /path/to/file.jar --collaborator-server

This command uses the G1 garbage collector, which significantly reduces the JVM pauses that occur during garbage collection.

Related pages

Launching Burp Suite from the command line.

You can also truncate interaction messages to reduce the load on the server. See Truncate interaction messages.

Setting up the configuration file

You need to write a configuration file to set up the Collaborator server. This file enables you to configure all options for the server.

Generally, you need to save the file under the name collaborator.config in the current working directory. By default, the Collaborator server looks for this file. To override this, amend the --collaborator-config argument in the command line. For example:

sudo java -jar /path/to/file.jar --collaborator-server --collaborator-config=myconfig.config

Related pages

For an example configuration file and details of the fields that you can include in your configuration file, see Example configuration file.

For information on key options you can configure for your private Collaborator server, see Configuring your private Collaborator server.

Launching the Collaborator server

To launch a Collaborator server with a custom configuration file, add the following argument to the command line:

--collaborator-config=myconfig.config

You don't need a license key to run your own instance of the server. The Collaborator server is included in the same executable file as Burp Suite Professional itself.

Once you've launched your server, you need to tell Burp where to find it:

Professional In Burp Suite Professional, do this under Project > Collaborator in the Settings dialog. Select Use a private Collaborator server, then add the server location.

DAST In Burp Suite DAST, do this under the Burp Collaborator server settings when you

create a custom scan configuration. Set the Collaborator type to private, then add the server location.

Related pages

Launching Burp Suite from

the command line.

Collaborator settings.

Health check and troubleshooting

Professional Before you start using your server, run the Collaborator health check to determine whether Burp is likely to be able to make use of Collaborator's features. You can find this under Project > Collaborator in the

Settings dialog.

Our troubleshooting guide may help you address any issues raised in the health check.

Related pages

Collaborator settings.

Basic setup

You can launch a basic Collaborator server instance without a configuration file and dedicated domain. This enables you to use basic Collaborator features to detect issues like external HTTP interactions. This setup may be useful for an individual or small team working on a closed network with no internet access.

Note

This setup doesn't support custom DNS resolution or valid trusted HTTPS connections.

To launch a basic Collaborator setup:

Add the --collaborator-server argument to the command line. For example:

sudo java -jar /path/to/file.jar --collaborator-server

Configure Burp to use your machine's IP address as its Collaborator server:

Professional In Burp Suite Professional, do this under Project > Collaborator in the Settings dialog. Select Use a private Collaborator server, then add the server location.

DAST In Burp Suite DAST, do this under the Burp Collaborator server settings when you create a custom scan configuration. Set the Collaborator type to private, then add the server location.

Related pages

Collaborator settings.

Launching Burp Suite from

the command line.
