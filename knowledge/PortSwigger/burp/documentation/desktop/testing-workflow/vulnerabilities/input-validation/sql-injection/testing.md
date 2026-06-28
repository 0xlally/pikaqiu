# Testing for SQL injection vulnerabilities with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/vulnerabilities/input-validation/sql-injection/testing
Fetched: 2026-06-28T09:15:59.785187+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Testing for vulnerabilities

Testing input validation

SQL injection

Testing for SQL injection vulnerabilities

ProfessionalCommunity Edition

Testing for SQL injection vulnerabilities with Burp Suite

Last updated:

June 18, 2026

Read time:

2 Minutes

SQL injection vulnerabilities occur when an attacker can interfere with the queries that an application makes to its database. You can use Burp to test for these vulnerabilities:

Professional Use Burp Scanner to automatically flag potential SQL injection vulnerabilities.

Use Burp Intruder to insert a list of SQL fuzz strings into a request. This may enable you to change the way SQL commands are executed.

Steps

You can follow this process using a lab with a SQL injection vulnerability. For example, SQL injection vulnerability in WHERE clause allowing retrieval of hidden data.

Scanning for SQL injection vulnerabilities

If you're using Burp Suite Professional, you can use Burp Scanner to test for SQL injection vulnerabilities:

Identify a request that you want to investigate.

In Proxy > HTTP history, right-click the request and select Do active scan. Burp Scanner audits the application.

Review the Issues list on the Dashboard to identify any SQL injection issues that Burp Scanner flags.

Manually fuzzing for SQL injection vulnerabilities

You can alternatively use Burp Intruder to test for SQL injection vulnerabilities. This process also enables you to closely investigate any issues that Burp Scanner has identified:

Identify a request that you want to investigate.

In the request, highlight the parameter that you want to test and select Send to Intruder.

Go to Intruder. Notice that the parameter has been automatically marked as a payload position.

In the Payloads side panel, under Payload configuration, add a list of SQL fuzz strings.

If you're using Burp Suite Professional, open the Add from list drop-down menu and select the built-in Fuzzing - SQL wordlist.

If you're using Burp Suite Community Edition, manually add a list.

Under Payload processing, click Add. Configure payload processing rules to replace any list placeholders with an appropriate value. You need to do this if you're using the built-in wordlist:

To replace the {base} placeholder, select Replace placeholder with base

value.

To replace other placeholders, select Match/Replace, then specify the

placeholder and replacement. For example, replace {domain} with the domain name

of the site you're testing.

Click Start attack. The attack starts running in a new dialog. Intruder sends a request for each SQL fuzz string on the list.

When the attack is finished, study the responses to look for any noteworthy behavior. For example, look for:

Responses that include additional data as a result of the query.

Responses that include other differences due to the query, such as a "welcome back" message or error

message.

Responses that had a time delay due to the query.

If you're using the lab, look for responses with a longer length. These may include additional products.

Related pages

Academy: SQL injection

Academy: Blind SQL injection

Burp Scanner - Auditing

Burp Intruder

Burp Intruder payload processing
