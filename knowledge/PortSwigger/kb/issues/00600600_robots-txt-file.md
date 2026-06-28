# Robots.txt file

Source: https://portswigger.net/kb/issues/00600600_robots-txt-file
Fetched: 2026-06-28T09:17:17.068293+00:00

Support Center

Issue Definitions

Robots.txt file

Robots.txt file

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Description: Robots.txt file

The file robots.txt is used to give instructions to web robots, such as search engine crawlers, about locations within the web site that robots are allowed, or not allowed, to crawl and index.

The presence of the robots.txt does not in itself present any kind of security vulnerability. However, it is often used to identify restricted or private areas of a site's contents. The information in the file may therefore help an attacker to map out the site's contents, especially if some of the locations identified are not linked from elsewhere in the site. If the application relies on robots.txt to protect access to these areas, and does not enforce proper access control over them, then this presents a serious vulnerability.

Remediation: Robots.txt file

The robots.txt file is not itself a security threat, and its correct use can represent good practice for non-security reasons. You should not assume that all web robots will honor the file's instructions. Rather, assume that attackers will pay close attention to any locations identified in the file. Do not rely on robots.txt to provide any kind of protection over unauthorized access.

Vulnerability classifications

CWE-200: Information Exposure

Typical severity

Information

Type index (hex)

0x00600600

Type index (decimal)

6292992

Twitter

WhatsApp

Facebook

Reddit

LinkedIn

Email

Burp Scanner

This issue - and many more like it - can be found using our

web vulnerability scanner

Read more

Get Burp

Scan your web application from just $499.00

Find out more
