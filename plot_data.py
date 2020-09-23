import os, sys, math
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from sklearn import preprocessing

drugs = ["Fentanyl", "Glucose", "Lidocaine", "Tylenol"]
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
molar_masses_counter = 0
target_diffusion_counter = 0
for drug in drug_folders:
    if drug == "Glucose":
        continue
    # Navigate to the drug's data directory
    cwd_path = os.chdir(pwd_path+data_path+drug)
    drug_txt_files = os.listdir(cwd_path)
    # Plot Pore Size vs. # of Pores for Wanted Diffusion
    drug_pore_numbers = []
    for txt_file in drug_txt_files:
        file = open(txt_file, 'r')
        time = []
        flux = []   # [mol/m^3]
        for line in file:
            time.append(float(line.split()[0]))
            flux.append(abs(float(line.split()[1])))
        # One Pore Conversion and [μg/mL]
        for diffusion in range(len(flux)):
            flux[diffusion] = flux[diffusion]*(milli/40)*(milli/micro)*molar_masses[molar_masses_counter]
        # Calculate the # of Pores for wanted diffusion
        pore_number_counter = 1
        diff_rate = 0
        while (diff_rate < target_diffusion[target_diffusion_counter]):
            diff_rate = sum(flux)*pore_number_counter/time[-1]  # [μg/(mL*hr)]
            pore_number_counter += 1
        if drug == "Fentanyl":
            fentanyl_pore_qty.append(pore_number_counter-1)
        if drug == "Lidocaine":
            lidocaine_pore_qty.append(pore_number_counter-1) 
        if drug == "Tylenol":
            tylenol_pore_qty.append(pore_number_counter-1)   
    os.chdir(pwd_path+image_path+drug)
    fig = plt.figure()
    if drug == "Fentanyl":
        plt.plot(pores_inv, fentanyl_pore_qty, 'o')
    if drug == "Lidocaine":
        plt.plot(pores_inv, lidocaine_pore_qty, 'o') 
    if drug == "Tylenol":
        plt.plot(pores_inv, tylenol_pore_qty, 'o')    
    plt.title("{:s} - {:f} [μg/(mL*hr)]".format(drug, target_diffusion[target_diffusion_counter]))
    plt.xlabel("Pore Diameter [μm]")
    plt.ylabel("Number of Pores")
    plt.grid()
    plt.savefig("{:s}PoreSizeToNumber.png".format(drug))
    plt.close()
    molar_masses_counter += 1
    target_diffusion_counter += 1 
