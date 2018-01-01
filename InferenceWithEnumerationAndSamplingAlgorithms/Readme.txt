1.	Input the evidence variables, followed by their truth values in this format.
Eg. [< N1, V1>, ..., < N N, V N >]
2.	These should be followed by query variables in the similar format:
Eg. [N Q1, ..., N QM].

3.	Then you should enter the number of samples.

4.	The output will be in this format [< J,0.9>]

Where j is the query variable for a given query.
All the inputs are taken as strings.

Sample example:

enter the input 
[<J,t><E,f>][B,M]

enter the sampling size10000

Output:

Enumeration : [<B,0.0164381492851><M,0.0333138844276>]
Prior Sampling : [<B,0.001><M,0.0115>]
Rejection Sampling : [<B,0.0187969924812><M,0.0300751879699>]
Likelihood Sampling : [<B,0.0139088729017><M,0.0373400057742>]
