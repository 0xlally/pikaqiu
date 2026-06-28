# Managing resource pools for scans

Source: https://portswigger.net/burp/documentation/desktop/running-scans/managing-resource-pools
Fetched: 2026-06-28T09:15:53.244402+00:00

Support Center

Documentation

Desktop editions

Running scans

Managing resource pools for scans

Professional

Managing resource pools for scans

Last updated:

June 18, 2026

Read time:

2 Minutes

A resource pool is a quota of resources that can be shared by multiple tasks. Resources pools make it easier for you to:

Manage and prioritize the use of system resources, particularly across different scans.

Test applications that tolerate automated requests at different rates.

Resource pools are used by scans and live audit tasks. They are not available for passive crawl tasks.

Each scan or live audit task is assigned to a resource pool when it is created. You can define the pool in the Resource pool tab in the scan launcher. Select an existing pool from the list, or create a new pool.

Note

If you do not select a resource pool, the scan uses the default resource pool.

Creating new resource pools

To create a new resource pool from the Resource pool tab in the scan launcher:

Select Create new resource pool.

Enter a name for the pool.

Configure the pool throttling settings.

Burp Suite creates the pool when you start the scan or live audit task. The pool is also added to the list of existing pools, for future use.

More information

For more information on the pool throttling settings available, see Task settings - Resource pools.

Reassigning resource pools

You can move a scan or live audit task to another resource pool during an attack. This enables you to manage the use of system resources in real time.

To reassign a task, click the icon to edit the task. You can select a new resource pool from the list of existing pools, or create a new resource pool.

Related pages

You can also create and manage your resource pools in the Settings dialog, under Tasks > Resource pools. For more information, see Task settings - Resource pools.

Burp Intruder also uses resource pools. For more information, see Managing Intruder resource pools.
