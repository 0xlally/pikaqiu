# Using Burp to Find SQL Injection Flaws

Source: https://portswigger.net/support/using-burp-to-find-sql-injection-flaws
Fetched: 2026-06-28T09:17:36.423244+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Find SQL Injection Flaws

Almost every web application employs a database to store the various kinds of information it needs to operate. The means of accessing information within the database is Structured Query Language (SQL). SQL can be used to read, update, add, and delete information held within the database.

SQL is an interpreted language, and web applications commonly construct SQL statements that incorporate user-supplied data. If this is done in an unsafe way the application maybe vulnerable to SQL injection (SQLi). This flaw is one of the most notorious vulnerabilities to have afflicted web applications. In the most serious cases, SQL injection can enable an anonymous attacker to read and modify all data stored within the database, and even take full control of the server on which the database is running.

Using Burp to Test for SQLi

The articles below describe how to use Burp Suite to detect, investigate and exploit SQL injection flaws:

Using Burp to Detect SQL Injection Flaws

Using Burp to Investigate SQL Injection Flaws

Using SQL Injection to Bypass Authentication

Using Burp to Exploit SQL Injection Vulnerabilities: The UNION Operator

Using Burp to Detect SQL Injection Via SQL-Specific Parameter Manipulation

Using Burp with SQLMap

Using Burp to Test for Blind SQLi

The articles below describe how to use Burp Suite to detect and exploit Blind SQL injection flaws:

Using Burp to Detect Blind SQL Injection Bugs

Using Burp to Exploit Bind SQL Injection Bugs

Using Burp to

The articles below demonstrate various techniques when performing SQLi in different statement types and in the query structure:

SQL Injection in Different Statement Types

SQL Injection in the Query Structure

SQLi Filters

This article provides examples of how to beat SQLi filters:

SQL Injection: Bypassing Common Filters
