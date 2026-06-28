# Using Burp to Test for OS Command Injection Vulnerabilities

Source: https://portswigger.net/support/using-burp-to-test-for-os-command-injection-vulnerabilities
Fetched: 2026-06-28T09:17:36.963647+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Test for OS Command Injection Vulnerabilities

An OS command injection attack occurs when an attacker attempts to execute system level commands through a vulnerable application. A successful attack could potentially violate the entire access control model applied by the web application, allowing unauthorized access to sensitive data and functionality.

Thsi tutorial uses versions of "WackoPicko" and "Mutillidae" taken from OWASP's Broken Web Application Project. Find out how to download, install and use this project.

Manually Detecting OS Command Injection

First, ensure that Burp is correctly configured with your browser.

Ensure "Intercept is off" in the Proxy "Intercept" tab.

Any instances where the web application might be interacting with the underlying operating system by calling external processes or accessing the filesystem should be probed for command injection flaws.

In general, the most reliable way to detect whether command injection is possible is to use time-delay inference in a similar manner with which you might test for blind SQL injection.

Visit the web page of the application that you are testing.

Return to Burp and ensure "Intercept is on" in the Proxy "Intercept" tab.

Now, enter some data in to the password field and send a request to the server. In this example by clicking the "Check" button.

The request will be captured in the Proxy "Intercept" tab.

Right click anywhere on the request to bring up the context menu.

Click "Send to Repeater".

Here we can place various payloads into the input field and monitor the response.

Click the "Go" button in Repeater to send the request to the server.

Beneath the Repeater Response panel we can see the time taken to receive the response in milliseconds.

The response in this example has taken 4 milliseconds.

You can normally use the ping command as a means of triggering a time delay by causing the server to ping its loopback interface for a specific period. There are minor differences between how Windows and UNIX-based platforms handle command separators and the ping command. However, the following all purpose test string should induce a 10-second time delay on either platform if no filtering is in place.

|| ping -c 10 127.0.0.1 ; x || ping -n 10 127.0.0.1 &

Add your payload to the request and click the "Go" button again to resend the request to the server.

Return to the Repeater Response console to monitor the time taken to receive the response with the addition of the payload.

The response in this example has taken 9,061 seconds milliseconds. Repeat the test case several times to confirm that the delay was not the result of network latency or other anomalies.

A time delay would indicate that the application may be vulnerable to OS Command Injection.

The next step is to determine whether you can retrieve the results of the command directly to your browser.

Try injecting a more interesting command, such as ls, dir or id.

We can see how this payload has executed in OWASPBWA Mutillidae:

555-555-0199@example.com| ls /var/www ; x &

If you are unable to retrieve results directly, you have other options.

You can attempt to open an out-of-band channel back to your computer or you can redirect the results of your commands to a file within the web root, which you can then retrieve directly using your browser.

In our WackoPicko example we were able to use the id command to create a file within the application's web root folder.

You can check the results of your injection in your browser by adding the specified filename to the URL of the web root.

The id command allows us to print real and effective User ID (UID) and Group ID (GID).

Having confirmed the ability to inject commands and retrieve results, the next step should be to determine your privilege level.

You may then seek to escalate privileges, gain backdoor access to sensitive application data, or attack other hosts reachable from the compromised server.

Related articles:

What is Burp Proxy?

Using Burp Repeater
