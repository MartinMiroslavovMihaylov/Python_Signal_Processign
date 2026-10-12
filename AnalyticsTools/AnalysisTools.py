import numpy as np 
from scipy.interpolate import interp1d
from numpy import polyfit, polyval
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size":22})




class AnalysisTools:
    '''
    
    Analysis tools for RF / microwave S-parameter processing.

    This class provides methods for calculating:
    - Characteristic impedance
    - Stability parameters
    - Mixed-mode S-parameters (4-port to 2-port reduction)
    - Maximum current density for IHP technologies (G2, G3, G2Cu, G3Cu)

    The class supports both 2-port and 4-port S-parameter datasets.

    Notes
    -----
    The input must be provided as a dictionary containing real and imaginary
    parts of the S-parameters in the following format:

    For example:
    - 'S11 Re', 'S11 Im'
    - 'S12 Re', 'S12 Im'
    - ...

    Depending on the number of keys:
    - 9 keys  -> 2-port network
    - 33 keys -> 4-port network

    Raises
    ------
    ValueError
        If the input dictionary does not match a supported format.
  

    How to set the Simulation Testbench
                           __________
            Port 1 o------|          |-----o Port 2
                          |   DUT    |
            Port 3 o------|__________|-----o Port 4    
                         
                           __________
                          |          |
            Port 1 o------|  DUT     |-----O Port 2
                          |__________|

    '''

    def __init__(self, Parameters=None):
        """
        Initialize AnalysisTools with S-parameter data.

        Parameters
        ----------
        Parameters : dict, optional
            Dictionary containing S-parameters with real and imaginary parts.
            Must include at least the key 'Frequency'.

        Examples
        --------
        For a 2-port device:

        {
            'Frequency': ...,
            'S11 Re': ..., 'S11 Im': ...,
            'S12 Re': ..., 'S12 Im': ...,
            'S21 Re': ..., 'S21 Im': ...,
            'S22 Re': ..., 'S22 Im': ...
        }
        """

        if Parameters is not None:
            
            self.Parameters_size = None
            # extract frequency from S-Parameters, it is important for 2 and 4 port S-Parameters
            self.frequency = Parameters['Frequency']



            # check if it is an two port or four port parameters
            if len(Parameters.keys()) == 33:
                self.Parameters_size = 4
                self.S11_re = Parameters['S11 Re']
                self.S11_im = Parameters["S11 Im"]
                self.S12_re = Parameters['S12 Re']
                self.S12_im = Parameters["S12 Im"]
                self.S13_re = Parameters['S13 Re']
                self.S13_im = Parameters["S13 Im"]
                self.S14_re = Parameters['S14 Re']
                self.S14_im = Parameters["S14 Im"]
                self.S21_re = Parameters['S21 Re']
                self.S21_im = Parameters["S21 Im"]
                self.S22_re = Parameters['S22 Re']
                self.S22_im = Parameters["S22 Im"]
                self.S23_re = Parameters['S23 Re']
                self.S23_im = Parameters["S23 Im"]
                self.S24_re = Parameters['S24 Re']
                self.S24_im = Parameters["S24 Im"]
                self.S31_re = Parameters['S31 Re']
                self.S31_im = Parameters["S31 Im"]
                self.S32_re = Parameters['S32 Re']
                self.S32_im = Parameters["S32 Im"]
                self.S33_re = Parameters['S33 Re']
                self.S33_im = Parameters["S33 Im"]
                self.S34_re = Parameters['S34 Re']
                self.S34_im = Parameters["S34 Im"]
                self.S41_re = Parameters['S41 Re']
                self.S41_im = Parameters["S41 Im"]
                self.S42_re = Parameters['S42 Re']
                self.S42_im = Parameters["S42 Im"]
                self.S43_re = Parameters['S43 Re']
                self.S43_im = Parameters["S43 Im"]
                self.S44_re = Parameters['S44 Re']
                self.S44_im = Parameters['S44 Im']

            elif len(Parameters.keys()) == 9:
                self.Parameters_size = 2
                self.S11_re = Parameters['S11 Re']
                self.S11_im = Parameters["S11 Im"]
                self.S12_re = Parameters['S12 Re']
                self.S12_im = Parameters["S12 Im"]
                self.S21_re = Parameters['S21 Re']
                self.S21_im = Parameters["S21 Im"]
                self.S22_re = Parameters['S22 Re']
                self.S22_im = Parameters["S22 Im"]

            else:
                raise ValueError(
                    "Input must contain S-parameters in the form Re{Sij} and Im{Sij}. "
                    "Only 2-port and 4-port networks are supported."
                )
            
        else:
            pass


    ##############################################
    # Current Metal Densisty Calculator IHP G3/G2
    ##############################################


    def MetalDensities_G3(self, Metal, Width):
        """
        Calculate the maximum current metal density of IHP G2 and G3 technologies.

        Parameters
        ----------
        Material : str
            Name of the metal for which the maximum current density is calculated.
            Supported values are:
            ['M1', 'M2', 'M3', 'M4', 'M5', 'TM1', 'TM2'].

            Example:
            Material = "M2"

        Width : int or float
            Width of the metal as defined in the Virtuoso layout editor.

        Returns
        -------
        MaxCurrent : float
            Maximum current allowed for the selected metal.

        Raises
        ------
        ValueError
            If an unsupported metal type is provided.

        """

        MetalList = ["M1", "M2", "M3", "M4", "M5", "TM1", "TM2"]

        if Metal in MetalList:
            if Metal == "M1":
                MaxCurrent = 1*(Width*0.42)
            elif Metal == "M2" or Metal == "M3" or Metal == "M4" or Metal == "M5":
                MaxCurrent = 2 * (Width * 0.49)
            elif Metal == "TM1":
                MaxCurrent = 7.5 * (Width * 2)
            elif Metal == "TM2":
                MaxCurrent = 5.33333 * (Width * 3)
        else:
            raise ValueError('Metals can be choosen from: "M1", "M2", "M3", "M4", "M5", "TM1", "TM2" !!!')

        return MaxCurrent




    #################################################
    # Current Metal Densisty Calculator IHP G3Cu/G2Cu
    #################################################


    def MetalDensities_G3Cu(self, Metal,Width):
        """
        Calculate the maximum current metal density of IHP G2Cu and G3Cu technologies.

        Parameters
        ----------
        Material : str
            Name of the metal for which the maximum current density is calculated.
            Supported values are:
            ['M1', 'M2', 'M3', 'M4', 'TC1', 'TC2', 'ThinAl', 'ThickAl'].

            Example:
            Material = "M2"

        Width : int or float
            Width of the metal as defined in the Virtuoso layout editor.

        Returns
        -------
        MaxCurrent : float
            Maximum current allowed for the selected metal.

        Raises
        ------
        ValueError
            If an unsupported metal type is provided.

        """

        MetalList = ["M1", "M2", "M3", "M4", "TC1", "TC2", "ThinAl", "ThickAl"]

        if Metal in MetalList:
            if Metal == "M1":
                MaxCurrent = 1.45*(Width - 0.06)
            elif Metal == "M2" or Metal == "M3" or Metal == "M4":
                MaxCurrent = 1.43 * (Width - 0.05)
            elif Metal == "TC1" or Metal == "TC2":
                MaxCurrent = 13.6 * (Width - 0.2)
            elif Metal == "ThinAl":
                MaxCurrent = 1.22* (Width - 0.06)
            elif Metal == "ThickAl":
                MaxCurrent = 5.099 * (Width - 0.47)
        else:
            raise ValueError('Metals can be choosen from: "M1", "M2", "M3", "M4", "TC1", "TC3", "ThinAl", "ThickAl" !!!')

        return MaxCurrent


    ###########################################################
    # S-Parameters
    ##########################################################

    def S_Parameters(self):
        """
        Convert complex S-parameter data into dB scale and return as a dictionary.

        This function computes magnitude-based S-parameters in dB form from
        real and imaginary components. It supports both 2-port and 4-port DUTs
        depending on the loaded dataset.

                            __________
                Port 1 o------|          |-----o Port 2
                            |   DUT    |
                Port 3 o------|__________|-----o Port 4    
                            
                            __________
                            |          |
                Port 1 o------|  DUT     |-----O Port 2
                            |__________|

        The conversion is defined as:

        .. math::
            S_{ij} = 20 \\log_{10} (|S_{ij,Re} + j S_{ij,Im}|)

        Returns
        -------
        dict
            Dictionary containing:
            - "Frequency": frequency axis
            - "Sij": S-parameters in dB (|Sij| in 20log10 scale)

            For 2-port:
                S11, S12, S21, S22

            For 4-port:
                S11, S12, S13, S14,
                S21, S22, S23, S24,
                S31, S32, S33, S34,
                S41, S42, S43, S44

        Notes
        -----
        - If `Parameters_size == 4`, a full 4-port matrix is returned.
        - Otherwise, a 2-port representation is assumed.
        - Results are expressed in dB.

        Examples
        --------
        >>> S = obj.S_Parameters()
        >>> S["S11"]
        array([...])
    """


        if self.Parameters_size == 4:
            # Transform Parameters
            S11 = 20*np.log10(np.abs(self.S11_re + 1j*self.S11_im))
            S12 = 20*np.log10(np.abs(self.S12_re + 1j*self.S12_im))
            S13 = 20*np.log10(np.abs(self.S13_re + 1j*self.S13_im))
            S14 = 20*np.log10(np.abs(self.S14_re + 1j*self.S14_im))
            S21 = 20*np.log10(np.abs(self.S21_re + 1j*self.S21_im))
            S22 = 20*np.log10(np.abs(self.S22_re + 1j*self.S22_im))
            S23 = 20*np.log10(np.abs(self.S23_re + 1j*self.S23_im))
            S24 = 20*np.log10(np.abs(self.S24_re + 1j*self.S24_im))
            S31 = 20*np.log10(np.abs(self.S31_re + 1j*self.S31_im))
            S32 = 20*np.log10(np.abs(self.S32_re + 1j*self.S32_im))
            S33 = 20*np.log10(np.abs(self.S33_re + 1j*self.S33_im))
            S34 = 20*np.log10(np.abs(self.S34_re + 1j*self.S34_im))
            S41 = 20*np.log10(np.abs(self.S41_re + 1j*self.S41_im))
            S42 = 20*np.log10(np.abs(self.S42_re + 1j*self.S42_im))
            S43 = 20*np.log10(np.abs(self.S43_re + 1j*self.S43_im))
            S44 = 20*np.log10(np.abs(self.S44_re + 1j*self.S44_im))
            
            S_Param = {}
            S_Param["Frequency"] = self.frequency
            S_Param["S11"] = S11
            S_Param["S12"] = S12
            S_Param["S13"] = S13
            S_Param["S14"] = S14
            S_Param["S21"] = S21
            S_Param["S22"] = S22
            S_Param["S23"] = S23
            S_Param["S24"] = S24
            S_Param["S31"] = S31
            S_Param["S32"] = S32
            S_Param["S33"] = S33
            S_Param["S34"] = S34
            S_Param["S41"] = S41
            S_Param["S42"] = S42
            S_Param["S43"] = S43
            S_Param["S44"] = S44
      
            return S_Param  

        else:
            S11 = 20*np.log10(np.abs(self.S11_re + 1j*self.S11_im))
            S12 = 20*np.log10(np.abs(self.S12_re + 1j*self.S12_im))
            S21 = 20*np.log10(np.abs(self.S21_re + 1j*self.S21_im))
            S22 = 20*np.log10(np.abs(self.S22_re + 1j*self.S22_im))

            S_Param = {}
            S_Param["Frequency"] = self.frequency
            S_Param["S11"] = S11
            S_Param["S12"] = S12
            S_Param["S21"] = S21
            S_Param["S22"] = S22

            return S_Param

        


    ###########################################################
    # S-Parameters Transofrmation from single to diff mode 
    ###########################################################


    def SingleToDiffS_Params(self):


        """
    Convert single-ended 4-port S-parameters into mixed-mode S-parameters.

    This function transforms a 4-port single-ended S-parameter matrix into
    differential and common-mode representations:

    - Differential-Differential (SDD)
    - Common-Differential (SCD)
    - Differential-Common (SDC)
    - Common-Common (SCC)

    The transformation is based on standard mixed-mode S-parameter theory.

    How to set the Simulation Testbench
                           __________
            Port 1 o------|          |-----o Port 3
                          |   DUT    |
            Port 2 o------|__________|-----o Port 4    
                         
                           __________
                          |          |
            Port 1 o------|  DUT     |-----O Port 2
                          |__________|

    Notes
    -----
    The conversion assumes the following port pairing:

        Port 1 / Port 3 → Differential pair 1
        Port 2 / Port 4 → Differential pair 2

    The mixed-mode transformation is defined by linear combinations of
    single-ended S-parameters.

    Returns
    -------
    tuple of dict
        A tuple containing four dictionaries:

        SDD : dict
            Differential-to-differential S-parameters (in dB)
        SDC : dict
            Common-to-differential S-parameters (in dB)
        SCD : dict
            Differential-to-common S-parameters (in dB)
        SCC : dict
            Common-to-common S-parameters (in dB)

        Each dictionary contains:
        - "Frequency"
        - S-parameter entries (e.g., SDD11, SDD12, ...)

    Raises
    ------
    ValueError
        If the input is not a 4-port S-parameter dataset.

    Examples
    --------
    >>> SDD, SDC, SCD, SCC = obj.SingleToDiffS_Params()
    >>> SDD["SDD11"]
    array([...])
    """


        if self.Parameters_size == 4:

            S11 = self.S11_re + 1j*self.S11_im
            S12 = self.S12_re + 1j*self.S12_im
            S13 = self.S13_re + 1j*self.S13_im
            S14 = self.S14_re + 1j*self.S14_im

            S21 = self.S21_re + 1j*self.S21_im
            S22 = self.S22_re + 1j*self.S22_im
            S23 = self.S23_re + 1j*self.S23_im
            S24 = self.S24_re + 1j*self.S24_im

            S31 = self.S31_re + 1j*self.S31_im
            S32 = self.S32_re + 1j*self.S32_im
            S33 = self.S33_re + 1j*self.S33_im
            S34 = self.S34_re + 1j*self.S34_im

            S41 = self.S41_re + 1j*self.S41_im
            S42 = self.S42_re + 1j*self.S42_im
            S43 = self.S43_re + 1j*self.S43_im
            S44 = self.S44_re + 1j*self.S44_im

            # ==========================================================
            # DIFFERENTIAL - DIFFERENTIAL
            # ==========================================================

            SDD11 = 0.5 * (S11 - S12 - S21 + S22)

            SDD12 = 0.5 * (S14 - S13 - S24 + S23)

            SDD21 = 0.5 * (S41 - S42 - S31 + S32)

            SDD22 = 0.5 * (S44 - S43 - S34 + S33)

            # ==========================================================
            # DIFFERENTIAL - COMMON
            #
            # Output differential due to common excitation
            # ==========================================================

            SDC11 = 0.5 * (S11 + S12 - S21 - S22)

            SDC12 = 0.5 * (S14 + S13 - S24 - S23)

            SDC21 = 0.5 * (S41 + S42 - S31 - S32)

            SDC22 = 0.5 * (S44 + S43 - S34 - S33)

            # ==========================================================
            # COMMON - DIFFERENTIAL
            #
            # Output common due to differential excitation
            # ==========================================================

            SCD11 = 0.5 * (S11 - S12 + S21 - S22)

            SCD12 = 0.5 * (S14 - S13 + S24 - S23)

            SCD21 = 0.5 * (S41 - S42 + S31 - S32)

            SCD22 = 0.5 * (S44 - S43 + S34 - S33)

            # ==========================================================
            # COMMON - COMMON
            # ==========================================================

            SCC11 = 0.5 * (S11 + S12 + S21 + S22)

            SCC12 = 0.5 * (S14 + S13 + S24 + S23)

            SCC21 = 0.5 * (S41 + S42 + S31 + S32)

            SCC22 = 0.5 * (S44 + S43 + S34 + S33)

            # ==========================================================
            # Convert to dB
            # ==========================================================

            eps = 1e-20

            SDD = {
                "Frequency": self.frequency,
                "SDD11": 20*np.log10(np.abs(SDD11) + eps),
                "SDD12": 20*np.log10(np.abs(SDD12) + eps),
                "SDD21": 20*np.log10(np.abs(SDD21) + eps),
                "SDD22": 20*np.log10(np.abs(SDD22) + eps),
            }

            SDC = {
                "Frequency": self.frequency,
                "SDC11": 20*np.log10(np.abs(SDC11) + eps),
                "SDC12": 20*np.log10(np.abs(SDC12) + eps),
                "SDC21": 20*np.log10(np.abs(SDC21) + eps),
                "SDC22": 20*np.log10(np.abs(SDC22) + eps),
            }

            SCD = {
                "Frequency": self.frequency,
                "SCD11": 20*np.log10(np.abs(SCD11) + eps),
                "SCD12": 20*np.log10(np.abs(SCD12) + eps),
                "SCD21": 20*np.log10(np.abs(SCD21) + eps),
                "SCD22": 20*np.log10(np.abs(SCD22) + eps),
            }

            SCC = {
                "Frequency": self.frequency,
                "SCC11": 20*np.log10(np.abs(SCC11) + eps),
                "SCC12": 20*np.log10(np.abs(SCC12) + eps),
                "SCC21": 20*np.log10(np.abs(SCC21) + eps),
                "SCC22": 20*np.log10(np.abs(SCC22) + eps),
            }

            return SDD, SDC, SCD, SCC

        else:
            raise ValueError(
                "This function only works for 4-port S-parameter networks!"
            )


    ########################################################
    # Impedanz calculator
    ########################################################

    def Zc_Calc(self, Zref = 50):

        """
        Calculate the characteristic impedance from S-parameters.

        This function estimates the characteristic impedance (Zc) of a transmission
        structure using S-parameters. For a 4-port system, mixed-mode S-parameters
        are first computed and then used to extract differential characteristic impedance.

        The calculation is based on the standard relation:

        .. math::
            Z_c = Z_0 \\sqrt{ \\frac{(1 + S_{11})^2 - S_{21}^2}{(1 - S_{11})^2 - S_{21}^2} }

        where Z₀ is the reference impedance (typically 50 Ω single-ended or 100 Ω differential).

        How to set the Simulation Testbench
                           __________
            Port 1 o------|          |-----o Port 2
                          |   DUT    |
            Port 3 o------|__________|-----o Port 4    
                         
                           __________
                          |          |
            Port 1 o------|  DUT     |-----O Port 2
                          |__________|
        Returns
        -------
        Zc : numpy.ndarray
            Characteristic impedance as a function of frequency.

        Notes
        -----
        - For 4-port systems, mixed-mode S-parameters are used (SDD11, SDD21).
        - For 2-port systems, single-ended S11 and S21 are used.
        - The result depends on the reference impedance assumption:
            * 100 Ω for differential mode (4-port case)
            * 50 Ω for single-ended (2-port case)

        Raises
        ------
        ValueError
            If the input S-parameter configuration is not supported.

        Examples
        --------
        >>> Zc = obj.Zc_Calc()
        >>> Zc[0]
        49.8
        """

        
        if self.Parameters_size == 4:
            SDD, SDC, SCD, SCC = self.SingleToDiffS_Params()
            # Read data
            S11= SDD["SDD11"]
            S21= SDD["SDD21"]

            Zc = Zref * np.sqrt( ((1+S11)**2 - S21**2)/ ((1-S11)**2 - S21**2) + 0j)

            return Zc

            
        else:
            # Read data
            S11= 20*np.log10(np.abs(self.S11_re + 1j*self.S11_im))
            S21= 20*np.log10(np.abs(self.S21_re + 1j*self.S21_im))

            Zc = Zref * np.sqrt( ((1+S11)**2 - S21**2)/ ((1-S11)**2 - S21**2) )

            return Zc



    ######################################################
    # Group Delay Caluclator
    ######################################################


    def GroupDelay(self):

        """
        Compute group delay from S-parameters.

        The group delay is calculated from the frequency derivative of the
        unwrapped phase of the S-parameters:

        .. math::
            \\tau = -\\frac{1}{2\\pi} \\frac{d\\phi}{df}

        where:
        - \\phi is the unwrapped phase of the S-parameter
        - f is frequency

        This function computes group delay for all S-parameter paths in
        both 2-port and 4-port configurations.

        How to set the Simulation Testbench
                           __________
            Port 1 o------|          |-----o Port 3
                          |   DUT    |
            Port 2 o------|__________|-----o Port 4       

        Notes
        -----
        - Phase is unwrapped to remove ±π discontinuities.
        - Numerical differentiation is performed using finite differences.
        - The result is scaled to picoseconds (ps).

        Returns
        -------
        dict
            Dictionary containing:
            - "Frequency": frequency axis
            - "gij": group delay from port i to j (in ps)

            For 4-port:
                g11, g12, ..., g44

            For 2-port:
                g11, g12, g21, g22

        Raises
        ------
        ValueError
            If the S-parameter configuration is not supported.

        Examples
        --------
        >>> tau = obj.GroupDelay()
        >>> tau["g21"]
        array([...])
        """


        if self.Parameters_size == 4:
            # Transform Parameters
            S11= self.S11_re + 1j*self.S11_im
            S12= self.S12_re + 1j*self.S12_im
            S13= self.S13_re + 1j*self.S13_im
            S14= self.S14_re + 1j*self.S14_im
            S21= self.S21_re + 1j*self.S21_im
            S22= self.S22_re + 1j*self.S22_im
            S23= self.S23_re + 1j*self.S23_im
            S24= self.S24_re + 1j*self.S24_im
            S31= self.S31_re + 1j*self.S31_im
            S32= self.S32_re + 1j*self.S32_im
            S33= self.S33_re + 1j*self.S33_im
            S34= self.S34_re + 1j*self.S34_im
            S41= self.S41_re + 1j*self.S41_im
            S42= self.S42_re + 1j*self.S42_im
            S43= self.S43_re + 1j*self.S43_im
            S44= self.S44_re + 1j*self.S44_im

            # Calucalte the phase and Phase jumps (±π) must be removed with unwrap
            phi11 = np.unwrap(np.angle(S11))
            phi12 = np.unwrap(np.angle(S12))
            phi13 = np.unwrap(np.angle(S13))
            phi14 = np.unwrap(np.angle(S14))
            phi21 = np.unwrap(np.angle(S21))
            phi22 = np.unwrap(np.angle(S22))
            phi23 = np.unwrap(np.angle(S23))
            phi24 = np.unwrap(np.angle(S24))
            phi31 = np.unwrap(np.angle(S31))
            phi32 = np.unwrap(np.angle(S32))
            phi33 = np.unwrap(np.angle(S33))
            phi34 = np.unwrap(np.angle(S34))
            phi41 = np.unwrap(np.angle(S41))
            phi42 = np.unwrap(np.angle(S42))
            phi43 = np.unwrap(np.angle(S43))
            phi44 = np.unwrap(np.angle(S44))

            
            # caluclate group delay phi 
            tau = {}
            tau["Frequency"] = self.frequency
            tau["g11"] = -np.gradient(phi11, self.frequency) / (2*np.pi) * 1e12
            tau["g12"] = -np.gradient(phi12, self.frequency) / (2*np.pi) * 1e12 
            tau["g13"] = -np.gradient(phi13, self.frequency) / (2*np.pi) * 1e12 
            tau["g14"] = -np.gradient(phi14, self.frequency) / (2*np.pi) * 1e12 
            tau["g21"] = -np.gradient(phi21, self.frequency) / (2*np.pi) * 1e12 
            tau["g22"] = -np.gradient(phi22, self.frequency) / (2*np.pi) * 1e12 
            tau["g23"] = -np.gradient(phi23, self.frequency) / (2*np.pi) * 1e12 
            tau["g24"] = -np.gradient(phi24, self.frequency) / (2*np.pi) * 1e12  
            tau["g31"] = -np.gradient(phi31, self.frequency) / (2*np.pi) * 1e12 
            tau["g32"] = -np.gradient(phi32, self.frequency) / (2*np.pi) * 1e12 
            tau["g33"] = -np.gradient(phi33, self.frequency) / (2*np.pi) * 1e12 
            tau["g34"] = -np.gradient(phi34, self.frequency) / (2*np.pi) * 1e12 
            tau["g41"] = -np.gradient(phi41, self.frequency) / (2*np.pi) * 1e12 
            tau["g42"] = -np.gradient(phi42, self.frequency) / (2*np.pi) * 1e12 
            tau["g43"] = -np.gradient(phi43, self.frequency) / (2*np.pi) * 1e12 
            tau["g44"] = -np.gradient(phi44, self.frequency) / (2*np.pi) * 1e12 

            return tau

        else:
            # Transform Parameters
            S11= self.S11_re + 1j*self.S11_im
            S12= self.S12_re + 1j*self.S12_im
            S21= self.S21_re + 1j*self.S21_im
            S22= self.S22_re + 1j*self.S22_im
            
            # Calucalte the phase and Phase jumps (±π) must be removed with unwrap
            phi11 = np.unwrap(np.angle(S11))
            phi12 = np.unwrap(np.angle(S12))
            phi21 = np.unwrap(np.angle(S21))
            phi22 = np.unwrap(np.angle(S22))


            # caluclate group delay phi 
            tau = {}
            tau["Frequency"] = self.frequency
            tau["g11"] = -np.gradient(phi11, self.frequency) / (2*np.pi) * 1e12
            tau["g12"] = -np.gradient(phi12, self.frequency) / (2*np.pi) * 1e12 
            
            tau["g21"] = -np.gradient(phi21, self.frequency) / (2*np.pi) * 1e12 
            tau["g22"] = -np.gradient(phi22, self.frequency) / (2*np.pi) * 1e12 

            return tau
             



    ########################################
    # mu - Stability caluclator
    ########################################

    def muStability(self):

        """
        Calculate stability factors (μ and μ′) from S-parameters.

        The function computes the Rollett stability-related factors μ and μ′,
        which are commonly used to evaluate unconditional stability of RF circuits.

        For a 2-port network, the classical definitions are:

        .. math::
            \\Delta = S_{11}S_{22} - S_{12}S_{21}

        .. math::
            \\mu = \\frac{1 - |S_{11}|^2}
            { |S_{22} - \\Delta S_{11}^*| + |S_{12}S_{21}| }

        .. math::
            \\mu' = \\frac{1 - |S_{22}|^2}
            { |S_{11} - \\Delta S_{22}^*| + |S_{12}S_{21}| }

        For 4-port systems, mixed-mode S-parameters (SDD) are used instead.

        How to set the Simulation Testbench
                           __________
            Port 1 o------|          |-----o Port 3
                          |   DUT    |
            Port 2 o------|__________|-----o Port 4     

        Notes
        -----
        - μ > 1 and μ′ > 1 indicate unconditional stability.
        - The function uses differential-mode S-parameters for 4-port cases.
        - Complex conjugates are used in stability factor computation.
        - Results are frequency-dependent.

        Returns
        -------
        tuple of numpy.ndarray
            (mu, mu_prime) stability factors over frequency.

        Raises
        ------
        ValueError
            If the S-parameter configuration is not supported.

        Examples
        --------
        >>> mu, mu_p = obj.muStability()
        >>> mu.min()
        1.2
        """

       

        # ==========================================================
        # 4-PORT DIFFERENTIAL CASE
        # ==========================================================
        if self.Parameters_size == 4:

            # ------------------------------------------------------
            # Build complex S-parameters
            # ------------------------------------------------------
            S11 = self.S11_re + 1j*self.S11_im
            S12 = self.S12_re + 1j*self.S12_im
            S13 = self.S13_re + 1j*self.S13_im
            S14 = self.S14_re + 1j*self.S14_im

            S21 = self.S21_re + 1j*self.S21_im
            S22 = self.S22_re + 1j*self.S22_im
            S23 = self.S23_re + 1j*self.S23_im
            S24 = self.S24_re + 1j*self.S24_im

            S31 = self.S31_re + 1j*self.S31_im
            S32 = self.S32_re + 1j*self.S32_im
            S33 = self.S33_re + 1j*self.S33_im
            S34 = self.S34_re + 1j*self.S34_im

            S41 = self.S41_re + 1j*self.S41_im
            S42 = self.S42_re + 1j*self.S42_im
            S43 = self.S43_re + 1j*self.S43_im
            S44 = self.S44_re + 1j*self.S44_im

            # ======================================================
            # DIFFERENTIAL S-PARAMETERS
            #
            # Input pair  = (1,2)
            # Output pair = (4,3)
            # ======================================================

            # Differential input reflection
            SDD11 = 0.5 * (S11 - S12 - S21 + S22)

            # Differential forward transmission
            SDD21 = 0.5 * (S41 - S42 - S31 + S32)

            # Differential reverse transmission
            SDD12 = 0.5 * (S14 - S13 - S24 + S23)

            # Differential output reflection
            SDD22 = 0.5 * (S44 - S43 - S34 + S33)

            # ======================================================
            # Stability calculations
            # ======================================================

            Delta = SDD11 * SDD22 - SDD12 * SDD21

            mu = ((1 - np.abs(SDD11)**2)/(np.abs(SDD22 - Delta * np.conj(SDD11))+ np.abs(SDD12 * SDD21)))

            mu_prime = ((1 - np.abs(SDD22)**2)/(np.abs(SDD11 - Delta * np.conj(SDD22))+ np.abs(SDD12 * SDD21)))

            return mu, mu_prime

        # ==========================================================
        # STANDARD 2-PORT CASE
        # ==========================================================
        else:

            S11 = self.S11_re + 1j*self.S11_im
            S12 = self.S12_re + 1j*self.S12_im

            S21 = self.S21_re + 1j*self.S21_im
            S22 = self.S22_re + 1j*self.S22_im

            Delta = S11 * S22 - S12 * S21

            mu = (
                (1 - np.abs(S11)**2)
                /
                (
                    np.abs(S22 - Delta * np.conj(S11))
                    + np.abs(S12 * S21)
                )
            )

            mu_prime = (
                (1 - np.abs(S22)**2)
                /
                (
                    np.abs(S11 - Delta * np.conj(S22))
                    + np.abs(S12 * S21)
                )
            )

            return mu, mu_prime


    def KStability(self):

        """
        Calculate the Rollett stability factor K for a standard 2-port network.

        For a 2-port network, the classical definition is:

        .. math::
            \\Delta = S_{11}S_{22} - S_{12}S_{21}

        .. math::
            K =
            \\frac{
                1 - |S_{11}|^2 - |S_{22}|^2 + |\\Delta|^2
            }{
                2|S_{12}S_{21}|
            }

        .. math::
            B_1 = 1 + |S_{11}|^2 - |S_{22}|^2 - |\\Delta|^2

        Unconditional stability requires:

        .. math::
            K > 1

        and

        .. math::
            |\\Delta| < 1

        Returns
        -------
        tuple of numpy.ndarray
            (K, Delta_abs, B1) stability factor, absolute value of Delta,
            and B1 over frequency.
        """

        # ==========================================================
        # S-parameters
        # ==========================================================

        S11 = self.S11_re + 1j * self.S11_im
        S12 = self.S12_re + 1j * self.S12_im
        S21 = self.S21_re + 1j * self.S21_im
        S22 = self.S22_re + 1j * self.S22_im

        # ==========================================================
        # Determinant of the S-parameter matrix
        # ==========================================================

        Delta = S11 * S22 - S12 * S21

        # ==========================================================
        # Rollett Stability Factor K
        # ==========================================================

        K = ( (1 - np.abs(S11)**2 - np.abs(S22)**2 + np.abs(Delta)**2) / (2 * np.abs(S12 * S21)) )

        # ==========================================================
        # Absolute value of Delta
        # ==========================================================

        Delta_abs = np.abs(Delta)

        # ==========================================================
        # B1 stability factor
        # ==========================================================

        B1 = ( 1 + np.abs(S11)**2 - np.abs(S22)**2 - np.abs(Delta)**2 )


        return K, Delta_abs, B1


