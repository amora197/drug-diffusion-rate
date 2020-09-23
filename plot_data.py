# 40 Pores Only, 3 Drugs, 12 Hours
import os, sys, math
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

drugs = ["Fentanyl", "Glucose", "Lidocaine", "Tylenol"]
pores = [400, 500, 600, 700, 800, 900, 999]    # in [μm]
temperature = 300   # Kelvin
milli = 1e-3   
micro = 1e-6
diff_coef = 1e-11   # [m^2/s] for Fentanyl 
concentration_ini = 0.594 * milli  # [mol/L] for Fentanyl

# Wanted diffusion rates [g/L*hr]
fentanyl_wanted_diff = 0.0108 * (micro/milli)
tylenol_wanted_diff = 100.0 * (micro/milli)
lidocaine_wanted_diff = 166.6 * (micro/milli)


# Molar masses  [g/mol]
fentanyl_mw = 336.471   
glucose_mw = 180.156   
tylenol_mw = 151.163
lidocaine_mw = 234.34 

poreSizes = []  # sizes in [μm]
poreAreas = []  # area in [m^2]
for pore in pores:
    poreSizes.append(pore*micro)
for pore in poreSizes:    
    poreAreas.append(math.pi*((pore/2)**2))

# for x in range(0,3):    # 3 is not included
#     print("We're on time %d" % (x))

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = "/Comsol_Data/40Pores_%s/" % drugs[2]
image_path = "/Comsol_Data/Images/"
file = "40Pores%dDiff.txt" % pores[0]
files = os.listdir(dir_path+data_path)

print(files)

os.chdir(dir_path + file_path)
f = open(files[0], "r")
time = []
diffusion = []
for line in f:
    time.append(float(line.split()[0]))
    diffusion.append(abs(float(line.split()[1])))

# Conversion from [mol/m^3] to [mol/L]
for flux in range(len(diffusion)):
    diffusion[flux] = diffusion[flux] * milli

# Calculations
total_time = time[-1]
diff_ave = sum(diffusion)/float(len(diffusion)) # 40 pores from COMSOL
print("Average Diffusion = {:.4e}\tTotal Time = {:.1f}".format(diff_ave, total_time))
diffusion_rate = (sum(diffusion)*151.163)/(total_time)  # [g/(L*hr)]
print("Diffusion Rate = {:.4e} ".format(diffusion_rate))
print("Wanted Diffusion Rate for {:s} = {:.4e} [g/(L*hr)]".format(drugs[0], fentanyl_wanted_diff))

one_pore_diff = diffusion_rate / 40
print("One pore average diffusion rate = {:.4e} [g/(L*hr)]".format(one_pore_diff))

pore_size_400 = {}
diff_per_num_pores = []
number_of_pores = [*range(1, 1001, 1)]
for pore in number_of_pores:
    diff_per_num_pores.append(one_pore_diff*pore)
    pore_size_400["{:d}".format(pore)] = diff_per_num_pores[pore-1]

print(pore_size_400)
    
print("{:d} Number of pores diffusiont rate = {:.4e}".format(number_of_pores[-1], diff_per_num_pores[-1]))


# diffusion_02 = []
# for value in range(len(diffusion)):
#     diffusion_02.append(diffusion[value]/40)
#     pore_size_400["{:d}".format(value)] = diffusion_02[value]

# fluxes = []
# # for flux in one_pore_diff:

# # Plotting
# fig = plt.figure()
# # for value in range(len(one_pore_diff)):
# plt.plot(time, fluxes[value], label='40')
# plt.xlabel("Time [hr]")
# plt.ylabel("Flux [mol/L]")
# plt.title("%s Diffusion, %d [μm] Diameter" % (drugs[0], pores[0]))
# plt.legend(title='Pore #', loc='upper right')
# plt.grid(which='major', axis='both', linestyle='dotted')
# plt.show()


# f.close()

print(sum(diffusion)/total_time)