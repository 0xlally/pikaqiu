# Lab: Clobbering DOM attributes to bypass HTML filters

Source: https://portswigger.net/web-security/dom-based/dom-clobbering/lab-dom-clobbering-attributes-to-bypass-html-filters
Fetched: 2026-06-28T09:17:48.581270+00:00

Web Security Academy

DOM-based

DOM clobbering

Lab

Lab: Clobbering DOM attributes to bypass HTML filters

This lab uses the HTMLJanitor library, which is vulnerable to DOM clobbering. To solve this lab, construct a vector that bypasses the filter and uses DOM clobbering to inject a vector that calls the print() function. You may need to use the exploit server in order to make your vector auto-execute in the victim's browser.

Note

The intended solution to this lab will not work in Firefox. We recommend using Chrome to complete this lab.

Solution

Go to one of the blog posts and create a comment containing the following HTML:

<form id=x tabindex=0 onfocus=print()><input id=attributes>

Go to the exploit server and add the following iframe to the body:

<iframe src=https://YOUR-LAB-ID.web-security-academy.net/post?postId=3 onload="setTimeout(()=>this.src=this.src+'#x',500)">

Remember to change the URL to contain your lab ID and make sure that the postId parameter matches the postId of the blog post into which you injected the HTML in the previous step.

Store the exploit and deliver it to the victim. The next time the page loads, the print() function is called.

The library uses the attributes property to filter HTML attributes. However, it is still possible to clobber the attributes property itself, causing the length to be undefined. This allows us to inject any attributes we want into the form element. In this case, we use the onfocus attribute to smuggle the print() function.

When the iframe is loaded, after a 500ms delay, it adds the #x fragment to the end of the page URL. The delay is necessary to make sure that the comment containing the injection is loaded before the JavaScript is executed. This causes the browser to focus on the element with the ID "x", which is the form we created inside the comment. The onfocus event handler then calls the print() function.

Find DOM-based vulnerabilities using Burp Suite

Try for free
