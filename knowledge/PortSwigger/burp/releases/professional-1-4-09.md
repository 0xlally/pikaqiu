# Professional 1.4.09

Source: https://portswigger.net/burp/releases/professional-1-4-09
Fetched: 2026-06-28T09:16:24.463765+00:00

This release fixes a few bugs arising from last week's beta release, notably:

The "double paste" problem affecting the HTTP message editor.

The failure of cut/copy/paste to work at all in some text fields.

Occasional UI freeze when (un)pausing the active scanner.

Also, some Mac users noticed that non-OSX look and feels use the Control key as the command modifier, and do not recognize the Command key. I've applied a workaround so that the Command key should always work on OSX, regardless of the look and feel.
