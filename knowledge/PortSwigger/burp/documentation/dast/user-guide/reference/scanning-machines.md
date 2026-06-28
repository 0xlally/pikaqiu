# Scanning machines

Source: https://portswigger.net/burp/documentation/dast/user-guide/reference/scanning-machines
Fetched: 2026-06-28T09:15:39.925931+00:00

DAST

Scanning machines

Last updated:

June 18, 2026

Read time:

1 Minute

A scanning machine is a virtual or physical machine that runs scans. You can run scans on the same machine as the web server and DAST server to begin with. When you follow the installation wizard, this is the default option that is selected.

Alternatively, you can set up as many external machines as you want and use them as dedicated scanning machines. In this way, you can spread your scans across multiple scanning machines to avoid overloading a single machine. You can assign a maximum number of concurrent scans that can be run on each machine. Please refer to the system requirements section for more information about how many machines you might need to deploy.

Note that if you decide to use external scanning machines, you need to authorize them in Burp Suite DAST before you can use them to run scans.

Scanning pools

For standard instances (as opposed to Kubernetes instances), scanning machines exist in one of several scanning pools. These pools are used to manage resources for different kinds of scans, or for scanning different sorts of sites. To assign the machine to a different pool, see Managing scanning pools.

CI-driven scans

You can run CI-driven scans in your CI/CD pipeline. These run in temporary scanning containers that are created in a container platform.

For more information, see Integrating CI-driven scans.

Related pages

Adding additional scanning machines.

Assigning scan limits.

Managing scanning pools.
