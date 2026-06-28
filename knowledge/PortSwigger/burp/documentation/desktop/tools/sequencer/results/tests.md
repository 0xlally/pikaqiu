# Burp Sequencer randomness tests

Source: https://portswigger.net/burp/documentation/desktop/tools/sequencer/results/tests
Fetched: 2026-06-28T09:16:08.285322+00:00

Support Center

Documentation

Desktop editions

Tools

Sequencer

Results

Tests

ProfessionalCommunity Edition

Burp Sequencer randomness tests

Last updated:

June 18, 2026

Read time:

6 Minutes

Burp Sequencer employs a variety of standard statistical tests for randomness. The tests performed by Burp Sequencer operate on two levels of analysis: character-level and bit-level. Test results are compiled and summarized.

Note

For general information about how results are presented in Sequencer, see Burp Sequencer results.

How the tests work

All Burp Sequencer tests start with the hypothesis that the tokens are randomly generated. Each test then:

Observes properties of the sample that are likely to have certain characteristics if the tokens are randomly generated. For example, Burp may observe the distribution of characters used at each position within the token. This is likely to be approximately uniform if the tokens are random.

Calculates the probability of the observed characteristics occurring if the tokens are randomly generated.

Compares the probability to a range of significance levels. You can reject the hypothesis that the sample is randomly generated if the probability falls below the significance level you choose for your analysis.

You can choose the probability you use to interpret the randomness of your findings - this is the significance level. Scientific experiments often use levels between 1% and 5%. FIPS tests often use levels between 0.002% and 0.03%. A lower significance level means that stronger evidence is required to reject the hypothesis that the tokens are randomly generated. This increases the chance that non-random data will be treated as random.

Character-level tests

The character-level tests operate on each character position of the token in its raw form.

Note

To calculate the number of bits of effective entropy at or above each significance level, each character position is assigned a number of bits of entropy. This is based on the size of its character set (for example, two bits for four characters, three bits for eight characters).

Two different character-level tests are performed at each character position:

Character count analysis

This test analyzes the distribution of characters used at each position within the token. If the sample is randomly generated, the distribution of characters is likely to be approximately uniform. At each position, the test calculates the probability of the observed distribution arising if the tokens are random.

Character transition analysis

This test analyzes the transitions between successive tokens in the sample. If the sample is randomly generated, a character appearing at a given position is equally likely to be followed in the next token by any one of the characters that is used at that position. At each position, the test calculates the probability of the observed transitions arising if the tokens are random.

Bit-level analysis

When using bit-level analysis, each token is converted into a set of bits. This enables Burp to perform powerful bit-level tests at each bit position. The total number of bits is determined by the size of the character set at each character position.

FIPS test results

Burp Sequencer carries out multiple types of FIPS tests on each bit. Sequencer records whether each bit passed or failed the FIPS test.

Sequencer adjusts the FIPS pass criteria to work with random sample sizes. However, to obtain results that are compliant with the formal FIPS standard, you must use a sample of 20,000 tokens.

FIPS monobit test

This test analyzes the distribution of ones and zeroes at each bit position. If the sample is randomly generated, the number of ones and zeroes is likely to be approximately equal. At each position, the test calculates the probability of the observed distribution arising if the tokens are random.

FIPS poker test

This test analyzes the distribution of four-bit numbers:

Divides the bit sequence at each position into consecutive, non-overlapping groups of four.

Derives a four-bit number from each group.

Counts the number of occurrences of each of the 16 possible numbers.

Performs a chi-square calculation to evaluate this distribution.

If the sample is randomly generated, the distribution of four-bit numbers is likely to be approximately uniform. At each position, the test calculates the probability of the observed distribution arising if the tokens are random.

FIPS runs test

This test divides the bit sequence at each position into runs of consecutive bits that have the same value. It then counts the number of runs with a length of 1, 2, 3, 4, 5, and 6 and above. If the sample is randomly generated, the number of runs with each of these lengths is likely to be within a range determined by the size of the sample set. At each position, the test calculates the probability of the observed runs occurring if the tokens are random.

FIPS long runs test

This test measures the longest run of bits with the same value at each bit position. If the sample is randomly generated, the longest run is likely to be within a range determined by the size of the sample set. At each position, the test calculates the probability of the observed longest run arising if the tokens are random.

Note

The FIPS result for the FIPS long runs test only records a fail if the longest run of bits is overly long. However, if the longest run of bits is too short, this also indicates that the sample is not random. Therefore some bits may record a probability that is below the FIPS significance level even though they do not fail the FIPS test.

Spectral tests

This test analyzes the bit sequence at each position. Sequencer treats each series of consecutive numbers as coordinates in a multi-dimensional space. It then plots a point in this space at each location determined by these coordinates. If the sample is randomly generated, the distribution of points within this space is likely to be approximately uniform. However, if clusters appear within the space then the data is likely to be non-random. At each position, the test calculates the probability of the observed distribution occurring if the tokens are random. The test is repeated for multiple sizes of number (between 1 and 8 bits) and for multiple numbers of dimensions (between 2 and 6).

This test can identify evidence of non-randomness in some samples that pass the other statistical tests.

Correlation test

This tests for any statistically significant relationships between the values at different bit positions within the tokens. If the sample is randomly generated, a value at a given bit position is equally likely to be accompanied by a one or a zero at any other bit position. At each position, this test calculates the probability of the relationships observed with bits at other positions arising if the tokens are random.

To prevent arbitrary results, when a degree of correlation is observed between two bits, the test adjusts the significance level of the bit whose significance level is lower based on all of the other bit-level tests.

Note

This test enables you to assess the amount of randomness in the token as a whole. This is important as each of the bit-level tests operates only on individual bit positions. The randomness at each bit position is calculated in isolation. This means that a sample of tokens with the same bit value at each position may appear to contain more entropy than a sample of shorter tokens with different values at each position.

Compression test

This test provides a simple intuitive indication of the amount of entropy at each bit position. The test attempts to compress the bit sequence at each position using standard ZLIB compression. The results indicate the proportional reduction in the size of the bit sequence when it is compressed. A higher degree of compression indicates that the data is less likely to be randomly generated.
