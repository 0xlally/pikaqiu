# Lab: Bypassing flawed input filters for server-side prototype pollution

Source: https://portswigger.net/web-security/prototype-pollution/server-side/lab-bypassing-flawed-input-filters-for-server-side-prototype-pollution
Fetched: 2026-06-28T09:17:58.969339+00:00

Web Security Academy

Prototype pollution

Server-side vulnerabilities

Lab

Lab: Bypassing flawed input filters for server-side prototype pollution

This lab is built on Node.js and the Express framework. It is vulnerable to server-side prototype pollution because it unsafely merges user-controllable input into a server-side JavaScript object.

To solve the lab:

Find a prototype pollution source that you can use to add arbitrary properties to the global Object.prototype.

Identify a gadget property that you can use to escalate your privileges.

Access the admin panel and delete the user carlos.

You can log in to your own account with the following credentials: wiener:peter

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

In the Response panel, switch to the Raw tab. Observe that the JSON indentation appears to be unaffected.

Modify the request to try polluting the prototype via the constructor property instead:

"constructor": {

"prototype": {

"json spaces":10

}

}

Resend the request.

In the Response panel, go to the Raw tab. This time, notice that the JSON indentation has increased based on the value of your injected property. This strongly suggests that you have successfully polluted the prototype.

Identify a gadget

Look at the additional properties in the response body.

Notice the isAdmin property, which is currently set to false.

Craft an exploit

Modify the request to try polluting the prototype with your own isAdmin property:

"constructor": {

"prototype": {

"isAdmin":true

}

}

Send the request. Notice that the isAdmin value in the response has been updated. This suggests that the object doesn't have its own isAdmin property, but has instead inherited it from the polluted prototype.

In the browser, refresh the page and confirm that you now have a link to access the admin panel.

Go to the admin panel and delete carlos to solve the lab.

Find prototype pollution vulnerabilities using Burp Suite

Try for free
