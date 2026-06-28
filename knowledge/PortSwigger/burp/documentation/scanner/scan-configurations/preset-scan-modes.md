# Preset scan modes

Source: https://portswigger.net/burp/documentation/scanner/scan-configurations/preset-scan-modes
Fetched: 2026-06-28T09:16:11.052828+00:00

Support Center

Documentation

Scanner

Scan configurations

Preset scan modes

DASTProfessional

Preset scan modes

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Scanner's scan modes are predefined collections of scan settings. They offer a quick way to adjust how the scan balances speed and coverage.

There are four preset scan modes:

Lightweight is the fastest scan mode, with scans capped at 15 minutes in length. It is useful in situations where you need fast feedback on a target.

Fast is intended to give you a general overview of a site's security posture quickly.

Balanced is useful for general-purpose scanning. It is designed to give a good balance between coverage and speed.

Deep is intended to give you an in-depth look at a site's security posture. The time taken to run a scan using the Deep configuration depends heavily on the site's size and complexity.

Using presets in Burp Suite Professional

In Burp Suite Professional, you can use preset scan modes in the following ways:

Select a preset and start scanning immediately.

Select a preset as a starting point, then configure its settings as desired.

Related pages

Configuring scans in Burp Suite Professional

Setting preset scan modes for folders

In Burp Suite DAST, you can select a preset scan mode for folders, subfolders, and sites. If you select a preset scan mode at multiple levels, Burp Scanner only runs the preset scan mode that you set at the lowest level.

Preset scan modes in Burp Suite DAST can't be customized. For more control, create a custom scan configuration.

Related pages

Defining the scan configuration for a folder

Custom scan configurations

Creating custom scan configurations (Burp Suite DAST)
