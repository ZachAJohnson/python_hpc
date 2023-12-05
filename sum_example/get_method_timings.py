import numpy as np
import subprocess
import time
import pandas as pd

def run_command(command):
    start = time.time()
    subprocess.run(command, shell=True)
    end = time.time()
    return end - start

def main():
    N_array = np.geomspace(1e9, 1e9, num=1)
    
    # Define run for all different methods
    cpp_program = "cd c++; make -B; pure_cpp_sum"
    numba_program = "python numba/numba_python_sum.py"
    python_program= "python pure_python/pure_python_sum.py"
    numpy_program = "python numpy/numpy_python_sum.py"
    cython_smart_program= "cd cython_smart; python setup.py build_ext --inplace; python cython_smart_sum.py"
    cython_dumb_program= "cd cython_dumb; python setup.py build_ext --inplace; python cython_dumb_sum.py"

    data = {"N": [], "C++": [], "Python": [], "Numba(njit)": [],
            "Numpy": [], "Cython(dumb)": [], "Cython(smart)": []}

    for N in N_array:
        cpp_time = 1#run_command(f"{cpp_program} {N}; cd ..")
        python_time = 1#run_command(f"{python_program} {N}")
        numba_time = 1#run_command(f"{numba_program} {N}")
        numpy_time = run_command(f"{numpy_program} {N}")
        cython_smart_time = 1#run_command(f"{cython_smart_program} {N}; cd ..")
        cython_dumb_time = 1#run_command(f"{cython_dumb_program} {N}; cd ..")


        data["N"].append(N)
        data["C++"].append(cpp_time)
        data["Python"].append(python_time)
        data["Numba(njit)"].append(numba_time)
        data["Numpy"].append(numpy_time)
        data["Cython(smart)"].append(cython_smart_time)
        data["Cython(dumb)"].append(cython_dumb_time)

        # print(f"N = {N}: C++ time = {cpp_time}, Python time = {python_time}")

    df = pd.DataFrame(data)
    df.to_csv('timing_results.csv', index=False, sep=' ')

if __name__ == "__main__":
    main()
