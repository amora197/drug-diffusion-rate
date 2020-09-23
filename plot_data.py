import os, sys, math, random
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from sklearn import preprocessing

drugs = ["Fentanyl", "Lidocaine", "Tylenol"]
pores = [400, 500, 600, 700, 800, 900, 999] # in [μm]
pores_inv = [999, 900, 800, 700, 600, 500, 400]

# Magnitude Conversions
milli = 1e-3
micro = 1e-6

# Wanted Diffusion Rates [μg/(mL*hr)]
fentanyl_wanted_diff = 0.0108
tylenol_wanted_diff = 100.0
lidocaine_wanted_diff = 166.6
target_diffusion = [fentanyl_wanted_diff, lidocaine_wanted_diff, tylenol_wanted_diff]

# Directories needed
pwd_path = os.path.dirname(os.path.realpath(__file__))
data_path = "/Comsol_Data/"
image_path = "/Images/"
drug_folders = os.listdir(pwd_path+data_path)

# Molar masses  [g/mol]
fentanyl_mw = 336.471   
# glucose_mw = 180.156   
tylenol_mw = 151.163
lidocaine_mw = 234.34
molar_masses = [fentanyl_mw, lidocaine_mw, tylenol_mw]

# Main Loop
drug_txt_files = []
fentanyl_pore_qty = []
lidocaine_pore_qty = []
tylenol_pore_qty = []
pore_qty = [fentanyl_pore_qty, lidocaine_pore_qty, tylenol_pore_qty]

#Navigate to the drug's data directory
cwd_path = os.chdir(pwd_path+data_path+drugs[2])
drug_txt_files = os.listdir(cwd_path)

# Extact data of each txt file
file = open(drug_txt_files[6], 'r')
time = []
flux = []   # [mol/m^3]
for line in file:
    time.append(float(line.split()[0]))
    flux.append(abs(float(line.split()[1])))
# One Pore Conversion and [μg/mL]
for diffusion in range(len(flux)):
    flux[diffusion] = flux[diffusion]*(milli/40)*(milli/micro)*molar_masses[2]/1e-9
# Calculate the # of Pores for wanted diffusion
pore_number_counter = 1
diff_rate = 0
while (diff_rate < target_diffusion[2]):
    diff_rate = sum(flux)*pore_number_counter/time[-1]  # [μg/(mL*hr)]
    pore_number_counter += 1
    print("{:d}\t{:.4e}".format(pore_number_counter,diff_rate))
# pore_qty[2].append(pore_number_counter-1)
 
# print(pore_qty[2])
# for pore_number in range(len(pore_qty[2])):
#     pore_qty[2][pore_number] = pore_qty[2][pore_number] / (1e2)
# print(pore_qty[2])

# Plot Pore Size vs. # of Pores for Wanted Diffusion and Save Image
# cwd_path = os.chdir(pwd_path+image_path+drugs[2])
# fig = plt.figure()
# plt.plot(pores_inv, pore_qty[2], 'o')  
# plt.title("{:s} - {:f} [μg/(mL*hr)] - Circles".format(drugs[2], target_diffusion[2]))
# plt.xlabel("Pore Diameter [μm]")
# plt.ylabel("Number of Pores")
# plt.grid()
# plt.savefig("{:s}PoreSizeToNumber.png".format(drugs[2]))
# plt.close()

# Save Pore Size to # of Pores to txt file
# xarray = np.array(pores_inv)
# yarray = np.array(pore_qty[2])
# # Data in two numpy arrays
# data = np.array([xarray, yarray])
# data = data.T
# # Data transposed to have it in two columns
# datafile_path = str(cwd_path) + "{:s}PoreSizeToNumber.txt".format(drugs[2])
# # Open the ascii file
# with open(datafile_path, 'w+') as datafile_id:
#     np.savetxt(datafile_id, data, fmt=['%d','%d'])
#     # ascii file is written.
#     datafile_id.close
