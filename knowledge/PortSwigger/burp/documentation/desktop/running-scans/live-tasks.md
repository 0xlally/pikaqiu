# Live tasks

Source: https://portswigger.net/burp/documentation/desktop/running-scans/live-tasks
Fetched: 2026-06-28T09:15:54.160631+00:00

Support Center

Documentation

Desktop editions

Running scans

Live tasks

Professional

Live tasks

Last updated:

June 18, 2026

Read time:

2 Minutes

Live tasks are scans that run in the background while you manually explore the target website using Burp's browser or when you send requests from Burp Repeater and Intruder. They enable you to perform some scanning operations, such as auditing for vulnerabilities or adding resources to Burp's Target site map, automatically.

Types of live task

When you set up a live task, you specify a scanning operation and a scope for items to be scanned. When the task encounters an item that meets the scope criteria, it performs the selected scanning operation on that item automatically.

There are two types of live task available in Burp Suite:

Live audit - Scans each identified request for vulnerabilities.

Live passive crawl - Populates the Target site map with items derived from the identified request.

Live task scope

You can specify items to be scanned by the live task based on the following criteria:

Tools scope - Specify the tools whose traffic is inspected. Live tasks can include traffic from Burp Proxy, Repeater, and Intruder.

URL scope - Specify which items from the selected tools are processed by the task, based on their URL.

You can also specify whether any duplicate items should be removed. If you enable deduplication, any items that share URL and parameter names are consolidated to reduce the amount of items scanned.

Scan configuration and resource pools

You can set scan configurations for all live tasks. The selected configurations apply when scanning any in-scope items.

For live audit tasks, you can also specify a resource pool. This option is not available for passive crawl tasks.

Related pages

Creating a live task - Explains how to create a new live task in Burp Suite.

Task execution settings - Explains how to manage the execution of tasks and the assignment of resources.

Configuring scans - Gives further information on creating scan configurations in Burp Suite Professional.

Managing resource pools - Gives information on the use cases for resource pools and how to configure them.
