import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
from scipy.interpolate import interp1d
from AnalysisTools import AnalysisTools
plt.rcParams.update({"font.size":22})


# =============================================================================
# S-Parameters
# =============================================================================

S_param = pd.read_csv(path_to_file, sep = ",")

# Put the S-PArameters into dictionary, is easy to work with later on. 
Parameters = {}
Parameters['Frequency'] = S_param['S11 re X']
Parameters["S11 Re"] = S_param['S11 re Y']
Parameters["S11 Im"] = S_param['S11 im Y']
Parameters["S12 Re"] = S_param['S12 re Y']
Parameters["S12 Im"] = S_param['S12 im Y']
Parameters["S13 Re"] = S_param['S13 re Y']
Parameters["S13 Im"] = S_param['S13 im Y']
Parameters["S14 Re"] = S_param['S14 re Y']
Parameters["S14 Im"] = S_param['S14 im Y']
Parameters["S21 Re"] = S_param['S21 re Y']
Parameters["S21 Im"] = S_param['S21 im Y']
Parameters["S22 Re"] = S_param['S22 re Y']
Parameters["S22 Im"] = S_param['S22 im Y']
Parameters["S23 Re"] = S_param['S23 re Y']
Parameters["S23 Im"] = S_param['S23 im Y']
Parameters["S24 Re"] = S_param['S24 re Y']
Parameters["S24 Im"] = S_param['S24 im Y']
Parameters["S31 Re"] = S_param['S31 re Y']
Parameters["S31 Im"] = S_param['S31 im Y']
Parameters["S32 Re"] = S_param['S32 re Y']
Parameters["S32 Im"] = S_param['S32 im Y']
Parameters["S33 Re"] = S_param['S33 re Y']
Parameters["S33 Im"] = S_param['S33 im Y']
Parameters["S34 Re"] = S_param['S34 re Y']
Parameters["S34 Im"] = S_param['S34 im Y']
Parameters["S41 Re"] = S_param['S41 re Y']
Parameters["S41 Im"] = S_param['S41 im Y']
Parameters["S42 Re"] = S_param['S42 re Y']
Parameters["S42 Im"] = S_param['S42 im Y']
Parameters["S43 Re"] = S_param['S43 re Y']
Parameters["S43 Im"] = S_param['S43 im Y']
Parameters["S44 Re"] = S_param['S44 re Y']
Parameters["S44 Im"] = S_param['S44 im Y']


# Load the class and the functions 
ATC = AnalysisTools(Parameters)
S_param = ATC.S_Parameters()


plt.figure(figsize=(20, 10))
plt.plot(S_param["Frequency"] * 1e-9 , S_param['S11'], color = "orange", linewidth = 3, label = "S11 with 30$\Omega$ Load")
plt.plot(S_param["Frequency"] * 1e-9 , S_param['S11'], color = "orange", linewidth = 3, linestyle = "--",  label = "S11 with 50$\Omega$ Load")
plt.plot(S_param["Frequency"] * 1e-9 , S_param['S22'], color = "green", linewidth = 3, label = "S22 with 30$\Omega$ Load")
plt.plot(S_param["Frequency"] * 1e-9 , S_param['S22'], color = "green", linewidth = 3, linestyle = "--", label = "S22 with 50$\Omega$ Load")
plt.plot(S_param["Frequency"] * 1e-9 , S_param['S21'], color = "red", linewidth = 3, label = "S21 with 30$\Omega$ Load")
plt.plot(S_param["Frequency"] * 1e-9 , S_param['S21'], color = "red", linewidth = 3, linestyle = "--", label = "S21 with 50$\Omega$ Load")
plt.xlabel("Freq / GHz")
plt.ylabel("S-Parameters / dB")
plt.legend()
plt.grid()
plt.show()



# =============================================================================
# Mixed Mode S-Parameters
# =============================================================================

S_param = pd.read_csv(path_to_files, sep = ",")


