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

# Wanted Diffusion Rates [g/L*hr]
fentanyl_wanted_diff = 0.0108 * (micro/milli)
tylenol_wanted_diff = 100.0 * (micro/milli)
lidocaine_wanted_diff = 166.6 * (micro/milli)
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
for drug in drug_folders:
    if drug == "Glucose":
        continue
    # Navigate to the drug's data directory
    cwd_path = os.chdir(pwd_path+data_path+drug)
    drug_txt_files = os.listdir(cwd_path)
    # Pores Counter
    pore_size_counter = 0
    for txt_file in drug_txt_files:
        lines = "-"*25
        print("{:s}{:s}{:s}{:d} [μm]{:s}".format(lines, drug, lines, pores[pore_size_counter], lines))
        # Open txt file with Time and Flux data
        file = open(txt_file, 'r')
        # Extract Time and Flux from txt file - 40 Pores
        time = []
        flux = []
        normalized_flux = []
        for line in file:
            # print(line)
            time.append(float(line.split()[0]))
            flux.append(abs(float(line.split()[1])))
        print(flux)
        # normalized_flux = preprocessing.normalize(flux)
        fig = plt.figure()
        plt.plot(time, flux, label='40 pores')
        # plt.plot(time, normalized_flux, label='normalized')
        plt.grid()
            
        # One Pore and Unit Conversions from [mol/m^3] to [mol/L]
        one_pore_fluxes = []
        for diffusion in range(len(flux)):

            one_pore_fluxes.append(flux[diffusion]*milli/40)
        # print(one_pore_fluxes)
        total_flux_1_pore = sum(one_pore_fluxes)
        # print(total_flux_1_pore)
        # Calculations
        diffusion_rates = []
        total_time = time[-1]   # [hr]
        # print(total_time)
        number_of_pores = [*range(1, 1001, 1)]
        for pore_qty in number_of_pores:
            # fluxes = []
            # for flux in one_pore_fluxes:
            #     if pore_qty > len(one_pore_fluxes):
            #         continue
            #     fluxes.append(flux*(pore_qty))
            diffusion_rates.append(total_flux_1_pore*pore_qty*target_diffusion[target_diffusion_counter])
            # print("#P = {:d}, TarDiffRate = {:.4e}, CalcDiffRate = {:.4e}".format(pore_qty, target_diffusion[target_diffusion_counter], diffusion_rates[pore_qty-1]))
        pore_size_counter += 1
    target_diffusion_counter += 1
    plt.close('all')
