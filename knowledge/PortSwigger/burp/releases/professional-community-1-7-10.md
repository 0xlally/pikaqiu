# Professional / Community 1.7.10

Source: https://portswigger.net/burp/releases/professional-community-1-7-10
Fetched: 2026-06-28T09:16:31.026315+00:00

This release adds some new APIs that extensions can use to easily implement powerful scan checks and other logic that involves response diffing.

Two new APIs have been added to IExtensionHelpers. The method:

IResponseVariations analyzeResponseVariations(byte[]... responses)

analyzes a collection of responses to identify variations in a range of attributes. The IResponseVariations object that is returned can be queried to determine the invariant or variant attributes, and the "value" of each attribute for each response:

List<String> getVariantAttributes();

List<String> getInvariantAttributes();

int getAttributeValue(String attributeName, int responseIndex);

The attributes that are currently supported are as follows:

anchor_labels

button_submit_labels

canonical_link

comments

content_length

content_type

css_classes

div_ids

etag_header

first_header_tag

header_tags

initial_body_content

input_image_labels

input_submit_labels

last_modified_header

limited_body_content

line_count

outbound_edge_count

outbound_edge_tag_names

page_title

set_cookie_names

status_code

tag_ids

tag_names

visible_text

visible_word_count

whole_body_content

word_count

Note that all values are represented as integer numbers, and the values of some attributes are intrinsically meaningful (e.g. word count) while the values of others are less so (e.g. checksum of HTML tag names).

The method:

IResponseKeywords analyzeResponseKeywords(List<String> keywords, byte[]... responses)

analyzes a collection of responses to identify the number of occurrences of the specified keywords. The IResponseKeywords object that is returned can be queried to determine the keywords whose counts vary or do not vary, and the number of occurrences of each keyword for each response:

List<String> getVariantKeywords();

List<String> getInvariantKeywords();

int getKeywordCount(String keyword, int responseIndex);

The new APIs allow your extensions to let Burp handle the messy work of analyzing responses to determine if they are the same or different, and you can easily create powerful scan checks with some simple logic:

Send novel payload.

Ask Burp whether the response changed in some interesting respect.

If so, report an issue.

On Friday, to coincide with our Backslash Powered Scanning talk at Black Hat EU, we will be releasing an extension to the BApp Store that demonstrates how the new APIs can be used to create powerful new scanning capabilities.
