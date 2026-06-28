# Professional 1.5rc2

Source: https://portswigger.net/burp/releases/professional-1-5rc2
Fetched: 2026-06-28T09:16:25.919974+00:00

This release fixes a number of minor bugs.

The Burp Repeater UI has been modified to conserve screen space. The previous fields for host / port / protocol have been removed, since these details are automatically populated when a request is sent to Repeater, and typically do not need to be modified. The details of the target server for the current request are still displayed, and you can change these details by clicking on the target server label, to open a dialog.

Burp's memory handling has been further refined, particularly when actively scanning, to reduce the overall memory footprint and improve Burp's resilience in low memory conditions.
