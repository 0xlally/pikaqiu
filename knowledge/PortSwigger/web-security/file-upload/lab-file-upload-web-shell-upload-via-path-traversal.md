# Lab: Web shell upload via path traversal

Source: https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal
Fetched: 2026-06-28T09:17:50.359505+00:00

Web Security Academy

File upload vulnerabilities

Lab

Lab: Web shell upload via path traversal

This lab contains a vulnerable image upload function. The server is configured to prevent execution of user-supplied files, but this restriction can be bypassed by exploiting a secondary vulnerability.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file /home/carlos/secret. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter

Solution

Log in and upload an image as your avatar, then go back to your account page.

In Burp, go to Proxy > HTTP history and notice that your image was fetched using a GET request to /files/avatars/<YOUR-IMAGE>. Send this request to Burp Repeater.

On your system, create a file called exploit.php, containing a script for fetching the contents of Carlos's secret. For example:

<?php echo file_get_contents('/home/carlos/secret'); ?>

Upload this script as your avatar. Notice that the website doesn't seem to prevent you from uploading PHP files.

In Burp Repeater, go to the tab containing the GET /files/avatars/<YOUR-IMAGE> request. In the path, replace the name of your image file with exploit.php and send the request. Observe that instead of executing the script and returning the output, the server has just returned the contents of the PHP file as plain text.

In Burp's proxy history, find the POST /my-account/avatar request that was used to submit the file upload and send it to Burp Repeater.

In Burp Repeater, go to the tab containing the POST /my-account/avatar request and find the part of the request body that relates to your PHP file. In the Content-Disposition header, change the filename to include a directory traversal sequence:

Content-Disposition: form-data; name="avatar"; filename="../exploit.php"

Send the request. Notice that the response says The file avatars/exploit.php has been uploaded. This suggests that the server is stripping the directory traversal sequence from the file name.

Obfuscate the directory traversal sequence by URL encoding the forward slash (/) character, resulting in:

filename="..%2fexploit.php"

Send the request and observe that the message now says The file avatars/../exploit.php has been uploaded. This indicates that the file name is being URL decoded by the server.

In the browser, go back to your account page.

In Burp's proxy history, find the GET /files/avatars/..%2fexploit.php request. Observe that Carlos's secret was returned in the response. This indicates that the file was uploaded to a higher directory in the filesystem hierarchy (/files), and subsequently executed by the server. Note that this means you can also request this file using GET /files/exploit.php.

Submit the secret to solve the lab.

Community solutions

Intigriti

Find file upload vulnerabilities using Burp Suite

Try for free
