# Using Burp to Bypass Client Side JavaScript Validation

Source: https://portswigger.net/support/using-burp-to-bypass-client-side-javascript-validation
Fetched: 2026-06-28T09:17:35.899233+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Bypass Client Side JavaScript Validation

It is common to see customized client-side input validation implemented within scripts. Client-side controls of this kind are usually easy to circumvent; it is possible to enter a benign value into the input field in the browser, intercept the validated submission with your proxy, and modify the data to your desired value. This article details this method.

Note: Client-side JavaScript routines to validate user input are common in web applications, but it should not be concluded that every such application is vulnerable. The application is exposed only if client-side validation is not replicated on the server, and even then only if crafted input that circumvents client-side validation can be used to cause some undesirable behavior by the application.

First, ensure that Burp is correctly configured with your browser.

With intercept turned off in the Proxy "Intercept" tab, visit the web application you are testing in your browser.

Access the page of the web application you wish to test.

In this example we are using the "Bypass Client Side JavaScript Validation" page of the "WebGoat" training tool.

Return to Burp.

In the Proxy "Intercept" tab, ensure "Intercept is on".

Return to your browser.

Enter a benign value into the input field of your browser.

Submit the request to the server, in this example by clicking the "Submit" button.

Burp will capture the request.

In this example we have used the "Params" tab to easily identify and edit the appropriate fields in the request.

Use the "Forward" button to send the request to the server.

In this example we have been able to bypass client-side JavaScript validation.

The web application has validated the input at the server and returned an error message for each field.

Related articles:

What is Burp Proxy?

Bypassing client-side controls
