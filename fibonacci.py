# This example prints 10 digits of the fibonacci sequence.
# You'll notice that we use the range() function to count up, this returns an iterable object containing 0,1,2,3,4,5,6,7,8,9,10.

a = 0
b = 1

for i in range(10):
    print a
    a, b = b, a + b
