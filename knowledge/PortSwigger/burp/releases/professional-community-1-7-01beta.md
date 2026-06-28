# Professional / Community 1.7.01beta

Source: https://portswigger.net/burp/releases/professional-community-1-7-01beta
Fetched: 2026-06-28T09:16:30.735975+00:00

This release fixes a number of minor bugs:

A bug affecting the sending of some requests from Intruder to other tools when a disk-based project is being used.

A bug that could sometimes cause the SSL client certificates configuration UI to become corrupted when restoring settings that are not valid on the current machine.

A bug that could sometimes cause superfluous semicolons to be introduced into requests when manipulating cookie parameters via the API.

A bug that could very occasionally cause Burp Proxy's processing of HTTPS requests to stop working.

Although we are not aware of any significant bugs in version 1.7, this update is still officially a beta release, to allow more time for bugs to be identified.
