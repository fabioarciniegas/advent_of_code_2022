# python 17.py print 10000 input_17.txt > cached_17.txt
#
# python 17.py cached 10000 input_17.txt cached_17.txt
# 15419
# python 17.py height 10000 input_17.txt 
# 15419

# simple count:
python 17.py height 2022 input_17.txt

# output the first 10000 blocks so we can figure out periodicity in the results
python 17.py print 10000 input_17.txt > cached_17.txt

# figure out periodicity and calculate in O(1) all the big periodic chunk in the middle
# then add the small reminder of blocks left

python 17.py cached 1000000000000 input_17.txt cached_17.txt
