import sys

def sum_N(N=int(1e7)):
    sum = 0
    for i in range(N):
        sum += i
    return sum

if __name__ == '__main__':
    _, N = sys.argv
    N = int(float(N))
    print(f"For N: {N:.3e}, sum = {sum_N(N):0.3e}")
