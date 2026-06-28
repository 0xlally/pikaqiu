# Professional / Community 2022.9.1

Source: https://portswigger.net/burp/releases/professional-community-2022-9-1
Fetched: 2026-06-28T09:16:39.642113+00:00

This release provides an upgrade for Burp's browser and some bug fixes.

Browser upgrade

We have upgraded Burp's browser to Chromium 105.0.5195.125, which patches a number of high-severity security issues.

Bug fixes

We have also fixed some minor bugs, including:

Previously, you could still use the Collaborator client to generate payloads and poll manually even if the Collaborator was disabled in the project options. We have now amended this so that disabling the Collaborator disables all of the Collaborator client's functions.

We have fixed a bug whereby disabling the Collaborator did not stop the Collaborator client from polling for payloads that had already been created.

We have fixed a performance issue with the Montoya API that was causing Burp to run slowly when an extension was writing a significant amount of data to its output stream.

We have fixed an issue with the Montoya API that was causing the Param Miner BApp to send a reduced number of requests and omit payloads when running a brute force attack

We have fixed an issue with the Montoya API whereby installing BApps could cause the Site Map to run very slowly when navigating between different elements.
