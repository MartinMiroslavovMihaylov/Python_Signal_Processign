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
# 1dB Compression and SDR
# =============================================================================

data = ATC.Compression_Point(path_to_files, 1e9)


# Plot
plt.figure(figsize=(20,10))
plt.plot(data["Pin"], data["Pout linear"], color="black", linewidth = 3, label="Linear fit")
plt.plot(data["Pin"], data["Pout"], color="red", linewidth = 3, label="Measured Pout")
plt.annotate(f'1 dB compression\nPout={data["Pout 1dB"]:.2f} dB',
             xy=(data["Pin 1dB"], data["Pout 1dB"]),               # coordinates on measured Pout
             xytext=(data["Pin 1dB"]+1, data["Pout 1dB"]-14),     # position of the text
             arrowprops=dict(facecolor='blue', shrink=0.05), 
             fontsize=20, color='blue')
plt.xlabel("$P_{In}$ / dB")
plt.ylabel("$P_{Out}$ / dB")
plt.grid(True)
plt.legend(loc="best")
plt.show()



# =============================================================================
# SDR
# =============================================================================

ATC = AnalysisTools()


data = ATC.SignalToDistortionRatio(path_to_files, 1e9)
voltage = np.arange(0,1.6,0.1)

plt.figure(figsize = (10,20))
plt.plot(voltage, data["SDR input"], linewidth = 3, color = "black", label = "SDR Input signal")
plt.plot(voltage[:], data['SDR output'][:], linewidth = 3, color = "red", label = "SDR Output signal")
plt.xlabel("$V_{In_{PP}}$ / GHz")
plt.ylabel("SDR / dB")
plt.legend(loc = "best")
plt.grid()
plt.show()




# =============================================================================
# Plot Spectrum of an signal
# =============================================================================

SDR_data = pd.read_csv(files[0], sep = ",")
ATC = AnalysisTools()

data = ATC.CalcFFT(SDR_data.iloc[:, 2:4], 1e9)
data2 = ATC.CalcFFT(SDR_data.iloc[:, 0:2], 1e9)
freq_array = data["freq"]
Y_array = data["Y"]
Y_array = data["Y_dB"]

freq_array2 = data2["freq"]
Y_array2 = data2["Y"]
Y_array2 = data2["Y_dB"]

f_target1 = 1e9
f_target2 = 3 * 1e9

# Find closest FFT bin
idx1 = np.argmin(np.abs(freq_array - f_target1))
idx2 = np.argmin(np.abs(freq_array - f_target2))

# Return magnitude in dB
Y_first_dB = Y_array[idx1] 
Y_second_dB = Y_array[idx2] 


plt.figure(figsize=(10,6))
plt.plot(freq_array*1e-9, Y_array, label="FFT spectrum BVD")            
plt.plot(freq_array*1e-9, Y_array2, label="FFT spectrum Cascode")            
plt.plot(freq_array[idx1]*1e-9, Y_array[idx1], "go", label="1st harmonic")  
plt.plot(freq_array[idx2]*1e-9, Y_array[idx2], "ro", label="3rd harmonic")  
# plt.yticks(np.arange(-100, 2, 5))
plt.xlabel("Freq (Hz)")
plt.ylabel("Amplitude (dB)")
plt.title("FFT with Harmonics")
plt.grid(True)
plt.legend()
plt.show()



# =============================================================================
# Calculate the THD 
# =============================================================================

THD_vec_in = []
THD_vec_out = []
ATC = AnalysisTools()

voltage = np.arange(0,1.6,0.1)

for i in range(len(files)):
    SDR_data = pd.read_csv(files[i], sep = ",")
    THD = ATC.TotalHarmonicDistortion(SDR_data, 1e9, 5)
    THD_vec_in.append(THD['THD_input_percent'])
    THD_vec_out.append(THD['THD_output_percent'])

plt.figure(figsize = (20,10))
plt.plot(voltage, THD_vec_in, color = "black", linewidth = 3, label = "Input Diff Signal THD")
plt.plot(voltage, THD_vec_out, color = "red", linewidth = 3, label = "Output Diff Signal THD")
plt.xlabel("Voltage/V")
plt.ylabel("THD/%")
plt.legend(loc = "best")
plt.grid()
plt.show()


