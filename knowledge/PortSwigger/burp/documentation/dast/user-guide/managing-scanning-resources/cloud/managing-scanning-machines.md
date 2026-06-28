# Managing self-hosted scanning machines with a Cloud instance

Source: https://portswigger.net/burp/documentation/dast/user-guide/managing-scanning-resources/cloud/managing-scanning-machines
Fetched: 2026-06-28T09:15:37.034358+00:00

DAST

Managing self-hosted scanning machines with a Cloud instance

Last updated:

June 18, 2026

Read time:

1 Minute

Cloud

You can manage the scanning pools for your self-hosted scanning machines. For more information, see Managing scanning pools.

Updating self-hosted scanning machines

Your self-hosted scanning machines update automatically.

Deleting a self-hosted scanning machine

To delete a self-hosted scanning machine:

Run the uninstaller for your scanning machine.

Go to Scanning resources and select Manage scanning machines. Under Self-hosted

scanning machines, the scanning machine will show as disconnected.

Click the trash icon next to the scanning machine.

Managing authentication tokens

You can only revoke a token if no scans are active on scanning machines that use that token. To revoke an authentication token:

Go to Scanning resources and select Manage scanning machines.

Under Authentication tokens, click the trash icon next to the token.

Any scanning machines that were using the authentication token will show as Disconnected.

Related pages

Managing scanning pools

Assigning scan limits