Parameters = {}
Parameters['Frequency'] = S_param['S11 re X']
Parameters["S11 Re"] = S_param['S11 re Y']
Parameters["S11 Im"] = S_param['S11 im Y']
Parameters["S12 Re"] = S_param['S12 re Y']
Parameters["S12 Im"] = S_param['S12 im Y']
Parameters["S13 Re"] = S_param['S13 re Y']
Parameters["S13 Im"] = S_param['S13 im Y']
Parameters["S14 Re"] = S_param['S14 re Y']
Parameters["S14 Im"] = S_param['S14 im Y']
Parameters["S21 Re"] = S_param['S21 re Y']
Parameters["S21 Im"] = S_param['S21 im Y']
Parameters["S22 Re"] = S_param['S22 re Y']
Parameters["S22 Im"] = S_param['S22 im Y']
Parameters["S23 Re"] = S_param['S23 re Y']
Parameters["S23 Im"] = S_param['S23 im Y']
Parameters["S24 Re"] = S_param['S24 re Y']
Parameters["S24 Im"] = S_param['S24 im Y']
Parameters["S31 Re"] = S_param['S31 re Y']
Parameters["S31 Im"] = S_param['S31 im Y']
Parameters["S32 Re"] = S_param['S32 re Y']
Parameters["S32 Im"] = S_param['S32 im Y']
Parameters["S33 Re"] = S_param['S33 re Y']
Parameters["S33 Im"] = S_param['S33 im Y']
Parameters["S34 Re"] = S_param['S34 re Y']
Parameters["S34 Im"] = S_param['S34 im Y']
Parameters["S41 Re"] = S_param['S41 re Y']
Parameters["S41 Im"] = S_param['S41 im Y']
Parameters["S42 Re"] = S_param['S42 re Y']
Parameters["S42 Im"] = S_param['S42 im Y']
Parameters["S43 Re"] = S_param['S43 re Y']
Parameters["S43 Im"] = S_param['S43 im Y']
Parameters["S44 Re"] = S_param['S44 re Y']
Parameters["S44 Im"] = S_param['S44 im Y']



# Load the class and the functions 
ATC = AnalysisTools(Parameters)
SDD, SDC, SCD ,SCC = ATC.SingleToDiffS_Params()


plt.figure(figsize=(20,10))
plt.plot(S_param['S11 re X'] * 1e-9, SDD['SDD11'], color = "red", linewidth = 3, label = "$SDD_{11}$")
plt.plot(S_param['S11 re X'] * 1e-9, SDD['SDD12'], color = "green", linewidth = 3, label = "$SDD_{12}$")
plt.plot(S_param['S11 re X'] * 1e-9, SDD['SDD21'], color = "blue", linewidth = 3, label = "$SDD_{21}$")
plt.plot(S_param['S11 re X'] * 1e-9, SDD['SDD22'], color = "orange", linewidth = 3, label = "$SDD_{22}$")
plt.ylabel("Differential S-Parameters / dB")
plt.xlabel("Freq / GHz")
plt.xticks(np.arange(min(S_param['S11 re X'] * 1e-9), max(S_param['S11 re X'] * 1e-9), 25))
plt.yticks(np.arange(-200, 50, 10))
plt.legend(loc = "best")
plt.grid()
plt.show()




# ###################################################
# # Group Delay
# ###################################################

# S_param = pd.read_csv(files[0], sep = ",")

# columns = S_param.columns

