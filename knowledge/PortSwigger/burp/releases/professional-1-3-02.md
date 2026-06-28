# Professional 1.3.02

Source: https://portswigger.net/burp/releases/professional-1-3-02
Fetched: 2026-06-28T09:16:22.958573+00:00

This release fixes a few minor bugs arising from version v1.3.01.

It also adds a facility to customise the preset payload lists that are included with Burp Intruder, and which are accessible via the "add from list" drop-down for various payload types. You can specify your own directory to hold payload lists, and these will automatically appear in the drop-down within Burp.

To access this feature, choose "configure preset payload lists" from the Intruder menu:

You can use the "copy" button to copy all of Burp's built-in payload lists into your custom directory, to use alongside your own payloads lists. You can then use your preferred text editor to modify any of the lists as required.

This release also adds a number of new built-in payload lists, including new fuzz strings and lists of interesting CGI files. These were kindly donated by Adam Muntner.
