import matplotlib.pyplot as plt
from pandas import read_csv

dir_list = ["numpy","cython_smart","cython_dumb","numba"]


for dir in dir_list:
	data = read_csv(dir+"/gofr.dat", delim_whitespace=True, header=0)

	fig, ax = plt.subplots(figsize=(8,6))


	ax.set_title(f"Lithium NVE Quantum Espresso ({dir})", fontsize=20)
	ax.plot(data['r'], data['g(r)'], 'k--.')

	ax.set_xlabel(r'$r$ [AU]', fontsize=20)
	ax.set_ylabel(r'$g(r)$', fontsize=20)
	ax.tick_params(labelsize=20)

	# ax.set_ylim(0,4)

	plt.savefig(dir+"/Lithium_run_gofr.png", dpi=400)
	# plt.show()



