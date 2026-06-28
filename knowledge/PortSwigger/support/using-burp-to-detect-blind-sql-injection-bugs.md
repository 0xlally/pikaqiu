# Using Burp to Detect Blind SQL Injection Bugs

Source: https://portswigger.net/support/using-burp-to-detect-blind-sql-injection-bugs
Fetched: 2026-06-28T09:17:36.009618+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Detect Blind SQL Injection Bugs

SQL injection vulnerabilities are often referred to as "blind" if they cannot be straightforwardly identified via error messages or direct retrieval of data. These vulnerabilities are harder, but by no means impossible, to detect and exploit. In this article, we will examine some of the possible ways through which blind SQL injection vulnerabilities can be identified, by injecting Boolean conditions, triggering time delays, and out-of-band channels.

Boolean Condition Injection

Here we have an example web application from the WebGoat training tool. The version of "WebGoat" we are using is taken from OWASP's Broken Web Application Project. Find out how to download, install and use this project.

This form is designed to be used for testing whether a supplied account number is valid. We can see that the account number 101 produces a positive result, so the account number is valid.

The "true" condition has been met.

Next, we must satisfy the "false" condition.

In this example we have used the account number 666. The application has returned a negative response, so the account number is invalid.

The "false" condition has been met.

The next step is to confirm that the input is being evaluated as a SQL query and whether we can perform a true/false test using SQL syntax.

Here we have entered 101 and 1=1. We know that both parts of this condition are true and would expect a positive "True" response.

Here we have entered 101 and 1=2. We know that only one part of this condition is true and should return a negative "False" response.

Now we know that we can ask the application "questions" using SQL syntax, we can inject SQL to find out any information that is accessible.

In this example we are looking for the pin number that corresponds with the cc_number.

To find the pin in this example we could alter the number in the SQL statement and wait for the application to produce a positive "True" response. To reduce the number of requests involved, we could also test each character in the number one at a time, and perform binary searches to efficiently find the correct answer.

We could use Burp Intruder to automate this task for us.

Using Time Delays

In some cases of blind SQL injection, where no differential response can be triggered via injected Boolean conditions, an alternative technique that is often effective is to inject time delays.

In this example we use an exercise from the MD Sec training labs.

We may have tried to induce conditional errors...

However, there have been no effects on the application's behavior, even if it induces an error within the database itself.

In this situation we can use Burp Suite to inject SQL that will cause a time delay, and monitor the time taken for the response to be returned.

Ensure "Intercept is on" in the Proxy "Intercept" tab and resend the request.

Right click anywhere on the request and click "Send to Repeater".

We can alter the request using either the "Raw" or "Params" tab in the Repeater "Request" panel.

In this example we are injecting in to a MS-SQL database. We inject the following string into the request parameter and monitor how long the application takes to identify any vulnerabilities.

1; waitfor delay '0:0:5'--

Beneath the "Repeater" Response console we can see the time taken to receive the response in milliseconds.

The response in this example has taken 5 seconds.

This would indicate that the application is indeed vulnerable to SQL injection.

Using Out-Of-Band Channels

In some situations, it isn't possible to trigger any noticeable effect in the application's response, either in its contents or in the time taken to receive it. In this situation, it is possible to detect SQL injection vulnerabilities by causing the database to make an out-of-band network connection to the tester's server.

Burp Scanner uses this technique via the Burp Collaborator feature.

In this example we can see that Burp Scanner has exploited a blind SQL injection vulnerability to cause the database to make a network connection to the Burp Collaborator server. This particular attack uses Microsoft SQL Server''s xp_dirtree stored procedure. Similar techniques exist on other database platforms, and these are used by Burp Scanner.

Related articles:

What is Burp Proxy?

Using Burp Repeater

Using Burp to Test For Injection Flaws

Using Burp to Exploit SQL Injection Vulnerabilities: The UNION Operator

Using Burp to Detect SQL-specific Parameter Manipulation Flaws

Using Burp to Exploit Bind SQL Injection Bugs
