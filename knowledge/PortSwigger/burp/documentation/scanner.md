# Burp Scanner

Source: https://portswigger.net/burp/documentation/scanner
Fetched: 2026-06-28T09:16:09.619545+00:00

Support Center

Documentation

Scanner

DASTProfessional

Burp Scanner

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Scanner is an automated dynamic application security testing (DAST) web vulnerability scanner. Designed to replicate the actions and methodologies of a skilled manual tester, Burp Scanner powers scans in Burp Suite's desktop editions and Burp Suite DAST.

How do scans work?

Burp Scanner handles virtually any target. Advanced features such as state management and automated logins enable it to deal with the challenges that scanning modern web applications can pose. Although the actions taken during a scan vary depending on target and configuration, scans generally comprise two key phases:

Crawling - The scanner catalogs the content of the application and the navigational paths within it. Burp Scanner navigates around the application in largely the same way that a human would. It follows links, submits forms, and logs in where necessary to create a map of the application's content.

Auditing - The scanner analyzes the application's traffic and behavior to identify security vulnerabilities and other issues. Burp Scanner sends a series of requests to the application and examines the results. It uses the information obtained in the crawl phase to determine the most efficient way to work.

This section of the site gives more information on Burp Scanner's features and how you can configure scans to best meet your needs.

Read more

Crawling.

Auditing.

Scan configurations.

Preset scan modes.

Custom scan configurations.

Burp Scanner built-in configurations.

Audit settings.

Crawl settings.

Browser-powered scanning.

Authenticated scanning.

Login credentials.

Identifying login and registration forms.

Recorded login sequences.

Requirements for API scanning.

Scanning single-page apps.

Burp Scanner error reference.

Vulnerabilities detected by Burp Scanner.

BChecks
