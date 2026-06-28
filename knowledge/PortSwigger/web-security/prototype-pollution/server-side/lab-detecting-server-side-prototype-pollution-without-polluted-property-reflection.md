# Lab: Detecting server-side prototype pollution without polluted property reflection

Source: https://portswigger.net/web-security/prototype-pollution/server-side/lab-detecting-server-side-prototype-pollution-without-polluted-property-reflection
Fetched: 2026-06-28T09:18:00.997849+00:00

Web Security Academy

Prototype pollution

Server-side vulnerabilities

Lab

Lab: Detecting server-side prototype pollution without polluted property reflection

This lab is built on Node.js and the Express framework. It is vulnerable to server-side prototype pollution because it unsafely merges user-controllable input into a server-side JavaScript object.

To solve the lab, confirm the vulnerability by polluting Object.prototype in a way that triggers a noticeable but non-destructive change in the server's behavior. As this lab is designed to help you practice non-destructive detection techniques, you don't need to progress to exploitation.

You can log in to your own account with the following credentials: wiener:peter

Note

When testing for server-side prototype pollution, it's possible to break application functionality or even bring down the server completely. If this happens to your lab, you can manually restart the server using the button provided in the lab banner. Remember that you're unlikely to have this option when testing real websites, so you should always use caution.

Solution

Note

There are a variety of techniques for non-destructively probing for prototype pollution. We'll use the status code override technique for this example, but you can also solve the lab using the charset override or the json spaces override techniques.

Study the address change feature

Log in and visit your account page. Submit the form for updating your billing and delivery address.

In Burp, go to the Proxy > HTTP history tab and find the POST /my-account/change-address request.

Observe that when you submit the form, the data from the fields is sent to the server as JSON. Notice that the server responds with a JSON object that appears to represent your user. This has been updated to reflect your new address information.

Send the request to Burp Repeater.

In Repeater, add a new property to the JSON with the name __proto__, containing an object with an arbitrary property:

"__proto__": {

"foo":"bar"

}

Send the request. Observe that the object in the response does not reflect the injected property. However, this doesn't necessarily mean that the application isn't vulnerable to prototype pollution.

Identify a prototype pollution source

In the request, modify the JSON in a way that intentionally breaks the syntax. For example, delete a comma from the end of one of the lines.

Send the request. Observe that you receive an error response in which the body contains a JSON error object.

Notice that although you received a 500 error response, the error object contains a status property with the value 400.

In the request, make the following changes:

Fix the JSON syntax by reversing the changes that triggered the error.

Modify your injected property to try polluting the prototype with your own distinct status property. Remember that this must be between 400 and 599.

"__proto__": {

"status":555

}

Send the request and confirm that you receive the normal response containing your user object.

Intentionally break the JSON syntax again and reissue the request.

Notice that this time, although you triggered the same error, the status and statusCode properties in the JSON response match the arbitrary error code that you injected into Object.prototype. This strongly suggests that you have successfully polluted the prototype and the lab is solved.

Find prototype pollution vulnerabilities using Burp Suite

Try for free
