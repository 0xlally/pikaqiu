# DOM-based local file-path manipulation

Source: https://portswigger.net/web-security/dom-based/local-file-path-manipulation
Fetched: 2026-06-28T09:17:48.831417+00:00

Web Security Academy

DOM-based

Local file-path manipulation

DOM-based local file-path manipulation

In this section, we'll talk about what DOM-based local file-path manipulation is, look at the potential impact of an attack, highlight some of the sinks that can lead to this kind of vulnerability, and suggest ways that you can reduce your exposure.

What is DOM-based local file-path manipulation?

Local file-path manipulation vulnerabilities arise when a script passes attacker-controllable data to a file-handling API as the filename parameter. An attacker may be able to use this vulnerability to construct a URL that, if visited by another user, will cause the user's browser to open an arbitrary local file.

What is the impact of DOM-based local file-path manipulation?

The potential impact of this vulnerability depends on how the website uses the opened file:

If the website reads data from the file, the attacker may be able to retrieve this data.

If the website writes specific data to a sensitive file, the attacker may also be able write their own data to the file, which could be the configuration file of the operating system, for example.

In both of these cases, the actual exploitability of the potential vulnerability may depend on other suitable functionality being present on the website.

Which sinks can lead to DOM-based local file-path manipulation vulnerabilities?

The following are some of the main sinks can lead to DOM-based local file path manipulation vulnerabilities:

FileReader.readAsArrayBuffer()

FileReader.readAsBinaryString()

FileReader.readAsDataURL()

FileReader.readAsText()

FileReader.readAsFile()

FileReader.root.getFile()

How to prevent DOM-based local file-path manipulation vulnerabilities

In addition to the general measures described on the DOM-based vulnerabilities page, you should avoid allowing data from any untrusted source to dynamically pass a filename to a file-handling API.

Find DOM-based vulnerabilities using Burp Suite

Try for free
