# Professional 1.6.02

Source: https://portswigger.net/burp/releases/professional-1-6-02
Fetched: 2026-06-28T09:16:26.679465+00:00

This release contains various bugfixes and minor enhancements:

A bug that caused certain HTML content to be wrongly inferred as JavaScript, with a knock-on effect on the Scanner's XSS checking logic, has been fixed.

A bug introduced in v1.6.01 affecting the passing through of command line arguments to extensions has been fixed.

A bug that sometimes caused session handling rules using macros to be incorrectly restored from state files, has been fixed

A bug that occasionally caused corruption in the rendering of live streaming responses has been fixed.

A bug where the "time of day" value in Intruder attack results was incorrectly reported when request throttling was enabled, has been fixed.

Logging options have been enabled for the Sequencer tool.

Links in the BApp details tab are now clickable and open in an external browser.

Renamable tab captions now prevent accidental renaming to an empty string, which previously resulted in a pixel-perfect double-click being required to rename the tab to anything else.

Efforts have been made to fix an occasional bug that causes the UI to freeze when changing the confidence or severity of Scanner issues. Feedback is welcomed on whether this bug has indeed gone away.
