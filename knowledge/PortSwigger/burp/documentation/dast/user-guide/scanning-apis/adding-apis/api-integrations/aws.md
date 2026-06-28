# Integrating with AWS

Source: https://portswigger.net/burp/documentation/dast/user-guide/scanning-apis/adding-apis/api-integrations/aws
Fetched: 2026-06-28T09:15:40.216503+00:00

DAST

Integrating with AWS

Last updated:

June 18, 2026

Read time:

2 Minutes

Cloud

Self-hosted

You can integrate Burp Suite DAST with Amazon API Gateway to automatically discover REST and HTTP APIs deployed in your AWS environment.

Note

This integration gives Burp Suite DAST read-only access to Amazon API Gateway. No APIs are created or scanned during the setup process. Once the connection is established, discovered APIs are shown in API finder.

Prerequisites

You have Modify Settings permission in Burp Suite DAST.

You have an AWS Access Key ID and Secret Access Key for an IAM user with the following permissions:

sts:GetCallerIdentity: This is used to verify your credentials during setup.

apigateway:GET on your API Gateway resources. This is used to discover your APIs.

The following minimal IAM policy grants these permissions:

{

"Version": "2012-10-17",

"Statement": [

{

"Effect": "Allow",

"Action": "sts:GetCallerIdentity",

"Resource": "*"

},

{

"Effect": "Allow",

"Action": "apigateway:GET",

"Resource": [

"arn:aws:apigateway:*::/restapis",

"arn:aws:apigateway:*::/restapis/*",

"arn:aws:apigateway:*::/apis",

"arn:aws:apigateway:*::/apis/*"

]

}

]

}

Connecting to Amazon API Gateway

Go to Settings > Integrations.

On the Amazon API Gateway tile, click Configure. The AWS connection details dialog opens.

Enter a name in the Integration name field.

Enter your Access Key ID.

Enter your Secret Access Key.

Select a Region from the drop-down list.

Enter a schedule for how often you want Burp Suite DAST to check the gateway for updates.

Click Save.

Once Burp Suite DAST connects to AWS successfully, a confirmation message appears. The connection is then listed on the Integrations page, where you can see its status and how many APIs have been discovered. Click View discovered APIs to review the discovered APIs in API finder.

When a scheduled update discovers changes to your APIs, you will see a red notification dot in the API finder tab. For more information, see Updating your API sites

Related pages

Discovering APIs from integrations
