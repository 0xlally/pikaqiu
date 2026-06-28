# Using Burp to Bypass Hidden Form Fields

Source: https://portswigger.net/support/using-burp-to-bypass-hidden-form-fields
Fetched: 2026-06-28T09:17:35.943386+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Bypass Hidden Form Fields

Hidden HTML form fields are a common mechanism for transmitting data via the client in a superficially unmodified way. If a field is flagged as hidden, it is not displayed on-screen. However, the field’s name and value are stored with the form and are sent back to the application when the user submits the form. Burp Proxy can be used to intercept the request that submits the form and modify the value. This is demonstrated in the example below.

First, ensure that Burp is correctly configured with your browser.

With intercept turned off in the Proxy "Intercept" tab, visit the web application you are testing in your browser.

Access the page of the web application you wish to test.

In this example we are using the "Exploit Hidden Fields" page of the WebGoat training tool.

Return to Burp.

In the Proxy "Intercept" tab, ensure "Intercept is on".

Return to your browser and submit a request to the server.

In this example by clicking the "Purchase" button.

Burp will capture the request, which can then be edited before being forwarded to the server.

Locate the value you wish to change in the hidden form field.

In this example we are altering the "Price" of an item from $2999.99 to $10.

Now use the "Forward" button to send the request to the server.

In this example, by intercepting a request and editing a hidden form field, we have been able to bypass a client-side control.

We have used this technique to alter the price of an item and purchase the product for a reduced cost.

Additionally, it is possible to use the "Response Modification" options to automatically modify responses and unhide hidden fields..

Go to the Proxy "Options" tab and locate the "Response Modification" section. Click the checkbox next to "Unhide hidden form fields".

There is also a sub-option to prominently highlight unhidden fields on-screen, for easy identification.

This option can be used to remove this specific client-side control over data.

The price of the item can be altered using your web browser without having to capture and modify the request in Burp.

Related articles:

What is Burp Proxy?

Bypassing client-side controls