# Parameters = {}
# Parameters['Frequency'] = S_param['S11 re X']
# Parameters["S11 Re"] = S_param['S11 re Y']
# Parameters["S11 Im"] = S_param['S11 im Y']
# Parameters["S12 Re"] = S_param['S12 re Y']
# Parameters["S12 Im"] = S_param['S12 im Y']
# Parameters["S13 Re"] = S_param['S13 re Y']
# Parameters["S13 Im"] = S_param['S13 im Y']
# Parameters["S14 Re"] = S_param['S14 re Y']
# Parameters["S14 Im"] = S_param['S14 im Y']
# Parameters["S21 Re"] = S_param['S21 re Y']
# Parameters["S21 Im"] = S_param['S21 im Y']
# Parameters["S22 Re"] = S_param['S22 re Y']
# Parameters["S22 Im"] = S_param['S22 im Y']
# Parameters["S23 Re"] = S_param['S23 re Y']
# Parameters["S23 Im"] = S_param['S23 im Y']
# Parameters["S24 Re"] = S_param['S24 re Y']
# Parameters["S24 Im"] = S_param['S24 im Y']
# Parameters["S31 Re"] = S_param['S31 re Y']
# Parameters["S31 Im"] = S_param['S31 im Y']
# Parameters["S32 Re"] = S_param['S32 re Y']
# Parameters["S32 Im"] = S_param['S32 im Y']
# Parameters["S33 Re"] = S_param['S33 re Y']
# Parameters["S33 Im"] = S_param['S33 im Y']
# Parameters["S34 Re"] = S_param['S34 re Y']
# Parameters["S34 Im"] = S_param['S34 im Y']
# Parameters["S41 Re"] = S_param['S41 re Y']
# Parameters["S41 Im"] = S_param['S41 im Y']
# Parameters["S42 Re"] = S_param['S42 re Y']
# Parameters["S42 Im"] = S_param['S42 im Y']
# Parameters["S43 Re"] = S_param['S43 re Y']
# Parameters["S43 Im"] = S_param['S43 im Y']
# Parameters["S44 Re"] = S_param['S44 re Y']
# Parameters["S44 Im"] = S_param['S44 im Y']


# ATC = AnalysisTools(Parameters)
# tau = ATC.GroupDelay()

# plt.figure(figsize=(20,10))
# plt.plot(S_param['S11 re X']*1e-9, tau['g21'], color = "red", linewidth = 3, label = "Group Delay $S_{21}$")
# plt.xlabel("Frequency / $GHz$")
# plt.ylabel("Group Delay / $ps$")
# plt.legend(loc="best")
# plt.grid()
# plt.show()


# =============================================================================
# Mu and Mu Prime Stability
# =============================================================================

S_param = pd.read_csv(path_to_files, sep = ",")


Parameters = {}
Parameters['Frequency'] = S_param['S11 re X']
Parameters["S11 Re"] = S_param['S11 re Y']
Parameters["S11 Im"] = S_param['S11 im Y']
Parameters["S12 Re"] = S_param['S12 re Y']
Parameters["S12 Im"] = S_param['S12 im Y']
Parameters["S13 Re"] = S_param['S13 re Y']
Parameters["S13 Im"] = S_param['S13 im Y']
Parameters["S14 Re"] = S_param['S14 re Y']
Parameters["S14 Im"] = S_param['S14 im Y']
Parameters["S21 Re"] = S_param['S21 re Y']
Parameters["S21 Im"] = S_param['S21 im Y']
Parameters["S22 Re"] = S_param['S22 re Y']
Parameters["S22 Im"] = S_param['S22 im Y']
Parameters["S23 Re"] = S_param['S23 re Y']
Parameters["S23 Im"] = S_param['S23 im Y']
Parameters["S24 Re"] = S_param['S24 re Y']
Parameters["S24 Im"] = S_param['S24 im Y']
Parameters["S31 Re"] = S_param['S31 re Y']
Parameters["S31 Im"] = S_param['S31 im Y']
Parameters["S32 Re"] = S_param['S32 re Y']
Parameters["S32 Im"] = S_param['S32 im Y']
Parameters["S33 Re"] = S_param['S33 re Y']
Parameters["S33 Im"] = S_param['S33 im Y']
Parameters["S34 Re"] = S_param['S34 re Y']
Parameters["S34 Im"] = S_param['S34 im Y']
Parameters["S41 Re"] = S_param['S41 re Y']
Parameters["S41 Im"] = S_param['S41 im Y']
Parameters["S42 Re"] = S_param['S42 re Y']
Parameters["S42 Im"] = S_param['S42 im Y']
Parameters["S43 Re"] = S_param['S43 re Y']
Parameters["S43 Im"] = S_param['S43 im Y']
Parameters["S44 Re"] = S_param['S44 re Y']
Parameters["S44 Im"] = S_param['S44 im Y']


