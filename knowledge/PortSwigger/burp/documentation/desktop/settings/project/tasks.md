# Tasks settings

Source: https://portswigger.net/burp/documentation/desktop/settings/project/tasks
Fetched: 2026-06-28T09:15:55.207490+00:00

Support Center

Documentation

Desktop editions

Settings

Project

Tasks

ProfessionalCommunity Edition

Tasks settings

Last updated:

June 18, 2026

Read time:

3 Minutes

The Tasks page contains settings for the following:

Resource pools.

New task auto-start.

Schedule tasks.

Resource pools

This setting enables you to create custom resource pools, to manage system resources across multiple tasks. Resource pools are used by both Burp Intruder and Burp Scanner.

Click New to create a new resource pool, or Edit to modify an existing resource pool. A new dialog opens, in which you name the pool and configure the throttling settings:

Maximum concurrent requests - Specify a limit to the number of requests that are sent simultaneously. This is useful so you don't overload the server or exceed the configured scan limit.

Delay between requests - Set a delay time in milliseconds. You can choose from three delay types:

Fixed.

With random variations.

Increase delay in increments - This enables you to determine the time taken for a session to expire if no

requests are sent.

Automatic throttling - Specify the response codes that you want to trigger automatic throttling. When Burp Scanner receives a response containing one of these codes, it adds a short delay between requests. The available options are:

429 (Too many requests)

503 (Service unavailable)

Other. Enter one or more codes into the text box. Use CSV format (e.g. 504, 505, etc.) to enter multiple codes.

To export your resource pools for use in other Burp installations, click the settings icon and select Save settings. All saved resource pools are exported in a single JSON file.

To import resource pools, click the settings icon and select Load settings. The imported pools replace any in your library, and tasks using overwritten pools update automatically. If a pool is removed, its tasks switch to the default pool.

The Resource pool settings are project settings. They apply to the current project only.

Note

While you can configure Burp Scanner to throttle requests on any code, we recommend that you only throttle error codes. Configuring throttling on standard response codes such as 200 (OK) could result in significantly decreased scan performance.

Related pages

Burp Intruder resource pools.

New task auto-start

This setting controls whether newly-created tasks start immediately. The following options are available:

Start tasks - Enable this setting for tasks to automatically start when they are created.

Pause tasks - Enable this setting for tasks to be paused when they are created. You can manually start paused tasks from the Dashboard.

The New task auto-start settings are project settings. They apply to the current project only.

Schedule tasks

This setting enables you to create rules to pause and resume automated tasks at specified times. You can set these rules to apply once, or repeat at regular intervals.

To add a rule:

Click Add to display the Schedule task dialog.

Select the rule type, from Pause task execution engine or Resume task execution engine.

Click Next to specify the rule details:

Start at - Specify the time that the rule should run from.

On - Specify the date that the rule should run on.

Repeat every - Specify how often the rule will repeat, in minutes, hours, or days. If you don't want the rule to repeat, leave this blank.

Click Finish.

You can Edit and Remove targets from the list.

The Schedule tasks settings are project settings. They apply to the current project only.
