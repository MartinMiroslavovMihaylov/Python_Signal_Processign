import numpy as np 
from scipy.interpolate import interp1d
from numpy import polyfit, polyval
import pandas as pd




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
            elif Metal == "TC1":
                MaxCurrent = 13.6 * (Width - 0.2)
            elif Metal == "TC2":
                MaxCurrent = 13.6* (Width - 0.2)
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
            Port 1 o------|          |-----o Port 2
                          |   DUT    |
            Port 3 o------|__________|-----o Port 4    
                         
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




            # Differential - Differential
            SDD11 = 0.5*(S11 - S13 - S31 + S33) # is the ratio of the differential signal coming out of Port 1 to the differential signal going into Port 1. It is the differential RL out of Port 1.
            SDD12 = 0.5*(S12 - S14 - S32 + S34) # is the ratio of the differential signal coming out of Port 1 to the differential signal going into Port 2. It is the differential IL from Port 2 to Port 1.
            SDD21 = 0.5*(S21 - S23 - S41 + S43) # is the ratio of the differential signal coming out of Port 2 to the differential signal going into Port 1. It is the differential IL from Port 1 to Port 2. 
            SDD22 = 0.5*(S22 - S24 - S42 + S44) # is the ratio of the differential signal coming out of Port 2 to the differential signal going into Port 2. It is the differential RL out of Port 2.

            # Common-Differential 
            SDC11 = 0.5*(S11 + S13 - S31 - S33) # is the ratio of the differential signal coming out of Port 1 to the common signal going into Port 1.
            SDC12 = 0.5*(S12 + S14 - S32 - S34) # is the ratio of the differential signal coming out of Port 1 to the common signal going into Port 2.
            SDC21 = 0.5*(S21 + S23 - S41 - S43) # is the ratio of the differential signal coming out of Port 2 to the common signal going into Port 1.
            SDC22 = 0.5*(S22 + S24 - S42 - S44) # is the ratio of the differential signal coming out of Port 2 to the common signal going into Port 2.

            # Differential-Common
            SCD11 = 0.5*(S11 - S13 + S31 - S33) # is the ratio of the common signal coming out of Port 1 to the differential signal going into Port 1.
            SCD12 = 0.5*(S12 - S14 + S32 - S34) # is the ratio of the common signal coming out of Port 1 to the differential signal going into Port 2.
            SCD21 = 0.5*(S21 - S23 + S41 - S43) # is the ratio of the common signal coming out of Port 2 to the differential signal going into Port 1.
            SCD22 = 0.5*(S22 - S24 + S42 - S44) # is the ratio of the common signal coming out of Port 2 to the differential signal going into Port 2.

            # Common-Common 
            SCC11 = 0.5*(S11 + S13 + S31 + S33) # is the ratio of the common signal coming out of Port 1 to the common signal going into Port 1.
            SCC12 = 0.5*(S12 + S14 + S32 + S34) # is the ratio of the common signal coming out of Port 1 to the common signal going into Port 2.
            SCC21 = 0.5*(S21 + S23 + S41 + S43) # is the ratio of the common signal coming out of Port 2 to the common signal going into Port 1.
            SCC22 = 0.5*(S22 + S24 + S42 + S44) # is the ratio of the common signal coming out of Port 2 to the common signal going into Port 2.

            SDD = {}
            SDD["Frequency"] = self.frequency
            SDD["SDD11"] = 20*np.log10(np.abs(SDD11))
            SDD["SDD12"] = 20*np.log10(np.abs(SDD12))
            SDD["SDD21"] = 20*np.log10(np.abs(SDD21))
            SDD["SDD22"] = 20*np.log10(np.abs(SDD22))

            SDC = {}
            SDC["Frequency"] = self.frequency
            SDC["SDC11"] = 20*np.log10(np.abs(SDC11))
            SDC["SDC12"] = 20*np.log10(np.abs(SDC12))
            SDC["SDC21"] = 20*np.log10(np.abs(SDC21))
            SDC["SDC22"] = 20*np.log10(np.abs(SDC22))

            SCD = {}
            SCD["Frequency"] = self.frequency
            SCD["SCD11"] = 20*np.log10(np.abs(SCD11))
            SCD["SCD12"] = 20*np.log10(np.abs(SCD12))
            SCD["SCD21"] = 20*np.log10(np.abs(SCD21))
            SCD["SCD22"] = 20*np.log10(np.abs(SCD22))

            SCC = {}
            SCC["Frequency"] = self.frequency
            SCC["SCC11"] = 20*np.log10(np.abs(SCC11))
            SCC["SCC12"] = 20*np.log10(np.abs(SCC12))
            SCC["SCC21"] = 20*np.log10(np.abs(SCC21))
            SCC["SCC22"] = 20*np.log10(np.abs(SCC22))


            return SDD, SDC, SCD, SCC
    

        else:
            raise ValueError("This function works only when you need to calculate an 4-Port S-Parameters to 2-Port!")




    ########################################################
    # Impedanz calculator
    ########################################################

    def Zc_Calc(self):

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

            Zc = 100 * np.sqrt( ((1+S11)**2 - S21**2)/ ((1-S11)**2 - S21**2) + 0j)

            return Zc

            
        else:
            # Read data
            S11= 20*np.log10(np.abs(self.S11_re + 1j*self.S11_im))
            S21= 20*np.log10(np.abs(self.S21_re + 1j*self.S21_im))

            Zc = 50 * np.sqrt( ((1+S11)**2 - S21**2)/ ((1-S11)**2 - S21**2) )

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
            Port 1 o------|          |-----o Port 2
                          |   DUT    |
            Port 3 o------|__________|-----o Port 4       

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
            Port 1 o------|          |-----o Port 2
                          |   DUT    |
            Port 3 o------|__________|-----o Port 4     

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


            SDD11 = 0.5*(S11 - S13 - S31 + S33) # is the ratio of the differential signal coming out of Port 1 to the differential signal going into Port 1. It is the differential RL out of Port 1.
            SDD12 = 0.5*(S12 - S14 - S32 + S34) # is the ratio of the differential signal coming out of Port 1 to the differential signal going into Port 2. It is the differential IL from Port 2 to Port 1.
            SDD21 = 0.5*(S21 - S23 - S41 + S43) # is the ratio of the differential signal coming out of Port 2 to the differential signal going into Port 1. It is the differential IL from Port 1 to Port 2. 
            SDD22 = 0.5*(S22 - S24 - S42 + S44) # is the ratio of the differential signal coming out of Port 2 to the differential signal going into Port 2. It is the differential RL out of Port 2.


            Delta = SDD11*SDD22 - SDD12*SDD21

            mu = (1 - np.abs(SDD11)**2) / (np.abs(SDD22 - Delta * np.conj(SDD11)) + np.abs(SDD12 * SDD21))

            # μ' (mu prime)
            mu_prime = (1 - np.abs(SDD22)**2) / (np.abs(SDD11 - Delta * np.conj(SDD22)) + np.abs(SDD12 * SDD21))

            return mu, mu_prime

        else:
            S11 = self.S11_re + 1j*self.S11_im
            S12 = self.S12_re + 1j*self.S12_im

            S21 = self.S21_re + 1j*self.S21_im
            S22 = self.S22_re + 1j*self.S22_im
        

            Delta = S11*S22 - S12*S21

            mu = (1 - np.abs(S11)**2) / (np.abs(S22 - Delta * np.conj(S11)) + np.abs(S12 * S21))

            # μ' (mu prime)
            mu_prime = (1 - np.abs(S22)**2) / (np.abs(S11 - Delta * np.conj(S22)) + np.abs(S12 * S21))

            return mu, mu_prime




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
    
    


    
    def ExtractFundamental(self, Signal, sim_frequency):
        """
        Extract the fundamental frequency component from an FFT spectrum.

        This function identifies the FFT bin closest to the expected fundamental
        frequency and returns its magnitude in dB.

        The spectrum is first computed using `CalcFFT`, and then the nearest
        frequency bin is selected.

        Parameters
        ----------
        Signal : pandas.DataFrame
            Time-domain signal data (see `CalcFFT` for format requirements).

        sim_frequency : float
            Expected fundamental frequency (Hz).

        Returns
        -------
        float
            Magnitude of the fundamental frequency component in dB.

        Notes
        -----
        - The function does NOT perform true quadratic interpolation.
        - The value is taken from the closest FFT bin only.
        - A small offset (1e-12) is added to avoid log(0).

        Examples
        --------
        >>> P_fund = obj.ExtractFundamental(df, 1e9)
        >>> print(P_fund)
        -12.3
        """
        # Get FFT
        data = self.CalcFFT(Signal, sim_frequency)
        freq_array = data["freq"]
        Y_array = data["Y"]

        # Step 1: find the index of the bin closest to the fundamental frequency
        idx = np.argmin(np.abs(freq_array - sim_frequency))

        # Step 2: select 3 bins: center and neighbors
        idx_min = max(0, idx - 1)
        idx_max = min(len(Y_array), idx + 2)  # Python slicing excludes last index
        # Y_local = Y_array[idx_min:idx_max]
        Y_local = 20*np.log10(Y_array[idx] + 1e-12)
        freq_local = freq_array[idx_min:idx_max]


        return Y_local
    
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
        




    def Compression_Point(self, files, sim_frequency):
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

        for file in files:
            Sig = pd.read_csv(file, sep=",")
            PIn.append(self.ExtractFundamental(Sig.iloc[:, :2], sim_frequency))
            POut.append(self.ExtractFundamental(Sig.iloc[:, 2:4], sim_frequency))

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

        data_vec = {
            f"col{i}": Sig.iloc[:, i].to_numpy()
            for i in range(Sig.shape[1])
        }

        return data_vec    