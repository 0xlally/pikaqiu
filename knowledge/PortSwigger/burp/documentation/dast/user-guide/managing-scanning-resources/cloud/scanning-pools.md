# Scanning pools for Cloud instances of Burp Suite DAST

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-scanning-resources/cloud/scanning-pools
Fetched: 2026-06-28T09:15:37.162718+00:00

DAST

Scanning pools for Cloud instances of Burp Suite DAST

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

You can use scanning pools to manage your self-hosted scanning machines. Scanning pools become available automatically when you install your first self-hosted scanning machine.

To learn more about self-hosted scanning machines, see Using self-hosted scanning machines with a Cloud instance.

You can use scanning pools to:

Keep the scanning machines and sites for one geographic area together.

Cordon off the resources of one team.

Scan sites with restricted access.

Reserve scanning machines for specific purposes, such as a CI/CD pipeline or ad-hoc scanning.

Features of scanning pools

Each self-hosted scanning machine is assigned to a pool. The important features of scanning pools are:

Each self-hosted scanning machine must belong to a scanning pool.

Only self-hosted scanning machines in the same pool as a site can scan that site.

Creating a new scanning pool

To create a new scanning pool:

From the settings menu , select Scanning resources.

Click Manage scanning machines.

Click on the Scanning pools tab.

Click Create pool.

Enter a name and description for the new scanning pool.

Assign the relevant scanning machines and sites to the new pool.

Click Save.

Reassigning a scanning machine to a different pool

To reassign an existing scanning machine to a different pool, do the following:

From the settings menu , select Scanning resources.

Click Manage scanning machines.

Make sure you are on the Scanning machines tab.

In the list of scanning machines, select the Scanning pool drop-down menu for the scanning machine you want to reassign, and click on the name of the scanning pool to place it in that pool.

Reassigning a site to a different pool

To reassign an existing site to a different scanning pool, do the following:

From the settings menu , select Scanning resources.

Click Manage scanning machines.

Select the Scanning pools tab.

Find the scanning pool you want to move your sites to, and click Edit.

Select the sites you want to move and click Save.

If you deselect sites from the scanning pool, they are moved to the default scanning pool.

Related pages

Assigning scan limits
