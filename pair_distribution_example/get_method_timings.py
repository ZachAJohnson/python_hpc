import numpy as np
import subprocess
import time
import pandas as pd

def run_command(command):
    start = time.time()
    subprocess.run(command, shell=True)
    end = time.time()
    return end - start

def main(time_cutoff = 3e2):
    N_array = np.geomspace(1, 4160, num=10)
    
    # Define run for all different methods
    # cpp_program = "cd c++; make -B; pure_cpp_sum"
    numba_program = "python numba/numba_gofr.py"
    python_program= "python pure_python/python_gofr.py"
    numpy_program = "python numpy/numpy_gofr.py"
    cython_smart_program= "cd cython_smart; python setup.py build_ext --inplace; python cython_smart_run.py"
    cython_dumb_program= "cd cython_dumb; python setup.py build_ext --inplace; python cython_dumb_run.py"

    data = {"N": [], "C++": [], "Python": [], "Numba(njit)": [],
            "Numpy": [], "Cython(dumb)": [], "Cython(smart)": []}

    data = {"N": [], "Python": [], "Numba(njit)": [],
            "Numpy": [], "Cython(dumb)": [], "Cython(smart)": []}

    python_too_slow, numba_too_slow, numpy_too_slow, cython_smart_too_slow, cython_dumb_too_slow = False,False,False,False,False
    python_time, numba_time, numpy_time, cython_smart_time, cython_dumb_time = 0,0,0,0,0
    for N in N_array:
        # cpp_time = run_command(f"{cpp_program} {N}; cd ..")
        if python_too_slow:
            python_time = None
        elif python_time>time_cutoff:
            python_too_slow=True
            python_time = None
        else: 
            python_time = run_command(f"{python_program} {N}")
        
        if numba_too_slow:
            numba_time = None
        elif numba_time>time_cutoff:
            numba_too_slow=True
            numba_time = None
        else: 
            numba_time = run_command(f"{numba_program} {N}")
        
        if numpy_too_slow:
            numpy_time = None
        elif numpy_time>time_cutoff:
            numpy_too_slow=True
            numpy_time=None
        else: 
            numpy_time = run_command(f"{numpy_program} {N}")
        
        if cython_smart_too_slow:
            cython_smart_time = None
        elif cython_smart_time>time_cutoff:
            cython_smart_too_slow=True
            cython_smart_time = None
        else:
            cython_smart_time = run_command(f"{cython_smart_program} {N}; cd ..")
        
        if cython_dumb_too_slow:
            cython_dumb_time = None
        elif cython_dumb_time>time_cutoff:
            cython_dumb_too_slow=True
            cython_dumb_time = None
        else:
            cython_dumb_time = run_command(f"{cython_dumb_program} {N}; cd ..")
        
        data["N"].append(N)
        # data["C++"].append(cpp_time)
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
