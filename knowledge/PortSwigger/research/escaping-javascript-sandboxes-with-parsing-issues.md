# Escaping JavaScript sandboxes with parsing issues

Source: https://portswigger.net/research/escaping-javascript-sandboxes-with-parsing-issues
Fetched: 2026-06-28T09:17:24.428503+00:00

Escaping JavaScript sandboxes with parsing issues

Gareth Heyes

Researcher

@garethheyes

Published: Friday, 10 July 2020 at 13:16 UTC

Updated: Tuesday, 8 September 2020 at 12:26 UTC

Parsing issues in sandboxes can lead to sandbox escapes and XSS on the target domain. Michał Bentkowski found issues in Caja (Google's JavaScript/HTML sandbox) that lead to XSS because the parser Caja used, parsed comments differently than the browser. If a JavaScript sandbox supported ES6 style Unicode escapes then you could bypass a theoretical sandbox using the techniques in this post:

\u{10ffdc}=''.sub;

typeof\u{10ffdc}['constructor']('alert(1)')()

It's been a while since we discovered an interesting JavaScript parsing issue. This time it's Safari and the way it handles Unicode escapes. There always seems to be a problem in handling Unicode escapes, probably because of how complex they are and how many different characters JavaScript allows as variables. To understand this problem let's look at how the browser interprets a Unicode escaped "a":

try {

\u0061

} catch(e){

alert(e);//ReferenceError: a is not defined

}

The Unicode escape is treated as character "a" and warns the variable "a" is not defined. Now, lets see what happens when we prefix an operator name like 'typeof'. Notice there is no space between the unicode escape and the typeof operator:

try {

typeof\u0061

} catch(e){

alert(e);//ReferenceError: typeofa is not defined

}

Here the code is treated like one variable "typeofa" rather than an operator and a variable.

Using this information we can now test Safari. We fuzzed all characters 0x00-0x10ffff to see how JavaScriptCore works with Unicode escapes and to our surprise it does not behave how the other JavaScript engines behave. Our fuzzing code found 721,520 inconsistently handled Unicode escapes! We'll show you one below

try {

typeof\u{10ffdc}// this returns "undefined"

} catch(e){

alert(e);// this is never called

}

There are two possibilities that you would expect to happen with the code above. 1) An exception would be thrown because \u{10ffdc} isn't a valid variable or 2) typeof\u{10ffdc} is treated as a variable and a reference error exception is thrown. But JavaScriptCore doesn't do either of those things. First it treats typeof as an operator and then the Unicode escape as a variable! So the parser has gone wrong here because if \u{10ffdc} is in fact a valid variable according to JavaScriptCore then a reference error should be thrown. We suspect that part of the parsing code thinks that "\u{10ffdc}" is not a variable therefore the typeof operator is parsed and then somewhere else "\u{10ffdc}" is accepted as a valid variable.

Finally to prove you can actually assign to this character, the following code executes on Safari but not any other browser:

\u{10ffdc}=alert;

typeof\u{10ffdc}(1)

This technique can be used as a sandbox escape if the JavaScript sandbox supports the ES6 style Unicode escapes. A parser might parse "typeof\u{10ffdc}" as an identifier/syntax error whereas Safari would treat those as an operator and an identifier. This could lead to a sandbox escape because the browser and the sandbox disagree on the parsed code and when this happens it is possible to fool the sandbox to execute different code that what was parsed as Bentkowski proved with Caja.

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
