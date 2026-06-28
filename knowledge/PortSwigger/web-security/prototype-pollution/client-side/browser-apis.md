# Prototype pollution via browser APIs

Source: https://portswigger.net/web-security/prototype-pollution/client-side/browser-apis
Fetched: 2026-06-28T09:17:58.381703+00:00

Web Security Academy

Prototype pollution

Client-side vulnerabilities

Browser APIs

Prototype pollution via browser APIs

You may be surprised to learn that there are a number of widespread prototype pollution gadgets in the JavaScript APIs commonly provided in browsers. In this section, we'll show you how to exploit these for DOM XSS, potentially bypassing flawed prototype pollution defenses implemented by developers.

PortSwigger research

The labs in this section are based on original PortSwigger research. For a technical insight into how we were able to discover these gadgets and more using DOM Invader, check out the related blog post.

Widespread prototype pollution gadgets by Gareth Heyes

Prototype pollution via fetch()

The Fetch API provides a simple way for developers to trigger HTTP requests using JavaScript. The fetch() method accepts two arguments:

The URL to which you want to send the request.

An options object that lets you to control parts of the request, such as the method, headers, body parameters, and so on.

The following is an example of how you might send a POST request using fetch():

fetch('https://normal-website.com/my-account/change-email', {

method: 'POST',

body: 'user=carlos&email=carlos%40ginandjuice.shop'

})

As you can see, we've explicitly defined method and body properties, but there are a number of other possible properties that we've left undefined. In this case, if an attacker can find a suitable source, they could potentially pollute Object.prototype with their own headers property. This may then be inherited by the options object passed into fetch() and subsequently used to generate the request.

This can lead to a number of issues. For example, the following code is potentially vulnerable to DOM XSS via prototype pollution:

fetch('/my-products.json',{method:"GET"})

.then((response) => response.json())

.then((data) => {

let username = data['x-username'];

let message = document.querySelector('.message');

if(username) {

message.innerHTML = `My products. Logged in as <b>${username}</b>`;

}

let productList = document.querySelector('ul.products');

for(let product of data) {

let product = document.createElement('li');

product.append(product.name);

productList.append(product);

}

})

.catch(console.error);

To exploit this, an attacker could pollute Object.prototype with a headers property containing a malicious x-username header as follows:

?__proto__[headers][x-username]=<img/src/onerror=alert(1)>

Let's assume that server-side, this header is used to set the value of the x-username property in the returned JSON file. In the vulnerable client-side code above, this is then assigned to the username variable, which is later passed into the innerHTML sink, resulting in DOM XSS.

Note

You can use this technique to control any undefined properties of the options object passed to fetch(). This may enable you to add a malicious body to the request, for example.

Prototype pollution via Object.defineProperty()

Developers with some knowledge of prototype pollution may attempt to block potential gadgets by using the Object.defineProperty() method. This enables you to set a non-configurable, non-writable property directly on the affected object as follows:

Object.defineProperty(vulnerableObject, 'gadgetProperty', {

configurable: false,

writable: false

})

This may initially seem like a reasonable mitigation attempt as this prevents the vulnerable object from inheriting a malicious version of the gadget property via the prototype chain. However, this approach is inherently flawed.

Just like the fetch() method we looked at earlier, Object.defineProperty() accepts an options object, known as a "descriptor". You can see this in the example above. Among other things, developers can use this descriptor object to set an initial value for the property that's being defined. However, if the only reason that they're defining this property is to protect against prototype pollution, they might not bother setting a value at all.

In this case, an attacker may be able to bypass this defense by polluting Object.prototype with a malicious value property. If this is inherited by the descriptor object passed to Object.defineProperty(), the attacker-controlled value may be assigned to the gadget property after all.

What next?

JavaScript is now commonly used to build back-end functionality. Naturally, this means that prototype pollution can also occur in server-side contexts. In the next section, you'll learn how to safely detect and exploit these vulnerabilities in applications running on Node.js.

LABS Server-side prototype pollution

Find prototype pollution vulnerabilities using Burp Suite

Try for free
