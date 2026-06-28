# DOM-based open redirection

Source: https://portswigger.net/web-security/dom-based/open-redirection
Fetched: 2026-06-28T09:17:49.160457+00:00

Web Security Academy

DOM-based

Open redirection

DOM-based open redirection

In this section, we'll talk about what DOM-based open redirection is, demonstrate how an attack is constructed, and suggest ways to reduce your exposure to DOM-based open-redirection vulnerabilities.

What is DOM-based open redirection?

DOM-based open-redirection vulnerabilities arise when a script writes attacker-controllable data into a sink that can trigger cross-domain navigation. For example, the following code is vulnerable due to the unsafe way it handles the location.hash property:

let url = /https?:\/\/.+/.exec(location.hash);

if (url) {

location = url[0];

}

An attacker may be able to use this vulnerability to construct a URL that, if visited by another user, will cause a redirection to an arbitrary external domain.

What is the impact of DOM-based open redirection?

This behavior can be leveraged to facilitate phishing attacks against users of the website, for example. The ability to use an authentic application URL targeting the correct domain and with a valid TLS certificate (if TLS is used) lends credibility to the phishing attack because many users, even if they verify these features, will not notice the subsequent redirection to a different domain.

If an attacker is able to control the start of the string that is passed to the redirection API, then it may be possible to escalate this vulnerability into a JavaScript injection attack. An attacker could construct a URL with the javascript: pseudo-protocol to execute arbitrary code when the URL is processed by the browser.

Which sinks can lead to DOM-based open-redirection vulnerabilities?

The following are some of the main sinks can lead to DOM-based open-redirection vulnerabilities:

location

location.host

location.hostname

location.href

location.pathname

location.search

location.protocol

location.assign()

location.replace()

open()

element.srcdoc

XMLHttpRequest.open()

XMLHttpRequest.send()

jQuery.ajax()

$.ajax()

How to prevent DOM-based open-redirection vulnerabilities

In addition to the general measures described in the DOM-vulnerabilities topic, you should avoid dynamically setting redirection targets using data that originated from any untrusted source.

Read more

URL validation bypass cheat sheet

Find DOM-based vulnerabilities using Burp Suite

Try for free
