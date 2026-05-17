import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
from scipy.interpolate import interp1d
from AnalysisTools import AnalysisTools
plt.rcParams.update({"font.size":22})



# =============================================================================
# Load the Analytic Tools Functions 
# =============================================================================

ATC = AnalysisTools()


# =============================================================================
# Eye Diagramm 
# =============================================================================

# Read the csv Data
SDR_data = pd.read_csv(path_to_file, sep = ",")

# Use eye Diagramm function! sim_frequency-> Simulated signal frewquency, move_sig1->move the signal to left and right
Sig = ATC.Eyediagramm(SDR_data, sim_frequency=30e9,move_sig1=35)


plt.figure(figsize=(20, 10))
for i in range(len(Sig['Signal'])-2):
    if i == 0:
        pass
    else:
        plt.plot(Sig['time']*1e12,Sig['cuts'][Sig['Signal'][i]:Sig['Signal'][i+1]], color = "red", linewidth = 3.0)

plt.xlabel("$Time$ / ps")
plt.ylabel("$Amplitude$ / V")
plt.grid()
plt.show()