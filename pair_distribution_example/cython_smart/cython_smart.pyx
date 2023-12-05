import sys
import numpy as np
from libc.math cimport sqrt, pi

 # π = 3.14159265359

def read_xyz(filename):
	with open(filename, 'r') as file:
		cum_gofr = np.zeros(N_bins)
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
				ti +=1
			ni += 1
			if ti==num_ti_to_average + num_to_wait:
				break
	ti_tot = ti-num_to_wait
	print(f"Reached {ti_tot} times")
	return cum_gofr/(ti_tot)#, gofr_list

cdef double distance(double[:] x1, double[:] x2, double[:] periodic_vec):
	cdef double dist = 0
	for i in range(3):
		dist += (x1[i] - x2[i] - periodic_vec[i])**2
	return sqrt(dist)

cpdef compute_g_of_r_at_t(double[:, :] positions):
	cdef int nx, ny, nz
	cdef double[3] periodic_vec = [0,0,0]
	cdef double[:] gofr = np.zeros(N_bins, dtype=np.float64)
	cdef double[:] x1, x2 = np.zeros(N_bins, dtype=np.float64)
	cdef double dist
	cdef int particle_i, particle_j
	cdef int bin_index

	for xi in range(3):
		for yi in range(3):
			for zi in range(3):
				nx, ny, nz = lattice_n[xi], lattice_n[yi], lattice_n[zi] 
				for i in range(3):
					periodic_vec[i] = L*nx*xhat[i] + L*ny*yhat[i] + L*nz*zhat[i]
				for particle_i in range(N):
					for particle_j in range(particle_i+1,N):
						dist = distance(positions[particle_i], positions[particle_j], periodic_vec)
						bin_index = int(dist/dr)
						if bin_index<N_bins:
							gofr[bin_index] += 1.
	for i in range(N_bins):
		gofr[i] *= histogram_to_gofr[i]

	return gofr



# file = "/home/zach/plasma/hpc_testing/pair_distribution_example/data/Li_054eV_0513gpercc_100_SHORT.nvt.xyz"
file = "/home/zach/plasma/hpc_testing/pair_distribution_example/data/Li_054eV_0513gpercc_100.nvt.xyz"

# Simulation information
cdef double L = 24.7938 # cell length in each direction
cdef int N = 100  # number particles
cdef double n0 = N/L**3 # average density

# binning information for g(r)
cdef int N_bins = 50
cdef double r_max = 1*L
cdef dr = r_max/N_bins
cdef double[:] r_mid_bins = np.zeros(N_bins, dtype=np.float64)
cdef double[:] bin_vols = np.zeros(N_bins, dtype=np.float64)
cdef double[:] histogram_to_gofr = np.zeros(N_bins, dtype=np.float64)
cdef int i 

for i in range(N_bins):
	r_mid_bins[i] = dr*(i + 0.5)
	bin_vols[i] = 4/3*pi* ( (dr*(i+1))**3 - (dr*i)**3 )  
	histogram_to_gofr[i] = N/(N*(N-1)/2)/(bin_vols[i]*n0 )

# Define periodicity
cdef int[3] lattice_n = [-1,0,1]  # periodic numbers
cdef double[3] xhat = [1,0,0]
cdef double[3] yhat = [0,1,0]
cdef double[3] zhat = [0,0,1]


# What data points to use 
# cdef int num_ti_to_average = 50 # how many timesteps to average g(r,t) over
cdef int num_ti_to_average = int(float(sys.argv[1]))

cdef int num_to_wait = 100  #Wait for some number to ignore issues with first timesteps

# print(f"Number of periodic boxes: {len(lattice_n)**3}")
# print(f"Max distance based on number of periods: {np.max(lattice_n)*L}")

av_gofr = read_xyz(file)

np.savetxt("gofr.dat", np.array([r_mid_bins,av_gofr]).T, header="r\t\t\t\tg(r)",comments='')

