# Professional 1.2.13

Source: https://portswigger.net/burp/releases/professional-1-2-13
Fetched: 2026-06-28T09:16:22.812017+00:00

1. You can now pause and resume active scanning, using the context menu on the scan queue tab. A new status bar shows you whether the scanner is running, and the number of currently active scan threads.

2. There is a new task scheduler, which you can use to automatically start and stop certain tasks at defined times and intervals. You can schedule a task on a specific URL using the new context menu item that appears throughout Burp:

This action starts a wizard which lets you configure the details and timing of the task. The tasks currently implemented are shown below:

You can configure each task to be one-off, or to repeat at regular intervals. Tasks that you have created appear in a table in the suite Options tab. For example, the following configuration will begin scanning a target overnight at 2am, and suspend the scanner each day during working hours:

You can also create a new task, and edit or remove existing tasks, using the above buttons.

3. The extensibility method IBurpExtenderCallbacks.getParameters now returns the type of each parameter, as well as its name and value. The method's signature is unchanged, however the implementation now returns the following object for each parameter:

String[] { name, value, type }

4. Passwords are now masked on-screen in the UI for configuring www and proxy authentication.
