# Lab: Insecure direct object references

Source: https://portswigger.net/web-security/access-control/lab-insecure-direct-object-references
Fetched: 2026-06-28T09:17:38.218161+00:00

Web Security Academy

Access control

Lab

Lab: Insecure direct object references

This lab stores user chat logs directly on the server's file system, and retrieves them using static URLs.

Solve the lab by finding the password for the user carlos, and logging into their account.

Solution

Select the Live chat tab.

Send a message and then select View transcript.

Review the URL and observe that the transcripts are text files assigned a filename containing an incrementing number.

Change the filename to 1.txt and review the text. Notice a password within the chat transcript.

Return to the main lab page and log in using the stolen credentials.

Community solutions

Intigriti

Rana Khalil

Michael Sommer (no audio)

Find access control vulnerabilities using Burp Suite

Try for free
