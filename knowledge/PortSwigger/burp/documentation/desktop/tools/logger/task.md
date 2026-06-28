# Task Logger

Source: https://portswigger.net/burp/documentation/desktop/tools/logger/task
Fetched: 2026-06-28T09:16:06.219651+00:00

Support Center

Documentation

Desktop editions

Tools

Logger

Task Logger

ProfessionalCommunity Edition

Task Logger

Last updated:

June 18, 2026

Read time:

1 Minute

You can examine traffic generated for a single task. This enables you to investigate a task that behaves unexpectedly, or monitor the progress of a specific task.

To view task-specific log entries:

Go to Dashboard.

Select the relevant tasks from the Tasks list.

In the main panel, go to the Logger tab.

The task-specific Logger functions in a similar way to Burp Logger, with a couple of notable differences:

The default memory allocation for each task is only 10MB, or 20MB if you give Burp Suite access to 1GB or more of memory.

You cannot capture or filter by tool, as the task-specific Logger only captures and displays traffic from the tool used for the task.

Related pages

For information on how to edit what Logger captures, see Capture filter.

For information on how to edit what Logger displays, see View filter.
