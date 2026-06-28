# Dashboard

Source: https://portswigger.net/burp/documentation/desktop/tools/dashboard
Fetched: 2026-06-28T09:16:02.327142+00:00

Support Center

Documentation

Desktop editions

Tools

Dashboard

ProfessionalCommunity Edition

Dashboard

Last updated:

June 18, 2026

Read time:

3 Minutes

Burp's Dashboard tab provides a central location for monitoring and controlling all of the automated tasks in your project. These can include:

Professional Crawl tasks that automate the process of mapping the available attack surface by browsing the target website just like a real user. For more information, see

Crawling.

Professional Full vulnerability scans that both crawl the target website and audit the discovered attack surface for security issues. For more information, see

Automated scanning.

Professional Live tasks that perform various crawling and auditing operations using the traffic you generate while manually browsing the target website. For more information, see

Live tasks.

Burp Intruder attacks that repeatedly reissue an HTTP request using variable payloads in predefined insertion points. These are primarily useful for automating repetitive enumeration tasks and fuzzing different inputs. For more information, see

Burp Intruder.

Task list

Each task is represented by an entry in the Tasks list. This shows some key information about each task to help you monitor its progress.

For live tasks, you can also toggle whether the task is capturing traffic or not. For more information, see

Disabling traffic capturing for live tasks.

You can also click on an entry to view more detailed information about the task. For more information, see

Viewing scan and live task results.

Tip

You can rename tasks to help you more easily identify them later. This is especially useful in combination with the search feature.

Launching new tasks

You can launch a new scan or live task directly from the Dashboard tab. To do this, go to the Dashboard tab and click the New scan or New live task button. For more information, see

Launching scans or

Creating live tasks.

Pausing and resuming running tasks

You may want to pause running tasks if, for example, you are experiencing performance issues due to running a large number of concurrent tasks. You can do this from the Dashboard tab.

To pause or resume all tasks:

Go to the Dashboard tab.

At the top of the Tasks list, click the play/pause button.

To pause or resume individual tasks:

Go to the Dashboard tab.

In the Tasks list, find the entry for the relevant task.

Click the play/pause button next to the task's header.

By default, all running tasks are paused when you reopen an existing project file. This is especially useful if you open project files from unknown or untrusted sources. If you prefer, you can change this behavior from the settings menu under

Suite settings > Startup behavior > Pause automated tasks.

Note

If you run a large number of concurrent tasks, we recommend configuring resource pools to manage and prioritize use of system resources. For more information, see

Managing resource pools for scans.

Disabling traffic capturing for live tasks

For live tasks, you can toggle whether the task is currently capturing traffic. When capturing is disabled, the task ignores all traffic until you re-enable it. This is different from pausing the task; while a task is paused, Burp still queues any relevant traffic, then continues processing it once you resume the task.

To enable or disable traffic capturing for a live task, go to the Dashboard tab and use the Capturing toggle on the relevant task's entry in the Tasks list.

Bottom dock

From the bottom dock of the Dashboard tab, you can open several panels that display key information taken from all tasks in your project. These include:

The project-level Event log, which contains a log of all events that occurred while executing tasks in your current project. For more information, see

Event log.

The All issues panel, which contains an interactive table listing all issues found by tasks in your project. For more information, see

Issues.

The dock also displays information about Burp's memory usage and the size of your project file on disk.
