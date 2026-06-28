# Bypassing Signature-Based XSS Filters: Modifying Script Code

Source: https://portswigger.net/support/bypassing-signature-based-xss-filters-modifying-script-code
Fetched: 2026-06-28T09:17:34.401350+00:00

This page may be out of date

We haven't updated it for a while because we're busy working on new, improved content to help you get the

most out of Burp Suite. In the meantime, please note that the information on this page may no longer be

accurate.

Visit our Support Center

Bypassing Signature-Based XSS Filters: Modifying Script Code

In some situations, you will find a way to manipulate reflected input to introduce a script context into the application's response. However, various other obstacles may prevent you from executing the code you need to deliver an actual attack. Some filters you may encounter seek to block the use of certain JavaScript keywords and other expressions. They may also block useful characters such as quotes, brackets, and dots. In this scenario, you can use numerous techniques to modify your desired script code to bypass common input filters.

Using JavaScript Escaping

JavaScript allows various kinds of escaping, which you can use to avoid including required expressions in their literal form.

Unicode escapes can be used to represent characters within JavaScript keywords, allowing an attacker to bypass many kinds of filters.

If you can make use of the eval command, possibly by using the preceding technique to escape some of its characters, you can execute other commands by passing them to the eval command in string form.

This allows you to use various string manipulation techniques to hide the command you are executing.

Within JavaScript strings, you can use Unicode escapes, hexadecimal escapes, and octal escapes.

Furthermore, superfluous escape characters within strings are ignored.

You can use sites such as Hackvector to help convert your payloads before testing them in your browser's web console.

Dynamically Constructing Strings

You can use other techniques to dynamically construct strings to use in your attacks, for example:

<script>eval('al'+'ert(1)');</script>

In the screenshot, the payload:

eval(atob('amF2YXNjcmlwdDphbGVydCgxKQ'));

is being tested in the Firefox web console.

The console allows a tester to run and execute arbitrary JavaScript.

This example allows you to decode a Base64-encoded command before it is passed to eval.

Alternatives to eval

If direct calls to the eval command are not possible, there are other methods you can use to execute commands in string form:

'alert(1)'.replace(/.+/,eval)

Avoiding dots

If the dot character is being blocked, you can use other methods to perform your attack:

alert(document['cookie'])

Combining multiple techniques

The techniques described so far can often be used in combination to apply several layers of obfuscation to your attack.

Furthermore, in cases where JavaScript is being used within an HTML tag attribute, you can combine these techniques with HTML encoding.

In this example the "e" character in "alert" has been escaped using Unicode escaping, and the backslash used in the Unicode escape has been HTML-encoded:

<img onerror=eval('al&#x5c;u0065rt(1)') src=a>
