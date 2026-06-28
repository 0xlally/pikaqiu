# Lab: Remote code execution via web shell upload

Source: https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload
Fetched: 2026-06-28T09:17:50.068009+00:00

Web Security Academy

File upload vulnerabilities

Lab

Lab: Remote code execution via web shell upload

This lab contains a vulnerable image upload function. It doesn't perform any validation on the files users upload before storing them on the server's filesystem.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file /home/carlos/secret. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter

Solution

While proxying traffic through Burp, log in to your account and notice the option for uploading an avatar image.

Upload an arbitrary image, then return to your account page. Notice that a preview of your avatar is now displayed on the page.

In Burp, go to Proxy > HTTP history. Click the filter bar to open the HTTP history filter window. Under Filter by MIME type, enable the Images checkbox, then apply your changes.

In the proxy history, notice that your image was fetched using a GET request to /files/avatars/<YOUR-IMAGE>. Send this request to Burp Repeater.

On your system, create a file called exploit.php, containing a script for fetching the contents of Carlos's secret file. For example:

<?php echo file_get_contents('/home/carlos/secret'); ?>

Use the avatar upload function to upload your malicious PHP file. The message in the response confirms that this was uploaded successfully.

In Burp Repeater, change the path of the request to point to your PHP file:

GET /files/avatars/exploit.php HTTP/1.1

Send the request. Notice that the server has executed your script and returned its output (Carlos's secret) in the response.

Submit the secret to solve the lab.

Community solutions

Intigriti

Find file upload vulnerabilities using Burp Suite

Try for free
