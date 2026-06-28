# The seventh way to call a JavaScript function without parentheses

Source: https://portswigger.net/research/the-seventh-way-to-call-a-javascript-function-without-parentheses
Fetched: 2026-06-28T09:17:29.942331+00:00

The seventh way to call a JavaScript function without parentheses

Gareth Heyes

Researcher

@garethheyes

Published: Monday, 12 September 2022 at 13:00 UTC

Updated: Sunday, 18 September 2022 at 17:20 UTC

I thought I knew all the ways to call functions without parentheses:

alert`1337`

throw onerror=alert,1337

Function`x${'alert\x281337\x29'}x```

'alert\x281337\x29'instanceof{[Symbol['hasInstance']]:eval}

valueOf=alert;window+''

x=new DOMMatrix;matrix=alert;x.a=1337;location='javascript'+':'+x

// or any DOMXSS sink such as location=name

In this post I'll show you yet another surprising way and help you understand how tagged template strings work. The techniques in this post don't directly enable exploitation, but they can be used to gain a greater understanding of the JavaScript language, providing a foundation for evasion of JavaScript sandboxes and WAFs. It all started with my post on Executing non-alphanumeric JavaScript without parentheses. I found that you could pass strings to tagged templates, tagged templates just means using a function prefixed before the template string literal. For example alert`123` is a tagged template that calls the alert function with 123. My realisation in the previous post was you could pass multiple arguments to those functions with just strings as the following code demonstrates:

function x(){

alert(arguments[0]);

alert(arguments[1]);

}

x`x${'ale'+'rt(1)'}x`

What happens here is all the strings get added as an array in the first argument and the second argument gets the string alert(1) but wait why does the string alert(1) get passed as a second argument to the function? Well, strings are treated differently than placeholders, a normal string without placeholders will get added to the first argument as an array whereas placeholders will get added as a new argument with their type. This last point is important, what I didn't realise at the time was that placeholders get added as an argument with their type not as a string! The following code demonstrates this:

function x(){

alert(arguments[0]);

arguments[1]('hello')

}

function y(str){

alert(str);

}

x`x${y}x`

Great this is cool behaviour, it means we can call functions and pass multiple arguments with any type. But we have a problem, when using strings in a tagged template they will always be added as the first argument, thus breaking functions that use the first argument. Our goal here is to call the function with an argument we choose. For instance we might want to call setTimeout because the first argument accepts a function or a string and the third argument calls that function with that value:

setTimeout(alert, 0, 'I get passed to alert')

Let's try calling setTimeout:

setTimeout`${alert}${0}${1}`//Uncaught SyntaxError: Unexpected token ','

We can see what is happening by using a custom function again:

function x(){

console.log(arguments);

}

x`${alert}${0}${1}`

So we can see the first argument contains an array of blank strings and another array at the end again full of blank strings. When setTimeout converts these arrays into a string we get a bunch of commas which causes a syntax error. Somehow we need the setTimeout function to ignore the first argument, how do you do that? Well, you can use setTimeout.call because the first argument will be the array which gets assigned to "this" of the setTimeout function and now alert will get passed as the first argument to the function but…

setTimeout.call`${alert}${0}${1}`//Illegal invocation

Damn because you are no longer calling the function directly, JavaScript will throw an exception preventing you from calling the function because "this" is no longer a window object. I thought game over, then I realised back in the past I've done some JS hacking with [].sort and others. They allow you to call functions without the illegal invocation error:

[].sort.call`${alert}1337`

You can of course use other functions such as eval and other array methods like map:

[].map.call`${eval}\\u{61}lert\x281337\x29`

I later discovered that you can use Reflect too:

The above uses the new navigation.navigate method in Chrome to cause a redirection with the payload coming from window.name. In order to call navigate you need to provide the correct "thisObject" to the function, this is done in the second argument to Reflect.apply. The window.name is used in the 3rd argument which has to be an array of arguments sent to the function. Using Reflect methods set and apply you can assign to pretty much any object or call any function! Note I'm using "window.name" to conceal a payload, normally the payload would come from another page or domain by passing it inside the "name" property of window which is passed across domains.

Conclusion

It's quite surprising that template strings support this behaviour and browsers allow you to use sort and other functions in this way. By hacking JavaScript you can learn new and interesting ways of abusing JavaScript features to produce unexpected results.

I hope and look forward to seeing someone finding the 8th way of executing JavaScript without parentheses!

JavaScript

no-parentheses

WAF

Back to all articles

Related Research

Bypassing WAFs with the phantom $Version cookie

04 December 2024

Bypassing WAFs with the phantom $Version cookie

Exploiting prototype pollution in Node without the filesystem

23 March 2023

Exploiting prototype pollution in Node without the filesystem

Evading defences using VueJS script gadgets

12 October 2020

Evading defences using VueJS script gadgets

Redefining Impossible: XSS without arbitrary JavaScript

23 September 2020

Redefining Impossible: XSS without arbitrary JavaScript
