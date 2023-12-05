import sys
import cython_sum_smart_generator

_, N = sys.argv
N = int(float(N))

print(f"Cython(smart): N= {N:0.3e}, sum = {cython_sum_smart_generator.sum_N(N):0.3e}")