###################################################################
# Signal Integrity 1dB, THD and SDR calculation and plot 
###################################################################

    def CalcFFT(self, Sig, frequency):
        """
            Compute FFT of a time-domain signal using interpolation and windowing.

            This function calculates the single-sided amplitude spectrum of a signal.
            The input signal is first resampled onto a uniform time grid based on an
            oversampled reference frequency, then a windowed FFT is performed.

            Steps performed:
            1. Extract time and signal from input DataFrame
            2. Interpolate signal onto uniform time grid
            3. Apply Hann window to reduce spectral leakage
            4. Compute FFT and normalize amplitude
            5. Convert to single-sided spectrum
            6. Compute magnitude in linear and dB scale

            Parameters
            ----------
            Sig : pandas.DataFrame
                Input signal data with:
                - column 0: time (s)
                - column 1: signal amplitude

            frequency : float
                Expected fundamental frequency of the signal (Hz).
                Used to define oversampling rate.

            Returns
            -------
            dict
                Dictionary containing:
                - "freq" : numpy.ndarray
                    Frequency axis (Hz), single-sided spectrum
                - "Y" : numpy.ndarray
                    Amplitude spectrum (linear scale)
                - "Y_dB" : numpy.ndarray
                    Amplitude spectrum in dB scale

            Notes
            -----
            - Signal is interpolated to a uniform grid before FFT.
            - Oversampling factor is fixed to 31× fundamental frequency.
            - Hann window is applied to reduce spectral leakage.
            - Coherent gain correction is included for amplitude accuracy.
            - DC component is corrected after FFT scaling.
            - A small offset (1e-20) is used to avoid log(0).

            Examples
            --------
            >>> result = obj.CalcFFT(df, 1e9)
            >>> result["freq"]
            array([...])
            """

        columns = Sig.columns

        # Extract time and signal
        t = Sig[columns[0]].values
        y = Sig[columns[1]].values


        # -------------------------------
        # Create uniform time grid
        # -------------------------------
        oversample = 31
        fs = frequency * oversample
        dt = 1 / fs
        t_uniform = np.arange(t[0], t[-1], dt)

        # Interpolation (linear = safer)
        interp_func = interp1d(t, y, kind='cubic', fill_value="extrapolate")
        y_uniform = interp_func(t_uniform)

        # -------------------------------
        # FFT
        # -------------------------------
        N = len(t_uniform)

        # Apply window to reduce leakage
        window = np.hanning(N) 
        # window = np.ones(N) 
        y_uniform = y_uniform * window
        coherent_gain = np.sum(window) / N

        # Y = np.fft.fft(y_uniform) / N 
        Y = np.fft.fft(y_uniform) / (N * coherent_gain)
        freq = np.fft.fftfreq(N, d=dt)

        # Single-sided spectrum
        freq_pos = freq[:N // 2] 
        Y_pos = 2 * np.abs(Y[:N // 2])

        # -------------------------------
        # Optional: dB scale (like Cadence)
        # -------------------------------
        Y_db = 20 * np.log10(Y_pos + 1e-20)  # avoid log(0)

        # Fix DC component
        Y_pos[0] /= 2



        return {
            "freq": freq_pos,
            "Y": Y_pos,
            "Y_dB":Y_db
        }
    
    


    
    def ExtractFundamental(self, Signal, sim_frequency, R=100):
        """
        Extract the fundamental frequency component from an FFT spectrum
        and calculate the corresponding power in dBm.

        Returns
        -------
        Y_local : float
            Magnitude of the fundamental frequency component in dB.

        P_dBm : float
            Fundamental power in dBm.
        """

        # Get FFT
        data = self.CalcFFT(Signal, sim_frequency)
        freq_array = data["freq"]
        Y_array = data["Y"]

        # Find the FFT bin closest to the fundamental frequency
        idx = np.argmin(np.abs(freq_array - sim_frequency))

        # Select 3 bins: center and neighbors
        idx_min = max(0, idx - 1)
        idx_max = min(len(Y_array), idx + 2)

        # Keep your existing voltage calculation
        Y_local = 20 * np.log10(Y_array[idx] + 1e-12)

        # Calculate power from the fundamental voltage
        V_peak = Y_array[idx]
        V_rms = V_peak / np.sqrt(2)

        P_watt = V_rms**2 / R

        # Convert power to dBm
        P_dBm = 10 * np.log10(P_watt / 1e-3)

        return Y_local, P_dBm

    
    def ExtractThirdFundamental(self, Signal, sim_frequency):
        """
        Extract the third harmonic component from the FFT spectrum.

        This function computes the FFT of the input signal and extracts the
        amplitude of the third harmonic (3 × fundamental frequency) by selecting
        the closest FFT bin.

        Parameters
        ----------
        Signal : pandas.DataFrame
            Time-domain signal data (see `CalcFFT` for required format).

        sim_frequency : float
            Fundamental frequency of the signal (Hz).

        Returns
        -------
        float
            Amplitude of the third harmonic in dB.

        Notes
        -----
        - The function uses nearest-bin selection (no interpolation).
        - The third harmonic is defined as 3 × fundamental frequency.
        - A small offset (1e-12) is added to avoid log(0).

        Examples
        --------
        >>> H3 = obj.ExtractThirdFundamental(df, 1e9)
        >>> print(H3)
        -45.2
        """


        # Compute FFT
        data = self.CalcFFT(Signal, sim_frequency)
        freq_array = data["freq"]
        Y_array = data["Y"]

        # Target: second harmonic
        f_target = 3 * sim_frequency

        # Find closest FFT bin
        idx = np.argmin(np.abs(freq_array - f_target))

        # Return magnitude in dB
        Y_second_dB = 20 * np.log10(Y_array[idx] + 1e-12)

        return Y_second_dB
    



    def ExtractAllFundamental(self, Signal, sim_frequency, number_of_harmonics):
        """
        Extract harmonic amplitudes of a signal from its FFT spectrum.

        This function computes the FFT of the input signal and extracts the
        amplitudes of higher-order harmonics starting from the second harmonic
        (2 × fundamental frequency).

        Each harmonic is obtained by selecting the closest FFT frequency bin.

        Parameters
        ----------
        Signal : pandas.DataFrame
            Time-domain signal data (see `CalcFFT` for required format).

        sim_frequency : float
            Fundamental frequency of the signal (Hz).

        number_of_harmonics : int
            Total number of harmonics to extract (including the fundamental).
            Extraction starts from the 2nd harmonic up to this value.

        Returns
        -------
        dict
            Dictionary containing harmonic amplitudes in dB.

            Keys:
                "2" → 2nd harmonic
                "3" → 3rd harmonic
                ...
                "N" → Nth harmonic

            Values:
                Amplitude in dB of each harmonic.

        Notes
        -----
        - The fundamental (1st harmonic) is not included in the output.
        - Harmonics are extracted using nearest FFT bin selection.
        - No interpolation is performed.
        - Requires frequency resolution sufficient to resolve harmonics.

        Examples
        --------
        >>> H = obj.ExtractAllFundamental(df, 1e9, 5)
        >>> H["2"]
        -40.2
        """

        # Compute FFT
        data = self.CalcFFT(Signal, sim_frequency)
        freq_array = data["freq"]
        Y_array = data["Y_dB"]

        harmonics_val = {}

        # Start from 2 to skip the fundamental
        for i in range(2, number_of_harmonics + 1):
            f_target = i * sim_frequency

            # Find closest FFT bin
            idx = np.argmin(np.abs(freq_array - f_target))

            # Return magnitude in dB
            Y_dB = Y_array[idx]

            # Store using harmonic number as key
            harmonics_val[f"{i}"] = Y_dB

        return harmonics_val
        




    def Compression_Point(self, files, sim_frequency, R=[100,100]):
        """
        Estimate the 1 dB compression point from power sweep measurements.

        This function calculates the input and output power levels from a set of
        CSV sweep files and determines the 1 dB compression point by comparing
        measured output power to a linear fit of the small-signal region.

        The 1 dB compression point is defined as the input power at which the
        output power deviates by 1 dB from the extrapolated linear response.

        Parameters
        ----------
        files : list of str
            List of CSV file paths. Each file must contain:
            - columns 0–1: time and input signal
            - columns 2–3: time and output signal

        sim_frequency : float
            Fundamental frequency of the signal (Hz), used for FFT extraction.

        R : array
            defoult R = [100, 100], this means 50 Ohm input and 50 Ohm Output
            

        Returns
        -------
        dict
            Dictionary containing:

            Pin : numpy.ndarray
                Input power levels (dB)

            Pout linear : numpy.ndarray
                Linear extrapolated output power (dB)

            Pout : numpy.ndarray
                Measured output power (dB)

            Pin 1dB : float or None
                Input power at 1 dB compression point

            Pout 1dB : float or None
                Output power at 1 dB compression point

        Notes
        -----
        - The small-signal linear region is assumed to be the first 5 data points
        (or fewer if dataset is smaller).
        - Linear regression is used to estimate ideal output response.
        - Compression is defined as:
            Pout_linear − Pout ≥ 1 dB
        - Results depend strongly on sweep resolution and data quality.

        Examples
        --------
        >>> result = obj.Compression_Point(files, 1e9)
        >>> result["Pin 1dB"]
        -12.5
        """


        PIn, POut = [], []
        R1 = R[0]
        R2 = R[1]
        for file in files:
            Sig = pd.read_csv(file, sep=",")
            # PIn.append(self.ExtractFundamental(Sig.iloc[:, :2], sim_frequency))
            # POut.append(self.ExtractFundamental(Sig.iloc[:, 2:4], sim_frequency))

            Y_in, P_in = self.ExtractFundamental(Sig.iloc[:, :2],sim_frequency, R1)
            # Extract output fundamental voltage and power
            Y_out, P_out = self.ExtractFundamental(Sig.iloc[:, 2:4],sim_frequency, R2)

            # Store power values for compression calculation
            PIn.append(P_in)
            POut.append(P_out)


        # Convert to NumPy arrays for vector operations
        PIn = np.array(PIn)
        POut = np.array(POut)

        # Fit linear region (first min(5, len(PIn)) points)
        n_fit = min(5, len(PIn))
        fit = polyfit(PIn[:n_fit], POut[:n_fit], 1)
        Pout_linear = polyval(fit, PIn)

        # Compute compression
        compression = Pout_linear - POut
        idx_candidates = np.where(compression >= 1)[0]

        if len(idx_candidates) > 0:
            idx_1dB = idx_candidates[0]
            Pin_1dB = PIn[idx_1dB]
            Pout_1dB = POut[idx_1dB]
        else:
            idx_1dB = None
            Pin_1dB = None
            Pout_1dB = None

        # Store results
        _data = {
            "Pin": PIn,
            "Pout linear": Pout_linear,
            "Pout": POut,
            "Pin 1dB": Pin_1dB,
            "Pout 1dB": Pout_1dB
        }

        return _data



    def CalcIIP3( self,files,f1,f2,R=[100, 100],im3='low',n_fit=5,force_ideal_slopes=False,start_idx=1):
        """
        Calculate IIP3 from a two-tone transient/IMD sweep.
        """

        # =========================================================
        # Check inputs
        # =========================================================

        if im3 not in ('low', 'high'):
            raise ValueError( "im3 must be either 'low' or 'high'.")

        if f2 <= f1:
            raise ValueError(  "f2 must be greater than f1.")

        if len(files) < 2:
            raise ValueError( "At least two sweep points are required." )

        if n_fit < 2:
            raise ValueError( "n_fit must be at least 2." )

        if start_idx < 0:
            raise ValueError( "start_idx must be >= 0." )

        # =========================================================
        # Select IM3 frequency
        # =========================================================

        if im3 == 'low':
            f_im3 = 2.0 * f1 - f2

        else:
            f_im3 = 2.0 * f2 - f1

        # =========================================================
        # Storage
        # =========================================================

        R1, R2 = R
        PIn = []
        Pfund = []
        PIM3 = []

        # =========================================================
        # Process every CSV
        # =========================================================

        for file in files:

            Sig = pd.read_csv( file, sep="," )

            if Sig.shape[1] < 4:
                raise ValueError(  f"File '{file}' must contain at least 4 columns." )

            # -----------------------------------------------------
            # Differential input
            # -----------------------------------------------------

            _, P_in = self.ExtractFundamental( Sig.iloc[:, :2], f1, R1 )

            # -----------------------------------------------------
            # Differential output fundamental
            # -----------------------------------------------------

            _, P_fund = self.ExtractFundamental( Sig.iloc[:, 2:4], f1, R2 )

            # -----------------------------------------------------
            # Differential output IM3
            # -----------------------------------------------------

            _, P_im3 = self.ExtractFundamental( Sig.iloc[:, 2:4], f_im3, R2 )

            PIn.append(P_in)
            Pfund.append(P_fund)
            PIM3.append(P_im3)

        # =========================================================
        # Convert to numpy arrays
        # =========================================================

        PIn = np.asarray( PIn, dtype=float )
        Pfund = np.asarray( Pfund, dtype=float )
        PIM3 = np.asarray( PIM3, dtype=float )

        # =========================================================
        # Sort according to input power
        # =========================================================

        sort_idx = np.argsort(PIn)

        PIn = PIn[sort_idx]
        Pfund = Pfund[sort_idx]
        PIM3 = PIM3[sort_idx]

        # =========================================================
        # Remove unwanted low-power points
        # =========================================================

        if start_idx >= len(PIn):
            raise ValueError( "start_idx removes all available data points.")

        PIn = PIn[start_idx:]
        Pfund = Pfund[start_idx:]
        PIM3 = PIM3[start_idx:]

        # =========================================================
        # Determine number of fitting points
        # =========================================================

        n_fit = min( n_fit, len(PIn) )

        if n_fit < 2:
            raise ValueError( "Not enough points available for linear fitting." )

        # =========================================================
        # Small-signal fitting
        # =========================================================

        if force_ideal_slopes:

            # -----------------------------------------------------
            # Fundamental = 1 dB/dB
            # -----------------------------------------------------

            b_fund = np.mean( Pfund[:n_fit] - PIn[:n_fit] )
            fit_fund = np.array([ 1.0, b_fund ])

            # -----------------------------------------------------
            # IM3 = 3 dB/dB
            # -----------------------------------------------------

            b_im3 = np.mean( PIM3[:n_fit] - 3.0 * PIn[:n_fit] )
            fit_im3 = np.array([ 3.0, b_im3 ])
        else:

            # -----------------------------------------------------
            # Actual measured slopes
            # -----------------------------------------------------

            fit_fund = np.polyfit( PIn[:n_fit], Pfund[:n_fit], 1 )
            fit_im3 = np.polyfit( PIn[:n_fit], PIM3[:n_fit], 1 )
        # =========================================================
        # Extract slopes
        # =========================================================

        fundamental_slope = fit_fund[0]
        im3_slope = fit_im3[0]

        # =========================================================
        # Extrapolated lines
        # =========================================================

        Pfund_line = np.polyval( fit_fund, PIn )
        PIM3_line = np.polyval( fit_im3, PIn )

        # =========================================================
        # Calculate IIP3
        # =========================================================

        denom = ( fit_fund[0] - fit_im3[0] )
        if np.isclose( denom, 0.0 ):
            IIP3 = None
            OIP3 = None
        else:

            IIP3 = ( fit_im3[1] - fit_fund[1] ) / denom
            OIP3 = np.polyval( fit_fund, IIP3 )

        # =========================================================
        # Return everything
        # =========================================================

        return {
            "Pin": PIn,
            "Pfund": Pfund,
            "PIM3": PIM3,
            "Pfund_line": Pfund_line,
            "PIM3_line": PIM3_line,
            "IIP3": IIP3,
            "OIP3": OIP3,
            "f1": f1,
            "f2": f2,
            "f_im3": f_im3,
            "fundamental_slope": fundamental_slope,
            "im3_slope": im3_slope,
            "n_fit": n_fit,
            "im3_type": im3,
        }



    def PlotIIP3(self,files,f1, f2,R=[100, 100], im3='low', n_fit=5,force_ideal_slopes=False,start_idx=1,figsize=(9, 6),title="IIP3 Analysis"):
        """
        Calculate and plot IIP3 from a two-tone transient/IMD sweep.
        """

        # =========================================================
        # Calculate IIP3
        # =========================================================

        result = self.CalcIIP3( files=files, f1=f1, f2=f2, R=R, im3=im3, n_fit=n_fit, force_ideal_slopes=force_ideal_slopes, start_idx=start_idx )

        # =========================================================
        # Extract results
        # =========================================================

        Pin = result["Pin"]
        Pfund = result["Pfund"]
        PIM3 = result["PIM3"]

        Pfund_line = result["Pfund_line"]
        PIM3_line = result["PIM3_line"]

        IIP3 = result["IIP3"]
        OIP3 = result["OIP3"]

        fundamental_slope = result["fundamental_slope"]
        im3_slope = result["im3_slope"]

        # =========================================================
        # Create figure
        # =========================================================

        fig, ax = plt.subplots( figsize=figsize )

        # =========================================================
        # Measured data
        # =========================================================

        ax.plot( Pin, Pfund, 'o', label="Fundamental", markersize=6 )
        ax.plot( Pin, PIM3, 's', label=f"IM3 ({im3})", markersize=6 )

        # =========================================================
        # Fitted lines
        # =========================================================

        ax.plot( Pin, Pfund_line, '--', label=( f"Fundamental fit " f"({fundamental_slope:.2f} dB/dB)" ) )
        ax.plot( Pin, PIM3_line, '--', label=( f"IM3 fit " f"({im3_slope:.2f} dB/dB)" ) )

        # =========================================================
        # Mark IIP3
        # =========================================================

        if IIP3 is not None and np.isfinite(IIP3):
            Pout_IIP3 = np.polyval(
                np.array([ fundamental_slope, result["Pfund_line"][0] - fundamental_slope * Pin[0]]), IIP3 )
            ax.plot( IIP3, Pout_IIP3, 'x', markersize=12, markeredgewidth=2, label=f"IIP3 = {IIP3:.2f} dBm" )
            ax.axvline(IIP3, linestyle=':', alpha=0.7)
            ax.axhline( OIP3, linestyle=':',alpha=0.7 )
            ax.annotate( f"IIP3 = {IIP3:.2f} dBm\n" f"OIP3 = {OIP3:.2f} dBm", xy=(IIP3, OIP3), xytext=(10, -40), textcoords="offset points", arrowprops=dict( arrowstyle="->" ), fontsize=10 )

        # =========================================================
        # Labels
        # =========================================================

        ax.set_xlabel( "Input Power at f₁ [dBm]" )
        ax.set_ylabel(  "Output Power [dBm]" )
        ax.set_title(  title )
        ax.grid(  True,  which="both", linestyle=":", alpha=0.6 )
        ax.legend()

        # =========================================================
        # Print results
        # =========================================================

        print("\n" + "=" * 60)
        print("IIP3 ANALYSIS")
        print("=" * 60)

        print(
            f"f1               = "
            f"{f1 / 1e9:.6f} GHz"
        )
        print(
            f"f2               = "
            f"{f2 / 1e9:.6f} GHz"
        )
        print(
            f"IM3 frequency    = "
            f"{result['f_im3'] / 1e9:.6f} GHz"
        )

        print("-" * 60)
        print(
            f"Fundamental slope = "
            f"{fundamental_slope:.3f} dB/dB"
        )
        print(
            f"IM3 slope         = "
            f"{im3_slope:.3f} dB/dB"
        )
        print("-" * 60)
        if IIP3 is not None:
            print(
                f"IIP3              = "
                f"{IIP3:.3f} dBm"
            )

        if OIP3 is not None:
            print(
                f"OIP3              = "
                f"{OIP3:.3f} dBm"
            )
        print("=" * 60)
        plt.tight_layout()
        return result, fig
            




    def PlotIIP3_HB( self, file, n_fit=5, cadence_IIP3=None, cadence_OIP3=12.10, figsize=(9, 6)):

        # ============================================================
        # Read Cadence HB CSV
        # ============================================================

        data = pd.read_csv( file, sep="," )
        if data.shape[1] < 4:
            raise ValueError(  "CSV file must contain at least 4 columns." )

        # ============================================================
        # Extract data
        #
        # Column 0: 3rd Order X = Pin
        # Column 1: 3rd Order Y = Pout IM3
        # Column 2: 1st Order X = Pin
        # Column 3: 1st Order Y = Pout Fundamental
        # ============================================================

        Pin_IM3 = data.iloc[:, 0].to_numpy( dtype=float )
        PIM3 = data.iloc[:, 1].to_numpy( dtype=float )
        Pin_Fund = data.iloc[:, 2].to_numpy( dtype=float )
        Pfund = data.iloc[:, 3].to_numpy( dtype=float )

        # ============================================================
        # Remove invalid values
        # ============================================================

        valid_IM3 = ( np.isfinite(Pin_IM3) & np.isfinite(PIM3) )
        valid_Fund = ( np.isfinite(Pin_Fund) & np.isfinite(Pfund) )
        Pin_IM3 = Pin_IM3[valid_IM3]
        PIM3 = PIM3[valid_IM3]
        Pin_Fund = Pin_Fund[valid_Fund]
        Pfund = Pfund[valid_Fund]

        # ============================================================
        # Sort by input power
        # ============================================================

        idx_IM3 = np.argsort( Pin_IM3 )
        idx_Fund = np.argsort( Pin_Fund )
        Pin_IM3 = Pin_IM3[idx_IM3]
        PIM3 = PIM3[idx_IM3]
        Pin_Fund = Pin_Fund[idx_Fund]
        Pfund = Pfund[idx_Fund]

        # ============================================================
        # Number of points used for linear fit
        # ============================================================

        n_fit = min( n_fit, len(Pin_Fund), len(Pin_IM3) )
        if n_fit < 2:
            raise ValueError( "Not enough data points for fitting." )

        # ============================================================
        # Linear fits
        #
        # Fundamental:
        #
        #     Pout = a1 * Pin + b1
        #
        # IM3:
        #
        #     Pout = a3 * Pin + b3
        # ============================================================

        fit_fund = np.polyfit( Pin_Fund[:n_fit], Pfund[:n_fit], 1 )
        fit_im3 = np.polyfit( Pin_IM3[:n_fit], PIM3[:n_fit], 1 )
        a1 = fit_fund[0]
        b1 = fit_fund[1]
        a3 = fit_im3[0]
        b3 = fit_im3[1]

        # ============================================================
        # Calculate Python IIP3
        #
        # a1*Pin + b1 = a3*Pin + b3
        #
        # IIP3 = (b3 - b1) / (a1 - a3)
        # ============================================================

        denominator = ( a1 - a3 )
        if np.isclose( denominator,  0.0 ):
            IIP3 = None
            OIP3 = None

        else:
            IIP3 = ( b3 - b1 ) / denominator
            OIP3 = ( a1 * IIP3 + b1 )

        # ============================================================
        # Cadence IIP3 / OIP3
        #
        # These are independent values.
        #
        # Cadence OIP3 is NOT calculated from the Python fit.
        # ============================================================

        cadence_IIP3_valid = ( cadence_IIP3 is not None and np.isfinite(cadence_IIP3) )
        cadence_OIP3_valid = ( cadence_OIP3 is not None and np.isfinite(cadence_OIP3) )

        # ============================================================
        # Generate extrapolation lines
        # ============================================================

        Pin_min = min( Pin_Fund.min(), Pin_IM3.min() )
        Pin_max = max( Pin_Fund.max(), Pin_IM3.max()  )
        # Extend plot to include Python IIP3
        if ( IIP3 is not None and np.isfinite(IIP3) ):
            Pin_max = max( Pin_max, IIP3 )

        # Extend plot to include Cadence IIP3
        # only if an independent Cadence IIP3 was provided.

        if cadence_IIP3_valid: Pin_max = max( Pin_max, cadence_IIP3 )
        Pin_fit = np.linspace( Pin_min, Pin_max, 500 )
        Pfund_fit = ( a1 * Pin_fit + b1 )
        PIM3_fit = ( a3 * Pin_fit + b3 )

        # ============================================================
        # Plot
        # ============================================================

        fig, ax = plt.subplots( figsize=figsize )

        # ============================================================
        # Measured fundamental
        # ============================================================

        ax.plot( Pin_Fund, Pfund, 'o', markersize=6, label="Fundamental" )

        # ============================================================
        # Measured IM3
        # ============================================================

        ax.plot( Pin_IM3,  PIM3, 's', markersize=6, label="3rd Order" )

        # ============================================================
        # Fundamental fit
        #
        # No legend entry
        # ============================================================

        ax.plot( Pin_fit,  Pfund_fit, '--' )

        # ============================================================
        # IM3 fit
        #
        # No legend entry
        # ============================================================

        ax.plot( Pin_fit, PIM3_fit, '--' )

        # ============================================================
        # Mark Python IIP3 / OIP3
        # ============================================================

        if (  IIP3 is not None and np.isfinite(IIP3)  and OIP3 is not None and np.isfinite(OIP3) ):
            ax.plot( IIP3, OIP3, 'x', markersize=14, markeredgewidth=3, label=( f"Python IIP3 = " f"{IIP3:.2f} dBm") )
            # Vertical Python IIP3 line
            ax.axvline( IIP3, linestyle=':', alpha=0.7 )
            # Horizontal Python OIP3 line
            ax.axhline(  OIP3, linestyle=':', alpha=0.7 )

            # Python annotation
            ax.annotate( f"Python IIP3 = " f"{IIP3:.2f} dBm\n" f"Python OIP3 = " f"{OIP3:.2f} dBm", xy=( IIP3,OIP3),xytext=( 15, 15 ),textcoords="offset points",arrowprops=dict(arrowstyle="->" ),fontsize=10 )

        # ============================================================
        # Mark Cadence OIP3
        #
        # OIP3 is independently entered from Cadence.
        #
        # Since Cadence OIP3 is an output-referred quantity,
        # it is plotted on the output-power axis.
        #
        # If Cadence IIP3 is not available, only the horizontal
        # OIP3 line and annotation are shown.
        # ============================================================

        if cadence_OIP3_valid:

            # Horizontal Cadence OIP3 line

            ax.axhline(cadence_OIP3,linestyle='-.',alpha=0.6 )

            # If Cadence IIP3 is also available,
            # mark the complete Cadence intercept point.

            if cadence_IIP3_valid:
                ax.plot( cadence_IIP3, cadence_OIP3,'D', markersize=9, markeredgewidth=2, label=( f"Cadence OIP3 = " f"{cadence_OIP3:.2f} dBm"))

                # Vertical Cadence IIP3 line
                ax.axvline(cadence_IIP3, linestyle='-.', alpha=0.6)

                # Cadence annotation
                ax.annotate( f"Cadence IIP3 = " f"{cadence_IIP3:.2f} dBm\n"  f"Cadence OIP3 = "  f"{cadence_OIP3:.2f} dBm", xy=( cadence_IIP3, cadence_OIP3 ), xytext=( 15, -45  ),  textcoords="offset points", arrowprops={ "arrowstyle": "->" }, fontsize=10 )

            else:
                # Cadence OIP3 only
                ax.plot( [], [],'D', markersize=9,  markeredgewidth=2, label=( f"Cadence OIP3 = "  f"{cadence_OIP3:.2f} dBm" )  )

                # OIP3 annotation
                ax.annotate( f"Cadence OIP3 = "  f"{cadence_OIP3:.2f} dBm",  xy=( Pin_max, cadence_OIP3 ),  xytext=( -150, -35),textcoords="offset points", arrowprops={"arrowstyle": "->"}, fontsize=10 )

        # ============================================================
        # Axis labels
        # ============================================================

        ax.set_xlabel( "Input Power [dBm]")
        ax.set_ylabel("Output Power [dBm]" )
        ax.grid( True, linestyle=":", alpha=0.6 )
        ax.legend()
        plt.tight_layout()

        # ============================================================
        # Print results
        # ============================================================

        print("\n" + "=" * 60)
        print("IIP3 ANALYSIS - CADENCE HARMONIC BALANCE")
        print("=" * 60)
        print( f"Number of fit points = " f"{n_fit}" )
        print( f"Fundamental slope = " f"{a1:.3f} dB/dB" )
        print( f"IM3 slope         = " f"{a3:.3f} dB/dB" )
        print("-" * 60)

        # ============================================================
        # Python results
        # ============================================================

        if ( IIP3 is not None and np.isfinite(IIP3) ):
            print( f"Python IIP3       = "f"{IIP3:.3f} dBm" )
            print( f"Python OIP3       = " f"{OIP3:.3f} dBm" )
        else:
            print( "Python IIP3 could not be calculated." )
        print("-" * 60)

        # ============================================================
        # Cadence results
        # ============================================================

        if cadence_IIP3_valid:
            print(f"Cadence IIP3      = " f"{cadence_IIP3:.3f} dBm" )
        else:
            print( "Cadence IIP3      = not provided" )
        if cadence_OIP3_valid:
            print(f"Cadence OIP3      = " f"{cadence_OIP3:.3f} dBm" )
        else:
            print( "Cadence OIP3      = not provided" )
        print("=" * 60)

        # ============================================================
        # Return
        # ============================================================

        return {
            "Pin_Fund": Pin_Fund,
            "Pfund": Pfund,

            "Pin_IM3": Pin_IM3,
            "PIM3": PIM3,

            "fundamental_slope": a1,
            "im3_slope": a3,

            "IIP3": IIP3,
            "OIP3": OIP3,

            "cadence_IIP3": cadence_IIP3,
            "cadence_OIP3": cadence_OIP3,

            "fig": fig
        }


    




    def SignalToDistortionRatio(self, files, sim_frequency):

        """
        Compute a signal-to-distortion metric based on harmonic content.

        This function estimates a distortion ratio using the difference between
        the fundamental component and the third harmonic extracted from FFT
        analysis of input and output signals.

        The metric is defined as:

        SDR ≈ P(fundamental) − P(3rd harmonic)

        Parameters
        ----------
        files : list of str
            List of CSV files. Each file must contain:
            - columns 0–1: time and input signal
            - columns 2–3: time and output signal

        sim_frequency : float
            Fundamental frequency of the signal (Hz).

        Returns
        -------
        dict
            Dictionary containing:

            Frequency : pandas.DataFrame
                Frequency axis from the last processed file

            SDR input : numpy.ndarray
                Difference (fundamental − 3rd harmonic) for input signal (dB)

            SDR output : numpy.ndarray
                Difference (fundamental − 3rd harmonic) for output signal (dB)

        Notes
        -----
        - This is a harmonic-based distortion metric, not a classical SDR definition.
        - It uses:
            P1 − P3 (fundamental minus third harmonic level).
        - Results depend on FFT resolution and harmonic extraction accuracy.

        Examples
        --------
        >>> sdr = obj.SignalToDistortionRatio(files, 1e9)
        >>> sdr["SDR input"]
        array([...])
        """
    
        SDR_in, SDR_out = [], []

        for file in files:
            Sig = pd.read_csv(file, sep=",")
            first_harmonic_in = self.ExtractFundamental(Sig.iloc[:, :2], sim_frequency)
            first_harmonic_out = self.ExtractFundamental(Sig.iloc[:, 2:4], sim_frequency)
            third_harmonic_in = self.ExtractThirdFundamental(Sig.iloc[:, :2], sim_frequency)
            third_harmonic_out = self.ExtractThirdFundamental(Sig.iloc[:, 2:4], sim_frequency)
            SDR_in.append(first_harmonic_in - third_harmonic_in) 
            SDR_out.append(first_harmonic_out - third_harmonic_out)

        # Convert to NumPy arrays for vector operations
        SDR_in = np.array(SDR_in)
        SDR_out = np.array(SDR_out)


        SDR = {}
        SDR["Frequency"] = Sig.iloc[:, :1]
        SDR["SDR input"] = SDR_in
        SDR["SDR output"] = SDR_out

        return SDR
    



    def TotalHarmonicDistortion(self, Sig, sim_frequency, number_of_harmonics):
        """
        Compute Total Harmonic Distortion (THD) from time-domain signals.

        This function calculates THD based on FFT-derived harmonic amplitudes.
        It supports both input-only and input/output signal configurations.

        THD is defined as:

        .. math::
            THD = \\frac{\\sqrt{\\sum_{n=2}^{N} V_n^2}}{V_1}

        where:
        - V₁ is the fundamental component
        - Vₙ are higher-order harmonics

        Parameters
        ----------
        Sig : pandas.DataFrame
            Signal data:
            - 2 columns: input only (time, amplitude)
            - 4+ columns: input + output signals

        sim_frequency : float
            Fundamental frequency of the signal (Hz).

        number_of_harmonics : int
            Number of harmonics used in THD computation (including fundamental).

        Returns
        -------
        dict
            Dictionary containing:

            THD_input_percent : float
                THD of input signal in percent

            THD_output_percent : float or None
                THD of output signal in percent (if available)

        Notes
        -----
        - Harmonics are extracted using FFT-based nearest-bin selection.
        - Magnitudes are converted from dB to linear scale using:
            V = 10^(dB/20)
        - THD is computed in linear domain and converted to percentage.
        - Accuracy depends on FFT resolution and harmonic extraction method.

        Raises
        ------
        ValueError
            If input signal does not contain 2 or 4+ columns.

        Examples
        --------
        >>> thd = obj.TotalHarmonicDistortion(df, 1e9, 5)
        >>> thd["THD_input_percent"]
        3.2
        """

        if Sig.shape[1] == 2:
            # Only one signal present
            V1_in = self.ExtractFundamental(Sig.iloc[:, :2], sim_frequency)
            V1_out = None  # No output
            harmonics_in = self.ExtractAllFundamental(Sig.iloc[:, :2], sim_frequency, number_of_harmonics)
            harmonics_out = None
        elif Sig.shape[1] >= 4:
            # Input + output
            V1_in = self.ExtractFundamental(Sig.iloc[:, :2], sim_frequency)
            V1_out = self.ExtractFundamental(Sig.iloc[:, 2:4], sim_frequency)
            harmonics_in = self.ExtractAllFundamental(Sig.iloc[:, :2], sim_frequency, number_of_harmonics)
            harmonics_out = self.ExtractAllFundamental(Sig.iloc[:, 2:4], sim_frequency, number_of_harmonics)
        else:
            raise ValueError("Sig must have 2 or 4 columns (time + signal)")

        # -------------------------------
        # Convert harmonics to linear amplitude
        # -------------------------------
        harmonics_in_vals = list(harmonics_in.values())
        harmonics_in_lin = [10**(v/20) for v in harmonics_in_vals]
        V1_in_lin = 10**(V1_in/20)

        THD_in = np.sqrt(np.sum(np.array(harmonics_in_lin)**2)) / V1_in_lin

        if V1_out is not None:
            harmonics_out_vals = list(harmonics_out.values())
            harmonics_out_lin = [10**(v/20) for v in harmonics_out_vals]
            V1_out_lin = 10**(V1_out/20)
            THD_out = np.sqrt(np.sum(np.array(harmonics_out_lin)**2)) / V1_out_lin
        else:
            THD_out = None

        # -------------------------------
        # Return THD in percentage
        # -------------------------------
        result = {"THD_input_percent": THD_in * 100}
        if THD_out is not None:
            result["THD_output_percent"] = THD_out * 100

        return result
    






    def Eyediagramm(self, Sig, sim_frequency, move_sig1=0, move_sig2=0):
        
        """
        Generate eye diagram data from time-domain signals.

        This function prepares data for eye diagram visualization by interpolating
        the signal onto a uniform time grid and slicing it into periodic segments
        based on the fundamental frequency.

        The eye diagram is constructed by overlapping multiple symbol periods.

        Parameters
        ----------
        Sig : pandas.DataFrame
            Input signal data:
            - 2 columns: [time, signal] (single signal)
            - 4 columns: [time1, signal1, time2, signal2] (dual signal case)

        sim_frequency : float
            Fundamental frequency of the signal (Hz), used to estimate symbol period.

        move_sig1 : int, optional
            Sample shift applied to eye diagram of signal 1.
            Used to horizontally shift the eye opening.

        move_sig2 : int, optional
            Sample shift applied to eye diagram of signal 2 (if present).

        Returns
        -------
        dict
            For single signal (2 columns):
                - "time" : time vector for eye plot
                - "cuts" : interpolated signal segments
                - "Signal" : index vector for slicing

            For dual signal (4 columns):
                - "time" : time vector
                - "cuts_sig1" : eye data for signal 1
                - "Signal1" : index vector for signal 1
                - "cuts_sig2" : eye data for signal 2
                - "Signal2" : index vector for signal 2

        Notes
        -----
        - Signal is interpolated using quadratic interpolation.
        - Time grid is constructed based on estimated symbol period.
        - Eye diagram is formed by overlapping multiple periods.
        - np.roll is used to shift eye position horizontally.
        - Accuracy depends on sampling resolution and interpolation quality.

        Examples
        --------
        >>> eye = obj.Eyediagramm(df, 1e9)
        >>> eye["cuts"]
        array([...])
        """
        if Sig.shape[1] == 2:

            # Read the values 
            time = Sig.iloc[:, 0].to_numpy()  
            signal = Sig.iloc[:, 1].to_numpy()
            
            samples_perT = 1/sim_frequency
            startInd = 2 * samples_perT  # ignore some transient effects at beginning of signal

            # Interpolate the signals
            t = np.arange(min(time),max(time),2*samples_perT*10e-3)
            f_11 = interp1d(time, signal,  kind='quadratic', fill_value="extrapolate")
            signal_interp = f_11(t)

            time_vec = np.linspace(0,startInd,100)
            SigVec = np.arange(0,len(signal_interp)+len(time_vec),len(time_vec))


            # Move the Eye lef and right by changing 0 to int value for example -10 or -10
            if move_sig1 == 0:
                cuts = np.roll(signal_interp, 0)
            else:
                cuts = np.roll(signal_interp, move_sig1)
            
            results = {
                        "time": time_vec,
                        "cuts": cuts,
                        "Signal": SigVec
            }

            return results



        elif Sig.shape[1] >= 4:
            # Read the values 
            time1 = Sig.iloc[:, 0].to_numpy()  
            signal1 = Sig.iloc[:, 1].to_numpy()
            time2 = Sig.iloc[:, 2].to_numpy()  
            signal2 = Sig.iloc[:, 3].to_numpy()
            
            samples_perT = 1/sim_frequency
            startInd = 2 * samples_perT  # ignore some transient effects at beginning of signal

            # Interpolate the signals
            t = np.arange(min(time1),max(time1),2*samples_perT*10e-3)
            f_11 = interp1d(time1, signal1,  kind='quadratic', fill_value="extrapolate")
            f_12 = interp1d(time2, signal2,  kind='quadratic', fill_value="extrapolate")
            signal_interp1 = f_11(t)
            signal_interp2 = f_12(t)


            

            time_vec = np.linspace(0,startInd,100)
            SigVec1 = np.arange(0,len(signal_interp1)+len(time_vec),len(time_vec))
            SigVec2 = np.arange(0,len(signal_interp2)+len(time_vec),len(time_vec))
            
            # Move the Eye lef and right by changing 0 to int value for example -10 or -10
            if move_sig1 == 0:
                cuts1 = np.roll(signal_interp1, 0)
            else:
                cuts1 = np.roll(signal_interp1, move_sig1)
            if move_sig2 == 0:
                cuts2 = np.roll(signal_interp2, 0)
            else:
                cuts2 = np.roll(signal_interp2, move_sig2)

            results = {
                        "time": time_vec,
                        "cuts_sig1": cuts1,
                        "Signal1": SigVec1,
                        "cuts_sig2": cuts2,
                        "Signal2": SigVec2
            }

            return results
        


    # def Eyediagramm(self, Sig, sim_frequency, fs=None, phase_shift1=0.0, phase_shift2=0.0):
        
    #     """
    #     Generate eye diagram data from time-domain signals.

    #     This function prepares data for eye diagram visualization by interpolating
    #     the signal onto a uniform time grid and slicing it into periodic segments
    #     based on the fundamental frequency.

    #     The eye diagram is constructed by overlapping multiple symbol periods.

    #     Parameters
    #     ----------
    #     Sig : pandas.DataFrame
    #         Input signal data:
    #         - 2 columns: [time, signal] (single signal)
    #         - 4 columns: [time1, signal1, time2, signal2] (dual signal case)

    #     sim_frequency : float
    #         Fundamental frequency of the signal (Hz), used to estimate symbol period.

    #     fs : float, optional
    #         Sampling frequency used for uniform resampling. If None, it is estimated
    #         from the input time vector.

    #     phase_shift1 : float, optional
    #         Fractional UI shift applied to eye diagram of signal 1.
    #         Used to horizontally shift the eye opening (0 to 1 corresponds to one symbol period).

    #     phase_shift2 : float, optional
    #         Fractional UI shift applied to eye diagram of signal 2 (if present).

    #     Returns
    #     -------
    #     dict
    #         For single signal (2 columns):
    #             - "time" : time vector for eye plot
    #             - "cuts" : eye diagram matrix (each row = one UI)
    #             - "Signal" : index vector for slicing

    #         For dual signal (4 columns):
    #             - "time" : time vector
    #             - "cuts_sig1" : eye data for signal 1
    #             - "Signal1" : index vector for signal 1
    #             - "cuts_sig2" : eye data for signal 2
    #             - "Signal2" : index vector for signal 2

    #     Notes
    #     -----
    #     - Signal is interpolated using quadratic interpolation.
    #     - Time grid is constructed on a uniform sampling basis.
    #     - Eye diagram is formed by reshaping into symbol-length segments.
    #     - Phase shifting is performed in the time domain (not via np.roll).
    #     - Accuracy depends on sampling resolution and interpolation quality.

    #     Examples
    #     --------
    #     >>> eye = obj.Eyediagramm(df, 1e9)
    #     >>> eye["cuts"]
    #     array([...])
    #     """

    #     import numpy as np
    #     from scipy.interpolate import interp1d

    #     Ts = 1 / sim_frequency  # symbol period

    #     # ---------------------------
    #     # SINGLE SIGNAL
    #     # ---------------------------
    #     if Sig.shape[1] == 2:

    #         time = Sig.iloc[:, 0].to_numpy()
    #         signal = Sig.iloc[:, 1].to_numpy()

    #         if fs is None:
    #             fs = 1 / np.median(np.diff(time))

    #         # uniform time grid
    #         t_uniform = np.arange(time[0], time[-1], 1/fs)

    #         f = interp1d(time, signal, kind='quadratic', fill_value="extrapolate")

    #         # phase shift in time domain (replaces np.roll)
    #         t_shifted = t_uniform + phase_shift1 * Ts
    #         sig = f(t_shifted)

    #         N = int(round(Ts * fs))

    #         sig = sig[:len(sig) - (len(sig) % N)]
    #         eye = sig.reshape((-1, N))

    #         eye_time = np.linspace(0, Ts, N)

    #         return {
    #             "time": eye_time,
    #             "cuts": eye,
    #             "Signal": np.arange(eye.shape[0])
    #         }

    #     # ---------------------------
    #     # DUAL SIGNAL
    #     # ---------------------------
    #     elif Sig.shape[1] >= 4:

    #         time1 = Sig.iloc[:, 0].to_numpy()
    #         signal1 = Sig.iloc[:, 1].to_numpy()
    #         time2 = Sig.iloc[:, 2].to_numpy()
    #         signal2 = Sig.iloc[:, 3].to_numpy()

    #         if fs is None:
    #             fs = 1 / np.median(np.diff(time1))

    #         t1_uniform = np.arange(time1[0], time1[-1], 1/fs)
    #         t2_uniform = np.arange(time2[0], time2[-1], 1/fs)

    #         f1 = interp1d(time1, signal1, kind='quadratic', fill_value="extrapolate")
    #         f2 = interp1d(time2, signal2, kind='quadratic', fill_value="extrapolate")

    #         sig1 = f1(t1_uniform + phase_shift1 * Ts)
    #         sig2 = f2(t2_uniform + phase_shift2 * Ts)

    #         N = int(round(Ts * fs))

    #         sig1 = sig1[:len(sig1) - (len(sig1) % N)]
    #         sig2 = sig2[:len(sig2) - (len(sig2) % N)]

    #         eye1 = sig1.reshape((-1, N))
    #         eye2 = sig2.reshape((-1, N))

    #         eye_time = np.linspace(0, Ts, N)

    #         return {
    #             "time": eye_time,
    #             "cuts_sig1": eye1,
    #             "Signal1": np.arange(eye1.shape[0]),
    #             "cuts_sig2": eye2,
    #             "Signal2": np.arange(eye2.shape[0])
    #         }



    def extract_csv_data(self, file_path):
        """
        Load a CSV file and return all columns as numpy arrays.

        This utility function reads a comma-separated CSV file and converts
        each column into a NumPy array stored in a dictionary with generic keys.

        Parameters
        ----------
        file_path : str
            Path to the CSV file.

        Returns
        -------
        dict
            Dictionary containing all CSV columns as NumPy arrays.

            Keys:
                "col0", "col1", ..., "colN"

            Values:
                numpy.ndarray containing the corresponding column data.

        Notes
        -----
        - The CSV file is assumed to be comma-separated.
        - No header parsing is performed; all rows are treated as data.
        - All columns are assumed to be numeric or convertible to NumPy arrays.
        - Column names are assigned automatically based on index order.

        Examples
        --------
        >>> data = obj.extract_csv_data("signal.csv")
        >>> data["col0"]
        array([0.0, 0.1, 0.2])
        """

        Sig = pd.read_csv(file_path, sep=",")

        data_vec = { f"col{i}": Sig.iloc[:, i].to_numpy() for i in range(Sig.shape[1])}

        return data_vec    


    def HBT_DC_Table_old(self, file_path, transistor_area):
        """
        Create an HBT DC operating-point table from a CSV file.

        Transistors that are not present in transistor_area are ignored.

        JC is calculated in mA/um²:

            JC = IC [mA] / Area [um²]
        """

        # =========================================================
        # Read CSV
        # =========================================================

        df = pd.read_csv( file_path, skipinitialspace=True)

        # Clean column names
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.lstrip("#").str.strip()

        # Replace INF values with NaN
        df = df.replace( [np.inf, -np.inf], np.nan )

        # =========================================================
        # Select required columns
        # =========================================================

        table = df[ [  "instance","temp [C]", "ic [A]", "vcei [V]","region"] ].copy()

        # =========================================================
        # Extract transistor name
        # =========================================================
        #
        # Supported formats:
        #
        # I133.Q5'_VGA.npn_hic_G3
        #       -> Q5'_VGA
        #
        # I135.Q2'_Buffer.npn_hic_G3
        #       -> Q2'_Buffer
        #
        # /I133/Q4_VGA/npn_hic_G3
        #       -> Q4_VGA
        #
        # I15.Q3_Driver.npn_hic_G3
        #       -> Q3_Driver
        #
        # =========================================================

        def extract_transistor_name(instance):

            name = str(instance).strip()

            # -----------------------------------------------------
            # Dot-separated format
            # I133.Q5'_VGA.npn_hic_G3
            # -----------------------------------------------------

            if "." in name:

                parts = name.split(".")

                if len(parts) >= 2:
                    name = parts[1]

            # -----------------------------------------------------
            # Slash-separated format
            # /I133/Q4_VGA/npn_hic_G3
            # -----------------------------------------------------

            elif "/" in name:
                parts = [ part for part in name.split("/")if part != "" ]

                if len(parts) >= 2:
                    name = parts[-2]

            # -----------------------------------------------------
            # Remove model suffix if necessary
            # -----------------------------------------------------

            if name.endswith("npn_hic_G3"):
                name = name.replace( "npn_hic_G3", "").rstrip(".")

            # -----------------------------------------------------
            # Convert escaped apostrophe
            #
            # Q5\'_VGA -> Q5'_VGA
            # -----------------------------------------------------

            name = name.replace( "\\'", "'")
            return name.strip()

        # Extract transistor names
        table["Transistor"] = table["instance"].apply(extract_transistor_name)

        # =========================================================
        # Ignore transistors that are not in transistor_area
        # =========================================================

        table = table[ table["Transistor"].isin(transistor_area.keys() )].copy()

        # Reset index after filtering
        table.reset_index( drop=True, inplace=True)

        # =========================================================
        # Add emitter area
        # =========================================================

        table["Area [um²]"] = table["Transistor"].map( transistor_area )

        # =========================================================
        # Convert collector current
        #
        # A -> mA
        # =========================================================

        table["ic [mA]"] = (table["ic [A]"] * 1e3 )

        # =========================================================
        # Calculate collector current density
        #
        # JC = IC / Area
        #
        # IC   -> mA
        # Area -> um²
        # JC   -> mA/um²
        # =========================================================

        table["JC [mA/um²]"] = ( table["ic [mA]"] /table["Area [um²]"])

        # =========================================================
        # Rename columns
        # =========================================================

        table = table.rename(
            columns={
                "instance": "Instance",
                "temp [C]": "Temp. [°C]",
                "ic [mA]": "IC [mA]",
                "vcei [V]": "VCE [V]",
                "region": "Region"
            }
        )

        # =========================================================
        # Final column order
        # =========================================================

        table = table[
            [
                "Instance",
                "Transistor",
                "Temp. [°C]",
                "IC [mA]",
                "Area [um²]",
                "JC [mA/um²]",
                "VCE [V]",
                "Region"
            ]
        ]

        # =========================================================
        # Round values
        # =========================================================

        table["Temp. [°C]"] = (table["Temp. [°C]"].round(2) )
        table["IC [mA]"] = (table["IC [mA]"].round(3) )
        table["Area [um²]"] = (table["Area [um²]"].round(4))
        table["JC [mA/um²]"] = ( table["JC [mA/um²]"].round(3) )
        table["VCE [V]"] = ( table["VCE [V]"].round(3) )

        # =========================================================
        # Create Matplotlib table
        # =========================================================

        fig, ax = plt.subplots( figsize=(20, 3.5) )
        ax.axis("off")

        tbl = ax.table(
            cellText=table.values,
            colLabels=table.columns,
            cellLoc="center",
            loc="center",
            colWidths=[
                0.30,   # Instance
                0.14,   # Transistor
                0.10,   # Temperature
                0.10,   # IC
                0.11,   # Area
                0.14,   # JC
                0.10,   # VCE
                0.15    # Region
            ]
        )

        # =========================================================
        # Table formatting
        # =========================================================

        tbl.auto_set_font_size(False)
        tbl.set_fontsize(12)
        tbl.scale(  1, 2.0 )

        # =========================================================
        # Return
        # =========================================================

        return table, fig
        



    def HBT_DC_Table(self, file_path, transistor_area):
        """
        Create an HBT DC operating-point table from old or new CSV data.

        Supported CSV formats:

        OLD:
            instance, temp [C], ..., ic [A], ..., vcei [V], ..., region

        NEW:
            instance, trise [C], ..., vce [V], ..., temp [C], ..., ic [A], ..., region

        Supported instance formats:

            I97.Q4'_VGA.npn_hic_G3
                -> Q4'_VGA

            /I97/Q4_VGA/npn_hic_G3
                -> Q4_VGA

            /Q0
                -> Q0

        Transistors that are not present in transistor_area are ignored.

        JC is calculated in mA/um²:

            JC = IC [mA] / Area [um²]
        """

        # =========================================================
        # Read CSV
        # =========================================================

        df = pd.read_csv( file_path, skipinitialspace=True)

        # =========================================================
        # Clean column names
        # =========================================================

        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.lstrip("#").str.strip()

        # =========================================================
        # Replace INF values with NaN
        # =========================================================

        df = df.replace( [np.inf, -np.inf],np.nan)

        # =========================================================
        # Determine VCE column
        #
        # Old:
        #     vcei [V]
        #
        # New:
        #     vce [V]
        # =========================================================

        if "vcei [V]" in df.columns:
            vce_column = "vcei [V]"

        elif "vce [V]" in df.columns:
            vce_column = "vce [V]"

        else:
            raise ValueError("No VCE column found. ""Expected either 'vcei [V]' or 'vce [V]'.")

        # =========================================================
        # Check required columns
        # =========================================================

        required_columns = [
            "instance",
            "temp [C]",
            "ic [A]",
            vce_column,
            "region"
        ]

        missing_columns = [column for column in required_columns if column not in df.columns]
        if missing_columns:
            raise ValueError( f"Missing required columns: {missing_columns}" )

        # =========================================================
        # Select required columns
        # =========================================================

        table = df[
            [
                "instance",
                "temp [C]",
                "ic [A]",
                vce_column,
                "region"
            ]
        ].copy()

        # =========================================================
        # Extract transistor name
        # =========================================================

        def extract_transistor_name(instance):

            name = str(instance).strip()

            # -----------------------------------------------------
            # NEW FORMAT
            #
            # /Q0
            # /Q1
            # /Q2
            #
            # -----------------------------------------------------

            if name.startswith("/"):

                parts = [ part for part in name.split("/") if part != "" ]
                # /Q0
                if len(parts) == 1:
                    name = parts[0]

                # -------------------------------------------------
                # OLD slash format
                #
                # /I97/Q4_VGA/npn_hic_G3
                #
                # -> Q4_VGA
                # -------------------------------------------------

                elif len(parts) >= 2:
                    if parts[-1] == "npn_hic_G3":
                        name = parts[-2]
                    else:
                        name = parts[-1]

            # -----------------------------------------------------
            # OLD dot format
            #
            # I97.Q4'_VGA.npn_hic_G3
            #
            # -> Q4'_VGA
            # -----------------------------------------------------

            elif "." in name:
                parts = name.split(".")
                if len(parts) >= 2:
                    name = parts[1]

            # -----------------------------------------------------
            # Remove model suffix if necessary
            # -----------------------------------------------------

            if name.endswith("npn_hic_G3"):
                name = name.replace( "npn_hic_G3", "" ).rstrip(".")

            # -----------------------------------------------------
            # Convert escaped apostrophe
            #
            # Q4\'_VGA -> Q4'_VGA
            # -----------------------------------------------------

            name = name.replace( "\\'", "'" )
            return name.strip()

        # =========================================================
        # Extract transistor names
        # =========================================================

        table["Transistor"] = table["instance"].apply( extract_transistor_name )

        # =========================================================
        # Ignore transistors not in transistor_area
        # =========================================================

        table = table[ table["Transistor"].isin(  transistor_area.keys()  )  ].copy()

        # =========================================================
        # Check whether anything matched
        # =========================================================

        if table.empty:

            raise ValueError(
                "No matching transistors found.\n\n"
                "Transistors extracted from CSV:\n"
                f"{df['instance'].apply(extract_transistor_name).tolist()}\n\n"
                "Transistors in transistor_area:\n"
                f"{list(transistor_area.keys())}"
            )

        # =========================================================
        # Reset index
        # =========================================================

        table.reset_index(  drop=True, inplace=True )

        # =========================================================
        # Add emitter area
        # =========================================================

        table["Area [um²]"] = table["Transistor"].map( transistor_area )

        # =========================================================
        # Convert collector current
        #
        # A -> mA
        # =========================================================

        table["ic [mA]"] = ( table["ic [A]"] * 1e3 )

        # =========================================================
        # Calculate collector current density
        #
        # JC = IC / Area
        #
        # IC   -> mA
        # Area -> um²
        # JC   -> mA/um²
        # =========================================================

        table["JC [mA/um²]"] = ( table["ic [mA]"] / table["Area [um²]"] )

        # =========================================================
        # Rename columns
        # =========================================================

        table = table.rename(
            columns={
                "instance": "Instance",
                "temp [C]": "Temp. [°C]",
                "ic [mA]": "IC [mA]",
                vce_column: "VCE [V]",
                "region": "Region"
            }
        )

        # =========================================================
        # Final column order
        # =========================================================

        table = table[
            [
                "Instance",
                "Transistor",
                "Temp. [°C]",
                "IC [mA]",
                "Area [um²]",
                "JC [mA/um²]",
                "VCE [V]",
                "Region"
            ]
        ]

        # =========================================================
        # Round values
        # =========================================================

        table["Temp. [°C]"] = ( table["Temp. [°C]"].round(2) )
        table["IC [mA]"] = ( table["IC [mA]"].round(3) )
        table["Area [um²]"] = ( table["Area [um²]"].round(4) )
        table["JC [mA/um²]"] = ( table["JC [mA/um²]"].round(3) )
        table["VCE [V]"] = ( table["VCE [V]"].round(3) )

        # =========================================================
        # Create Matplotlib table
        # =========================================================

        fig, ax = plt.subplots(figsize=(20, 3.5) )
        ax.axis("off")
        tbl = ax.table(
            cellText=table.values,
            colLabels=table.columns,
            cellLoc="center",
            loc="center",
            colWidths=[
                0.30,   # Instance
                0.14,   # Transistor
                0.10,   # Temperature
                0.10,   # IC
                0.11,   # Area
                0.14,   # JC
                0.10,   # VCE
                0.15    # Region
            ]
        )

        # =========================================================
        # Table formatting
        # =========================================================

        tbl.auto_set_font_size(False)
        tbl.set_fontsize(12)
        tbl.scale(  1, 2.0 )

        # =========================================================
        # Return
        # =========================================================

        return table, fig



    def Source_Table(self, file_path, instance_width=0.20):
        """
        Read a source operating-point CSV file and create a formatted table.

        Parameters
        ----------
        file_path : str
            Path to the source CSV file.

        instance_width : float
            Width of the Instance column in the matplotlib table.

        Returns
        -------
        table : pandas.DataFrame
            Processed source data including a Total row.

        fig : matplotlib.figure.Figure
            Matplotlib figure containing the table.

        total_power_mW : float
            Total absolute power of all sources in mW.
        """

        # ---------------------------------------------------------
        # Read CSV
        # ---------------------------------------------------------

        df = pd.read_csv( file_path, skipinitialspace=True )

        # ---------------------------------------------------------
        # Clean column names
        # ---------------------------------------------------------

        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.lstrip("#").str.strip()

        # ---------------------------------------------------------
        # Convert INF values to NaN
        # ---------------------------------------------------------

        df = df.replace([np.inf, -np.inf], np.nan)

        # ---------------------------------------------------------
        # Select parameters
        # ---------------------------------------------------------

        table = df[ [ "instance",  "v [V]", "i [A]", "pwr [W]" ]  ].copy()

        # ---------------------------------------------------------
        # Convert units
        # ---------------------------------------------------------

        table["i [mA]"] = table["i [A]"] * 1e3
        table["pwr [mW]"] = table["pwr [W]"] * 1e3

        # ---------------------------------------------------------
        # Rename columns
        # ---------------------------------------------------------

        table = table.rename( columns={"instance": "Instance", "v [V]": "V [V]" })

        # ---------------------------------------------------------
        # Select final columns
        # ---------------------------------------------------------

        table = table[ ["Instance", "V [V]", "i [mA]","pwr [mW]" ] ]

        # ---------------------------------------------------------
        # Calculate total absolute power
        # ---------------------------------------------------------

        total_power_mW = table["pwr [mW]"].abs().sum()

        # ---------------------------------------------------------
        # Add total row
        # ---------------------------------------------------------

        total_row = pd.DataFrame(
            [{
                "Instance": "Total",
                "V [V]": np.nan,
                "i [mA]": np.nan,
                "pwr [mW]": total_power_mW
            }]
        )

        table = pd.concat( [table, total_row], ignore_index=True )

        # ---------------------------------------------------------
        # Round values
        # ---------------------------------------------------------

        table["V [V]"] = table["V [V]"].round(3)
        table["i [mA]"] = table["i [mA]"].round(3)
        table["pwr [mW]"] = table["pwr [mW]"].round(3)

        # ---------------------------------------------------------
        # Create table
        # ---------------------------------------------------------

        fig, ax = plt.subplots(figsize=(10, 3.5))
        ax.axis("off")

        tbl = ax.table(
            cellText=table.values,
            colLabels=table.columns,
            cellLoc="center",
            loc="center"
        )

        tbl.auto_set_font_size(False)
        tbl.set_fontsize(12)
        tbl.scale(1, 2.0)

        # ---------------------------------------------------------
        # Make Instance column wider
        # ---------------------------------------------------------

        for row in range(len(table) + 1):
            tbl[(row, 0)].set_width(instance_width)

        # ---------------------------------------------------------
        # Highlight total row
        # ---------------------------------------------------------

        total_row_index = len(table)

        for col in range(len(table.columns)):
            tbl[(total_row_index, col)].set_text_props(weight="bold")

        return table, fig, total_power_mW