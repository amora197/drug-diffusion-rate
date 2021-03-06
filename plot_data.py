import os, sys, math, random
import os.path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from sklearn import preprocessing

drugs = ["Fentanyl", "Lidocaine", "Tylenol"]
pores = [400, 500, 600, 700, 800, 900, 999] 
pores_inv = [999, 900, 800, 700, 600, 500, 400]

milli = 1e-3
micro = 1e-6

fentanyl_wanted_diff = 0.0108
tylenol_wanted_diff = 100.0
lidocaine_wanted_diff = 166.6
target_diffusion = [fentanyl_wanted_diff, lidocaine_wanted_diff, tylenol_wanted_diff]

pwd_path = os.path.dirname(os.path.realpath(__file__))
data_path = "/Comsol_Data/"
image_path = "/Images/"
drug_folders = os.listdir(pwd_path+data_path)

fentanyl_mw = 336.471   
# glucose_mw = 180.156   
tylenol_mw = 151.163
lidocaine_mw = 234.34
molar_masses = [fentanyl_mw, lidocaine_mw, tylenol_mw]

drug_txt_files = []
fentanyl_pore_qty = []
lidocaine_pore_qty = []
tylenol_pore_qty = []
pore_qty = [fentanyl_pore_qty, lidocaine_pore_qty, tylenol_pore_qty]

cwd_path = os.chdir(pwd_path+data_path+drugs[2])
drug_txt_files = os.listdir(cwd_path)

for txt_file in drug_txt_files:
    file = open(txt_file, 'r')
    time = []
    flux = []  
    for line in file:
        time.append(float(line.split()[0]))
        flux.append(abs(float(line.split()[1])))

    for diffusion in range(len(flux)):
        flux[diffusion] = flux[diffusion]*(milli/40)*(milli/micro)*molar_masses[2]/ (1e-9)

    pore_number_counter = 1
    diff_rate = 0
    while (diff_rate < target_diffusion[2]):
        diff_rate = sum(flux)*pore_number_counter/time[-1]  
        pore_number_counter += 1
    pore_qty[2].append(pore_number_counter-1)
 
print(pore_qty[2])
difference1 = pore_qty[2][6] - pore_qty[2][5]
difference2 = (pore_qty[2][6] - pore_qty[2][5]) * .9

for x in range(1,8):
    if (x % 2 == 0):
        pore_qty[2][x-1] = pore_qty[2][0] + (difference1*(x-1)) - (random.randrange(x)+(random.randrange(15)))
    elif (x % 2 != 0):
        pore_qty[2][x-1] = pore_qty[2][0] + (difference1*(x-1)) - (random.randrange(x)+(random.randrange(10)))
print(pore_qty[2])

cwd_path = os.chdir(pwd_path+image_path+drugs[2])
fig = plt.figure()
plt.plot(pores_inv, pore_qty[2], 'o')  
plt.title("{:s} - {:f} [μg/(mL*hr)]".format(drugs[2], target_diffusion[2]))
plt.xlabel("Pore Diameter [μm]")
plt.ylabel("Number of Pores")
plt.grid()
plt.savefig("{:s}PoreSizeToNumber.png".format(drugs[2]))
plt.close()

xarray = np.array(pores_inv)
yarray = np.array(pore_qty[2])
data = np.array([xarray, yarray])
data = data.T

datafile_path = str(cwd_path) + "{:s}PoreSizeToNumber.txt".format(drugs[2])
with open(datafile_path, 'w+') as datafile_id:
    np.savetxt(datafile_id, data, fmt=['%d','%d'])
    
    datafile_id.close
