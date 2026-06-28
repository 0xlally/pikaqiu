# Saving attacks

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/results/saving-attacks
Fetched: 2026-06-28T09:16:05.143671+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Results

Saving results

ProfessionalCommunity Edition

Saving attacks

Last updated:

June 18, 2026

Read time:

2 Minutes

Burp Intruder attacks are not saved by default, as they can result in large project files. In Burp Suite Professional, with the results window open, you can use the commands in the top-level Save menu to save various aspects of the attack:

Results table - Save the results table as a text file, which you can use for further analysis.

You can configure which rows and columns to save, and the delimiter. This means, for example, that you can save a single column to use as an input file for subsequent attacks.

Server responses - Save the full responses received for all requests. You can choose whether these are saved as sequentially numbered individual files, or sequentially concatenated into a single file.

Attack configuration - Save the configuration of the current attack as a file.

You can use a saved attack configuration with future attacks. Go to the top level Intruder menu and select Load attack config.

Project file - Save a complete copy of the attack configuration and results to the project file. This is only available for disk-based projects.

You can save the attack to your project file before, during, or after the attack. The state of the attack is saved from that point on.

If you close a saved attack, select Open saved attack in Burp's top-level Intruder menu to open it later.

Note

Intruder attacks can no longer be saved to state files. Legacy state files can still be loaded, by selecting Open saved attack from the top level Intruder menu.

Closing attacks

If you close a results window while an attack is in progress, you are prompted to either:

Let the attack carry on in the background.

Discard the attack.

If you close a results window once the attack is finished, you can also choose to save the attack to a project file (for disk-based projects in Burp Suite Professional) or keep the attack in memory.

You can specify a default answer for either prompt in Burp's Settings dialog. Click on Settings in the top toolbar and scroll down to Behavior

when closing result windows on the Intruder page.

Note

If you are missing information on the attack results table, you may have shut down Burp Suite while an attack was in progress, before the relevant requests could be sent.
