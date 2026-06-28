# DOM-based Ajax request-header manipulation

Source: https://portswigger.net/web-security/dom-based/ajax-request-header-manipulation
Fetched: 2026-06-28T09:17:48.088954+00:00

Web Security Academy

DOM-based

Ajax request-header manipulation

DOM-based Ajax request-header manipulation

In this section, we'll look at what DOM-based Ajax request-header manipulation is, talk about the potential impact of this kind of attack, and suggest ways to reduce your exposure to Ajax request-header manipulation vulnerabilities.

What is DOM-based Ajax request-header manipulation?

Using Ajax enables a website to make asynchronous requests to the server so that web applications can dynamically change content on the page without the need to reload the entire page. However, Ajax request-header manipulation vulnerabilities arise when a script writes attacker-controllable data into the request header of an Ajax request that is issued using an XmlHttpRequest object. An attacker may be able to use this vulnerability to construct a URL that, if visited by another user, will set an arbitrary header in the subsequent Ajax request. This can then be used as a starting point to chain together other kinds of attack, thereby increasing the potential severity of this vulnerability.

What is the impact of DOM-based Ajax request-header manipulation?

The potential impact of the vulnerability depends on the role of specific HTTP headers in the server-side processing of the Ajax request. If the header is used to control the behavior that results from the Ajax request, the attacker may be able to cause the user to perform unintended actions by manipulating the header. The impact also depends on what exactly the attacker is able to inject into the headers.

Which sinks can lead to DOM-based Ajax request-header manipulation vulnerabilities?

The following are some of the main sinks can lead to DOM-based Ajax request-header vulnerabilities:

XMLHttpRequest.setRequestHeader()

XMLHttpRequest.open()

XMLHttpRequest.send()

jQuery.globalEval()

$.globalEval()

How to prevent DOM-based Ajax request-header manipulation

In addition to the general measures described on the DOM-based vulnerabilities page, you should avoid allowing data from any untrusted source dynamically set Ajax request headers.

Find DOM-based vulnerabilities using Burp Suite

Try for free
