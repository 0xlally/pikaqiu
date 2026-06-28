# Client-side template injection

Source: https://portswigger.net/web-security/cross-site-scripting/contexts/client-side-template-injection
Fetched: 2026-06-28T09:17:43.907592+00:00

Web Security Academy

Cross-site scripting

Contexts

Client-side template injection

Client-side template injection

In this section, we'll look at client-side template injection vulnerabilities and how you can exploit them for XSS attacks. This attack technique was pioneered by our research team - read more in XSS without HTML: Client-Side Template

Injection with AngularJS. Although client-side template injection is a generic issue, we'll focus on examples from the AngularJS framework as this is the most common. We'll describe how you can craft exploits that escape from the AngularJS sandbox, and how you can potentially use AngularJS features to bypass content security policy (CSP).

What is client-side template injection?

Client-side template injection vulnerabilities arise when applications using a client-side template framework dynamically embed user input in web pages. When rendering a page, the framework scans it for template expressions and executes any that it encounters. An attacker can exploit this by supplying a malicious template expression that launches a cross-site scripting (XSS) attack.

What is the AngularJS sandbox?

The AngularJS sandbox is a mechanism that prevents access to potentially dangerous objects, such as window or document, in AngularJS template expressions. It also prevents access to potentially dangerous properties, such as __proto__. Despite not being considered a security boundary by the AngularJS team, the wider developer community generally thinks otherwise. Although bypassing the sandbox was initially challenging, security researchers have discovered numerous ways of doing so. As a result, it was eventually removed from AngularJS in version 1.6. However, many legacy applications still use older versions of AngularJS and may be vulnerable as a result.

How does the AngularJS sandbox work?

The sandbox works by parsing an expression, rewriting the JavaScript, and then using various functions to test whether the rewritten code contains any dangerous objects. For example, the ensureSafeObject() function checks whether a given object references itself. This is one way to detect the window object, for example. The Function constructor is detected in roughly the same way, by checking whether the constructor property references itself.

The ensureSafeMemberName() function checks each property access of the object and, if it contains dangerous properties such as __proto__ or __lookupGetter__, the object will be blocked. The ensureSafeFunction()function prevents call(), apply(), bind(), or constructor() from being called.

You can see the sandbox in action for yourself by visiting this fiddle and setting a breakpoint at line 13275 of the angular.js file. The variable fnString contains your rewritten code, so you can look at how AngularJS transforms it.

How does an AngularJS sandbox escape work?

A sandbox escape involves tricking the sandbox into thinking the malicious expression is benign. The most well-known escape uses the modified charAt() function globally within an expression:

'a'.constructor.prototype.charAt=[].join

When it was initially discovered, AngularJS did not prevent this modification. The attack works by overwriting the function using the [].join method, which causes the charAt() function to return all the characters sent to it, rather than a specific single character. Due to the logic of the isIdent() function in AngularJS, it compares what it thinks is a single character against multiple characters. As the first character of the longer string are within the range of the compared characters, the isIdent() function always returns true, as demonstrated by the following example:

isIdent = function(ch) {

return ('a' <= ch && ch <= 'z' || 'A' <= ch && ch <= 'Z' || '_' === ch || ch === '$');

}

isIdent('x9=9a9l9e9r9t9(919)')

Once the isIdent() function is fooled, you can inject malicious JavaScript. For example, an expression such as $eval('x=alert(1)') would be allowed because AngularJS treats every character as an identifier. Note that we need to use AngularJS's $eval() function because overwriting the charAt() function will only take effect once the sandboxed code is executed. This technique would then bypass the sandbox and allow arbitrary JavaScript execution.

PortSwigger Research broke the AngularJS sandbox comprehensively, multiple times.

Constructing an advanced AngularJS sandbox escape

So you've learned how a basic sandbox escape works, but you may encounter sites that are more restrictive with which characters they allow. For example, a site may prevent you from using double or single quotes. In this situation, you need to use functions such as String.fromCharCode() to generate your characters. Although AngularJS prevents access to the String constructor within an expression, you can get round this by using the constructor property of a string instead. This obviously requires a string, so to construct an attack like this, you would need to find a way of creating a string without using single or double quotes.

In a standard sandbox escape, you would use $eval() to execute your JavaScript payload, but in the lab below, the $eval() function is undefined. Fortunately, we can use the orderBy filter instead. The typical syntax of an orderBy filter is as follows:

[123]|orderBy:'Some string'

Note that the | operator has a different meaning than in JavaScript. Normally, this is a bitwise OR operation, but in AngularJS it indicates a filter operation. In the code above, we are sending the array [123] on the left to the orderBy filter on the right. The colon signifies an argument to send to the filter, which in this case is a string. The orderBy filter is normally used to sort an object, but it also accepts an expression, which means we can use it to pass a payload.

You should now have all the tools you need to tackle the next lab.

How does an AngularJS CSP bypass work?

Content security policy (CSP) bypasses work in a similar way to standard sandbox escapes, but usually involve some HTML injection. When the CSP mode is active in AngularJS, it parses template expressions differently and avoids using the Function constructor. This means the standard sandbox escape described above will no longer work.

Depending on the specific policy, the CSP will block JavaScript events. However, AngularJS defines its own events that can be used instead. When inside an event, AngularJS defines a special $event object, which simply references the browser event object. You can use this object to perform a CSP bypass. On Chrome, there is a special property on the $event/event object called path. This property contains an array of objects that causes the event to be executed. The last property is always the window object, which we can use to perform a sandbox escape. By passing this array to the orderBy filter, we can enumerate the array and use the last element (the window object) to execute a global function, such as alert(). The following code demonstrates this:

<input autofocus ng-focus="$event.path|orderBy:'[].constructor.from([1],alert)'">

Notice that the from() function is used, which allows you to convert an object to an array and call a given function (specified in the second argument) on every element of that array. In this case, we are calling the alert() function. We cannot call the function directly because the AngularJS sandbox would parse the code and detect that the window object is being used to call a function. Using the from() function instead effectively hides the window object from the sandbox, allowing us to inject malicious code.

PortSwigger Research created a CSP bypass using AngularJS in 56 characters using this technique.

Bypassing a CSP with an AngularJS sandbox escape

This next lab employs a length restriction, so the above vector will not work. In order to exploit the lab, you need to think of various ways of hiding the window object from the AngularJS sandbox. One way of doing this is to use the array.map() function as follows:

[1].map(alert)

map() accepts a function as an argument and will call it for each item in the array. This will bypass the sandbox because the reference to the alert() function is being used without explicitly referencing the window. To solve the lab, try various ways of executing alert() without triggering AngularJS's window detection.

How to prevent client-side template injection vulnerabilities

To prevent client-side template injection vulnerabilities, avoid using untrusted user input to generate templates or expressions. If this is not practical, consider filtering out template expression syntax from user input prior to embedding it within client-side templates.

Note that HTML-encoding is not sufficient to prevent client-side template injection attacks, because frameworks perform an HTML-decode of relevant content prior to locating and executing template expressions.

Find XSS vulnerabilities using Burp Suite

Try for free
