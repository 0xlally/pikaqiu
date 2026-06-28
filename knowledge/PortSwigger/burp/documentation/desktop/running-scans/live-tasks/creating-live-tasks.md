# Creating live tasks

Source: https://portswigger.net/burp/documentation/desktop/running-scans/live-tasks/creating-live-tasks
Fetched: 2026-06-28T09:15:53.867071+00:00

Support Center

Documentation

Desktop editions

Running scans

Live tasks

Creating live tasks

Professional

Creating live tasks

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Suite's Live tasks feature enables you to perform some scanning operations automatically. You can use live tasks to audit for vulnerabilities, or add resources to Burp's Target site map.

Related pages

Live tasks - Gives further information around how live tasks work.

To create a new live task:

From the Dashboard, click New live task to display a dialog.

Select a Task type:

Live audit.

Live passive crawl.

Select the Tools scope. You can set the task to inspect the traffic from the following tools:

Proxy.

Repeater.

Intruder.

Select the URL scope. You can set the task to process the following items for the selected tools:

Everything - Includes all URLs.

Suite scope - Includes all URLs covered by the current suite-wide scope.

Custom scope - Enables you to specify your own URLs for the task to match. Live tasks use Burp Suite's standard URL matching and advanced scope control rules. See URL matching for more details.

If required, select Ignore duplicate items based on URL and parameter names to reduce the number of items processed by the task.

If required, click the Scan configuration tab and select a scan configuration for the task. For more information, see

Configuring scans.

If required, and if you are creating an audit task, click the Resource pool tab and configure the resource pool that the task runs in. For more information on configuring resource pools, see Managing resource pools for scans.

Click OK to start the task.

You can also add a pre-configured live task. Choose a task from the Choose predefined task drop-down in the Scan details tab. The available options are:

Passively scan all traffic through Proxy.

Actively scan all in-scope traffic through Proxy.

Add all items requested through Proxy to site map.

Add all links observed in traffic through Proxy to site map.
