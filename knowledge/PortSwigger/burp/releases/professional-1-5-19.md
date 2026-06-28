# Professional 1.5.19

Source: https://portswigger.net/burp/releases/professional-1-5-19
Fetched: 2026-06-28T09:16:25.702809+00:00

This release contains a number of enhancements to the Scanner tool.

Active Scanner optimization

There is a new set of Scanner options which let you control the behavior of the active scanning logic in relation to scan speed and accuracy:

Scan speed - This option determines how thorough certain scan checks will be when checking for vulnerabilities. The "Fast" setting makes fewer requests, and checks for fewer derivations of some vulnerabilities. The "Thorough" setting makes many more requests and checks for more derivative types of vulnerabilities. The "Normal" setting is mid-way between the two, and represents a suitable trade-off between speed and thoroughness for many applications.

Scan accuracy - This option determines the amount of evidence that the Scanner will require before reporting certain types of vulnerabilities. Some issues can only be detected using "blind" techniques, in which Burp infers the probable existence of a vulnerability based on some observed behavior, such as a time delay or a differential response. Because these observed behaviors can occur anyway, in the absence of the associated vulnerability, the techniques are inherently more prone to false positives than other techniques, such as the observation of error messages. To attempt to reduce false positives, Burp repeats certain tests a number of times when a putative issue is inferred, to try and establish a reliable correlation between submitted inputs and observed behaviors. The accuracy option is used to control how many times Burp will retry these tests. The "Minimize false negatives" setting performs fewer retries, and so is more likely to report false positive issues, but is also less likely to miss genuine issues due to inconsistent application behavior. The "Minimize false positives" setting performs many more retries, and so is less likely to report false positive issues, but may as a result wrongly miss some genuine issues, because some of the retry requests might just happen to fail to return the result being tested for. The "Normal" setting is mid-way between the two, and represents a suitable trade-off between false positive and false negative issues for many applications.

Payload encoding

Burp's internal logic handling the placement of scan payloads into insertion points has been reworked to resolve some occasional problems. In previous versions, Burp applied incorrect encoding to certain payloads in certain insertion points - for example, wrongly URL-encoding some characters in locations where URL-encoding is not necessary. This caused Burp to miss some edge case vulnerabilities in applications where Burp's non-standard encoding was not tolerated.

The improved handling of encoding within insertion points paves the way for some further enhancements to the Scanner's capabilities, and the next Scanner update will include more more powerful insertion point types, enabling Burp to find more vulnerabilities in today's complex applications.

Extensions

In order to fix the erroneous handling of encoding within some insertion points, Burp's contract with extensions in relation to customizing the Scanner has unfortunately needed to change. We apologize for this, however the previous contract was in any case not consistent, and left extensions with impossible responsibilities in some situations.

Previously, Burp-provided insertion points did not do any payload encoding, and extension-provided checks were required to submit suitably encoded payloads based on the insertion point type (for example, URL-encoding spaces in URL parameters, HTML-encoding tag brackets in XML parameters, etc.). In some cases, it wasn't actually possible for extensions to fully determine the encoding that was needed. Further, the old approach risked leaving extensions unable to deal with new insertion point types that we plan to introduce to Burp. In the new contract, Burp-provided insertion points will automatically carry out suitable encoding of payloads, and so extension-provided checks should submit raw payloads.

Regarding extension-provided insertion points, the contract has always been that Burp will submit raw payloads (although this contract may have been inconsistently honored by Burp due to the payload encoding issues described in the previous section). This contract remains in place and is now strictly followed by Burp, so extension-provided insertion points need to handle encoding of relevant payload characters based on the nature of the insertion point.

This change in the contract brings consistency to the responsibility of Burp- and extension-provided insertion points, and enables both Burp and extensions to function in a less coupled, more future-proof way.

Note that in a few rare cases, an extension-provided check may require complete control over how its payloads are encoded within insertion points - for example, in order to violate protocol-level rules for the proper representation of data in different contexts. In this situation, the extension should also create its own custom insertion points, in order to gain full control over the end-to-end payload handling process.

In addition to the previous changes, as an aid to extension authors, Burp's implementation of IScannerInsertionPoint.buildRequest() has been modified so that Burp always fixes the Content-Length header when the message body length has changed. Extension-provided implementations of this method are not obliged to do this.

XML reporting

The XML-based reporting of Scanner issues now includes the following details:

A method attribute on request elements, indicating the HTTP method used in the request.

A collection of issueDetailItem elements on some issue types, such as disclosure of email or IP addresses, containing the individual information items in machine-readable form.

User interface

In Scanner options, the panels with checkboxes to enable specific active and passive checks now have "Select all" and "Select none" buttons.

The Scanner reporting wizard, the panel with checkboxes to select specific types of issue to report now has "Select all" and "Select none" buttons.
