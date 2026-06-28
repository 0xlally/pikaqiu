# Task execution settings

Source: https://portswigger.net/burp/documentation/desktop/running-scans/live-tasks/task-execution-settings
Fetched: 2026-06-28T09:15:53.407471+00:00

Support Center

Documentation

Desktop editions

Running scans

Live tasks

Task execution settings

ProfessionalCommunity Edition

Task execution settings

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Suite lets you configure multiple automated tasks simultaneously. Executing a large volume of work in parallel is liable to cause problems, either in your own machine (by exhausting CPU, memory, or your network connection) or in the applications being tested. Burp helps to avoid this happening by managing the execution of tasks and the way in which resources are assigned to them.

The task execution settings can be accessed by clicking the gear icon at the top of the Tasks panel on the Burp Dashboard.

Task auto-start

You can individually pause and resume tasks in Burp's Dashboard. You can also configure whether to automatically start new tasks as they are created. The following options are available:

Create new tasks paused.

Create new tasks running.

Resource pools

A resource pool is a grouping of tasks that share a quota of network resources. Each resource pool can be configured with its own throttling settings which control the number of requests that can be made concurrently, or the rate at which requests can be made, or both.

Each task is assigned to a resource pool when it is created, and tasks can be moved between resource pools at any time.

Using resource pools is particularly useful if you are testing different applications that tolerate automated requests at different rates. They are also useful to prioritize different areas of your testing. For example, you might create one task performing a full crawl and audit of an application, and let this run in the background with a small number of concurrent requests; you might create another task for auditing specific individual requests that you select, and let this run with a larger number of concurrent requests to give it priority.
