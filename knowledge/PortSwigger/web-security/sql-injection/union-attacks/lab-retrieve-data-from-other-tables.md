# Lab: SQL injection UNION attack, retrieving data from other tables

Source: https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables
Fetched: 2026-06-28T09:18:03.953236+00:00

Web Security Academy

SQL injection

UNION attacks

Lab

Lab: SQL injection UNION attack, retrieving data from other tables

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you need to combine some of the techniques you learned in previous labs.

The database contains a different table called users, with columns called username and password.

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user.

Solution

Use Burp Suite to intercept and modify the request that sets the product category filter.

Determine the number of columns that are being returned by the query and which columns contain text data. Verify that the query is returning two columns, both of which contain text, using a payload like the following in the category parameter:

'+UNION+SELECT+'abc','def'--

Use the following payload to retrieve the contents of the users table:

'+UNION+SELECT+username,+password+FROM+users--

Verify that the application's response contains usernames and passwords.

Community solutions

Intigriti

Rana Khalil

z3nsh3ll

Find SQL injection vulnerabilities using Burp Suite

Try for free
