# Professional 1.2.09

Source: https://portswigger.net/burp/releases/professional-1-2-09
Fetched: 2026-06-28T09:16:22.277972+00:00

This release contains some major enhancements to Burp's extensibility APIs. You only need to download this release if you want to extend Burp's capabilities with your own code.

I'll produce full Javadoc for the new interfaces at a later date, but below is a summary of the new APIs, followed by an example of how they might be used. If you encounter any problems getting the new APIs working, email me.

The existing IBurpExtender interface adds two new methods which you can optionally implement:

public void processHttpMessage(String toolName, boolean messageIsRequest, IHttpRequestResponse messageInfo);

public void newScanIssue(IScanIssue issue);

The processHttpMessage method is invoked whenever any of Burp's tools makes an HTTP request or receives a response. This is effectively a generalised version of the existing processProxyMessage method, and can be used to intercept and modify the HTTP traffic of all Burp tools.

The newScanIssue method is invoked whenever Burp Scanner discovers a new, unique issue, and can be used to perform customised reporting or logging of issues.

The existing IBurpExtenderCallbacks interface adds several new methods which you can invoke to query and update Burp's state, and to parse raw HTTP messages for parameters and headers. These methods are hopefully self-explanatory:

public IHttpRequestResponse[] getProxyHistory();

public IHttpRequestResponse[] getSiteMap(String urlPrefix);

public void restoreState(java.io.File file) throws Exception;

public void saveState(java.io.File file) throws Exception;

public String[][] getParameters(byte[] request) throws Exception;

public String[] getHeaders(byte[] message) throws Exception;

The existing IBurpExtenderCallbacks.doActiveScan method, which previously returned void, has been modified to return an object which can be used to query and control the resulting item in the active scanning queue:

public IScanQueueItem doActiveScan(String host, int port, boolean useHttps, byte[] request) throws Exception;

The methods described above make use of three new interfaces, all of which reside in the burp package.

The new IHttpRequestResponse interface contains the following methods, which can be used to query and update details of HTTP requests and responses:

public String getHost();

public int getPort();

public String getProtocol();

public void setHost(String host) throws Exception;

public void setPort(int port) throws Exception;

public void setProtocol(String protocol) throws Exception;

public byte[] getRequest() throws Exception;

public java.net.URL getUrl() throws Exception;

public void setRequest(byte[] message) throws Exception;

public byte[] getResponse() throws Exception;

public void setResponse(byte[] message) throws Exception;

public short getStatusCode() throws Exception;

Note that the set methods can only be used where the message has been intercepted before being forwarded (i.e. using IBurpExtender.processHttpMessage) and not in read-only contexts (e.g. using IBurpExtender.getProxyHistory). Also, the methods relating to responses can only be used after the request has been issued and the response received.

The new IScanIssue interface contains the following methods, which can be used to query information about issues discovered by Burp Scanner:

public String getHost();

public int getPort();

public String getProtocol();

public java.net.URL getUrl();

public String getIssueName();

public String getSeverity();

public String getConfidence();

public String getIssueBackground();

public String getRemediationBackground();

public String getIssueDetail();

public String getRemediationDetail();

public IHttpRequestResponse[] getHttpMessages();

The new IScanQueueItem interface contains the following methods, which can be used to query and control items in the active scanning queue:

public String getStatus();

public byte getPercentageComplete();

public int getNumRequests();

public int getNumErrors();

public int getNumInsertionPoints();

public void cancel();

public IScanIssue[] getIssues();

Note that different items within the scan queue may contain duplicated versions of the same issue - for example, if the same request has been scanned multiple times. Duplicated issues are consolidated in the main view of scan results. You can implementIBurpExtender.newScanIssue to get details only of unique, newly discovered scan issues post-consolidation.

The new extensibility APIs should enable users to create much more powerful extensions to Burp's functionality. One example of this is a means of fully automating periodic scanning of a specific application to identify any new vulnerabilities it contains. There are various ways of accomplishing this, but one way is described below. First, on a single occasion, you will need to manually explore all of the application's functionality using Burp Proxy, and save the state of Burp's target site map and scope configuration to file, in the usual way. Then, on future occasions, you can create an extension which performs the following actions:

Load the saved site map and scope configuration back into Burp, using IBurpExtenderCallbacks.restoreState.

Use IBurpExtenderCallbacks.getSiteMap to retrieve all of the site map items for the target application, by specifying a suitable URL prefix (e.g. "https://myapp.example.org/").

If required, use IBurpExtenderCallbacks.sendToSpider to discover any content that has been newly added to the application, and then use IBurpExtenderCallbacks.getSiteMap again to obtain the updated site map.

Use IBurpExtenderCallbacks.doActiveScan to initiate active scans of each site item that interests you (based on URL, file extension, parameters etc). Keep a reference to each IScanQueueItem returned from this method.

If the application uses authentication, implement IBurpExtender.processHttpMessage to intercept every request made by Burp, and modify the Scanner's requests to add suitable session information to each request as required. You can use IBurpExtenderCallbacks.makeHttpRequest to make arbitrary additional HTTP requests to perform an application login and obtain a valid session token to be added into the Scanner's requests.

Implement IBurpExtender.newScanIssue to retrieve details about each discovered scan issue, and save these details if required.

Monitor the progress of each IScanQueueItem created in step #4, to determine when all your initiated scans are completed.

Use IBurpExtenderCallbacks.saveState to save the full state of Burp when all scanning is completed, to enable manual review and reporting as required.
