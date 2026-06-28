# Using Burp to Detect SQL Injection Flaws

Source: https://portswigger.net/support/using-burp-to-detect-sql-injection-flaws
Fetched: 2026-06-28T09:17:36.049859+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Detect SQL Injection Flaws

SQL injection vulnerabilities arise when user-controllable data is incorporated into database SQL queries in an unsafe manner. An attacker can supply crafted input to break out of the data context in which their input appears and interfere with the structure of the surrounding query.

A wide range of damaging attacks can often be delivered via SQL injection, including reading or modifying critical application data, interfering with application logic, escalating privileges within the database and taking control of the database server.

In this example we will demonstrate how to detect SQL injection flaws using Burp Suite. This tutorial uses exercises from the "DVWA", "WebGoat" and "Mutillidae" training tools taken from OWASP's Broken Web Application Project. Find out how to download, install and use this project.

Scanning for SQL injection flaws

First, ensure that Burp is correctly configured with your browser.

Ensure "Intercept is off" in the Proxy "Intercept" tab.

Visit the web page of the application that you are testing.

Return to Burp and ensure "Intercept is on" in the Proxy "Intercept" tab.

Now send a request to the server. In this example by clicking the "Submit" button.

The request will be captured in the Proxy "Intercept" tab.

One way to test an application for SQL injection vulnerabilities is to send the request to Burp Scanner.

Right click anywhere on the request to bring up the context menu.

Click "Do an active scan".

Note: You can also send requests to the Scanner via the context menu in any location where HTTP requests are shown, such as the site map or Proxy history.

Once the scan is complete, go to the Target "Site map" tab.

In this example the Scanner has found a number of SQL injection issues.

Click on an individual issue to view the "Advisory" tab, which provides details about each specific vulnerability.

You can also view the requests and responses on the basis of which Burp has reported the issue.

Manual testing for SQL injection flaws

Alternatively, you can use Burp to manually test the application for injection vulnerabilities.

With intercept turned off in the Proxy "Intercept" tab, visit the web application you are testing in your browser.

Visit the web page you are testing.

You can often detect SQL injection by inputting certain characters in to the application's parameters.

In this example, submitting a ' (single quote) produces a custom error message.

However, inputting '' (two single quotes) does not.

The reason for this difference is that SQL strings are contained within single quote delimiters. Submitting one quote breaks the representation of the string, and therefore the wider SQL statement. Two single quotes are an escape sequence representing a literal single quote. So submitting two quotes inside the string just modifies the value of the string and does not break the SQL statement,

If you are not already familiar with SQL and SQL Injection, you can learn more about it here and here.

Now that you have detected a potential SQL vulnerability you can use Burp to investigate the vulnerability further.

Related articles:

What is Burp Proxy?

Scanning websites with Burp Scanner

Using Burp to Investigate SQL Injection Flaws

Using Burp to Exploit SQL Injection Vulnerabilities: The UNION Operator

Using Burp to Detect SQL-specific Parameter Manipulation Flaws

Using Burp to Detect Blind SQL Injection Bugs

Using Burp to Exploit Bind SQL Injection Bugs
