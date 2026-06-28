# Professional 1.6.08

Source: https://portswigger.net/burp/releases/professional-1-6-08
Fetched: 2026-06-28T09:16:26.400974+00:00

This release contains various new features and enhancements:

The Scanner has been updated with the ability to detect cross-site request forgery (CSRF) vulnerabilities. We have held off reporting CSRF for a long time, because in our experience many scanners that attempt to automate this end up generating more heat than light. If a scanner generates too many false positives, then users lose faith in its output and start to ignore all of the issues it reports of that type. Because of this, we've worked hard to make our CSRF detection actually provide value to Burp users. We have deliberately erred on the side of reducing the number of false positives. The CSRF issues that Burp does report should all be worthy of manual investigation to determine whether the affected application functionality should be protected against CSRF attacks. We welcome real-world feedback about the performance of the new check, and we will aim to refine this further in future.

The Scanner logic for the detection of XSS and SQL injection vulnerabilities has been further enhanced.

Burp's use of temporary files has been updated to use a small number of large temporary files, rather than an individual file for each saved HTTP request and response. This change should resolve problems that some users have experienced with the operating system running out of open file handles, or even running out of file nodes within the temporary directory.

In the previous release, the Extender tool was modified so that its own configuration was not modified when an extension initiated a restore of a Burp state file. In this release, the same change has been made for the case where an extension initiates an update to Burp's configuration.

The maximum number of threads that can be configured for the Spider tool, and for an Intruder attack, has been increased to 999.

A hotkeyable action has been added to start the current Intruder attack. By default, no hotkey is assigned to this action, but one can be configured at Options / Misc / Hotkeys / Edit hotkeys.
