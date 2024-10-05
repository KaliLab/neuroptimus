import numpy
# Fixed parameters
protoparams_fixed = { 'Duration': 9240000, 'tolerance': 1e-6, 'Ca_input_onset': 7200000}

# Stimulus protocols:       HFS (100 Hz, 1 s)
protoparams_var = { #    	[0]
    'Ca_input_Ns':      	[100], 
    'Ca_input_freqs':   	[100],
    'Ca_input_Ntrains': 	[1],
    'Ca_input_trainTs': 	[1],
    'Ca_input_durs':    	[3]         #used a standard 3-ms Ca flux for all cases
}

# Measured species
Measured_species = [ ['Ca'],
                     ['GluR1_S845', 'GluR1_S845_S831', 'GluR1_S845_CKCam', 'GluR1_S845_CKpCam', 'GluR1_S845_CKp', 'GluR1_S845_PKCt', 'GluR1_S845_PKCp', 'GluR1_S845_PP1', 'GluR1_S845_S831_PP1', 'GluR1_S845_PP2B', 'GluR1_S845_S831_PP2B', 'GluR1_memb_S845', 'GluR1_memb_S845_S831', 'GluR1_memb_S845_CKCam', 'GluR1_memb_S845_CKpCam', 'GluR1_memb_S845_CKp', 'GluR1_memb_S845_PKCt', 'GluR1_memb_S845_PKCp', 'GluR1_memb_S845_PP1', 'GluR1_memb_S845_S831_PP1', 'GluR1_memb_S845_PP2B', 'GluR1_memb_S845_S831_PP2B'],
                     ['GluR1_S831', 'GluR1_S845_S831', 'GluR1_S831_PKAc', 'GluR1_S845_S831_PP1', 'GluR1_S831_PP1', 'GluR1_S845_S831_PP2B', 'GluR1_memb_S831', 'GluR1_memb_S845_S831', 'GluR1_memb_S831_PKAc', 'GluR1_memb_S845_S831_PP1', 'GluR1_memb_S831_PP1', 'GluR1_memb_S845_S831_PP2B'],
                     ['GluR1_S845_S831', 'GluR1_S845_S831_PP1', 'GluR1_S845_S831_PP2B', 'GluR1_memb_S845_S831', 'GluR1_memb_S845_S831_PP1', 'GluR1_memb_S845_S831_PP2B'],
                     ['GluR1_memb', 'GluR1_memb_S845', 'GluR1_memb_S831', 'GluR1_memb_S845_S831', 'GluR1_memb_PKAc', 'GluR1_memb_CKCam', 'GluR1_memb_CKpCam', 'GluR1_memb_CKp', 'GluR1_memb_PKCt', 'GluR1_memb_PKCp', 'GluR1_memb_S845_CKCam', 'GluR1_memb_S845_CKpCam', 'GluR1_memb_S845_CKp', 'GluR1_memb_S845_PKCt', 'GluR1_memb_S845_PKCp', 'GluR1_memb_S831_PKAc', 'GluR1_memb_S845_PP1', 'GluR1_memb_S845_S831_PP1', 'GluR1_memb_S831_PP1', 'GluR1_memb_S845_PP2B', 'GluR1_memb_S845_S831_PP2B'],
                     ['GluR1_memb_S831', 'GluR1_memb_S845_S831', 'GluR1_memb_S831_PKAc', 'GluR1_memb_S845_S831_PP1', 'GluR1_memb_S831_PP1', 'GluR1_memb_S845_S831_PP2B'],
                     ['GluR2_S880', 'GluR2_S880_PP2A', 'GluR2_memb_S880', 'GluR2_memb_S880_PP2A'],
                     ['GluR2_memb', 'GluR2_memb_PKCt', 'GluR2_memb_PKCp', 'GluR2_memb_S880', 'GluR2_memb_S880_PP2A'],
                     ['CK', 'CKCaMCa4', 'CKpCaMCa4', 'CKp', 'Complex', 'pComplex', 'CKpPP1', 'CKpCaMCa4PP1', 'Ng', 'NgCaM', 'CaM', 'CaMCa2', 'CaMCa3', 'CaMCa4', 'GluR1_CKCam', 'GluR1_CKpCam', 'GluR1_CKp'],
                     ['PKAcLR', 'PKAcpLR', 'PKAcppLR', 'PKAcpppLR', 'PKAcR', 'PKAcpR', 'PKAcppR', 'PKAcpppR', 'PKA', 'PKAcAMP4', 'PKAr', 'PKAc', 'I1PKAc', 'GluR1_PKAc', 'GluR1_S831_PKAc', 'GluR1_memb_PKAc', 'GluR1_memb_S831_PKAc', 'PKAcPDE4', 'PKAc_PDE4_cAMP'],
                     ['Glu', 'MGluR', 'MGluR_Glu', 'MGluR_Glu_desens', 'PLC', 'PLCCa', 'PLCCaGqaGTP', 'PLCGqaGTP', 'Pip2', 'PLCCaPip2', 'PLCCaGqaGTPPip2', 'Ip3', 'PLCCaDAG', 'PLCCaGqaGTPDAG', 'PIkinase', 'Ip3degPIk', 'PKC', 'PKCCa', 'PKCt', 'PKCp', 'DAG', 'DGL', 'CaDGL', 'DAGCaDGL', 'GluR2_PKCt', 'GluR2_PKCp', 'PLA2', 'CaPLA2', 'CaPLA2Pip2', 'AA'],
                     ['CaOut', 'CaOutLeak', 'Leak', 'Calbin', 'CalbinC', 'LOut', 'Epac1', 'Epac1cAMP', 'PMCA', 'NCX', 'PMCACa', 'NCXCa', 'L', 'R', 'Gs', 'Gi', 'LR', 'LRGs', 'pLR', 'ppLR', 'pppLR', 'ppppLR', 'ppppLRGi', 'ppppLRGibg', 'pR', 'ppR', 'pppR', 'ppppR', 'ppppRGi', 'ppppRGibg'],
                     ['GsR', 'GsaGTP', 'GsaGDP', 'GiaGTP', 'GiaGDP', 'Gibg', 'Gsbg', 'LRGsbg', 'AC1', 'AC1GsaGTP', 'AC1GsaGTPCaMCa4', 'AC1GsaGTPCaMCa4ATP', 'AC1GiaGTP', 'AC1GiaGTPCaMCa4', 'AC1GiaGTPCaMCa4ATP', 'AC1GsaGTPGiaGTP', 'AC1GsaGTPGiaGTPCaMCa4', 'AC1GsGiCaMCa4ATP', 'ATP', 'cAMP', 'AC1CaMCa4', 'AC1CaMCa4ATP', 'AC8', 'AC8CaMCa4', 'AC8CaMCa4ATP'],
                     ['PDE1', 'PDE1CaMCa4', 'PDE1CaMCa4cAMP', 'AMP', 'PP2B', 'PP2BCaM', 'PP2BCaMCa2', 'PP2BCaMCa3', 'PP2BCaMCa4', 'I1', 'Ip35', 'PP1', 'Ip35PP1', 'Ip35PP2BCaMCa4', 'Ip35PP1PP2BCaMCa4', 'PP1PP2BCaMCa4'],
                     ['PDE4', 'PDE4cAMP', 'pPDE4', 'pPDE4cAMP', 'fixedbuffer', 'fixedbufferCa', 'MGluR_Gqabg_Glu', 'GluOut', 'Gqabg', 'GqaGTP', 'GqaGDP', 'DAGK', 'DAGKdag', 'PA',  '2AG', '2AGdegrad', 'Ip3degrad', 'PP2A', 'ACh', 'M1R', 'AChM1R', 'M1RGq', 'AChM1RGq'],
                     ['GluR1_PKCt','GluR1_PKCp', 'GluR2', 'ACh', 'AChM1R', 'AChM1RGq'],
                     'syncond']

# Experiments: [ [STIMULUS PROTOCOL INDEX], [CAFLUX COEFF], [LFLUX COEFF], [GLUFLUX COEFF], [ACHFLUX COEFF], [BLOCKED], [ALTERED] ]
Experiments = [ [0, 1.0, 0.0, 1.0, 0.0, 'None', []],				        # 0: control
                [0, 1.0, 0.0, 1.0, 0.0, 'None', [[317],0]] ] 	            # 1: PKAc separation from PKAcAMP4 blocked

#Measurement:  [ [ [EXPERIMENT_INDEX] ] ]
Measurements = [ [ [0,1]  ] ]

Measurements_txt = [['Ma 2008 differential, ascending', 'Control (HFS LTP)', 'PKA blocked (HFS LTP)'] ]

def get_measurement_protocol():
    return [Measurements, Experiments, protoparams_fixed, protoparams_var, Measured_species, Measurements_txt]
