import sys
import numpy as np

def read_xyz(filename):
    with open(filename, 'r') as file:
        cum_gofr = [0]*N_bins
        gofr_list = []
        ni=0 # which particle
        ti=0 # which timepoint
        in_loop=False

        for line in file:
            # print(line)
            if len(line.strip()) == 0 :# finds empty line
                atom_positions = [] #reset atoms array
                ni = 1
                in_loop=True
                continue 

            if in_loop and ti>=num_to_wait:
                parts = line.split()
                atom_positions.append([float(parts[1]), float(parts[2]), float(parts[3])])
            if ni==N:
                in_loop=False
                if ti>=num_to_wait:
                    gofr = compute_g_of_r_at_t(atom_positions)
                    gofr_list.append(gofr)
                    cum_gofr = [new_num + cum_num  for new_num, cum_num in zip(gofr, cum_gofr)]
                ti +=1
            ni += 1
            if ti==num_ti_to_average + num_to_wait:
                break
    ti_tot = ti-num_to_wait
    print(f"Reached {ti_tot} times")
    return [num/ti_tot for num in cum_gofr]#, gofr_list

def distance(x1, x2, periodic_vec):
    dist = 0
    for i in range(3):
        dist += (x1[i] - x2[i] - periodic_vec[i])**2
    return dist**0.5

def compute_g_of_r_at_t(positions):
    gofr = [0]*N_bins
    periodic_vec = [0,0,0]
    
    for xi in range(3):
        for yi in range(3):
            for zi in range(3):
                nx, ny, nz = lattice_n[xi], lattice_n[yi], lattice_n[zi]
                for i in range(3):
                    periodic_vec[i] = L * nx * xhat[i] + L * ny * yhat[i] + L * nz * zhat[i]
                for particle_i in range(N):
                    for particle_j in range(particle_i + 1, N):
                        dist = distance(positions[particle_i], positions[particle_j], periodic_vec)
                        bin_index = int(dist / dr)
                        if bin_index < N_bins:
                            gofr[bin_index] += 1.0

    for i in range(N_bins):
        gofr[i] *= histogram_to_gofr[i]

    return gofr

# Define parameters
L = 24.7938  # cell length in each direction
N = 100  # number particles
n0 = N / L**3  # average density
N_bins = 50
r_max = L
dr = r_max / N_bins
r_mid_bins = [0]*N_bins
bin_vols = [0]*N_bins
histogram_to_gofr = [0]*N_bins

for i in range(N_bins):
    r_mid_bins[i] = dr * (i + 0.5)
    bin_vols[i] = 4 / 3 * np.pi * ((dr * (i + 1))**3 - (dr * i)**3)
    histogram_to_gofr[i] = N / (N * (N - 1) / 2) / (bin_vols[i] * n0)

lattice_n = [-1, 0, 1]
xhat = [1, 0, 0]
yhat = [0, 1, 0]
zhat = [0, 0, 1]

num_ti_to_average = int(float(sys.argv[1]))
num_to_wait = 100

file = "/home/zach/plasma/hpc_testing/pair_distribution_example/data/Li_054eV_0513gpercc_100.nvt.xyz"
av_gofr = read_xyz(file)

np.savetxt("gofr.dat", np.array([r_mid_bins,av_gofr]).T, header="r\t\t\t\tg(r)",comments='')
