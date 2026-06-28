# SQL Injection in the Query Structure

Source: https://portswigger.net/support/sql-injection-in-the-query-structure
Fetched: 2026-06-28T09:17:34.992973+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

SQL Injection in the Query Structure

If user-supplied data is being inserted into the structure of the SQL query itself, rather than an item of data within the query, exploiting SQL injection simply involves directly supplying valid syntax. No "escaping" is required to break out of any data context.

The most common injection point within the SQL query structure is within an ORDER BY clause. The ORDER BY keyword takes a column name or number and orders the result set according to the values in that column. This functionality is frequently exposed to the user to allow sorting of a table within the browser.

The example uses a version of the "Magical Code Injection Rainbow" taken from OWASP's Broken Web Application Project. Find out how to download, install and use this project.

Detecting SQLi in an ORDER BY clause

When mapping an application you should make a note of any parameters that appear to control the order or field types within the results that the application returns.

Make a series of requests supplying a numeric value in the parameter, starting with the number 1 and incrementing it with each subsequent request.

If changing the number in the input affects the ordering of the results, the input is probably being inserted in to an ORDER BY clause.

Increasing this number to 2 should then change the display order of data to order by the second column.

However, in this example, we are dealing with only one column. The number supplied is therefore greater than the number of columns in the results set and the query fails.

In this situation, you can confirm that further SQL can be injected by checking whether the results order can be reversed, using the following:

1 ASC --

1 DESC --

DESC reorganizes the results in to descending order.

Exploiting SQLi in an ORDER BY clause

Exploiting SQL injection in an ORDER BY clause is significantly different from most other cases. A database will not accept a UNION, WHERE, OR, or AND keyword at this point in the query.

In our example, exploitation requires the attacker to specify a nested query in place of the ORDER BY parameter identified above.

The vulnerable query allows you to test a single piece of information (e.g. a single string character) from anywhere in the database in a boolean query.

This crafted input will allow you to tell whether or not the first character of the username is 'P'. If it is, the article list will be returned sorted by username. If not, it will be returned sorted by id.

The results have been returned sorted by username, indicating that the username we have queried begins with P.

The crafted input above produces a "positive" response from the database. However, submitting a slightly different input produces a negative response. Thereby inferring that the condition tested was false.

By submitting a large number of such queries, cycling through the range of likely ASCII codes for each character until a hit occurs, you can extract the entire string, one byte at a time.
