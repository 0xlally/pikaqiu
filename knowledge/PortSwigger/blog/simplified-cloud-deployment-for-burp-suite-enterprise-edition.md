# Simplified cloud deployment for Burp Suite Enterprise Edition

Source: https://portswigger.net/blog/simplified-cloud-deployment-for-burp-suite-enterprise-edition
Fetched: 2026-06-28T09:15:24.564525+00:00

Simplified cloud deployment for Burp Suite Enterprise Edition

Dayna Shoemaker |

Friday, 26 March 2021 at 14:40 UTC

Last year, we made Burp Suite Enterprise Edition cloud-friendly. Organizations migrating to the cloud, or taking a cloud-first approach, are able to deploy Burp Suite Enterprise Edition to AWS or Azure. We have additional cloud services support planned for the future, so stay tuned for further updates.

Since the initial launch of our cloud-friendly solution, we have been working on a number of cloud deployment enhancements. The improvements in our latest

2021.3.1 release will support faster, more efficient setup, and give you additional configuration options to help you meet your security requirements.

AWS CloudFormation template changes

If you are looking to deploy Burp Suite Enterprise Edition within your AWS cloud infrastructure, we have created a number of improvements to the existing process. These are designed to provide simplification, as well as additional options for configuration to meet your specific deployment requirements:

AWS infrastructure is now created via a series of nested CloudFormation templates, making it easier to instantiate a subset of the infrastructure while using existing resources for the remainder.

You are no longer required to provide an AWS access key ID and secret key in the AWS CloudFormation template. Instead you can use Role Based Access Control (RBAC) to control permissions.

You can now add an optional PostgreSQL database to the AWS CloudFormation template to set it up at the same time.

Credentials provided in the AWS CloudFormation template are now obfuscated in nested templates.

Application logging is now enabled at the beginning of the deployment phase on AWS. This means that database migration errors are now captured in CloudWatch for improved monitoring and support.

Azure Resource Manager improvements

Azure Resource Manager (ARM) templates are the Microsoft Azure version of AWS CloudFormation templates. They enable you to quickly spin up infrastructure with set configurations. In this way, you can more efficiently set up the infrastructure to deploy Burp Suite Enterprise Edition using an ARM template.

While a template has previously been available for those on Azure cloud, we now provide nested templates to facilitate separate deployment of infrastructure and application. This is helpful if you want to instantiate a subset of the infrastructure while using existing resources for the remainder.

Burp Suite Enterprise Edition for the cloudGet started with the latest version of

Burp Suite Enterprise Edition for the cloud.

Dayna Shoemaker

Latest Posts

Burp Extensibility 2026: Awards, Talks, and Highlights

19 June 2026

Burp Extensibility 2026: Awards, Talks, and Highlights

The beast needs a cage: What's next for AppSec post-Mythos

12 May 2026

The beast needs a cage: What's next for AppSec post-Mythos

3 ways custom scan checks turn practitioner knowledge into scalable automation

01 May 2026

3 ways custom scan checks turn practitioner knowledge into scalable automation

Senior pentesters have a deeply refined intuition about what is vulnerable in an environment. The problem? That expertise is often siloed with an individual and trapped in their notes or Python scripts.
