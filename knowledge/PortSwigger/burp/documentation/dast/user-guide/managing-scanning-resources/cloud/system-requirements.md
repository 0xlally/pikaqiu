# System requirements for self-hosted scanning machines

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-scanning-resources/cloud/system-requirements
Fetched: 2026-06-28T09:15:37.629351+00:00

DAST

System requirements for self-hosted scanning machines

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

This page specifies the system requirements for self-hosted scanning machines, using a Cloud instance of Burp Suite DAST.

The system requirements depend on several factors:

The number of concurrent scans you want to run.

The size and complexity of the applications you want to scan.

The number of issues expected.

The number of active Burp Suite DAST users in your organization.

In most use cases, the system requirements on this page support satisfactory performance. However, you may need to

use infrastructure with a higher specification to meet your particular needs.

Note

These instructions only apply to Cloud instances of Burp Suite DAST. If you're looking

for system requirements for a self-hosted instance of Burp Suite DAST, see Burp

Suite Burp Suite DAST system requirements.

If you need help with the system requirements, please email our support team.

General requirements

Make sure you meet the following conditions:

The application is self-hosted in your own environment.

All the components are installed on machines with 64-bit architecture.

We recommend that you use dedicated server-class machines.

Supported operating systems

The following operating systems are supported:

Windows: 10, 11. Server 2016, 2019, 2022.

Linux: Most 64-bit distributions except CentOS/RHEL v7.x. We recommend the latest Ubuntu LTS release.

Note

For Linux, you may need to install packages to allow Burp's Chromium browser to run. The packages depend on the Linux distribution and operating system image you use.

For more information, please refer to our browser-powered scanning documentation or email our support team.

Minimum specification

These are the minimum specifications required for your scanning machines. They are suitable for smaller, more static scan targets with simple website interactions:

Concurrent scans

CPU cores

Ram (GB)

Free disk space (GB)

Swap space (Linux only)

1

2

4

30

6

2

4

8

50

10

3

6

12

70

14

4

8

16

90

18

5

10

20

110

22

10

20

40

210

42

Recommended specification

For larger, more dynamic scan targets with complex website interactions, we recommend the following specifications:

Concurrent scans

CPU cores

Ram (GB)

Free disk space (GB)

Swap space (Linux only)

1

4

8

30

10

2

8

16

50

18

3

12

24

70

26

4

16

32

90

34

5

20

40

110

42

10

40

80

210

82

Related pages

Network and firewall settings for self-hosted scanning machines
