# Hackability inspector

Source: https://portswigger.net/research/hackability-inspector
Fetched: 2026-06-28T09:17:25.449145+00:00

Hackability inspector

Gareth Heyes

Researcher

@garethheyes

Published: Friday, 6 July 2018 at 12:30 UTC

Updated: Tuesday, 16 August 2022 at 09:43 UTC

I presented this research at AppSecEU, you can watch the video here:

You can download the slides here:

Exploiting unknown browsers and objects slides

We released Hackability a few months ago to enable researchers to probe unknown rendering engines using a series of tests. Hackability will also find interesting JavaScript objects but often Chrome devtools won’t be available to inspect such objects as the page is rendered without Chrome. We decided we needed a new tool focused on security to inspect JavaScript objects regardless of which rendering engine is used.

The inspector will enumerate any object by default and will attempt to find all properties using ES5/6 features and bruteforce. It will order the properties by most interesting using a list of known window properties to determine if the property is from the rendering engine or a user defined object.

When the object is enumerated it will do some checks on the property to see if it’s constructor is leaking a cross domain object which often leads to a same origin policy bypass, if you can set properties on a cross domain object, if the exception is leaking the cross domain origin, check if it’s a Java bridge and call getOwnPropertyDescriptor to retrieve information on if the property is configurable, enumerable and writable.

To use the inspector simply enter the object you wish to inspect in input box and hit return. Inspector will then show you the property name on the left and it’s value in the middle with extra information on its type on the right. Underneath the object will be the list of properties, you can enumerate these properties further by clicking the arrow. It’s possible to filter the list of properties by regex using the regex box, you can execute JavaScript on each of the properties using the js box “obj” will refer to the object in your JavaScript and “prop” will refer to the property. For example if you wanted to call every function on the object then you could do this: obj[prop](“My argument”). You can also filter each object by type using the select menu. The types filter allows you to filter by regular JavaScript types as well as window objects, cross domain window object, dom nodes, java bridges etc.

Like the Chrome devtools console you can cycle through your history using the up and down arrows. You can clear the console using Control+Backspace and clear your history using Control+Shift+Backspace. Inspector also supports HTML and if you hit Control+Enter JavaScript will be executed but not inspected (useful in multiline mode), if your command starts with a “<” character this will be detected as HTML input too.

All these options are available from the query string in case you are testing a client that doesn’t allow user interaction. The “input” parameter is the input you want to send to the inspector. “regex” parameter allows you to filter by regex, “js” parameter is the code you want to execute on every property and finally the “type” parameter allows you to filter the properties by type.

You might encounter a rendering engine that does not display the results to you. If you use the blind option as a query parameter. The inspector will render the HTML and store it so you can view it later. Simply send blind=1 as a query parameter to the inspector.

You can find a demo of Hackability inspector here but we encourage you to fork and host it on your own server.

Safari leaking origin

Whilst testing Safari with Hackability inspector for the __proto__ bug I found a new cross domain issue. When trying to access a x-domain object, Safari throws an exception and includes the origin of the frame, that discloses the location of any iframe on a different domain or any cross domain window.

The code looks like this:

var win = document.getElementById('iframe').contentWindow, regex;

try {

win.location.x;

} catch(e){

regex = /accessing a frame with origin "(.+?)"/.exec(e); if(regex) {

alert('frame is pointing to:'+regex[1]);

}

}

"win" contains a reference to a cross domain contentWindow from an iframe, accessing "x" throws an exception and the exception contains the origin of the iframe. If you read the length property of the contentWindow you can read every iframe origin on that window. The PoC below does that. subdomain1.portswigger-labs.net contains an iframe pointing to subdomain2.portswigger-labs.net and burpcollaborator.net, we can read the origins using the technique above.

PoC

Although the PoC above uses iframes, X-Frame-Options wouldn't save you because we could use popups instead see the PoC below.

PoC using popups

Hackability Inspector Shortcuts

Enter - Evaluate and inspect the input

Control + Return - Execute JS but don’t inspect and don’t return result

Shift + Return - Evaluate but don’t inspect the result

Control + Backspace - Clear the console

Control + Shift + Backspace - Clear console history

Up - Go backwards in history

Down - Go forwards in history

Up + Alt - Go backwards in history (used in multiline mode)

Down + Alt - Go forwards in history ( used in multiline mode)

Supported query parameters

input=Your input to be sent and evaluated in the console

interesting=true

regex=Filter properties of object by a regular expression

js=Execute JavaScript on every property. “obj” will refer to the object and “prop” will refer to the property.

type=Filter properties by type

blind=1

Examples

Pass input to the inspector

Only show interesting properties

Filter properties by regex

Execute js on every property

obj contains a reference to current enumerated object.

prop contains a string of the property name

Filter properties by type

The html parameter can be used to pass html

You can also pass html and then inspect it

Use the blind option to save a copy of the enumeration html when you can't see it's output

The results are stored here

Note you can't interact with this display but you can send multiple requests to determine an objects structure

You can combine all parameters

JavaScript

hacktools

inspector

hackability

Presentations

Back to all articles

Related Research

Exploiting prototype pollution in Node without the filesystem

23 March 2023

Exploiting prototype pollution in Node without the filesystem

The seventh way to call a JavaScript function without parentheses

12 September 2022

The seventh way to call a JavaScript function without parentheses

Browser-Powered Desync Attacks

10 August 2022

Browser-Powered Desync Attacks

Hunting evasive vulnerabilities

13 May 2022

Hunting evasive vulnerabilities
