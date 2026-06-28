# Burp Intruder resource pools

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/configure-attack/resource-pool
Fetched: 2026-06-28T09:16:04.586391+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Configure attack

Resource pools

ProfessionalCommunity Edition

Burp Intruder resource pools

Last updated:

June 18, 2026

Read time:

2 Minutes

A resource pool is a group of tasks that share a quota of resources. Resource pools make it easier for you to:

Manage and prioritize the usage of system resources, particularly across multiple attacks.

Test applications that tolerate automated requests at different rates.

Creating resource pools

New tasks are assigned to a default resource pool. You can create a custom pool at any point before you start the attack. To create a resource pool:

Go to Intruder and click Resource pool. The Resource pool side panel opens.

Select Create new resource pool.

Enter a name for the pool and configure the pool settings.

The pool is created when you start the attack.

If you want to create a new pool after the attack has started, you need to do so in a different task or in Burp's Settings dialog under Project > Tasks. To open the dialog, click

Settings in the top toolbar.

Resource pool settings

Each resource pool can be configured with its own throttling settings:

Maximum concurrent requests - Limit the number of requests that the attack sends simultaneously. This is useful so you don't overload the target server or exceed the configured rate limit.

Delay between requests - This is in milliseconds. You can choose from three delay types:

Fixed.

With random variations.

Increase delay in increments - This enables you to determine the time taken for a session to expire if no requests are sent.

Automatic throttling - Automatically add a short delay between requests when the server responds with one of the specified codes. You can enable and configure this setting in the default resource pool.

Moving tasks between resource pools

To move a task before you start an attack, click Resource pool to open the

Resource pool side panel, then select the pool.

To move a task during an attack, click Resource pool in the results window, then select the pool. This enables you to manage the use of system resources in real time.
