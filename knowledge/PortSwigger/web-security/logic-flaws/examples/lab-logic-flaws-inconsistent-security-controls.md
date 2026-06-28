# Lab: Inconsistent security controls

Source: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-inconsistent-security-controls
Fetched: 2026-06-28T09:17:56.401405+00:00

Web Security Academy

Business logic vulnerabilities

Examples

Lab

Lab: Inconsistent security controls

This lab's flawed logic allows arbitrary users to access administrative functionality that should only be available to company employees. To solve the lab, access the admin panel and delete the user carlos.

Solution

Open the lab then go to the "Target" > "Site map" tab in Burp. Right-click on the lab domain and select "Engagement tools" > "Discover content" to open the content discovery tool.

Click "Session is not running" to start the content discovery. After a short while, look at the "Site map" tab in the dialog. Notice that it discovered the path /admin.

Try and browse to /admin. Although you don't have access, the error message indicates that DontWannaCry users do.

Go to the account registration page. Notice the message telling DontWannaCry employees to use their company email address. Register with an arbitrary email address in the format:

anything@your-email-id.web-security-academy.net

You can find your email domain name by clicking the "Email client" button.

Go to the email client and click the link in the confirmation email to complete the registration.

Log in using your new account and go to the "My account" page. Notice that you have the option to change your email address. Change your email address to an arbitrary @dontwannacry.com address.

Notice that you now have access to the admin panel, where you can delete carlos to solve the lab.

Community solutions

Rana Khalil

Michael Sommer

Find business logic vulnerabilities using Burp Suite

Try for free
