# Professional 1.3beta2

Source: https://portswigger.net/burp/releases/professional-1-3beta2
Fetched: 2026-06-28T09:16:23.578282+00:00

As well as various bugfixes, this release adds some handy conversion functions to the request/response editor, which are accessible via the context menu and shortcut keys. To use these, simply select the text you want to convert, and choose the relevant conversion:

Available conversions include URL-encoding, HTML-encoding and Base64-encoding. You can also convert raw data into a "constructed string" for various code-injection contexts. For example, selecting the expression:

xss

and choosing "JavaScript constructed string" will convert this to:

String.fromCharCode(120,115,115)

This release also improves Mac compatibility in the message viewer/editor. Keyboard shortcuts now work with both the Ctrl and Command keys. And you can display the context menu without losing the current text selection. If you're experiencing other Mac pain, do let me know.
