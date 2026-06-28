# Enterprise Edition 2022.7

Source: https://portswigger.net/burp/releases/enterprise-edition-2022-7
Fetched: 2026-06-28T09:16:19.008278+00:00

This release greatly improves scan progress tracking. We've also made it easier to view and remediate scan errors.

Increased visibility of scan progress

The new Timeline tab contains a progress bar, so you can easily monitor how your scans are progressing. You can now see which phase of the scan is being performed, with live updates as issues are discovered and an estimate of the time remaining.

Improved scan error handling

The Timeline tab also supports our improved scan error handling. Errors are reported as they're discovered, along with meaningful descriptions of the cause and possible remediation. You can now also download the scan debug log from a dedicated Logging tab.

Other improvements

We've also made the following improvements:

For Kubernetes users, we've added a ClusterIP service for the web server to the application Helm chart. This enables you to bind your ingress solution to the web server.

For Kubernetes users, we've added the Kubernetes YAML for scan jobs to a configuration map in the Helm chart. This means scan jobs are created from the template rather than in code, which allows them to be customized.

Bug fixes

We've fixed some bugs. For example:

We've fixed a bug in the GraphQL API that prevented you from fetching the scan_metrics for a scan.

You can now upload certificates that have a subject alternative name containing a non-string value.
