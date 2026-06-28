# Performance settings

Source: https://portswigger.net/burp/documentation/desktop/settings/suite/performance
Fetched: 2026-06-28T09:15:55.947615+00:00

Support Center

Documentation

Desktop editions

Settings

Suite

Performance

ProfessionalCommunity Edition

Performance settings

Last updated:

June 18, 2026

Read time:

3 Minutes

The Performance settings enable you to control how Burp's performs and share feedback to help improve performance.

Performance feedback

You can help to improve Burp by submitting feedback about Burp's performance. To do this, select Automatically submit feedback about Burp's performance.

The feedback contains technical information about Burp's internal functioning. It is linked to your debug ID, which identifies the session in which the exception was raised.

You can also report a bug by email. Include your debug ID to help us to diagnose any problems that your instance of Burp has encountered.

Logging exceptions to a local directory

In some cases, it may not be possible for us to automatically receive data about your performance issues. For example, your security policy might block data from being sent to our support team.

In this case, we might ask you to temporarily select the Log exceptions to a local directory setting and attempt to replicate the issue. Burp logs exceptions to a local file in the specified directory. You can then send a copy of the file to our support team.

The log entries contain:

The time of the exception.

A brief description.

A stack trace. The stack trace is fully obfuscated, so no personal data can be read from the file.

The file name is a combination of the current date and your debug ID. Each instance of Burp generates its own log.

Note

If you change the directory in which the log should be saved, make sure that the user who is replicating the issue has write access to the specified directory. Otherwise, Burp will be unable to generate the file.

Performance feedback is a user setting. It applies to all installations of Burp on your machine.

Maximum memory usage

You can set an upper limit on how much system memory Burp can use. By default, Burp can use half of your system memory.

Burp maximizes performance by using all allocated RAM before attempting to free memory. It will use RAM up to the limit you set. This makes tasks faster at the cost of higher memory usage.

When to adjust the limit

Adjusting this limit enables you to balance Burp's performance with your system's needs:

Decrease it if Burp's memory use is impacting your system performance. This leaves more memory for other processes, but can slow Burp during resource-intensive tasks (for example, large scans or Intruder attacks). The minimum value is 256MB.

Increase it to speed up Burp when working on large projects or when you have spare RAM. This lets Burp keep more data in memory, but leaves less for other applications. Make sure to specify a value within the limits of your available memory.

Restart Burp to apply the change.

Note

If you're using a temporary project and your memory usage is high, consider switching to a disk-based project. This moves some of the load from memory to a hard disk. To do this, click Project on the top-level menu, then select Save copy.

For more information, see Using a disk-based project.

Maximum memory usage is a user setting. It applies to all installations of Burp on your machine.
