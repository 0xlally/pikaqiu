# Pausing and resuming scans

Source: https://portswigger.net/burp/documentation/dast/user-guide/working-with-scans/pausing-scans
Fetched: 2026-06-28T09:15:44.152035+00:00

DAST

Pausing and resuming scans

Last updated:

June 18, 2026

Read time:

3 Minutes

Cloud

Self-hosted

You can schedule pauses for your scans. This is useful if you want to avoid scanning during peak business hours or maintenance windows, for example. There are two ways to pause scans:

Scan freeze windows - Schedule scans to pause automatically, in one or more weekly time periods. You can configure your scan freeze windows to repeat as required.

Manual pause and resume - Manually pause and resume your scans when required.

When you pause a scan, Burp Suite DAST creates a project file on the DAST server. This enables the scan to resume from the same point.

Note

Depending on the size and complexity of your site, the project file may reach several gigabytes in size.

If you use a self-hosted version of Burp Suite DAST, make sure you have sufficient storage space on the DAST server before you pause any scans.

Creating scan freeze windows

Scan freeze windows enable you to set times when scans are automatically paused.

You can set up scan freeze windows that repeat weekly, or you can set specific start and end dates.

To create a scan freeze window:

Go to the Sites page and select the sites or folders you want to apply the scan freeze window to.

From the menu at the bottom of the window, click Add scan freeze window.

In the New scan freeze window dialog, enter a name for the scan freeze window. You can also enter a description to help identify it later.

In the Sites field, confirm or modify the sites and folders that the scan freeze window applies to.

Select how the scan freeze window repeats:

Repeat forever - The scan freeze window repeats every week.

Choose start and end date - Enter the dates when the scan freeze window applies.

In the Time zone field, select the time zone.

On the weekly calendar, click and drag the red time blocks to define a time period when scanning is paused. Green blocks show when scanning is allowed.

To add more time periods when scanning is paused, click on a timeline and drag the red time blocks as required.

To remove a time period, click the Delete icon.

Click Save.

When a scan freeze window is active, Burp Suite DAST pauses all running scans on the selected sites. It also prevents new scans from starting until the scan freeze window ends.

Managing scan freeze windows

To manage scan freeze windows, go to Settings > Pause and freeze scans.

The Scan freeze windows table shows all your scan freeze windows with their current status.

To edit a scan freeze window, click the adjacent Edit

icon.

To delete a scan freeze window, click the Delete icon.

To turn a scan freeze window on or off, use the toggle in the Status column.

Viewing paused scans

To view scans that are paused by a scan freeze window, go to the Scans page. The Status column shows which scans are paused.

Manually pausing and resuming scans

You can manually pause and resume one or more scans from the Scans page.

To pause scans:

Go to the Scans page and select the scans you want to pause.

From the menu at the bottom of the window, click Pause.

In the dialog box, click Confirm.

To resume scans:

Go to the Scans page and select the scans you want to resume.

From the menu at the bottom of the window, click Resume.

In the dialog box, click Confirm.

Note

If you manually pause a scan during a scan freeze window, the scan does not automatically resume when the freeze window ends. You need to manually resume the scan.

If you manually resume a scan during a scan freeze window, the scan remains paused until the freeze window ends.

Related pages

Managing scheduled scans - explains how to set up regularly-scheduled scans.
