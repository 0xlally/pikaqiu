# Professional / Community 1.7.06

Source: https://portswigger.net/burp/releases/professional-community-1-7-06
Fetched: 2026-06-28T09:16:31.164597+00:00

This release introduces a new scan check for second-order SQL injection vulnerabilities. In situations where Burp observes stored user input being returned in a response, Burp Scanner now performs its usual logic for detecting SQL injection, with payloads supplied at the input submission point, and evidence for a vulnerability detected at the input retrieval point.

The release also fixes a number of minor bugs.
