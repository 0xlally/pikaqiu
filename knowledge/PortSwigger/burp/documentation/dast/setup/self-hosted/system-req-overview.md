# Burp Suite DAST system requirements

Source: https://portswigger.net/burp/documentation/dast/setup/self-hosted/system-req-overview
Fetched: 2026-06-28T09:15:33.687830+00:00

DAST

Burp Suite DAST system requirements

Last updated:

June 18, 2026

Read time:

1 Minute

The system requirements for Burp Suite DAST depend on several factors:

The number of concurrent scans you want to run.

The applications you want to scan.

The number of issues expected.

The number of active Burp Suite DAST users in your installation.

The system requirements that we recommend provide satisfactory performance for most use cases. However, you may need to use infrastructure with a higher specification to meet your particular needs.

For the best performance, we recommend you distribute scans across multiple scanning machines. If you need help with the system requirements, please email our support team.

The system requirements are specific to the deployment method you choose. For more information, see Which deployment method is right for me?.

For the system requirements relevant to your instance type, see the links below:

System requirements (standard instances)

Setting up an external database (standard instances)

System requirements (Kubernetes instances)

Setting up an external database (Kubernetes instances)

Concurrent scans

When you determine your system requirements, you need to consider the number of concurrent scans that you plan to run. In Burp Suite DAST, concurrent scans are the number of scans that you want to run at the same time. The links above explain how concurrent scans change your system requirements.
