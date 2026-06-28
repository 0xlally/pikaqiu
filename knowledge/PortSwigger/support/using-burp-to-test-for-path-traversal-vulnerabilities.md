# Using Burp to Test for Path Traversal Vulnerabilities

Source: https://portswigger.net/support/using-burp-to-test-for-path-traversal-vulnerabilities
Fetched: 2026-06-28T09:17:37.016343+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Using Burp to Test for Path Traversal Vulnerabilities

Many types of functionality commonly found in web applications involve processing user-supplied input as a file or directory name. If the user-supplied input is improperly validated, this behavior can lead to various security vulnerabilities, one of which is file path traversal.

Path traversal vulnerabilities arise when applications use user-controllable data to access files and directories on the application server or another back-end filesystem in an unsafe way. By submitting crafted input, an attacker may be able to cause arbitrary content to be read from, or written to, anywhere on the filesystem. This often enables an attacker to read sensitive information from the server, or overwrite sensitive files, ultimately leading to arbitrary command execution on the server.

During your initial mapping of the application, you should already have identified any obvious areas of attack surface in relation to path traversal vulnerabilities. Any functionality with the explicit purpose of uploading or downloading files should be thoroughly tested. This functionality is often found in workflow applications where users can share documents, in blogging and social media applications where users can upload images, and in informational applications where users can retrieve documents such as ebooks, technical manuals, and company reports.

This tutorial uses a version of "WebGoat.net" taken from OWASP's Broken Web Application Project. Find out how to download, install and use this project.

First, ensure that Burp is correctly configured with your browser.

Ensure "Intercept is off" in the Proxy "Intercept" tab.

The vulnerability arises because an attacker can place path traversal sequences into the filename to backtrack up from current directory.

The classic path traversal sequence is known as "dot-dot-slash".

Visit the web page of the application that you are testing.

Return to Burp and ensure "Intercept is on" in the Proxy "Intercept" tab.

Now, access the URL that includes the parameter you wish to test. In this example by clicking the "architecture.pdf" link.

The request will be captured in the Proxy "Intercept" tab.

Right click anywhere on the request to bring up the context menu.

Click "Send to Repeater".

Here we can input various payloads in to the input field of a web application and monitor the response.

Click the "Go" button in Repeater to send the request to the server.

You can observe the response from the server in the Repeater "Response" panel.

Continue to monitor the response as you utilize path traversal detection techniques..

Initially we can check whether our input is used in the filepath or ignored.

To perform this test we can compare the response from the server when injecting ./ and ../ in to the filename parameter.

Here we can see that the response appears unchanged after inserting the ./ payload.

However, when we use the ../ payload, the response is altered significantly.

This suggests that the application is using our input within a filepath.

Now, working on the assumption that the parameter you are targeting is being appended to a preset directory specified by the application, you can modify the parameter's value to insert an arbitrary subdirectory and single traversal sequence.

If the application's response is identical to the initial response, it may be vulnerable.

If you find any instances where the application may be vulnerable, the next test is to attempt to traverse out of the starting directory and access files from elsewhere on the server filesystem.

The manner in which you access files is dependent on the server and web framework you are testing.

In this example we are using an ASP.NET web framework. We know that web.config is the main settings and configuration file for an ASP.NET web application.

If we were attacking a Tomcat application server we might look for a web.xml file.

In some situations you may be able to traverse out of the starting directory and access a known word-readable file on the operating system in question.

Submit one of the following values as the filename parameter you control:

../../../../../../../../../../../../../../../../etc/passwd

../../../../../../../../../../../../../../../../windows/win.ini

In this example we have been able to access the passwd file of a Linux system.

Related articles:

What is Burp Proxy?

Using Burp Repeater
