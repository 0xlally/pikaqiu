# System requirements for standard instances

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/standard/standard-system-requirements
Fetched: 2026-06-28T09:15:33.858459+00:00

DAST

System requirements for standard instances

Last updated:

June 18, 2026

Read time:

4 Minutes

You can set up a standard instance of Burp Suite DAST either on-premise, or on cloud-hosted virtual machines.

The system requirements for Burp Suite DAST depend on several factors:

The number of concurrent scans you want to run.

The size and complexity of the applications you want to scan.

The number of issues expected.

The number of active Burp Suite DAST users in your organization.

The system requirements on this page ensure satisfactory performance for most use cases. However, you may need to use infrastructure with a higher specification to meet your particular needs.

Note

If you need help with the system requirements, please email our support team.

General requirements

Make sure you meet the following conditions:

The application is self-hosted in your own environment.

All the components are installed on machines with 64-bit architecture.

The disk location (configured during the installation process) must be locally attached storage rather than a network file system.

Please note that the values given for free space required (below) include space for data storage during updates and scans as well as the installation itself.

We recommend that you use dedicated server-class machines.

For production use, we recommend that you use an external database. To learn more, see External database requirements.

Supported operating systems

The following operating systems are supported:

Windows: 10, 11. Server 2016, 2019, 2022.

Linux: Most 64-bit distributions except CentOS/RHEL v7.x. We recommend the latest Ubuntu LTS release.

Note

For Linux, you may need to install packages to allow Burp's Chromium browser to run. The packages depend on the Linux distribution and operating system image you use.

For more information, please refer to our browser-powered scanning documentation or

email our support team.

Single-machine architecture

A single-machine architecture enables you to run up to five concurrent scans. In this setup, the DAST

server, web server, and scanning components are installed on a single machine.

Machine hardware requirements

The exact hardware requirements for your installation of Burp Suite DAST depends on the number of concurrent scans you want to run.

Note

In the specification tables below, CPU cores refers to the number of cores, not the number of CPUs or vCPUs.

Minimum specification

These are the minimum specifications for a single-machine architecture. They are suitable for smaller, more static scan targets with simple website interactions:

Concurrent scans

CPU cores

Ram (GB)

Free disk space (GB)

Swap space (Linux only)

1

4

16

30

18

2

6

20

50

22

3

8

24

70

26

4

10

28

90

30

5

12

32

110

34

Recommended specification

For larger, more dynamic scan targets with complex website interactions, we recommend the following specifications:

Concurrent scans

CPU cores

Ram (GB)

Free disk space (GB)

Swap space (Linux only)

1

8

24

30

26

2

12

28

50

30

3

16

36

70

38

4

20

44

90

46

5

24

52

110

54

AWS EC2 instance recommendations

For a single-machine architecture using an AWS EC2 instance, we recommend the following specifications:

Number of concurrent scans

Minimum

Recommended

1

c6i.2xlarge

c6i.4xlarge

5

c6i.8xlarge

c6i.12xlarge

Multi-machine architecture

A multi-machine architecture enables you to run more than five concurrent scans.

We recommend this method for production use.

Note

In the specification tables below, CPU cores refers to the number of cores, not the number of CPUs or vCPUs.

DAST server machine requirements

This is the specification for a dedicated DAST server machine, with no scanning components:

Specification

Minimum

Recommended

CPU cores

2

4

RAM (GB)

8

16

Free disk space (GB)

10

10

AWS EC2

c6i.xlarge

c6i.2xlarge

Scanning machine hardware requirements

The exact requirements for your installation of Burp Suite DAST depends on the number of concurrent scans you want to run.

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

AWS EC2 instance recommendations

If you want to deploy a scanning machine to an AWS EC2 instance, we recommend the following specifications:

Number of concurrent scans

Minimum

Recommended

1

c6i.xlarge

c6i.2xlarge

4

c6i.4xlarge

c6i.8xlarge

10

c6i.12xlarge

c6i.24xlarge

Next step - System requirements for external databases

CONTINUE
