# Exposing Intranets with reliable Browser-based Port scanning

Source: https://portswigger.net/research/exposing-intranets-with-reliable-browser-based-port-scanning
Fetched: 2026-06-28T09:17:24.781736+00:00

Exposing Intranets with reliable Browser-based Port scanning

Gareth Heyes

Researcher

@garethheyes

Published: Friday, 9 November 2018 at 14:47 UTC

Updated: Friday, 9 November 2018 at 14:47 UTC

In this blog post I describe how I created a port scanner using JavaScript. If you are just interested in the tool you can get it here:

Port scanner proof of concept

Scanning for ports on Chrome

There have been a few articles in the past about doing port scanning from the Internet zone to the Intranet zone. Jeremiah Grossman wrote about port scanning without JavaScript using link elements and timings in the past and Berend Jan Wever (Skylined) wrote a lan scanner that uses timing attacks too along with WebRTC and XHR. Both used timings and so they are not 100% accurate. I think I've come up with a technique that is more reliable but scans for mostly web servers.

Whilst testing a web application that uses a browser to render user supplied content in a restricted environment. I was looking for ways to extract information about the services running on a given IP. Chrome was my target because the web application was using that. I noticed some interesting behaviour when Chrome gets a connection refused for a port that isn't being used by the host. It displays a message to the user but also and this is the interesting bit, it changes the actual url to chrome-error://chromewebdata/.

When you make a request using an iframe to a port that doesn't exist on the server you get a successful onload event even though the port doesn't have anything listening on it. If the port does have a server listening it will also have a successful onload event, Chrome probably does this to prevent you from knowing if the port is open or not. I can use this behaviour to my advantage, I came up with a technique to use iframe onload events to determine if the port is open.

If you first load the url and capture the onload event and increment a counter and then make the same request again but this time with a # because the url has changed to chrome-error: instead of the original url you'll get a second onload event because the url has changed. If it has a web server listening you'll only get one onload event because the second url contains a hash and the browser doesn't reload the page when a hash is sent to an existing already loaded page.

To construct a port scanner, I first created an iframe and anchor element. The anchor element will be used to perform the click to the # url. I then need to assign the iframe name and anchor target to the same value so the click is performed on the iframe not the top document:

iframe.name = a.target = 'probe'+Date.now();

Then I need to set the iframe url and the anchor href to the target:

iframe.src = url + ":" + pos;

a.href = iframe.src + '#';

The iframe requires an onload and I need a timer when a valid port is encountered because we only get one onload event for the valid port and we need to move onto the next test:

iframe.onload = function(){

calls++;

if(calls > 1) {

clearTimeout(timer);

next();

return;

}

a.click();

};

timer = setTimeout(function(){

validPorts.push(pos);

next();

}, 5000);

That's the main basis of the technique and you can use this to scan any host for web servers including local IP's.

Note: X-Frame-Options with deny on the latest version of Chrome changes the url so this would be detected as a closed port by the tool.

Scanning for ports on Firefox

I looked into using the same technique with Firefox but it turned out to be even easier than that. Firefox fires an onload event for valid web servers but not for connection refused so it's dead easy to find them without having to automatically click a link. Simply see if the onload event is fired or timeout for when it's not. Firefox also allows you to create a large amount of iframes without a performance impact.

This time I use a pool of iframes instead of a single one that I used for Chrome. Firefox allows lots of iframes so I use 1000.

var id = 'iframe'+(pos%1000),

iframe = document.getElementById(id) ? document.getElementById(id) : document.createElement('iframe'), timer;

Then I simply use the onload event to determine if it's valid web server or not:

iframe.onload = function(){

validPorts.push(pos);

clearTimeout(timer);

next();

};

The Firefox version is super fast and more powerful then the others because it allows you to scan even invalid responses. This allows you to detect other services such as Redis servers for example.

Scanning for ports on Edge

The Edge version of the scanner was the opposite of the Chrome version, so if there's a valid port then the url will change to the error page causing an onload event to fire but if it's an invalid port then only the hash will change and an onload event won't be fired.

iframe.onload = function(){

calls++;

if(calls > 1) {

validPorts.push(currentPos);

return;

}

var a = document.createElement('a');

a.href = 'ms-appx-web://microsoft.microsoftedge/assets/errorpages/dnserror.html#123';

a.target = iframe.name;

a.click();

a = null;

if(calls === 1) {

next();

}

};

I combined all the techniques above into one tool which I wrote in lovely asynchronous JavaScript. You can find the tool here:

Port scanner proof of concept

Back to all articles

Related Research

05 February 2026

06 January 2026

The Fragile Lock:

Novel Bypasses For SAML Authentication

10 December 2025

The Fragile Lock:

Novel Bypasses For SAML Authentication

Introducing HTTP Anomaly Rank

11 November 2025

Introducing HTTP Anomaly Rank
