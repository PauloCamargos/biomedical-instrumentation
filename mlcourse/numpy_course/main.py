import numpy as np
import time
import sys

# creating an 1d array
a  = np.array([5,6,9])

# accessing the elements
print(a[0])
print(a[2])

# creating a 2d array of float 64
a2d = np.array([[1,2,3], [4,5,6], [7,8,9]], dtype=np.float64)

# printing the dimension of the aray
print(a.ndim)  
print(a2d.ndim)

# printing the size of each element in the array
print(a.itemsize)

# print the datatype
a.dtype

# number of element of an array
a.size

# row and cols
a.shape

# init with zeros
azeros = np.zeros((3,5))
azeros

# init with ones
aones = np.ones((5,4))
aones

# Creating an array from range
arange = np.arange(1,9,2,dtype=np.int8)
arange

# linspace
alinspace = np.linspace(1,10,10)
alinspace

# reshaping
areshaped = alinspace.reshape(2,5)
areshaped

# making 1d array 
aravel = alinspace.ravel()
aravel

# obs.: they dont change the original one

# commom operations
arange.min()
arange.max()
arange.sum()
arange.sum(axis=0)

np.sqrt(arange)
np.std(arange)
np.mean(arange)

a = np.arange(1,16).reshape(3,5)
b = a

result = a + b
result

result = a - b
result

result = a / b
result

result = a * b
result

# VIDEO 2 indexing, iterating, stacking
# slicing 1d
a = np.arange(1,10)
a[0:2]
a[-1]

# slicing 2d
a = np.arange(1,10).reshape(3,3)
a[0:2,2]
a[-1]
a[-1, 0:3]
a[:, 0]
a[1, :]

# iterating an array
for row in a:
    print(np.sqrt(row[2]))

for cell in a.flat:
    print(cell)


# stacking
b = np.arange(11,20).reshape(3,3)
np.vstack((a,b))
np.hstack((a,b))

# spliting big array
a = np.arange(30).reshape(2,15)
result = np.hsplit(a,3)
result

result = np.vsplit(a,2)
result

# indexing with boolean array
a = np.arange(12).reshape(3,4)
b = a > 4
b
result = a[b]
result

a[b] = 0

# VIDEO 3: iteraing with nditer
# https://www.youtube.com/watch?v=XawR6CjAYV4&list=PLeo1K3hjS3uset9zIVzJWqplaWBiacTEU&index=4

# iterating through 2 arrays simultaneously
a = np.arange(3,15,4).reshape(3,1)
b = np.array([['canal 1'], ['canal 2'], ['canal 3']])

for x, y in np.nditer([a,b]):
    print(y,x)


conda install spyder‑kernels=0.*
