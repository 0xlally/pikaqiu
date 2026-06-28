# Identifying supported HTTP methods with Burp Suite

Source: https://portswigger.net/burp/documentation/desktop/testing-workflow/analyzing/supported-http-methods
Fetched: 2026-06-28T09:15:58.266049+00:00

Support Center

Documentation

Desktop editions

Testing workflow

Analyzing the attack surface

Identifying supported HTTP methods

ProfessionalCommunity Edition

Identifying supported HTTP methods with Burp Suite

Last updated:

June 18, 2026

Read time:

4 Minutes

Due to misconfiguration, some websites support additional HTTP methods that may be useful to an attacker in a number of ways. These include:

Enabling you to perform destructive actions like modifying sensitive data or uploading malicious files.

Enabling you to bypass flawed access controls and other weak defenses.

Disclosing additional information about the website and its infrastructure.

Websites may also ignore the method completely and respond in the same way even if you specify an arbitrary, non-standard method. This could enable you to bypass WAFs and weak input filters, as well as some defenses against cross-site attacks.

The most reliable approach for identifying supported HTTP methods is to send a request using each potential method to see how the server responds. Burp Intruder provides several ways to automate this time-consuming process.

Note

Although sending an OPTIONS request sometimes causes the server to tell you which methods it supports, this information is often misleading or incomplete.

Before you start

Map the target website. For more information, see Mapping the target website with Burp Suite.

Enumerating supported methods for a single endpoint

The simplest approach is to test a single endpoint. Supported methods are often fairly consistent across the website as they are usually the result of server-level configuration and the default configuration of back-end frameworks. That said, there may be some exceptions.

To enumerate supported methods on a single endpoint:

Identify a relevant request. If you're testing the general configuration, use a GET request for the website's home page.

In the request, highlight the request method, then right-click the message and select Send to

Intruder.

Go to Intruder. Notice that the request method has been automatically marked as a payload position.

In the Payloads side panel, make sure that the payload type Simple list is selected.

Under Payload configuration, add a list of HTTP methods that you want to test:

If you're using Burp Suite Professional, open the Add from list dropdown menu and select the built-in HTTP verbs wordlist.

If you're using Burp Suite Community Edition, manually add a list of HTTP methods. Make sure you also include an arbitrary, non-existent method like XYZ to see how the server responds.

Click Start attack. The attack starts running in a new dialog.

When the attack is finished, study the responses to look for any noteworthy behavior. Don't rely purely on the HTTP status code as this may be misleading.

Note

In Burp Suite Community Edition, the rate at which Burp Intruder sends requests is restricted, so your attack will take significantly longer to run.

Enumerating supported methods for multiple endpoints

You may encounter inconsistent behavior in response to the same methods on different parts of the site. This often occurs when websites are maintained by multiple teams of developers, who may configure their own custom request handling. You might also find that specific endpoints behave differently.

To enumerate supported methods for multiple endpoints at once in order to identify these inconsistencies:

In Burp, go to the Target > Site map tab.

From the site map, right-click on the host and select Copy URLs in this host.

Send a GET request for the target host to Burp Intruder.

In Burp Intruder, make the following settings:

Select Cluster bomb attack from the attack type drop-down menu.

Select the request method, then click Add § to mark this as a payload position.

Select the request path, then click Add § to mark this as a second payload position.

In the Payloads side panel, make sure that payload position 1 and the payload type Simple list are selected.

Under Payload configuration, add a list of HTTP methods that you want to test:

If you're using Burp Suite Professional, open the Add from list dropdown menu and select the

built-in HTTP verbs wordlist.

If you're using Burp Suite Community Edition, manually add a list of HTTP methods. Make sure you also include an arbitrary, non-existent method to see how the server responds.

Select position 2 from the Payload position drop-down list. Make the following settings:

Under Payload configuration, click Paste to paste the list of URLs you copied from the site map.

Under Payload processing, click Add. In the dialog that appears, create a Match/replace rule that replaces the scheme and hostname of your URLs with an empty string.

Under Payload encoding, deselect the URL-encode these characters checkbox. This prevents the forward-slash characters in the path from being encoded.

Click Start attack. The attack starts running in a new dialog. Burp Intruder sends a request using each of the specified methods to each of the endpoints you selected.

When the attack is finished, study the responses to look for any noteworthy behavior. Don't rely purely on the HTTP status code as this may be misleading.

Note

In Burp Suite Community Edition, the rate at which Burp Intruder sends requests is restricted, so your attack will take significantly longer to run.

Related pages

Burp Intruder

LAB: Broken access control resulting from platform misconfiguration

LAB: Information disclosure due to insecure configuration

LAB: Bypass Lax SameSite restrictions using GET requests

LAB: CSRF validation depends on request method
