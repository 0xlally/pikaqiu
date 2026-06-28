# Tick Tock Enumerator

Source: https://portswigger.net/bappstore/bc0a8cc810aa46afacbf91cce986f015
Fetched: 2026-06-28T09:14:57.432655+00:00

Support Center

BApp Store

Tick Tock Enumerator

Professional

Community

Tick Tock Enumerator

Download BApp

TickTockEnum is a timing-based enumeration extension that identifies vulnerabilities through response time analysis.

The extension detects discrepancies in server response times between valid and invalid inputs, making it

particularly effective for username enumeration attacks where authentication timing varies based on user existence.

Features

Automated timing analysis with configurable request volumes

Visual graph generation for response time comparison

Tabular results display with response times and status codes

Single-threaded request processing for maximum timing accuracy

CSV and JPG export capabilities for reporting

Placeholder-based request templating with $ticktock$ marker

Usage

Right-click on any HTTP request in Proxy, Repeater, or Target and select "Send to TickTock Enum"

Configure the extension parameters:

Set a known valid input (e.g., existing username)

Set a known invalid input (e.g., non-existent username)

Place $ticktock$ placeholder where enumeration data should be injected

Specify the number of requests per input value

Verify connection settings (host, port, protocol) are correctly populated

Click "Start" to begin the enumeration process

Analyze results in the table and graph showing response time patterns

Export results as CSV data or graph images for documentation

Note: Use caution with login forms to avoid account lockouts. The extension sends requests

sequentially for accurate timing measurements.

Author

Author

scho-d4n

Version

Version

1.0.0

Rating

Rating

Popularity

Popularity

Last updated

Last updated

30 September 2025

Estimated system impact

Estimated system impact

Overall impact:

Empty

Memory

Empty

CPU

Empty

General

Empty

Scanner

Empty

You can install BApps directly within Burp, via the BApp Store feature in the Burp Extender tool. You can also download them from here, for offline installation into Burp.

You can view the source code for all BApp Store extensions on our

GitHub page.

Follow

@BApp_Store on Twitter to receive notifications of all BApp releases and updates.

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.

Go back to

BappStore

Note:

Please note that extensions are written by third party users of Burp, and PortSwigger Web Security makes no warranty about their quality or usefulness for any particular purpose.
