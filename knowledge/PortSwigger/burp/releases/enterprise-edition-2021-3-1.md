# Enterprise Edition 2021.3.1

Source: https://portswigger.net/burp/releases/enterprise-edition-2021-3-1
Fetched: 2026-06-28T09:16:17.226089+00:00

This release provides several major enhancements to our cloud-friendly version of Burp Suite Enterprise Edition, as well as support for a new database version.

Additional database support

You can now use an Oracle 19c database with Burp Suite Enterprise Edition. For a full list of supported database types, please refer to the system requirements.

Nested cloud templates

Both the main AWS CloudFormation template and the Azure Resource Manager template now comprise multiple "nested" templates, each with their own URL. This gives you the option to skip parts of the template and perform some of the process independently.

For example, you may prefer to set up the required infrastructure on your own and just use the template to deploy the main application. In this case, instead of entering the top-level URL for the full template in AWS/Azure, you can now just enter the URL for the deployment part.

You can find the URLs for the nested templates within the main template for each platform. We've also provided direct links at the bottom of these release notes. If you still want to use the full template, you can just ignore the nested ones and use the main URL in the same way as before.

Role-based access control using AWS Identity and Access Management

We now support role-based access control (RBAC) for the entire deployment process on AWS.

In previous releases, you had to provide an AWS access key and secret for the user who would be performing the deployment. This requirement has been removed completely. Instead, our IAM CloudFormation template now automatically generates roles that cover all of the required permissions, along with a corresponding group. Simply assigning the user to this group will allow them to perform the rest of the deployment.

Optional PostgreSQL database for AWS

The main AWS CloudFormation template now provides the option to automatically create and configure a new PostgreSQL database using Amazon's Relational Database Service (RDS). This should make it much easier to get started as you won't have to manually set up and connect to a database; most of the configuration will be done for you.

This is completely optional. If you prefer, you can still connect to any of our supported database types in the same way as before.

Improved logging for AWS deployment

On AWS, application logging is now enabled at the beginning of the deployment phase. This means that any errors that occur during the database migration will now be captured in CloudWatch, which should help with debugging.

Obfuscated credentials in AWS

All credentials that you provide in the CloudFormation template are now obfuscated. This prevents them from being viewed by other users who have access to your Burp Suite Enterprise Edition resources in the AWS Management Console.

Cloud deployment links

We no longer provide AWS CloudFormation or Azure Resource Manager templates. We're releasing an improved, much simpler deployment method soon and recommend waiting for this instead.
