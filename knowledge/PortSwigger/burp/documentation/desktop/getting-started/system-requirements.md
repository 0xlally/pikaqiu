# Burp Suite system requirements

Source: https://portswigger.net/burp/documentation/desktop/getting-started/system-requirements
Fetched: 2026-06-28T09:15:50.611486+00:00

Support Center

Documentation

Desktop editions

Getting started

System requirements

ProfessionalCommunity Edition

Burp Suite system requirements

Last updated:

June 18, 2026

Read time:

2 Minutes

The system requirements for Burp Suite are largely dependent on your intended use for the software. While you can generally perform most tasks on a relatively low-spec machine, some use cases (for example, running multiple scans concurrently) may require significantly more power to run without a noticeable effect on performance.

CPU cores / memory

Minimum: 2x cores, 4GB RAM - This spec is suitable for basic tasks such as proxying web traffic and simple Intruder attacks. While Burp Suite may run on a machine with a lower specification than this, we do not recommend doing so for performance reasons.

Recommended: 2x cores, 16GB RAM - This is a good general-purpose spec.

Advanced: 4x cores, 32GB RAM - This spec is suitable for more intensive tasks, such as complex Intruder attacks or large automated scans.

Free disk space

Basic installation: 1GB

Per project file: 2GB

Note:

While 2GB is the recommended minimum free disk space for a project, note that project files can get significantly larger than this (potentially up to many tens of GB), depending on factors such as the amount of proxy history included, the number of scans run, and the number of Repeater tabs open.

Operating system and architecture

Burp Suite supports the latest versions of the following operating systems:

Windows (Intel 64-bit)

Linux (Intel and ARM 64-bit)

OS X (Intel 64-bit and Apple M1)

Embedded browser

Burp's browser has some additional operating system and architecture requirements. It is not compatible with the following:

Older versions of Windows, including Windows 7, Windows 8/8.1, Windows Server 2012, and Windows Server 2012 R2.

Instances of Burp Suite that run via the JAR file on Apple Silicon and ARM 64-bit based systems. If you want to use Burp's browser on systems with these chip sets, make sure that you install Burp using the native platform installers.

Note

You can still run multiple instances of Burp simultaneously when using the platform installer versions. This functionality is not limited to instances of Burp run from the JAR file.
