# Lab: Blind OS command injection with out-of-band interaction

Source: https://portswigger.net/web-security/os-command-injection/lab-blind-out-of-band
Fetched: 2026-06-28T09:17:57.650530+00:00

Web Security Academy

OS command injection

Lab

Lab: Blind OS command injection with out-of-band interaction

This lab contains a blind OS command injection vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The command is executed asynchronously and has no effect on the application's response. It is not possible to redirect output into a location that you can access. However, you can trigger out-of-band interactions with an external domain.

To solve the lab, exploit the blind OS command injection vulnerability to issue a DNS lookup to Burp Collaborator.

Note

To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.

Solution

Use Burp Suite to intercept and modify the request that submits feedback.

Modify the email parameter, changing it to:

email=x||nslookup+x.BURP-COLLABORATOR-SUBDOMAIN||

Right-click and select "Insert Collaborator payload" to insert a Burp Collaborator subdomain where indicated in the modified email parameter.

Note

The solution described here is sufficient simply to trigger a DNS lookup and so solve the lab. In a real-world situation, you would use Burp Collaborator to verify that your payload had indeed triggered a DNS lookup. See the lab on blind OS command injection with out-of-band data exfiltration for an example of this.

Community solutions

Rana Khalil

Michael Sommer

Find OS command injection vulnerabilities using Burp Suite

Try for free
