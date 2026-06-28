# Editing attacks

Source: https://portswigger.net/burp/documentation/desktop/tools/intruder/results/editing-attacks
Fetched: 2026-06-28T09:16:04.760773+00:00

Support Center

Documentation

Desktop editions

Tools

Intruder

Results

Editing attacks

ProfessionalCommunity Edition

Editing attacks

Last updated:

June 18, 2026

Read time:

1 Minute

You can monitor and control the attack while it's running in the results window. You have the following options:

To pause the attack, click .

To resume the attack, click .

To restart the attack, click Attack, then select Repeat from the drop-down menu. This is especially useful after refining your attack configuration based on the initial results.

You can adjust most aspects of the attack configuration in the results window side panel, except for elements that are fundamental to the attack structure. This includes:

The attack type.

The payload positions.

The payload type.

To change these fundamental aspects of the configuration, return to the original Intruder tab and start a new attack.

Note

We recommend that you pause attacks before you modify your configuration. Changing the configuration while the attack is running may have unanticipated impacts, as changes will execute as each key is pressed.

For example, if you are using the Numbers payload type and delete a digit from the To field, the attack may abruptly complete because the To field now contains a smaller number.

Related pages

For information on how to save and close an attack, see Saving attacks.
