# Using Burp to Test a REST API

Source: https://portswigger.net/support/using-burp-to-test-a-rest-api
Fetched: 2026-06-28T09:17:36.452639+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Test a REST API

REST (representational state transfer) is an architectural style consisting of a coordinated set of constraints applied to components, connectors, and data elements, within a distributed hypermedia system.

Burp can test any REST API endpoint, provided you can use a normal client for that endpoint to generate normal traffic. The process is to proxy the client's traffic through Burp and then test it in the normal way.

Most attacks which are possible on a typical web application are possible when testing REST API's. In this example we will demonstrate a SQLi injection attack on an application using a REST API. The example uses a version of “DVWS”. Find out how to download, install and use this project.

Identifying an API and mapping the attack surface

In a white or grey box testing situation you may be presented with the API documentation. This information should ensure good coverage of the attack surface.

However, in a black box test situation you may not have been informed that you are testing a REST API. How, then, do we identify the underlying technology?

In our example, the API is accessed from the URL:

http://localhost/dvws/vulnerabilities/sqli/api.php/users/2

Additionally, we can use Burp Suite to intercept the response and identify information in JSON format.

JSON (JavaScript Object Notation) is the most common means of exchanging data using a REST API.

Another common language is XML.

The next step is to identify parameters.

In our example, the parameter we have identified is in the URL:

api.php/users/2

We can alter this parameter to display different results:

api.php/users/3

Testing the API

Send the request to the Repeater tab.

We can use the Repeater tab to send the request to the server, like we would when testing any any other web application.

We have already demonstrated altering the value to a different number. Ascertaining that the parameter has an effect on the application.

The next step is to detect that the parameter is being evaluated arithmetically.

We can enter a calculation in to the parameter and monitor the response from the server.

In this example, we supply the value 3-2 and the application returns the information for "User/1" - "Darth Vader". The application is therefore evaluating the parameter arithmetically.

This behavior may point towards various possible vulnerabilities, including SQL injection.

The next step is to input SQL-specific keywords and syntax in to the parameter to compute the required value, thereby verifying that a SQL injection vulnerability is present.

A good example of this is the ASCII command, which returns the numeric ASCII code of the supplied character. In this example, because the ASCII value of the character 1 is 49, the following expression is equivalent to 1 in SQL:

50-ASCII(1)

The page is displayed without any errors and shows the details of "user/1". This is because the injected SQL syntax is equivalent to the value 1. This shows that the application is evaluating the input as a SQL query.
