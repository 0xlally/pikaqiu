# Professional / Community 2021.5

Source: https://portswigger.net/burp/releases/professional-community-2021-5
Fetched: 2026-06-28T09:16:35.439716+00:00

This release includes several improvements to Intruder, one of which allows you to save Intruder attacks to project files. The release also includes other minor Burp Suite improvements.

Persistable Intruder attacks

You can now save Intruder attacks to project files, so you can close Burp Suite and come back later to continue your attacks, or view the results of completed attacks. This is done on an opt-in basis: attacks are not saved by default, to avoid bloating project files. An attack can be saved before, during, or after it has been performed. The title bar of an attack window shows whether it has been saved or not.

We have made several other improvements to Intruder. These include:

Intruder attacks are now visible in the task list of the Dashboard. The Dashboard's task list can filter tasks to show only scans or only Intruder attacks, to allow a granular view of your running tasks.

Intruder attacks are no longer ended if the attack window is closed, and can be re-opened from the Dashboard's task list. This allows you to run multiple attacks in the background without needing to keep several windows open.

Intruder attacks are managed with resource pools in the same way as scans. Resource pools can be configured to limit the frequency of requests, so as not to overload network resources or the target.

Saving attacks to project files means that you no longer need to use the old way of saving Intruder attacks to a file, although legacy files can still be loaded into Burp Suite.

Chromium version update and security fix

We have updated Burp Suite's embedded browser to Chromium version 90.0.4430.93, which fixes several security issues that Google has classified as high.

TTL value for DNS records in Burp Collaborator

You can now optionally supply a specific TTL value when configuring custom DNS records in Burp Collaborator. You can read more here.
