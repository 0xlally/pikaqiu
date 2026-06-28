# Using Burp to Detect SQL Injection Via SQL-Specific Parameter Manipulation

Source: https://portswigger.net/support/using-burp-to-detect-sql-injection-via-sql-specific-parameter-manipulation
Fetched: 2026-06-28T09:17:36.055006+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Detect SQL Injection Via SQL-Specific Parameter Manipulation

In the most obvious cases, a SQL injection flaw may be discovered and conclusively verified by supplying a single item of unexpected input to the application. In other cases, bugs may be extremely subtle and may be difficult to distinguish from other categories of vulnerability or from benign anomalies that do not present a security threat. Nevertheless, you can carry out various steps in an ordered way to reliably verify the majority of SQL injection flaws.

It is often possible to detect subtle SQL injection vulnerabilities by manipulating parameters to use SQL-specific syntax to construct their values, and observing the effects on application responses.

Manual testing for numeric SQL-specific parameter manipulation

First, ensure that Burp is correctly configured with your browser.

Ensure "Intercept is off" in the Proxy "Intercept" tab.

Visit the web page of the application that you are testing.

Return to Burp and ensure "Intercept is on" in the Proxy "Intercept" tab.

Now send a request to the server. In this example by refreshing the page.

The request will be captured in the Proxy "Intercept" tab.

The parameter we will attempt to manipulate is the "id" parameter in the URL.

Right click on anywhere on the request and click "Send to Repeater".

Go to the Repeater tab.

We can alter the value of the parameter in either the "Raw" or "Params" tabs.

The first step is to alter the value simply to a different number.

By using this method, we can ascertain whether altering the parameter has an effect on the application.

Click "Go" to send the altered request to the server.

The results of the request can be viewed in the response section of the "Repeater" tool.

In this example we have chosen to represent the response using the "Render" tab.

We can clearly see the "User ID", "User name" and "Email" have changed.

The application is displaying the details of another user.

We have confirmed that the application is using the 'id' parameter to retrieve stored data.

The next step is to detect that the parameter is being evaluated arithmetically.

We can enter a calculation in to the parameter and monitor the response from the server.

In this example, we supply the value 3-2 and the application returns the information for "User id 1". The application is therefore evaluating the parameter arithmetically.

This behavior may point towards various possible vulnerabilities, including SQL injection.

The next step is to input SQL-specific keywords and syntax in to the parameter to compute the required value, thereby verifying that a SQL injection vulnerability is present.

A good example of this is the ASCII command, which returns the numeric ASCII code of the supplied character. In this example, because the ASCII value of the character 1 is 49, the following expression is equivalent to 1 in SQL:

50-ASCII(1)

The page is displayed without any errors and shows the details of user 1. This is because the injected SQL syntax is equivalent to the value 1. This shows that the application is evaluating the input as a SQL query.

Manual testing for string based SQL-specific parameter manipulation

First, ensure that Burp is correctly configured with your browser.

Ensure "Intercept is off" in the Proxy "Intercept" tab.

Visit the web page of the application that you are testing.

Return to Burp and ensure "Intercept is on" in the Proxy "Intercept" tab.

Now send a request to the server. In this example by clicking the help button.

The request will be captured in the Proxy "Intercept" tab.

The parameter we will attempt to manipulate is the "id" parameter in the URL.

Right click on anywhere on the request and click "Send to Repeater".

Go to the Repeater tab.

Use the "Go" button to send the request to the server.

The response can be viewed in the opposite side of the Repeater panel.

We can alter the value of the parameter in either the "Raw" or "Params" tabs.

In this example we have added a single letter "z" to the value of the parameter.

The additional letter causes a change in the response from the application.

This demonstrates that the parameter is being used to retrieve content.

The next step is to confirm that the value of the parameter is being evaluated as a SQL query. Thereby verifying the possibility of a SQL injection flaw.

In this example we have changed the value of the parameter from user-info.php to user'%20'-info.php.

%20 is a URL-encoded space, and a space can be used to concatenate strings in some SQL databases.

If the response from the application now matches the original response, then it is clear that the application is evaluating the parameter within a SQL query.

On this occasion there is no error message or change in the response.

This indicates that the input is being incorporated into a SQL query in an unsafe way.

We can verify this in the "Response" section of the repeater tab or by sending the request to the application via the browser.

Related articles:

What is Burp Proxy?

Using Burp Repeater

Using Burp to Test For Injection Flaws

Using Burp to Exploit SQL Injection Vulnerabilities: The UNION Operator

Using Burp to Detect Blind SQL Injection Bugs

Using Burp to Exploit Bind SQL Injection Bugs
