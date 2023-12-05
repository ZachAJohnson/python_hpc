import matplotlib.pyplot as plt
from pandas import read_csv
import numpy as np

# dir_list = ["numpy","cython_smart","cython_dumb","numba"]
dir_list = ["numba"]
VASP_Luke_data = read_csv("VASP_Luke_data.dat", delim_whitespace=True, header=0)
ri = 3.3137

colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

for dir in dir_list:
	data = read_csv(dir+"/gofr.dat", delim_whitespace=True, header=0)

	fig, ax = plt.subplots(figsize=(8,6))

	# Plot Luke data for reference
	ax.plot(np.array(VASP_Luke_data['r/ri']), np.array(VASP_Luke_data['g(r)']), color='k', label='Luke FM-MD')

	# Plot Quantum Espresso data
	ax.set_title(f"Lithium NVE Quantum Espresso ({dir})", fontsize=20)
	ax.plot(np.array(data['r'])/ri, data['g(r)'],'--',color=colors[0], label=r'QE: $\bar{g}$')
	# ax.errorbar(np.array(data['r'])/ri, data['g(r)'], yerr=data['σ(r)'])
	g_minus_σ = np.array(data['g(r)']) - np.array(data['σ(r)'])
	g_plus_σ  = np.array(data['g(r)']) + np.array(data['σ(r)'])
	ax.fill_between(np.array(data['r'])/ri, g_minus_σ, g_plus_σ, color=colors[0], alpha=0.2, label=r'QE: $\bar{g} \pm\sigma$')

	ax.set_xlabel(r'$r$ [AU]', fontsize=20)
	ax.set_ylabel(r'$g(r)$', fontsize=20)
	ax.tick_params(labelsize=20)

	# ax.set_ylim(0,4)
	# ax.set_xlim(0,10)

	plt.legend(fontsize=13)
	plt.savefig(dir+"/Lithium_run_gofr.png", dpi=400)
	# plt.show()



