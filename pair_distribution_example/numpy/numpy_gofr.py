import sys
import numpy as np

def read_xyz(filename):
	with open(filename, 'r') as file:
		cum_gofr = np.zeros(Nbins)
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
					gofr = compute_g_of_r_at_t(np.array(atom_positions))
					gofr_list.append(gofr)
					cum_gofr += gofr 
				ti +=1
			ni += 1
			if ti==num_ti_to_average + num_to_wait:
				break
	ti_tot = ti-num_to_wait
	print(f"Reached {ti_tot} times")
	return cum_gofr/(num_ti_to_average)#, gofr_list

def distance(x1, x2):
	dist = np.linalg.norm(np.abs(x1-x2), axis=-1)
	return dist

def compute_g_of_r_at_t(positions):	
	distance_tensor = distance(positions[np.newaxis,np.newaxis,np.newaxis,unique_pair_indcs[0], :],
				 L*lattice_tensor[:,:,:,np.newaxis,np.newaxis,:] + 
				 positions[np.newaxis,np.newaxis,np.newaxis,unique_pair_indcs[1], :])
	
	gofr = np.histogram(distance_tensor.flatten(), bins = bins)[0]*histogram_to_gofr
	return gofr


# Specific information for run
# file = "/home/zach/plasma/hpc_testing/pair_distribution_example/data/Li_054eV_0513gpercc_100_SHORT.nvt.xyz"
file = "/home/zach/plasma/hpc_testing/pair_distribution_example/data/Li_054eV_0513gpercc_100.nvt.xyz"
L = 24.7938 # cell length in each direction
N = 100  # number particles
n0 = N/L**3 # average density

# Define periodicity
lattice_n = np.array([-1,0,1])  # periodic numbers
xhat, yhat, zhat = np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1])
lattice_tensor = (lattice_n[:,np.newaxis, np.newaxis,np.newaxis]*xhat + 
			lattice_n[np.newaxis,:,np.newaxis, np.newaxis]*yhat +
	 		lattice_n[np.newaxis,np.newaxis,:, np.newaxis]*zhat)

unique_pair_indcs = np.triu_indices(N, k=1) 

# Binning information
r_max, Nbins = 1*L, 50
bins = np.linspace(0, r_max, num=Nbins+1, endpoint=True) # how to bin the g(r)

r_mid_bin = (bins[1:]+bins[:-1])/2
bin_vols = 4/3*np.pi* ( bins[1:]**3-bins[:-1]**3)  
pair_normalization = N/(N*(N-1)/2)
histogram_to_gofr = pair_normalization/(bin_vols*n0 )

# num_ti_to_average = 50 # how many timesteps to average g(r,t) over
num_ti_to_average = int(float(sys.argv[1]))
num_to_wait = 100  #Wait for some number to ignore issues with first timesteps

print(f"Number of periodic boxes: {len(lattice_n)**3}")
print(f"Max distance based on number of periods: {np.max(lattice_n)*L}")

av_gofr = read_xyz(file)
np.savetxt("gofr.dat", np.array([r_mid_bin,av_gofr]).T, header="r\t\t\t\tg(r)",comments='')

