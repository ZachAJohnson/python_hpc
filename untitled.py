import sys
import cython_sum_dumb_generator

_, N = sys.argv
N = int(float(N))

print(f"Cython(dumb): N= {N:0.3e}, sum = {cython_sum_dumb_generator.sum_N(N):0.3e}")