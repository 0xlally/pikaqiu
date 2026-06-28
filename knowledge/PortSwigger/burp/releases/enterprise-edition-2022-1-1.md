# Enterprise Edition 2022.1.1

Source: https://portswigger.net/burp/releases/enterprise-edition-2022-1-1
Fetched: 2026-06-28T09:16:17.410997+00:00

This release does not provide any additional functionality. It simply implements some background changes in preparation for a future release, which will enable a brand new option for deploying to Kubernetes using a Helm chart. This will replace our existing AWS CloudFormation and Azure Resource Manager deployment methods.

Please note that if you deployed Burp Suite Enterprise Edition using our existing AWS CloudFormation or Azure Resource Manager templates, this is the last version that those deployments will support. You will need to migrate using the new Helm chart (coming soon) before you can install any future updates.
