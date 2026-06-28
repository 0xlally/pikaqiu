# Setting Java options

Source: https://portswigger.net/burp/documentation/desktop/troubleshooting/setting-java-options
Fetched: 2026-06-28T09:16:09.508336+00:00

Support Center

Documentation

Desktop editions

Troubleshooting

Setting Java options

ProfessionalCommunity Edition

Setting Java options

Last updated:

June 18, 2026

Read time:

1 Minute

You can use a user.vmoptions file to configure options for Burp's Java Virtual Machine (JVM). This enables you to resolve certain issues or customize your experience when using Burp Suite.

Unlike the default vmoptions file, the user.vmoptions file persists when you upgrade Burp Suite.

Note

You can only use the user.vmoptions file to configure standard Java options for the virtual machine that Burp Suite runs in, such as heap size and RAM usage. You can't use the file to configure any options for Burp Suite itself.

Creating a user.vmoptions file

To specify custom Java options, create a user.vmoptions file:

Open the directory that the vmoptions file is located in. The location of the file depends on your operating system:

For Windows / Linux, open the Burp Suite installation directory.

For MacOS, right-click on the Burp Suite icon, select Show Package Contents, and then open the Contents directory.

Copy and paste the default vmoptions file. This file is called either BurpSuitePro.vmoptions or BurpSuiteCommunity.vmoptions on Windows and Linux, and vmoptions.txt on Mac.

Rename the copied file to user.vmoptions.

Specifying options

To specify an option, add it to the user.vmoptions file on a new line. For example, the following configuration limits its maximum RAM to 50% of the total system memory:

-XX:MaxRAMPercentage=50
