# REST API

Source: https://portswigger.net/burp/documentation/dast/user-guide/api-documentation/rest
Fetched: 2026-06-28T09:15:34.662658+00:00

DAST

REST API

Last updated:

June 18, 2026

Read time:

1 Minute

Self-hosted

If you have a self-hosted installation of Burp Suite DAST, you can use the REST API to initiate scans from your CI system and failing software builds whenever certain issues are reported. It is closely related to the Burp Suite Professional API, and represents a simple migration from that API surface.

While the REST API may be more familiar to users of Burp Suite Professional, it is only able to expose a limited range of Burp Suite DAST's functionality. Therefore, we strongly recommend using the GraphQL API for your new integrations wherever possible.

To view interactive documentation for the REST API, browse to: [DAST server URL]/api/[API key].
