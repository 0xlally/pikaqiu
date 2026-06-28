# Professional 1.2.05

Source: https://portswigger.net/burp/releases/professional-1-2-05
Fetched: 2026-06-28T09:16:21.841489+00:00

Beta release containing a new text editor for raw HTTP requests and responses. The new editor has a number of enhancements:

Much faster display of large messages.

Colouring of request parameters and response syntax with minimal processing overhead.

Undo/redo.

Mouseover URL-decoding (in requests) and HTML-decoding (in responses).

Configurable font and text size.

The editor supports the following control keys:

Ctrl + A, select all

Ctrl + C, copy selected text

Ctrl + F, find and highlight the selected text throughout the message

Ctrl + V, paste

Ctrl + X, cut selected text

Ctrl + Y, redo last undone edit

Ctrl + Z, undo last edit

Ctrl + left, move to previous word

Ctrl + right, move to next word

Ctrl + up, move to previous paragraph

Ctrl + down, move to next paragraph

Ctrl + home, go to start of message

Ctrl + end, go to end of message

Ctrl + backspace, delete previous word

Ctrl + del, delete next word

Any feedback and suggestions much appreciated, particularly from users on less mainstream OS platforms.

This release also fixes a problem saving state when responses contain international characters, and addresses various other bugs.
