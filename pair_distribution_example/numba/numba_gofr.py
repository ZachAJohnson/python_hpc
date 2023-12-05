import sys
import numpy as np
from numba import njit


def read_xyz(filename):
    with open(filename, 'r') as file:
        cum_gofr = np.zeros(N_bins)
        cum_gofr_square = np.zeros(N_bins)
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
                # print("g: ", compute_g_of_r_at_t(np.array(atom_positions)),"\n")
                if ti>=num_to_wait:
                    gofr = compute_g_of_r_at_t(np.array(atom_positions,dtype=np.float64))
                    gofr_list.append(gofr)
                    cum_gofr += gofr 
                    cum_gofr_square  += gofr**2
                ti +=1
            ni += 1
            if ti==num_ti_to_average + num_to_wait:
                break
    ti_tot = ti-num_to_wait
    print(f"Reached {ti_tot} times")
    av_gofr = np.array(cum_gofr/(ti_tot))
    σ_gofr  = np.sqrt( cum_gofr_square/ti_tot - av_gofr**2 )
    return av_gofr, σ_gofr

@njit
def distance(x1, x2, periodic_vec):
    dist = 0
    for i in range(3):
        dist += (x1[i] - x2[i] - periodic_vec[i])**2
    return np.sqrt(dist)

@njit
def compute_g_of_r_at_t(positions):
    gofr = np.zeros(N_bins)
    periodic_vec = np.zeros(3)
    
    for xi in range(N_lattice_numbs):
        for yi in range(N_lattice_numbs):
            for zi in range(N_lattice_numbs):
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
N_bins = 100
r_max = L
dr = r_max / N_bins
r_mid_bins = np.zeros(N_bins)
bin_vols = np.zeros(N_bins)
histogram_to_gofr = np.zeros(N_bins)

for i in range(N_bins):
    r_mid_bins[i] = dr * (i + 0.5)
    bin_vols[i] = 4 / 3 * np.pi * ((dr * (i + 1))**3 - (dr * i)**3)
    histogram_to_gofr[i] = N / (N * (N - 1) / 2) / (bin_vols[i] * n0)

lattice_n = np.array([-2,-1, 0,1, 2])
N_lattice_numbs = len(lattice_n)
xhat = np.array([1, 0, 0])
yhat = np.array([0, 1, 0])
zhat = np.array([0, 0, 1])

num_ti_to_average = int(float(sys.argv[1]))
num_to_wait = 100

file = "/home/zach/plasma/hpc_testing/pair_distribution_example/data/Li_054eV_0513gpercc_100.nvt.xyz"
av_gofr, σ_gofr = read_xyz(file)
np.savetxt("gofr.dat", np.array([r_mid_bins,av_gofr,σ_gofr]).T, header="r\t\t\t\tg(r)\t\t\tσ(r)",comments='')
