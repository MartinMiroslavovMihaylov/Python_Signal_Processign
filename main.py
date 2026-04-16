import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
import tkinter as tk 
from tkinter import filedialog
from scipy.interpolate import interp1d
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from AnalysisTools import AnalysisTools

plt.rcParams.update({"font.size":22})



######################################
# Select and open file/files
######################################

root = tk.Tk()
files = filedialog.askopenfilename(parent=root, title = "select file/s", multiple = True)
root.destroy()




# # ######################################################
# # # S-Parameters
# # ######################################################

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
# S_param = ATC.S_Parameters()


# plt.figure(figsize=(20, 10))
# plt.plot(S_param["Frequency"] * 1e-9 , S_param['S11'], color = "orange", linewidth = 3, label = "S11 with 30$\Omega$ Load")
# plt.plot(S_param["Frequency"] * 1e-9 , S_param['S11'], color = "orange", linewidth = 3, linestyle = "--",  label = "S11 with 50$\Omega$ Load")
# plt.plot(S_param["Frequency"] * 1e-9 , S_param['S22'], color = "green", linewidth = 3, label = "S22 with 30$\Omega$ Load")
# plt.plot(S_param["Frequency"] * 1e-9 , S_param['S22'], color = "green", linewidth = 3, linestyle = "--", label = "S22 with 50$\Omega$ Load")
# plt.plot(S_param["Frequency"] * 1e-9 , S_param['S21'], color = "red", linewidth = 3, label = "S21 with 30$\Omega$ Load")
# plt.plot(S_param["Frequency"] * 1e-9 , S_param['S21'], color = "red", linewidth = 3, linestyle = "--", label = "S21 with 50$\Omega$ Load")
# # plt.plot(S1['S21 dB20 X'] * 1e-9 , S1['S21 dB20 Y'], color = "red", linewidth = 3, label = "S21")
# # plt.plot(S1['S22 dB20 X'] * 1e-9 , S1['S22 dB20 Y'], color = "orange", linewidth = 3, label = "S22")
# plt.xlabel("Freq / GHz")
# plt.ylabel("S-Parameters / dB")
# # plt.annotate('$-3 dB$', xy=(129.2, 1.85), color="black", fontsize=22.0)
# # plt.plot([129.2],[1.71], marker="o", color = "black", markersize=10)
# # labels = ["$f_{-3dB}$ = 127 GHz"]
# plt.legend()
# # plt.legend(loc = "best")
# plt.grid()
# plt.show()



# ######################################################
# # Mixed Mode S-Parameters
# ######################################################

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



# # Parameters = {}
# # Parameters['Frequency'] = S_param['S11 re X']
# # Parameters["S11 Re"] = S_param['S11 re Y']
# # Parameters["S11 Im"] = S_param['S11 im Y']
# # Parameters["S12 Re"] = S_param['S12 re Y']
# # Parameters["S12 Im"] = S_param['S12 im Y']
# # Parameters["S21 Re"] = S_param['S21 re Y']
# # Parameters["S21 Im"] = S_param['S21 im Y']
# # Parameters["S22 Re"] = S_param['S22 re Y']
# # Parameters["S22 Im"] = S_param['S22 im Y']

# ATC = AnalysisTools(Parameters)

# SDD, SDC, SCD ,SCC = ATC.SingleToDiffS_Params()


# plt.figure(figsize=(20,10))
# plt.plot(S_param['S11 re X'] * 1e-9, SDD['SDD11'], color = "red", linewidth = 3, label = "$SDD_{11}$")
# # plt.plot(S_param['S11 re X'] * 1e-9, Sdd11, color = "red", linewidth = 3, label = "$SDD_{11}$")
# plt.plot(S_param['S11 re X'] * 1e-9, SDD['SDD12'], color = "green", linewidth = 3, label = "$SDD_{12}$")
# plt.plot(S_param['S11 re X'] * 1e-9, SDD['SDD21'], color = "blue", linewidth = 3, label = "$SDD_{21}$")
# plt.plot(S_param['S11 re X'] * 1e-9, SDD['SDD22'], color = "orange", linewidth = 3, label = "$SDD_{22}$")
# plt.ylabel("Differential S-Parameters / dB")
# plt.xlabel("Freq / GHz")
# plt.xticks(np.arange(min(S_param['S11 re X'] * 1e-9), max(S_param['S11 re X'] * 1e-9), 25))
# plt.yticks(np.arange(-200, 50, 10))
# plt.legend(loc = "best")
# plt.grid()
# plt.show()





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


# ###################################################
# # Mu and Mu Prime Stability
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
# mu, mu_prime = ATC.muStability()

