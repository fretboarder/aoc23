Every stage has a number of "mapping channels":
the first input is a continuous range of values,

eg input range(10,31) == values 10..30

12-22 ----- transforms to ------- 13 - 23
25-35 ----- transforms to ------- 45 - 55

range(10, 12) -> passes untransformed range(10, 12)
range(12, 23) -> transformed to range(13, 24) (op +1)
range(23, 25) -> passes untransformed range(23, 25)
range(25, 31) -> transforms to range(45, 51)  (op +20)

the result are 4 new ranges returned from the stage, which
are now the input for the next stage.


the mapping channels are sorted in increasing order

for 1 input range:

1. take the start value of the input range and compare it to start value of the next input channel
2. compare the stop value of the input range to the start value of the next input channel
3. if both values are less then the mapping range => there will be no more match => return the range as UNMAPPED
4. if both values are inside the mapping range => there's only one match => return the range as MAPPED

5. if only the stop value is within the range of the mapping range (start is less than mapping)
6. create a UNMAPPED range of mapping_range.start - input_range.start
7. create a MAPPED range of input_range.stop - mapping_range.start
8. => there can be no more channel mapping, because the input range is exhausted

9.  if the stop value is greater than the stop value of the mapping range
10.  create an unmapped range of mapping_range.start - input_range.start
11. create a mapped range mapping_range.stop - mapping_range.start
12. and remove this range from the input_range => this creates a new (sub-)input_range

13. if there's no more channel available => return this range as unmapped

14. Otherwise repeat the loop starting with step 1