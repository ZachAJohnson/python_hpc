import sys
import numpy as np

def sum_N(N=int(1e7)):
    return np.sum(np.arange(N)/1.)

if __name__ == '__main__':
    _, N = sys.argv
    N = int(float(N))
    print(f"Numpy: N= {N:0.3e}, sum = {sum_N(N):0.3e}")