# plt.figure(figsize=(20,10))
# plt.plot(S_param['S11 re X']*1e-9, mu, color = "red", linewidth = 3, label = "$\mu$")
# plt.plot(S_param['S11 re X']*1e-9, mu_prime, color = "green", linewidth = 3, label = "$\mu$'")
# plt.axhline(1, linestyle = "--", color = "black")
# plt.xlabel("Frequency / $GHz$")
# plt.ylabel("$\mu$ - Stability")
# plt.legend(loc = "best")
# plt.grid()


# # Create inset axes: [x0, y0, width, height] in relative coordinates (0 to 1)
# ax_inset = inset_axes(plt.gca(), width="40%", height="30%", loc='upper right')

# # Plot the same data in the inset
# ax_inset.plot(S_param['S11 re X']*1e-9, mu, linewidth=2, color="red")
# ax_inset.plot(S_param['S11 re X']*1e-9, mu_prime, linewidth=2, color="green")
# ax_inset.axhline(1, linestyle="--", color="black")

# # Set the zoom limits (replace with the region you want to zoom)
# x1, x2 = 1, 250  # example x limits in GHz
# y1, y2 = 0.8, 2.8  # example y limits
# ax_inset.set_xlim(x1, x2)
# ax_inset.set_ylim(y1, y2)
# ax_inset.grid()
# # Show legend under the inset
# # plt.show()

# plt.show()


# #######################################################
# # Characteristic Impedanz
# ######################################################

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
# Zc = ATC.Zc_Calc()

# plt.figure(figsize=(20,10))
# plt.plot(S_param['S11 re X']*1e-9, np.abs(Zc), linewidth=3, color ="red", label = "$Z_{Cdiff}$")
# plt.xlabel("Frequency / $GHz$")
# plt.ylabel("$Z_{C}$ / $\Omega$")
# plt.grid()
# plt.show()




# # #########################################################
# # # 1dB Compression and SDR
# # #########################################################


# ATC = AnalysisTools()

# data = ATC.Compression_Point(files, 1e9)


# # Plot
# plt.figure(figsize=(20,10))
# plt.plot(data["Pin"], data["Pout linear"], color="black", linewidth = 3, label="Linear fit")
# plt.plot(data["Pin"], data["Pout"], color="red", linewidth = 3, label="Measured Pout")
# # plt.scatter(Pin_1dB, Pout_1dB, color="blue", s=100, label=f"1 dB compression\n Pin={Pin_1dB:.2f} dB \n Pout={Pout_1dB:.2f}")
# plt.annotate(f'1 dB compression\nPout={data["Pout 1dB"]:.2f} dB',
#              xy=(data["Pin 1dB"], data["Pout 1dB"]),               # coordinates on measured Pout
#              xytext=(data["Pin 1dB"]+1, data["Pout 1dB"]-14),     # position of the text
#              arrowprops=dict(facecolor='blue', shrink=0.05), 
#              fontsize=20, color='blue')
# plt.xlabel("$P_{In}$ / dB")
# plt.ylabel("$P_{Out}$ / dB")
# plt.grid(True)
# plt.legend(loc="best")
# plt.show()



# #############################################################
# # SDR
# ############################################################


# ATC = AnalysisTools()


# # Sig = pd.read_csv(files[9], sep=",") 
# # d = ATC.ExtractThirdFundamental(Sig.iloc[:, :2], 1e9)

# data = ATC.SignalToDistortionRatio(files, 1e9)
# voltage = np.arange(0,1.6,0.1)

# plt.figure(figsize = (10,20))
# plt.plot(voltage, data["SDR input"], linewidth = 3, color = "black", label = "SDR Input signal")
# plt.plot(voltage[:], data['SDR output'][:], linewidth = 3, color = "red", label = "SDR Output signal")
# plt.xlabel("$V_{In_{PP}}$ / GHz")
# plt.ylabel("SDR / dB")
# plt.legend(loc = "best")
# plt.grid()
# plt.show()




# ########################################
# # Plot Spectrum of an signal
# ########################################

# SDR_data = pd.read_csv(files[9], sep = ",")
# ATC = AnalysisTools()

# data = ATC.CalcFFT(SDR_data.iloc[:, 2:4], 1e9)
# freq_array = data["freq"]
# Y_array = data["Y"]
# Y_array = data["Y_dB"]

# f_target1 = 1e9
# f_target2 = 3 * 1e9

# # Find closest FFT bin
# idx1 = np.argmin(np.abs(freq_array - f_target1))
# idx2 = np.argmin(np.abs(freq_array - f_target2))

# # Return magnitude in dB
# Y_first_dB = Y_array[idx1] 
# Y_second_dB = Y_array[idx2] 


# plt.figure(figsize=(10,6))
# plt.plot(freq_array, Y_array, label="FFT spectrum")            
# plt.plot(freq_array[idx1], Y_array[idx1], "go", label="1st harmonic")  
# plt.plot(freq_array[idx2], Y_array[idx2], "ro", label="3rd harmonic")  
# # plt.yticks(np.arange(-100, 2, 5))
# plt.xlabel("Freq (Hz)")
# plt.ylabel("Amplitude (dB)")
# plt.title("FFT with Harmonics")
# plt.grid(True)
# plt.legend()
# plt.show()



