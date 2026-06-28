# REST API settings

Source: https://portswigger.net/burp/documentation/desktop/settings/suite/rest-api
Fetched: 2026-06-28T09:15:56.053374+00:00

Support Center

Documentation

Desktop editions

Settings

Suite

REST API

ProfessionalCommunity Edition

REST API settings

Last updated:

June 18, 2026

Read time:

2 Minutes

The REST API enables external tools to integrate with Burp Suite. These settings enable you to:

Enable the service.

Specify the URL on which it should run.

Configure API keys.

Enabling the REST API

To enable the REST API service, select the Service running checkbox.

Service URL

To specify the service URL and port:

Click Change next to the current URL to display the Configure REST API URL dialog.

Enter the port number that Burp should bind to.

Select the address that Burp should bind to. Burp can bind to the loopback address, all interfaces, or a specified address.

Click OK.

Note

We strongly recommend that you do not configure Burp to bind to non-loopback interfaces when connected to untrusted networks.

API key

By default, Burp's REST API requires you to use an API key to authenticate when you make calls. To disable this requirement, select Allow access without API key.

Note

The Allow access without API key option is not recommended. If API keys are not required then anyone with network access to the service endpoint can trigger actions within Burp and access its data. This includes CSRF requests from untrusted websites that you browse on the same machine as Burp. API keys should always be used even when the service is only listening on the loopback interface.

The API key settings display a list of current API keys. You can create separate API keys for different purposes, and enable or disable them using the checkboxes in the list.

To create a new API key:

Click New next to the list of API users to display the New API key dialog.

Enter a name for the API key.

Click Copy key to clipboard and store the key in a safe place.

Click OK.

Note

API keys are secret, and should be handled carefully. Note that you can only retrieve the value of an API key at the time that it is created.

You can also click Edit to edit the name of a key, or Delete to remove it from the list.

Once you have configured the service, you can browse the API documentation and interact with the API at [Service URL]/[API key].

Note

The REST API exposes sensitive functionality and data. You should not enable the REST API service on untrusted network interfaces, and you should use separate API keys for each client that you grant access to.

The REST API settings are user settings. They apply to all installations of Burp on your machine.
