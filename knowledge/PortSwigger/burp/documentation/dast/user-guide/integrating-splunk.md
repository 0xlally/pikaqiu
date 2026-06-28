# Integrating Burp Suite DAST with Splunk

Source: https://portswigger.net/burp/documentation/dast/user-guide/integrating-splunk
Fetched: 2026-06-28T09:15:37.312619+00:00

DAST

Integrating Burp Suite DAST with Splunk

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

If you or your teams use Splunk for your Security Information and Event Management (SIEM), you may like to integrate this with Burp Suite DAST.

Once configured, this enables you to stream issues directly to Splunk for advanced analysis, enabling real-time monitoring and event management.

Note

Cloud If you're a Cloud user, you need to use Splunk Cloud Platform and host on *.splunkcloud.com.

Prerequisites

You have access to Burp Suite DAST as an administrator.

You have access to Splunk as an administrator.

Configuring a connection to Splunk

To configure a connection to Splunk:

In Splunk:

Make a note of the URL where Splunk is hosted.

Create a new HTTP Event Collector token. Copy the Token Value.

Make a note of the HTTP Port Number. This is typically 8088.

In Burp Suite DAST, go to Settings and select Integrations.

Find the tile for Splunk and click Configure.

Enter the Splunk URL and HTTP Port Number in the Splunk URL field. For example, http://10.100.1.100:8088.

Enter the Splunk Token Value in Splunk token value.

Click Connect, and make a note of the name of the integration token that Burp Suite DAST sends to Splunk.

In Splunk, go to Search & Reporting and search for the integration token in the Event list.

Creating a new event type in Splunk

If you want to use the Vulnerabilities data model in the Splunk Common Information Model (CIM) add-on, you need to configure a new Event type in Splunk:

In your Splunk settings, create a new Event type.

Specify a search string for the Event type, in order to use the HTTP Event Collector token to filter events from Burp Suite DAST.

Enter a name for the Event type that enables you to identify issues sent by Burp Suite DAST.

Add the tags report and vulnerability to the Event type.

Save the Event type.

Disconnecting from Splunk

To disconnect from Splunk:

In Burp Suite DAST, Go to Settings and select Integrations.

Find the tile for Splunk and click Edit.

Click Disconnect Splunk and then click OK.
