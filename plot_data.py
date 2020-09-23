# Example for just one pore size sample

import os, sys, math
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from sklearn import preprocessing

drugs = ["Fentanyl", "Glucose", "Lidocaine", "Tylenol"]
pores = [400, 500, 600, 700, 800, 900, 999] # in [μm]

# Magnitude Conversions
milli = 1e-3
micro = 1e-6

# Wanted Diffusion Rates [μg/(mL*hr)]
fentanyl_wanted_diff = 0.0108
tylenol_wanted_diff = 100.0
lidocaine_wanted_diff = 166.6 
target_diffusion = [fentanyl_wanted_diff, lidocaine_wanted_diff, lidocaine_wanted_diff]

# Directories needed
pwd_path = os.path.dirname(os.path.realpath(__file__))
data_path = "/Comsol_Data/"
image_path = "/Images/"
drug_folders = os.listdir(pwd_path+data_path)

# Correction of pore units
poreSizes = []  # list of pores from [μm] to [m]
for pore in pores:
    poreSizes.append(pore*micro)

# Molar masses  [g/mol]
fentanyl_mw = 336.471   
glucose_mw = 180.156   
tylenol_mw = 151.163
lidocaine_mw = 234.34

target_diffusion_counter = 0
# Main Loop
drug_txt_files = []
cwd_path = os.chdir(pwd_path+data_path+drugs[0])
drug_txt_files = os.listdir(cwd_path)

file = open(drug_txt_files[0], 'r')
time = []
flux = []   # [mol/m^3]
for line in file:
    time.append(float(line.split()[0]))
    flux.append(abs(float(line.split()[1])))

for diffusion in range(len(flux)):
    flux[diffusion] = flux[diffusion] * milli * 336.471 * (milli/micro)  # [μg/mL]
    # print("#{:d}\t{:.4e}".format(diffusion,flux[diffusion]))

pore_number_counter = 1
diff_rate = 0
drug_pore_number = []
while (diff_rate < target_diffusion[0]):
    diff_rate = sum(flux) * pore_number_counter / time[-1]    # [μg/(mL*hr)]
    pore_number_counter += 1
drug_pore_number.append(pore_number_counter-1)
print("{:s} Wanted Diffusion: {:.4e} [μg/mL]\t Number of Pores: {:d}\tCalculated Diffusion Rate: {:.4e} [μg/mL]".format(drugs[0], target_diffusion[0], (pore_number_counter-1), diff_rate))

os.chdir(pwd_path+image_path+drugs[0])
fig = plt.figure()
plt.plot(pores[0], pore_number_counter-1, 'o')
plt.title("{:s} - {:f} [μg/(mL*hr)]".format(drugs[0], target_diffusion[0]))
plt.xlabel("Pore Diameter [μm]")
plt.ylabel("Number of Pores")
plt.grid()
plt.savefig("{:s}PoreSizeToNumber.png".format(drugs[0]))
plt.show()
