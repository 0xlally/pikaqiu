# Lab: Web shell upload via Content-Type restriction bypass

Source: https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass
Fetched: 2026-06-28T09:17:50.141060+00:00

Web Security Academy

File upload vulnerabilities

Lab

Lab: Web shell upload via Content-Type restriction bypass

This lab contains a vulnerable image upload function. It attempts to prevent users from uploading unexpected file types, but relies on checking user-controllable input to verify this.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file /home/carlos/secret. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter

Solution

Log in and upload an image as your avatar, then go back to your account page.

In Burp, go to Proxy > HTTP history and notice that your image was fetched using a GET request to /files/avatars/<YOUR-IMAGE>. Send this request to Burp Repeater.

On your system, create a file called exploit.php, containing a script for fetching the contents of Carlos's secret. For example:

<?php echo file_get_contents('/home/carlos/secret'); ?>

Attempt to upload this script as your avatar. The response indicates that you are only allowed to upload files with the MIME type image/jpeg or image/png.

In Burp, go back to the proxy history and find the POST /my-account/avatar request that was used to submit the file upload. Send this to Burp Repeater.

In Burp Repeater, go to the tab containing the POST /my-account/avatar request. In the part of the message body related to your file, change the specified Content-Type to image/jpeg.

Send the request. Observe that the response indicates that your file was successfully uploaded.

Switch to the other Repeater tab containing the GET /files/avatars/<YOUR-IMAGE> request. In the path, replace the name of your image file with exploit.php and send the request. Observe that Carlos's secret was returned in the response.

Submit the secret to solve the lab.

Community solutions

Intigriti

Find file upload vulnerabilities using Burp Suite

Try for free
