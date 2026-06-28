# Lab: Web shell upload via obfuscated file extension

Source: https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-obfuscated-file-extension
Fetched: 2026-06-28T09:17:50.907915+00:00

Web Security Academy

File upload vulnerabilities

Lab

Lab: Web shell upload via obfuscated file extension

This lab contains a vulnerable image upload function. Certain file extensions are blacklisted, but this defense can be bypassed using a classic obfuscation technique.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file /home/carlos/secret. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter

Solution

Log in and upload an image as your avatar, then go back to your account page.

In Burp, go to Proxy > HTTP history and notice that your image was fetched using a GET request to /files/avatars/<YOUR-IMAGE>. Send this request to Burp Repeater.

On your system, create a file called exploit.php, containing a script for fetching the contents of Carlos's secret. For example:

<?php echo file_get_contents('/home/carlos/secret'); ?>

Attempt to upload this script as your avatar. The response indicates that you are only allowed to upload JPG and PNG files.

In Burp's proxy history, find the POST /my-account/avatar request that was used to submit the file upload. Send this to Burp Repeater.

In Burp Repeater, go to the tab for the POST /my-account/avatar request and find the part of the body that relates to your PHP file. In the Content-Disposition header, change the value of the filename parameter to include a URL encoded null byte, followed by the .jpg extension:

filename="exploit.php%00.jpg"

Send the request and observe that the file was successfully uploaded. Notice that the message refers to the file as exploit.php, suggesting that the null byte and .jpg extension have been stripped.

Switch to the other Repeater tab containing the GET /files/avatars/<YOUR-IMAGE> request. In the path, replace the name of your image file with exploit.php and send the request. Observe that Carlos's secret was returned in the response.

Submit the secret to solve the lab.

Community solutions

Intigriti

Find file upload vulnerabilities using Burp Suite

Try for free
