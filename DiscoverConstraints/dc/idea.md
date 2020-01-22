# K-L Divergence
* leave numerical value as it was!!!
* for data without error, we can set a param that excluding all kl > 0

## fd
* H(Y given X) = 0
* distribution:
	* w/o violations: P(Y|X = x) = 1 for a specific value, 0 otherwise

## Trump-rule neg(t1.A = t2.A and t1.B = t2.B)
* distribution:
	* w/o violations: P(Y|X = x) = 1/k for k values with emprical pb not equal to 0, 0 otherwise

## for constants, one constant?
* keep a record of distinct score, append to the dictionary of edges? one more layer? extra load?
* or just keep those passing a threshold? 
* output when fd or trump does not hold overall

### fd

### trump-rule

## ordered dependency, neg(t1.A < t2.A and t1.B > t1.B)
* sort by A, B
* distribution
	* table of P(XY) with violation:

	|X\Y|1|2|3|4|
	|:-|:-|:-|:-|:-|
	|1|2|1|0|0|
	|2|0|0|3|0|
	|3|0|1|0|2|

	* table of P(XY) without violation:

	|X\Y|1|2|3|4|
	|:-|:-|:-|:-|:-|
	|1|2|1|0|0|
	|2|0|0|3|0|
	|3|0|0|0|2|

## cross-column, neg(t1.A > t1.B)
* alike ordered dependency, create a table of P(XY)
	* table with violation

	|XY|1|2|3|4|
	|:-|:-|:-|:-|:-|
	|1|0|0|**1**|0|
	|3|2|3|0|0|
	|4|0|0|2|0|
	|5|3|1|2|5|

	* table without violation

	|XY|1|2|3|4|
	|:-|:-|:-|:-|:-|
	|1|0|0|0|0|
	|3|2|3|0|0|
	|4|0|0|2|0|
	|5|0|0|0|5|


