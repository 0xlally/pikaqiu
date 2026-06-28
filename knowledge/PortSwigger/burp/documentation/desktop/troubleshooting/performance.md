# Troubleshooting performance issues in Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/troubleshooting/performance
Fetched: 2026-06-28T09:16:09.764483+00:00

Support Center

Documentation

Desktop editions

Troubleshooting

Troubleshooting performance issues

ProfessionalCommunity Edition

Troubleshooting performance issues in Burp Suite

Last updated:

June 18, 2026

Read time:

6 Minutes

There are circumstances in which Burp Suite can run slowly. In this section, we'll describe some quick steps you can take to troubleshoot performance issues in Burp Suite and increase the efficiency of your testing.

Optimize memory usage

Optimize your memory usage in the following ways:

Disabling extensions

Burp Suite extensions are useful, but can increase the load on your system. PortSwigger does not test extensions for resource optimization and some extensions will impact Burp Suite's performance. It is best to be cautious about the extensions you use and remove any that you do not need. If Burp Suite appears to be using an excessive amount of memory, try disabling your extensions one by one to discover if any of them are causing problems.

Adjusting Burp's memory usage

You can adjust Burp's RAM allocation to balance Burp's performance with your system's needs:

Decrease it if Burp's memory use is impacting your system performance. This leaves more memory for other processes, but can slow Burp during resource-intensive tasks (for example, large scans or Intruder attacks).

Increase it to speed up Burp when working on large projects or when you have spare RAM. This lets Burp keep more data in memory, but leaves less for other applications.

To adjust Burp's memory usage:

From the settings menu , click Suite > Performance.

Go to the Maximum memory usage section.

In the Set custom value field, specify a value. The value should be under the limits of your available memory,

and must be above 256MB.

Restart Burp to apply the change.

Using a disk-based project

Temporary projects have more demands on memory than disk-based projects, as all the project data needs to be stored in memory rather than on a disk. If your memory use is maximized, switching to a disk-based project will move some of the load from memory to a hard disk. However, note that RAM is faster than hard drives, and it's possible that doing this will introduce delays, especially if your disks are slow (e.g. hard disk drives rather than solid state drives). You may need to experiment to see whether disk-based or temporary projects are faster for you. You can convert a temporary project to a disk-based project by going to the Project menu and selecting Save copy.

Note

Due to the way our persistence framework operates, we recommend using a local drive for saving project files rather than a network drive.

Check the minimum system requirements

All editions of Burp Suite require 64-bit hardware. For the best experience with Burp Suite Professional, we recommend using a machine with at least 8 GB of memory and 2 CPU cores. If you are performing large amounts of work, or testing large or complex applications, you may need a more powerful machine than this.

Identify potential bottlenecks: CPU, memory, and network

Burp Suite places additional load on your machine's CPU and memory, and on the network over which it runs.

If Burp Scanner is causing high CPU usage, you can Optimize CPU usage.

If your work with Burp Suite is using all available memory, you can Optimize memory usage.

If your work is using all available network resources, you can Optimize network usage.

Optimize CPU usage

Manage Burp's CPU use by disabling certain features and configuring scans in the following ways:

Disabling pretty printing

Wherever HTTP requests or responses are displayed in Burp Suite, such as in the Target tab or in Burp Repeater, you have the option to view a prettified version of the message as well as the raw content. Prettifying larger files, especially JavaScript files, can take some time. By default, Burp Suite uses the Pretty view for all supported content types. However, if you find that this is causing poor performance, you can disable this option so that the Raw view is used instead. To do this:

Select Settings > UI > Message editor.

Under the HTTP Message Display section, uncheck the Pretty print by default box.

Disabling JavaScript analysis

JavaScript analysis is computationally expensive and can slow down the auditing phase of a scan. If you are not interested in the JavaScript running on your target, you can disable the analysis.

Note

You can disable JavaScript analysis by applying one of Burp Scanner's built-in configurations:

Audit checks - all except JavaScript analysis. Alternatively, you can make your own custom scan configuration by following the steps below.

From the menu bar at the top of the screen, select Burp > Configuration library.

Select a new scan configuration or edit an existing one. Select Auditing.

Expand the Scan checks section.

Click JavaScript to filter the table by checks that use JavaScript analysis.

Deselect the top checkbox to disable all JavaScript analysis.

Save the configuration and select OK.

Configuring your scans for performance

Burp Scanner has many configurable options for optimizing performance during both the crawl and audit phases. Applying the following built-in scan configurations can help to improve performance:

Crawl strategy - faster.

Crawl strategy - fastest.

Crawl limit - 10, 30, or 60 minutes.

Audit checks - light active.

Audit checks - medium active.

Alternatively, you can make your own custom configuration by following the steps below.

From the menu bar at the top of the screen, select Burp > Configuration library.

Create a new scan configuration or edit an existing one.

Alter the configuration as described in the following two sections.

Save the edited configuration.

To optimize performance during crawling:

In the Crawl strategy area, select the Faster or Fastest crawl strategies. There is some risk of losing coverage when using either of these strategies, but they may still be suitable for scanning mostly static targets.

In the Crawl strategy area, reduce the Maximum crawl depth if the locations relevant to your work are being found early in the scan.

Likewise, in the Crawl limits area, reduce the Maximum crawl time if you are finding the relevant locations early in the scan.

To optimize performance during auditing:

In the Scan checks area, filter the built-in scan checks by Intrusive, then toggle the top checkbox to disable all intrusive checks. Intrusive auditing is computationally expensive, and some intrusive scans rely on a target timing out, so can take considerable time to complete. Doing this will miss vulnerabilities that are detected only by intrusive techniques, however.

Likewise, unchecking the Medium active scan checks in the same area will speed up performance, at the cost of missing vulnerabilities that are detected by medium active techniques.

In the Audit strategy area, set Audit speed to Fast to increase performance at the cost of thoroughness. Also, unchecking Automatically maintain session in the same area will improve performance, but this should not be done unless the target site is mostly static. A third option, under Ignore insertion points, is to limit which insertion points are audited if you are not interested in looking for certain vulnerability types or locations.

Narrowing the scope of your scans

Ensure that you are only scanning the areas of the target site that you are interested in. Narrowing your scope will improve performance. Fine-tune the scope of a scan from the Detailed scope configuration area of the scan launcher.

Scanning a single protocol

If your target only supports one of HTTP and HTTPS, ensure that Burp Scanner only sends requests using the supported protocol. In Scan details, in the URLs to scan section, include the desired protocol in each URL that you want to scan. Then select Scan using my specified protocols in the same area.

Optimize network usage

Manage network issues in the following ways:

Reducing concurrent scans

To reduce the load on your network, reduce the number of scans running together.

Configuring resource pools

Burp Suite can overload target applications by sending requests faster than a target can handle or will allow during active scans. Stop requests hanging or timing out by reducing the number of requests that Burp Suite makes at once:

Click on the cog icon next to New Live Task to bring up the Settings dialogue.

Create a new resource pool or edit an existing one, and reduce the maximum number of concurrent tasks.

Save the resource pool.
