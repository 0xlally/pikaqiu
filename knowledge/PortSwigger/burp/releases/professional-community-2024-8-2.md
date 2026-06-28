# Professional / Community 2024.8.2

Source: https://portswigger.net/burp/releases/professional-community-2024-8-2
Fetched: 2026-06-28T09:16:49.376165+00:00

This release introduces the ability to manually create issues, easier testing functionality for match and replace rules, and the option to save requests derived from an OpenAPI definition to the site map. It also includes a number of bug fixes.

Manually creating issues for reports

In Burp Suite Professional, you can now manually create issues for vulnerabilities discovered during your penetration testing. This enables you to include all identified vulnerabilities in your final report for a more comprehensive and customized overview of your findings.

Testing match and replace rules

You can now test your match and replace rules using the built-in test function in the match and replace rule editor. This enables you to more quickly and easily confirm that the string or regex pattern matches and replaces the intended text.

We've also made the match and replace rules more visible by adding a Proxy > Match and replace tab. This makes it easier to access and manage your rules.

Saving OpenAPI request to the site map

If Burp identifies an OpenAPI definition in a response, you can now save the derived requests to the site map. Burp supports versions 2.0 and 3.0.x of OpenAPI.

Bug fixes

We've fixed the following bugs:

When you access our documentation through Burp, embedded videos now play correctly.

When you use the search function in Logger, Burp now correctly displays all requests that contain the text entered in the search box.

The Organizer table now updates correctly when notes are added and the status of an entry is changed.

We've corrected the Issues table rendering to ensure proper display and functionality on secondary monitors, even with a large number of issues in the table.

We've fixed a bug in the recorded login editor that was causing the login process to fail during click events.

Resending or editing some messages caused them to become unintentionally modified.

Using the Send hotkey in Repeater didn't clear the response pane, making it harder to see when a new request was processed.

Multi-position Intruder attacks using simple payload lists unintentionally shared the same payload values.

Java update

We've updated Java from 21.0.3 to 21.0.4.
