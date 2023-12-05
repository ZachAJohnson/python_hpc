import sys

cpdef long long sum_N(int N= int(1e7)):
    cdef long long sum = 0
    cdef int i
    for i in range(N):
        sum += i
    return sum

if __name__ == '__main__':
    _, N = sys.argv
    N = int(float(N))
    print(f"For N: {N:.3e}, sum = {sum_N(N):0.3e}")
