# Lab: SQL injection UNION attack, determining the number of columns returned by the query

Source: https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns
Fetched: 2026-06-28T09:18:03.814333+00:00

Web Security Academy

SQL injection

UNION attacks

Lab

Lab: SQL injection UNION attack, determining the number of columns returned by the query

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. The first step of such an attack is to determine the number of columns that are being returned by the query. You will then use this technique in subsequent labs to construct the full attack.

To solve the lab, determine the number of columns returned by the query by performing a SQL injection UNION attack that returns an additional row containing null values.

Solution

Use Burp Suite to intercept and modify the request that sets the product category filter.

Modify the category parameter, giving it the value '+UNION+SELECT+NULL--. Observe that an error occurs.

Modify the category parameter to add an additional column containing a null value:

'+UNION+SELECT+NULL,NULL--

Continue adding null values until the error disappears and the response includes additional content containing the null values.

Community solutions

Rana Khalil

z3nsh3ll

Find SQL injection vulnerabilities using Burp Suite

Try for free