# ######################################
# # Calculate the THD 
# ######################################

# THD_vec_in = []
# THD_vec_out = []
# ATC = AnalysisTools()

# for i in range(len(files)):
#     SDR_data = pd.read_csv(files[i], sep = ",")
#     THD = ATC.TotalHarmonicDistortion(SDR_data, 1e9, 5)
#     THD_vec_in.append(THD['THD_input_percent'])
#     THD_vec_out.append(THD['THD_output_percent'])

# plt.figure(figsize = (10,20))
# plt.plot(voltage, THD_vec_in, color = "black", linewidth = 3, label = "Input Diff Signal THD")
# plt.plot(voltage, THD_vec_out, color = "red", linewidth = 3, label = "Output Diff Signal THD")
# plt.xlabel("Voltage/V")
# plt.ylabel("THD/%")
# plt.legend(loc = "best")
# plt.grid()
# plt.show()



# ######################################################
# # Eye Diagramm 
# ######################################################

# ATC = AnalysisTools()
# SDR_data = pd.read_csv(files[0], sep = ",")

# Sig = ATC.Eyediagramm(SDR_data, sim_frequency=140e9)
# # move_sig1 = -15, move_sig2 = -15

# plt.figure(figsize=(20, 10))
# for i in range(len(Sig['Signal'])-2):
#     if i == 0:
#         pass
#     else:
#         plt.plot(Sig['time']*1e12,Sig['cuts'][Sig['Signal'][i]:Sig['Signal'][i+1]], color = "red", linewidth = 3.0)
#         # plt.plot(Sig['time']*1e12,Sig['cuts_sig1'][Sig['Signal1'][i]:Sig['Signal1'][i+1]], color = "red", linewidth = 3.0)
#         # plt.plot(Sig['time']*1e12,Sig['cuts_sig2'][Sig['Signal2'][i]:Sig['Signal2'][i+1]], color = "gold", linewidth = 3.0)

# plt.xlabel("$Time$ / ps")
# plt.ylabel("$Amplitude$ / V")
# # labels = ["Single Ended Eye Diagram EM Sim"]
# # plt.legend(labels, loc = "lower right")
# # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# # plt.yticks(np.arange(-2, 2, 0.5))
# # plt.xticks(np.arange(0, startInd*1e12 + ((samples_perT*1e12)*10e-2), (samples_perT*1e12)*10e-2))
# # plt.tight_layout()
# plt.grid()
# plt.show()





# # #########################################
# # # Plot ft vs ic 
# # #########################################


# ATC = AnalysisTools()

# # plt.figure(figsize = (20,20))
# # for file in files:
# #     _data = ATC.extract_csv_data(file)
# #     plt.plot(_data["col3"]*1e3 , _data["col1"]*1e-9, linewidth = 3, label = f"{files[0].split("/")[-1].split(".")[0]}")
# #     id_max = np.argmax(_data["col1"]*1e-9)
# # plt.xlabel("ic / $mA$")
# # plt.ylabel("ft / $GHz$")
# # plt.legend(loc = "best")
# # plt.grid()
# # plt.show()



# plt.figure(figsize = (20,20))

# _data = ATC.extract_csv_data(files[0])


# num_cols = len(_data)

# plt.figure(figsize = (20,20))
# for i in range(0, num_cols, 2):
#     EF_num = i // 2 + 1 
#     plt.plot(_data[f"col{i}"]*1e3 , _data[f"col{i+1}"]*1e-9, linewidth = 3, label = f"Sweep EF {EF_num}")
# plt.xlabel("ic / $mA$")
# plt.ylabel("ft / $GHz$")
# plt.legend(loc = "best")
# plt.grid()
# plt.show()






# ##########################
# # Gain Plots
# ##########################


# ATC = AnalysisTools()
# _data = ATC.extract_csv_data(files[0])


# plt.figure()
# plt.plot(_data['col0']*1e-9, _data['col1'], linewidth = 3, color = "red", label = "Gain EM sim")
# plt.annotate('$-3 dB$', xy=(155.0, 5.4), color="black", fontsize=22.0)
# plt.plot([152.0],[5.4], marker="o", color = "black", markersize=10)
# labels = ["$f_{-3dB}$ = 152 GHz"]
# # h2 = Line2D([0], [0], marker='o', markersize=np.sqrt(20), color='black', linestyle='None')
# # Lin = plt.legend([h2], ['$-3dB$ Grenzfrequenz'], loc="lower left", markerscale=2, scatterpoints=1)
# plt.xlabel("$Frequency$ / GHz")
# plt.ylabel("$Gain$ / dB")
# plt.legend(labels, loc = 'best')
# # plt.gca().add_artist(Lin)
# # plt.tight_layout()
# plt.grid()
# plt.show()