# Load the class and the functions 
ATC = AnalysisTools(Parameters)
mu, mu_prime = ATC.muStability()

plt.figure(figsize=(20,10))
plt.plot(S_param['S11 re X']*1e-9, mu, color = "red", linewidth = 3, label = "$\mu$")
plt.plot(S_param['S11 re X']*1e-9, mu_prime, color = "green", linewidth = 3, label = "$\mu$'")
plt.axhline(1, linestyle = "--", color = "black")
plt.xlabel("Frequency / $GHz$")
plt.ylabel("$\mu$ - Stability")
plt.legend(loc = "best")
plt.grid()


# Create inset axes: [x0, y0, width, height] in relative coordinates (0 to 1)
ax_inset = inset_axes(plt.gca(), width="40%", height="30%", loc='upper right')

# Plot the same data in the inset
ax_inset.plot(S_param['S11 re X']*1e-9, mu, linewidth=2, color="red")
ax_inset.plot(S_param['S11 re X']*1e-9, mu_prime, linewidth=2, color="green")
ax_inset.axhline(1, linestyle="--", color="black")

# Set the zoom limits (replace with the region you want to zoom)
x1, x2 = 1, 250  # example x limits in GHz
y1, y2 = 0.8, 2.8  # example y limits
ax_inset.set_xlim(x1, x2)
ax_inset.set_ylim(y1, y2)
ax_inset.grid()

plt.show()


# =============================================================================
# Characteristic Impedanz
# =============================================================================

S_param = pd.read_csv(path_to_files, sep = ",")



Parameters = {}
Parameters['Frequency'] = S_param['S11 re X']
Parameters["S11 Re"] = S_param['S11 re Y']
Parameters["S11 Im"] = S_param['S11 im Y']
Parameters["S12 Re"] = S_param['S12 re Y']
Parameters["S12 Im"] = S_param['S12 im Y']
Parameters["S13 Re"] = S_param['S13 re Y']
Parameters["S13 Im"] = S_param['S13 im Y']
Parameters["S14 Re"] = S_param['S14 re Y']
Parameters["S14 Im"] = S_param['S14 im Y']
Parameters["S21 Re"] = S_param['S21 re Y']
Parameters["S21 Im"] = S_param['S21 im Y']
Parameters["S22 Re"] = S_param['S22 re Y']
Parameters["S22 Im"] = S_param['S22 im Y']
Parameters["S23 Re"] = S_param['S23 re Y']
Parameters["S23 Im"] = S_param['S23 im Y']
Parameters["S24 Re"] = S_param['S24 re Y']
Parameters["S24 Im"] = S_param['S24 im Y']
Parameters["S31 Re"] = S_param['S31 re Y']
Parameters["S31 Im"] = S_param['S31 im Y']
Parameters["S32 Re"] = S_param['S32 re Y']
Parameters["S32 Im"] = S_param['S32 im Y']
Parameters["S33 Re"] = S_param['S33 re Y']
Parameters["S33 Im"] = S_param['S33 im Y']
Parameters["S34 Re"] = S_param['S34 re Y']
Parameters["S34 Im"] = S_param['S34 im Y']
Parameters["S41 Re"] = S_param['S41 re Y']
Parameters["S41 Im"] = S_param['S41 im Y']
Parameters["S42 Re"] = S_param['S42 re Y']
Parameters["S42 Im"] = S_param['S42 im Y']
Parameters["S43 Re"] = S_param['S43 re Y']
Parameters["S43 Im"] = S_param['S43 im Y']
Parameters["S44 Re"] = S_param['S44 re Y']
Parameters["S44 Im"] = S_param['S44 im Y']


# Load the class and the functions 
ATC = AnalysisTools(Parameters)
Zc = ATC.Zc_Calc()

plt.figure(figsize=(20,10))
plt.plot(S_param['S11 re X']*1e-9, np.abs(Zc), linewidth=3, color ="red", label = "$Z_{Cdiff}$")
plt.xlabel("Frequency / $GHz$")
plt.ylabel("$Z_{C}$ / $\Omega$")
plt.grid()
plt.show()


