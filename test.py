import numpy as np
import cupy as cp

from cupyx.scipy.fft import fftn, ifftn
from numpy 
# Generate a random 2D array
input_array = np.random.rand(800, 800)

# Transfer the input array to the GPU memory
input_gpu = cp.asarray(input_array)

# Perform 2D FFT on the GPU
import timeit
s = timeit.default_timer()
# a = [fftn(input_gpu) for _ in range(3)]
a = [fftn(input_gpu) for _ in range(3)]
# output_gpu = fftn(input_gpu)
# output_gpu = ifftn(input_gpu)
e = timeit.default_timer()
# print(output_gpu == input_gpu)
print(e-s)

# Transfer the result back to the CPU memory
output_array = cp.asnumpy(a[0])

# Print the result
print(output_array)
