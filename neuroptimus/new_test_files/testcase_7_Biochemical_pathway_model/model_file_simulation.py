from neuron import h, rxd
import numpy as np
import time
import scipy.io
import sys
import re
import os
import matplotlib.pyplot as plt

h.load_file('stdrun.hoc')
dend = h.Section(name='dend')
dend.L=1
dend.diam=0.79788
cyt = rxd.Region([dend], name='cyt', nrn_region='i')
my_volume = 0.50000*1e-15 #litres

Duration = 1000
tolerance = 1e-6
Ca_input_onset = 800
Ca_input_N     = 100
Ca_input_freq  = 100
Ca_input_dur   = 0.005
Ca_input_flux  = 600.0
L_input_onset  = 800
L_input_flux   = 2.0
Glu_input_flux = 50.0
ACh_input_flux = 2.0
Ntrains        = 1
trainT = 3000

initfile = ''
addition = ''
blocked = []
blockeds = []
block_factor = 1.0
alteredk = []
alteredks = []
altered_factor = 1.0
tolstochange = 'Gs,Calbin,CalbinC,PMCA,PMCACa,PP2B,Gi,GiaGDP,Gibg,Gsbg,GsaGDP,CaOut,CaOutLeak,Leak,PDE1,Ng,NgCaM,CaM,CaMCa2,CaMCa4,fixedbuffer,fixedbufferCa,DGL,CaDGL'.split(',')
tolschange = [float(x) for x in '3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,2,2,1,1'.split(',')]
filename = 'nrn_tstop'+str(Duration)+'_tol'+str(tolerance)+addition+'_onset'+str(Ca_input_onset)+'_n'+str(Ca_input_N)+'_freq'+str(Ca_input_freq)+'_dur'+str(Ca_input_dur)+'_flux'+str(Ca_input_flux)+'_Lflux'+str(L_input_flux)+'_Gluflux'+str(Glu_input_flux)+'_AChflux'+str(ACh_input_flux)+'_Ntrains'+str(Ntrains)+'_trainT'+str(trainT)

if len(sys.argv) > 1:
  Duration = int(sys.argv[1])
if len(sys.argv) > 2:
  tolerance = float(sys.argv[2])
if len(sys.argv) > 3:
  Ca_input_onset = float(sys.argv[3])
if len(sys.argv) > 4:
  Ca_input_N     = int(sys.argv[4])
if len(sys.argv) > 5:
  Ca_input_freq  = float(sys.argv[5])
if len(sys.argv) > 6:
  Ca_input_dur   = float(sys.argv[6])
if len(sys.argv) > 7:
  Ca_input_flux  = float(sys.argv[7])
if len(sys.argv) > 8:
  L_input_onset  = float(sys.argv[8])
if len(sys.argv) > 9:
  L_input_flux   = float(sys.argv[9])
if len(sys.argv) > 10:
  Glu_input_flux = float(sys.argv[10])
if len(sys.argv) > 11:
  ACh_input_flux = float(sys.argv[11])
if len(sys.argv) > 12:
  Ntrains  = int(float(sys.argv[12]))
if len(sys.argv) > 13:
  trainT  = float(sys.argv[13])
if len(sys.argv) > 14:
  initfile = sys.argv[14]
if len(sys.argv) > 15:
  filename = sys.argv[15]
if len(sys.argv) > 16:
  blocked = sys.argv[16]
  blockeds = blocked.split('~')
  print('blocked species:')
  print(blockeds)
if len(sys.argv) > 17:
  block_factor = sys.argv[17]    
  block_factors = [float(x) for x in block_factor.split('~')]
  print('block factors:')
  print(block_factors)
if type(blocked) is not list:
  addition = '_'+blocked+'x'+str(block_factor)
if len(sys.argv) > 18:
  alteredk = sys.argv[18]
  alteredks = [int(x) for x in alteredk.split('-')]
  print('alteredks:')
  print(alteredks)
if len(sys.argv) > 19:
  alteredk_factor = sys.argv[19]
  alteredk_factors = [float(x) for x in alteredk_factor.split('-')]
  print('alteredk_factors:')
  print(alteredk_factors)
if type(alteredk) is not list:
  addition = addition+'_k'+alteredk+'x'+str(alteredk_factor)
if len(sys.argv) > 20:
  toltochange = 'Gs,Calbin,CalbinC,PMCA,PMCACa,PP2B,Gi,GiaGDP,Gibg,Gsbg,GsaGDP,CaOut,CaOutLeak,Leak,PDE1,Ng,NgCaM,CaM,CaMCa2,CaMCa4,fixedbuffer,fixedbufferCa,DGL,CaDGL,'+sys.argv[20]
  tolstochange = toltochange.split(',')
if len(sys.argv) > 21:
  tolchange = '3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,2,2,1,1,'+sys.argv[21]
  tolschange = [float(x) for x in tolchange.split(',')]
  
initvalues = [0.0, 1.9, 0.0, 0.002, 0.15, 0.015, 2.5, 0.0005, 0.0, 0.022, 0.54, 0.0, 0.0, 1e-05, 0.0016, 0.013, 0.0026, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00043, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.00037, 0.0, 0.0, 0.012, 0.0, 0.0, 0.00098, 0.02, 0.0, 0.06, 0.0, 0.0, 0.0, 0.0023, 0.0, 0.0, 0.0, 0.0, 0.023, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0064, 0.0, 0.0, 0.0, 0.0022, 0.0, 0.0, 0.0016, 0.0, 0.0, 0.0, 0.0, 0.00018, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00067, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0008, 0.0, 0.0, 0.0, 1.0, 0.0014, 0.0, 0.0, 0.00025, 0.0, 0.0, 0.0, 0.024, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00029, 0.0004, 0.015, 0.0, 0.0, 0.0, 9e-05, 0.0003, 0.0, 0.0, 0.0016, 0.00025, 9e-05, 0.0, 0.0, 0.0006, 1.4e-05, 0.0, 0.0, 0.0, 0.0, 0.000256, 0.0, 0.0, 0.0, 0.0, 0.0005, 0.0, 0.00045, 0.0, 0.0, 0.0, 0.001, 0.0, 0.0, 0.0]
species = ['Ca', 'CaOut', 'CaOutLeak', 'Leak', 'Calbin', 'CalbinC', 'LOut', 'Epac1', 'Epac1cAMP', 'PMCA', 'NCX', 'PMCACa', 'NCXCa', 'L', 'R', 'Gs', 'Gi', 'LR', 'LRGs', 'PKAcLR', 'PKAcpLR', 'PKAcppLR', 'PKAcpppLR', 'pLR', 'ppLR', 'pppLR', 'ppppLR', 'ppppLRGi', 'ppppLRGibg', 'PKAcR', 'PKAcpR', 'PKAcppR', 'PKAcpppR', 'pR', 'ppR', 'pppR', 'ppppR', 'ppppRGi', 'ppppRGibg', 'GsR', 'GsaGTP', 'GsaGDP', 'GiaGTP', 'GiaGDP', 'Gibg', 'Gsbg', 'LRGsbg', 'AC1', 'AC1GsaGTP', 'AC1GsaGTPCaMCa4', 'AC1GsaGTPCaMCa4ATP', 'AC1GiaGTP', 'AC1GiaGTPCaMCa4', 'AC1GiaGTPCaMCa4ATP', 'AC1GsaGTPGiaGTP', 'AC1GsaGTPGiaGTPCaMCa4', 'AC1GsGiCaMCa4ATP', 'ATP', 'cAMP', 'AC1CaMCa4', 'AC1CaMCa4ATP', 'AC8', 'AC8CaMCa4', 'AC8CaMCa4ATP', 'PDE1', 'PDE1CaMCa4', 'PDE1CaMCa4cAMP', 'AMP', 'Ng', 'NgCaM', 'CaM', 'CaMCa2', 'CaMCa3', 'CaMCa4', 'PP2B', 'PP2BCaM', 'PP2BCaMCa2', 'PP2BCaMCa3', 'PP2BCaMCa4', 'CK', 'CKCaMCa4', 'CKpCaMCa4', 'CKp', 'Complex', 'pComplex', 'CKpPP1', 'CKpCaMCa4PP1', 'PKA', 'PKAcAMP4', 'PKAr', 'PKAc', 'I1', 'I1PKAc', 'Ip35', 'PP1', 'Ip35PP1', 'Ip35PP2BCaMCa4', 'Ip35PP1PP2BCaMCa4', 'PP1PP2BCaMCa4', 'GluR1', 'GluR1_S845', 'GluR1_S831', 'GluR1_S845_S831', 'GluR1_PKAc', 'GluR1_CKCam', 'GluR1_CKpCam', 'GluR1_CKp', 'GluR1_PKCt', 'GluR1_PKCp', 'GluR1_S845_CKCam', 'GluR1_S845_CKpCam', 'GluR1_S845_CKp', 'GluR1_S845_PKCt', 'GluR1_S845_PKCp', 'GluR1_S831_PKAc', 'GluR1_S845_PP1', 'GluR1_S845_S831_PP1', 'GluR1_S831_PP1', 'GluR1_S845_PP2B', 'GluR1_S845_S831_PP2B', 'GluR1_memb', 'GluR1_memb_S845', 'GluR1_memb_S831', 'GluR1_memb_S845_S831', 'GluR1_memb_PKAc', 'GluR1_memb_CKCam', 'GluR1_memb_CKpCam', 'GluR1_memb_CKp', 'GluR1_memb_PKCt', 'GluR1_memb_PKCp', 'GluR1_memb_S845_CKCam', 'GluR1_memb_S845_CKpCam', 'GluR1_memb_S845_CKp', 'GluR1_memb_S845_PKCt', 'GluR1_memb_S845_PKCp', 'GluR1_memb_S831_PKAc', 'GluR1_memb_S845_PP1', 'GluR1_memb_S845_S831_PP1', 'GluR1_memb_S831_PP1', 'GluR1_memb_S845_PP2B', 'GluR1_memb_S845_S831_PP2B', 'PDE4', 'PDE4cAMP', 'PKAcPDE4', 'pPDE4', 'pPDE4cAMP', 'PKAc_PDE4_cAMP', 'fixedbuffer', 'fixedbufferCa', 'Glu', 'MGluR', 'MGluR_Glu', 'MGluR_Glu_desens', 'MGluR_Gqabg_Glu', 'GluOut', 'Gqabg', 'GqaGTP', 'GqaGDP', 'PLC', 'PLCCa', 'PLCCaGqaGTP', 'PLCGqaGTP', 'Pip2', 'PLCCaPip2', 'PLCCaGqaGTPPip2', 'Ip3', 'PLCCaDAG', 'PLCCaGqaGTPDAG', 'PIkinase', 'Ip3degPIk', 'PKC', 'PKCCa', 'PKCt', 'PKCp', 'DAG', 'DAGK', 'DAGKdag', 'PA', 'DGL', 'CaDGL', 'DAGCaDGL', '2AG', '2AGdegrad', 'Ip3degrad', 'GluR2', 'GluR2_PKCt', 'GluR2_PKCp', 'GluR2_S880', 'GluR2_S880_PP2A', 'GluR2_memb', 'GluR2_memb_PKCt', 'GluR2_memb_PKCp', 'GluR2_memb_S880', 'GluR2_memb_S880_PP2A', 'PP2A', 'ACh', 'M1R', 'AChM1R', 'M1RGq', 'AChM1RGq', 'PLA2', 'CaPLA2', 'CaPLA2Pip2', 'AA']

if len(initfile) > 3 and initfile != 'None':
  DATA_init = scipy.io.loadmat(initfile)
  for mykey in list(DATA_init.keys()):
    if mykey[0:2] != '__':
      DATA_init[mykey] = DATA_init[mykey][0]
  for ispec in range(0,len(species)):
    initvalues[ispec] = DATA_init[species][-1]
tolscales = [1.0 for i in range(0,len(species))]
for ispec in range(0,len(species)):
  for iblock in range(0,len(blockeds)):
    if re.match(blockeds[iblock]+'$',species[ispec]):
      initvalues[ispec] = block_factors[iblock]*initvalues[ispec]
  for itol in range(0,len(tolstochange)):
    if tolstochange[itol] == species[ispec]:
      tolscales[ispec] = tolscales[ispec]*10**(-tolschange[itol])

specs = []
for ispec in range(0,len(species)):
  specs.append(rxd.Species(cyt, name='spec'+str(ispec), charge=0, initial=initvalues[ispec], atolscale=tolscales[ispec]))
specs.append(rxd.Species(cyt, name='null', charge=0, initial=0.0))

Ca_flux_rate = rxd.Parameter(cyt, initial=0)
L_flux_rate = rxd.Parameter(cyt, initial=0)
Glu_flux_rate = rxd.Parameter(cyt, initial=0)
ACh_flux_rate = rxd.Parameter(cyt, initial=0)

ks = [1.0]*413
ks[0]   = 50.0         # Ca + PMCA <-> PMCACa (forward)
ks[1]   = 0.007        # Ca + PMCA <-> PMCACa (backward)
ks[2]   = 0.0035       # PMCACa --> PMCA + CaOut (forward)
ks[3]   = 16.8         # Ca + NCX <-> NCXCa (forward)
ks[4]   = 0.0112       # Ca + NCX <-> NCXCa (backward)
ks[5]   = 0.0056       # NCXCa --> NCX + CaOut (forward)
ks[6]   = 1.5          # CaOut + Leak <-> CaOutLeak (forward)
ks[7]   = 0.0011       # CaOut + Leak <-> CaOutLeak (backward)
ks[8]   = 0.0011       # CaOutLeak --> Ca + Leak (forward)
ks[9]   = 28.0         # Ca + Calbin <-> CalbinC (forward)
ks[10]  = 0.0196       # Ca + Calbin <-> CalbinC (backward)
ks[11]  = 0.0005       # L <-> LOut (forward)
ks[12]  = 2e-09        # L <-> LOut (backward)
ks[13]  = 5.555        # L + R <-> LR (forward)
ks[14]  = 0.005        # L + R <-> LR (backward)
ks[15]  = 0.6          # LR + Gs <-> LRGs (forward)
ks[16]  = 1e-06        # LR + Gs <-> LRGs (backward)
ks[17]  = 0.04         # Gs + R <-> GsR (forward)
ks[18]  = 3e-07        # Gs + R <-> GsR (backward)
ks[19]  = 2.5          # GsR + L <-> LRGs (forward)
ks[20]  = 0.0005       # GsR + L <-> LRGs (backward)
ks[21]  = 0.02         # LRGs --> LRGsbg + GsaGTP (forward)
ks[22]  = 0.08         # LRGsbg --> LR + Gsbg (forward)
ks[23]  = 0.8          # LR + PKAc <-> PKAcLR (forward)
ks[24]  = 0.00448      # LR + PKAc <-> PKAcLR (backward)
ks[25]  = 0.001        # PKAcLR --> pLR + PKAc (forward)
ks[26]  = 0.8          # pLR + PKAc <-> PKAcpLR (forward)
ks[27]  = 0.00448      # pLR + PKAc <-> PKAcpLR (backward)
ks[28]  = 0.001        # PKAcpLR --> ppLR + PKAc (forward)
ks[29]  = 17.12        # ppLR + PKAc <-> PKAcppLR (forward)
ks[30]  = 0.00448      # ppLR + PKAc <-> PKAcppLR (backward)
ks[31]  = 0.001        # PKAcppLR --> pppLR + PKAc (forward)
ks[32]  = 1712.0       # pppLR + PKAc <-> PKAcpppLR (forward)
ks[33]  = 0.00448      # pppLR + PKAc <-> PKAcpppLR (backward)
ks[34]  = 0.001        # PKAcpppLR --> ppppLR + PKAc (forward)
ks[35]  = 150.0        # ppppLR + Gi <-> ppppLRGi (forward)
ks[36]  = 0.00025      # ppppLR + Gi <-> ppppLRGi (backward)
ks[37]  = 0.000125     # ppppLRGi --> ppppLRGibg + GiaGTP (forward)
ks[38]  = 0.001        # ppppLRGibg --> ppppLR + Gibg (forward)
ks[39]  = 2.5e-06      # pLR --> LR (forward)
ks[40]  = 2.5e-06      # ppLR --> pLR (forward)
ks[41]  = 2.5e-06      # pppLR --> ppLR (forward)
ks[42]  = 2.5e-06      # ppppLR --> pppLR (forward)
ks[43]  = 0.04         # R + PKAc <-> PKAcR (forward)
ks[44]  = 0.00448      # R + PKAc <-> PKAcR (backward)
ks[45]  = 0.001        # PKAcR --> pR + PKAc (forward)
ks[46]  = 0.4          # pR + PKAc <-> PKAcpR (forward)
ks[47]  = 0.00448      # pR + PKAc <-> PKAcpR (backward)
ks[48]  = 0.001        # PKAcpR --> ppR + PKAc (forward)
ks[49]  = 4.0          # ppR + PKAc <-> PKAcppR (forward)
ks[50]  = 0.00448      # ppR + PKAc <-> PKAcppR (backward)
ks[51]  = 0.001        # PKAcppR --> pppR + PKAc (forward)
ks[52]  = 400.0        # pppR + PKAc <-> PKAcpppR (forward)
ks[53]  = 0.00448      # pppR + PKAc <-> PKAcpppR (backward)
ks[54]  = 0.001        # PKAcpppR --> ppppR + PKAc (forward)
ks[55]  = 75.0         # ppppR + Gi <-> ppppRGi (forward)
ks[56]  = 0.000125     # ppppR + Gi <-> ppppRGi (backward)
ks[57]  = 6.25e-05     # ppppRGi --> ppppRGibg + GiaGTP (forward)
ks[58]  = 0.001        # ppppRGibg --> ppppR + Gibg (forward)
ks[59]  = 2.5e-06      # pR --> R (forward)
ks[60]  = 2.5e-06      # ppR --> pR (forward)
ks[61]  = 2.5e-06      # pppR --> ppR (forward)
ks[62]  = 2.5e-06      # ppppR --> pppR (forward)
ks[63]  = 0.01         # GsaGTP --> GsaGDP (forward)
ks[64]  = 100000.0     # GsaGDP + Gsbg --> Gs (forward)
ks[65]  = 0.000125     # GiaGTP --> GiaGDP (forward)
ks[66]  = 1250.0       # GiaGDP + Gibg --> Gi (forward)
ks[67]  = 38.5         # GsaGTP + AC1 <-> AC1GsaGTP (forward)
ks[68]  = 0.01         # GsaGTP + AC1 <-> AC1GsaGTP (backward)
ks[69]  = 6.0          # AC1GsaGTP + CaMCa4 <-> AC1GsaGTPCaMCa4 (forward)
ks[70]  = 0.0009       # AC1GsaGTP + CaMCa4 <-> AC1GsaGTPCaMCa4 (backward)
ks[71]  = 10.0         # AC1GsaGTPCaMCa4 + ATP <-> AC1GsaGTPCaMCa4ATP (forward)
ks[72]  = 2.273        # AC1GsaGTPCaMCa4 + ATP <-> AC1GsaGTPCaMCa4ATP (backward)
ks[73]  = 0.02842      # AC1GsaGTPCaMCa4ATP --> cAMP + AC1GsaGTPCaMCa4 (forward)
ks[74]  = 62.5         # GiaGTP + AC1GsaGTP <-> AC1GsaGTPGiaGTP (forward)
ks[75]  = 0.01         # GiaGTP + AC1GsaGTP <-> AC1GsaGTPGiaGTP (backward)
ks[76]  = 6.0          # AC1GsaGTPGiaGTP + CaMCa4 <-> AC1GsaGTPGiaGTPCaMCa4 (forward)
ks[77]  = 0.0009       # AC1GsaGTPGiaGTP + CaMCa4 <-> AC1GsaGTPGiaGTPCaMCa4 (backward)
ks[78]  = 10.0         # AC1GsaGTPGiaGTPCaMCa4 + ATP <-> AC1GsGiCaMCa4ATP (forward)
ks[79]  = 2.273        # AC1GsaGTPGiaGTPCaMCa4 + ATP <-> AC1GsGiCaMCa4ATP (backward)
ks[80]  = 0.002842     # AC1GsGiCaMCa4ATP --> cAMP + AC1GsaGTPGiaGTPCaMCa4 (forward)
ks[81]  = 62.5         # GiaGTP + AC1CaMCa4 <-> AC1GiaGTPCaMCa4 (forward)
ks[82]  = 0.01         # GiaGTP + AC1CaMCa4 <-> AC1GiaGTPCaMCa4 (backward)
ks[83]  = 10.0         # AC1GiaGTPCaMCa4 + ATP <-> AC1GiaGTPCaMCa4ATP (forward)
ks[84]  = 2.273        # AC1GiaGTPCaMCa4 + ATP <-> AC1GiaGTPCaMCa4ATP (backward)
ks[85]  = 0.0005684    # AC1GiaGTPCaMCa4ATP --> cAMP + AC1GiaGTPCaMCa4 (forward)
ks[86]  = 6.0          # AC1 + CaMCa4 <-> AC1CaMCa4 (forward)
ks[87]  = 0.0009       # AC1 + CaMCa4 <-> AC1CaMCa4 (backward)
ks[88]  = 10.0         # AC1CaMCa4 + ATP <-> AC1CaMCa4ATP (forward)
ks[89]  = 2.273        # AC1CaMCa4 + ATP <-> AC1CaMCa4ATP (backward)
ks[90]  = 0.005684     # AC1CaMCa4ATP --> cAMP + AC1CaMCa4 (forward)
ks[91]  = 62.5         # AC1GiaGTP + GsaGTP <-> AC1GsaGTPGiaGTP (forward)
ks[92]  = 0.01         # AC1GiaGTP + GsaGTP <-> AC1GsaGTPGiaGTP (backward)
ks[93]  = 1.25         # AC8 + CaMCa4 <-> AC8CaMCa4 (forward)
ks[94]  = 0.001        # AC8 + CaMCa4 <-> AC8CaMCa4 (backward)
ks[95]  = 10.0         # AC8CaMCa4 + ATP <-> AC8CaMCa4ATP (forward)
ks[96]  = 2.273        # AC8CaMCa4 + ATP <-> AC8CaMCa4ATP (backward)
ks[97]  = 0.002842     # AC8CaMCa4ATP --> cAMP + AC8CaMCa4 (forward)
ks[98]  = 17000.0      # CaM + Ca*2 <-> CaMCa2 (forward)
ks[99]  = 0.035        # CaM + Ca*2 <-> CaMCa2 (backward)
ks[100] = 14.0         # CaMCa2 + Ca <-> CaMCa3 (forward)
ks[101] = 0.228        # CaMCa2 + Ca <-> CaMCa3 (backward)
ks[102] = 26.0         # CaMCa3 + Ca <-> CaMCa4 (forward)
ks[103] = 0.064        # CaMCa3 + Ca <-> CaMCa4 (backward)
ks[104] = 28.0         # CaM + Ng <-> NgCaM (forward)
ks[105] = 0.036        # CaM + Ng <-> NgCaM (backward)
ks[106] = 4.6          # CaM + PP2B <-> PP2BCaM (forward)
ks[107] = 1.2e-06      # CaM + PP2B <-> PP2BCaM (backward)
ks[108] = 46.0         # CaMCa2 + PP2B <-> PP2BCaMCa2 (forward)
ks[109] = 1.2e-06      # CaMCa2 + PP2B <-> PP2BCaMCa2 (backward)
ks[110] = 46.0         # CaMCa4 + PP2B <-> PP2BCaMCa4 (forward)
ks[111] = 1.2e-06      # CaMCa4 + PP2B <-> PP2BCaMCa4 (backward)
ks[112] = 170000.0     # PP2BCaM + Ca*2 <-> PP2BCaMCa2 (forward)
ks[113] = 0.35         # PP2BCaM + Ca*2 <-> PP2BCaMCa2 (backward)
ks[114] = 14.0         # PP2BCaMCa2 + Ca <-> PP2BCaMCa3 (forward)
ks[115] = 0.228        # PP2BCaMCa2 + Ca <-> PP2BCaMCa3 (backward)
ks[116] = 26.0         # PP2BCaMCa3 + Ca <-> PP2BCaMCa4 (forward)
ks[117] = 0.064        # PP2BCaMCa3 + Ca <-> PP2BCaMCa4 (backward)
ks[118] = 10.0         # CaMCa4 + CK <-> CKCaMCa4 (forward)
ks[119] = 0.003        # CaMCa4 + CK <-> CKCaMCa4 (backward)
ks[120] = 0.1          # CKCaMCa4*2 <-> Complex (forward)
ks[121] = 0.01         # CKCaMCa4*2 <-> Complex (backward)
ks[122] = 0.1          # CKpCaMCa4 + CKCaMCa4 <-> pComplex (forward)
ks[123] = 0.01         # CKpCaMCa4 + CKCaMCa4 <-> pComplex (backward)
ks[124] = 0.1          # CKpCaMCa4 + Complex --> CKpCaMCa4 + pComplex (forward)
ks[125] = 0.1          # CKCaMCa4 + Complex --> CKCaMCa4 + pComplex (forward)
ks[126] = 10.0         # Complex*2 --> Complex + pComplex (forward)
ks[127] = 30.0         # Complex + pComplex --> pComplex*2 (forward)
ks[128] = 8e-07        # CKpCaMCa4 <-> CaMCa4 + CKp (forward)
ks[129] = 10.0         # CKpCaMCa4 <-> CaMCa4 + CKp (backward)
ks[130] = 0.004        # CKp + PP1 <-> CKpPP1 (forward)
ks[131] = 0.00034      # CKp + PP1 <-> CKpPP1 (backward)
ks[132] = 8.6e-05      # CKpPP1 --> PP1 + CK (forward)
ks[133] = 0.004        # CKpCaMCa4 + PP1 <-> CKpCaMCa4PP1 (forward)
ks[134] = 0.00034      # CKpCaMCa4 + PP1 <-> CKpCaMCa4PP1 (backward)
ks[135] = 8.6e-05      # CKpCaMCa4PP1 --> PP1 + CKCaMCa4 (forward)
ks[136] = 1600000000.0 # PKA + cAMP*4 <-> PKAcAMP4 (forward)
ks[137] = 6e-05        # PKA + cAMP*4 <-> PKAcAMP4 (backward)
ks[138] = 0.031        # Epac1 + cAMP <-> Epac1cAMP (forward)
ks[139] = 6.51e-05     # Epac1 + cAMP <-> Epac1cAMP (backward)
ks[140] = 1.4          # I1 + PKAc <-> I1PKAc (forward)
ks[141] = 0.0056       # I1 + PKAc <-> I1PKAc (backward)
ks[142] = 0.0014       # I1PKAc --> Ip35 + PKAc (forward)
ks[143] = 1.0          # Ip35 + PP1 <-> Ip35PP1 (forward)
ks[144] = 1.1e-06      # Ip35 + PP1 <-> Ip35PP1 (backward)
ks[145] = 96.25        # Ip35 + PP2BCaMCa4 <-> Ip35PP2BCaMCa4 (forward)
ks[146] = 0.33         # Ip35 + PP2BCaMCa4 <-> Ip35PP2BCaMCa4 (backward)
ks[147] = 0.055        # Ip35PP2BCaMCa4 --> I1 + PP2BCaMCa4 (forward)
ks[148] = 96.25        # Ip35PP1 + PP2BCaMCa4 <-> Ip35PP1PP2BCaMCa4 (forward)
ks[149] = 0.33         # Ip35PP1 + PP2BCaMCa4 <-> Ip35PP1PP2BCaMCa4 (backward)
ks[150] = 0.055        # Ip35PP1PP2BCaMCa4 --> I1 + PP1PP2BCaMCa4 (forward)
ks[151] = 0.0015       # PP1PP2BCaMCa4 --> PP1 + PP2BCaMCa4 (forward)
ks[152] = 4.02         # GluR1 + PKAc <-> GluR1_PKAc (forward)
ks[153] = 0.024        # GluR1 + PKAc <-> GluR1_PKAc (backward)
ks[154] = 0.006        # GluR1_PKAc --> GluR1_S845 + PKAc (forward)
ks[155] = 0.02224      # GluR1 + CKCaMCa4 <-> GluR1_CKCam (forward)
ks[156] = 0.0016       # GluR1 + CKCaMCa4 <-> GluR1_CKCam (backward)
ks[157] = 0.0004       # GluR1_CKCam --> GluR1_S831 + CKCaMCa4 (forward)
ks[158] = 0.0278       # GluR1 + CKpCaMCa4 <-> GluR1_CKpCam (forward)
ks[159] = 0.002        # GluR1 + CKpCaMCa4 <-> GluR1_CKpCam (backward)
ks[160] = 0.0005       # GluR1_CKpCam --> GluR1_S831 + CKpCaMCa4 (forward)
ks[161] = 0.02224      # GluR1 + CKp <-> GluR1_CKp (forward)
ks[162] = 0.0016       # GluR1 + CKp <-> GluR1_CKp (backward)
ks[163] = 0.0004       # GluR1_CKp --> GluR1_S831 + CKp (forward)
ks[164] = 0.0278       # GluR1 + PKCt <-> GluR1_PKCt (forward)
ks[165] = 0.002        # GluR1 + PKCt <-> GluR1_PKCt (backward)
ks[166] = 0.0005       # GluR1_PKCt --> GluR1_S831 + PKCt (forward)
ks[167] = 0.0278       # GluR1 + PKCp <-> GluR1_PKCp (forward)
ks[168] = 0.002        # GluR1 + PKCp <-> GluR1_PKCp (backward)
ks[169] = 0.0005       # GluR1_PKCp --> GluR1_S831 + PKCp (forward)
ks[170] = 0.02224      # GluR1_S845 + CKCaMCa4 <-> GluR1_S845_CKCam (forward)
ks[171] = 0.0016       # GluR1_S845 + CKCaMCa4 <-> GluR1_S845_CKCam (backward)
ks[172] = 0.0004       # GluR1_S845_CKCam --> GluR1_S845_S831 + CKCaMCa4 (forward)
ks[173] = 0.0278       # GluR1_S845 + CKpCaMCa4 <-> GluR1_S845_CKpCam (forward)
ks[174] = 0.002        # GluR1_S845 + CKpCaMCa4 <-> GluR1_S845_CKpCam (backward)
ks[175] = 0.0005       # GluR1_S845_CKpCam --> GluR1_S845_S831 + CKpCaMCa4 (forward)
ks[176] = 0.02224      # GluR1_S845 + CKp <-> GluR1_S845_CKp (forward)
ks[177] = 0.0016       # GluR1_S845 + CKp <-> GluR1_S845_CKp (backward)
ks[178] = 0.0004       # GluR1_S845_CKp --> GluR1_S845_S831 + CKp (forward)
ks[179] = 0.0278       # GluR1_S845 + PKCt <-> GluR1_S845_PKCt (forward)
ks[180] = 0.002        # GluR1_S845 + PKCt <-> GluR1_S845_PKCt (backward)
ks[181] = 0.0005       # GluR1_S845_PKCt --> GluR1_S845_S831 + PKCt (forward)
ks[182] = 0.0278       # GluR1_S845 + PKCp <-> GluR1_S845_PKCp (forward)
ks[183] = 0.002        # GluR1_S845 + PKCp <-> GluR1_S845_PKCp (backward)
ks[184] = 0.0005       # GluR1_S845_PKCp --> GluR1_S845_S831 + PKCp (forward)
ks[185] = 4.0          # GluR1_S831 + PKAc <-> GluR1_S831_PKAc (forward)
ks[186] = 0.024        # GluR1_S831 + PKAc <-> GluR1_S831_PKAc (backward)
ks[187] = 0.006        # GluR1_S831_PKAc --> GluR1_S845_S831 + PKAc (forward)
ks[188] = 0.87         # GluR1_S845 + PP1 <-> GluR1_S845_PP1 (forward)
ks[189] = 0.00068      # GluR1_S845 + PP1 <-> GluR1_S845_PP1 (backward)
ks[190] = 0.00017      # GluR1_S845_PP1 --> GluR1 + PP1 (forward)
ks[191] = 0.875        # GluR1_S845_S831 + PP1 <-> GluR1_S845_S831_PP1 (forward)
ks[192] = 0.0014       # GluR1_S845_S831 + PP1 <-> GluR1_S845_S831_PP1 (backward)
ks[193] = 0.00035      # GluR1_S845_S831_PP1 --> GluR1_S845 + PP1 (forward)
ks[194] = 0.00035      # GluR1_S845_S831_PP1 --> GluR1_S831 + PP1 (forward)
ks[195] = 0.875        # GluR1_S831 + PP1 <-> GluR1_S831_PP1 (forward)
ks[196] = 0.0014       # GluR1_S831 + PP1 <-> GluR1_S831_PP1 (backward)
ks[197] = 0.00035      # GluR1_S831_PP1 --> GluR1 + PP1 (forward)
ks[198] = 2.01         # GluR1_S845 + PP2BCaMCa4 <-> GluR1_S845_PP2B (forward)
ks[199] = 0.008        # GluR1_S845 + PP2BCaMCa4 <-> GluR1_S845_PP2B (backward)
ks[200] = 0.002        # GluR1_S845_PP2B --> GluR1 + PP2BCaMCa4 (forward)
ks[201] = 2.01         # GluR1_S845_S831 + PP2BCaMCa4 <-> GluR1_S845_S831_PP2B (forward)
ks[202] = 0.008        # GluR1_S845_S831 + PP2BCaMCa4 <-> GluR1_S845_S831_PP2B (backward)
ks[203] = 0.002        # GluR1_S845_S831_PP2B --> GluR1_S831 + PP2BCaMCa4 (forward)
ks[204] = 4.02         # GluR1_memb + PKAc <-> GluR1_memb_PKAc (forward)
ks[205] = 0.024        # GluR1_memb + PKAc <-> GluR1_memb_PKAc (backward)
ks[206] = 0.006        # GluR1_memb_PKAc --> GluR1_memb_S845 + PKAc (forward)
ks[207] = 0.02224      # GluR1_memb + CKCaMCa4 <-> GluR1_memb_CKCam (forward)
ks[208] = 0.0016       # GluR1_memb + CKCaMCa4 <-> GluR1_memb_CKCam (backward)
ks[209] = 0.0004       # GluR1_memb_CKCam --> GluR1_memb_S831 + CKCaMCa4 (forward)
ks[210] = 0.0278       # GluR1_memb + CKpCaMCa4 <-> GluR1_memb_CKpCam (forward)
ks[211] = 0.002        # GluR1_memb + CKpCaMCa4 <-> GluR1_memb_CKpCam (backward)
ks[212] = 0.0005       # GluR1_memb_CKpCam --> GluR1_memb_S831 + CKpCaMCa4 (forward)
ks[213] = 0.02224      # GluR1_memb + CKp <-> GluR1_memb_CKp (forward)
ks[214] = 0.0016       # GluR1_memb + CKp <-> GluR1_memb_CKp (backward)
ks[215] = 0.0004       # GluR1_memb_CKp --> GluR1_memb_S831 + CKp (forward)
ks[216] = 0.0278       # GluR1_memb + PKCt <-> GluR1_memb_PKCt (forward)
ks[217] = 0.002        # GluR1_memb + PKCt <-> GluR1_memb_PKCt (backward)
ks[218] = 0.0005       # GluR1_memb_PKCt --> GluR1_memb_S831 + PKCt (forward)
ks[219] = 0.0278       # GluR1_memb + PKCp <-> GluR1_memb_PKCp (forward)
ks[220] = 0.002        # GluR1_memb + PKCp <-> GluR1_memb_PKCp (backward)
ks[221] = 0.0005       # GluR1_memb_PKCp --> GluR1_memb_S831 + PKCp (forward)
ks[222] = 0.02224      # GluR1_memb_S845 + CKCaMCa4 <-> GluR1_memb_S845_CKCam (forward)
ks[223] = 0.0016       # GluR1_memb_S845 + CKCaMCa4 <-> GluR1_memb_S845_CKCam (backward)
ks[224] = 0.0004       # GluR1_memb_S845_CKCam --> GluR1_memb_S845_S831 + CKCaMCa4 (forward)
ks[225] = 0.0278       # GluR1_memb_S845 + CKpCaMCa4 <-> GluR1_memb_S845_CKpCam (forward)
ks[226] = 0.002        # GluR1_memb_S845 + CKpCaMCa4 <-> GluR1_memb_S845_CKpCam (backward)
ks[227] = 0.0005       # GluR1_memb_S845_CKpCam --> GluR1_memb_S845_S831 + CKpCaMCa4 (forward)
ks[228] = 0.02224      # GluR1_memb_S845 + CKp <-> GluR1_memb_S845_CKp (forward)
ks[229] = 0.0016       # GluR1_memb_S845 + CKp <-> GluR1_memb_S845_CKp (backward)
ks[230] = 0.0004       # GluR1_memb_S845_CKp --> GluR1_memb_S845_S831 + CKp (forward)
ks[231] = 0.0278       # GluR1_memb_S845 + PKCt <-> GluR1_memb_S845_PKCt (forward)
ks[232] = 0.002        # GluR1_memb_S845 + PKCt <-> GluR1_memb_S845_PKCt (backward)
ks[233] = 0.0005       # GluR1_memb_S845_PKCt --> GluR1_memb_S845_S831 + PKCt (forward)
ks[234] = 0.0278       # GluR1_memb_S845 + PKCp <-> GluR1_memb_S845_PKCp (forward)
ks[235] = 0.002        # GluR1_memb_S845 + PKCp <-> GluR1_memb_S845_PKCp (backward)
ks[236] = 0.0005       # GluR1_memb_S845_PKCp --> GluR1_memb_S845_S831 + PKCp (forward)
ks[237] = 4.0          # GluR1_memb_S831 + PKAc <-> GluR1_memb_S831_PKAc (forward)
ks[238] = 0.024        # GluR1_memb_S831 + PKAc <-> GluR1_memb_S831_PKAc (backward)
ks[239] = 0.006        # GluR1_memb_S831_PKAc --> GluR1_memb_S845_S831 + PKAc (forward)
ks[240] = 0.87         # GluR1_memb_S845 + PP1 <-> GluR1_memb_S845_PP1 (forward)
ks[241] = 0.00068      # GluR1_memb_S845 + PP1 <-> GluR1_memb_S845_PP1 (backward)
ks[242] = 0.00017      # GluR1_memb_S845_PP1 --> GluR1_memb + PP1 (forward)
ks[243] = 0.875        # GluR1_memb_S845_S831 + PP1 <-> GluR1_memb_S845_S831_PP1 (forward)
ks[244] = 0.0014       # GluR1_memb_S845_S831 + PP1 <-> GluR1_memb_S845_S831_PP1 (backward)
ks[245] = 0.00035      # GluR1_memb_S845_S831_PP1 --> GluR1_memb_S845 + PP1 (forward)
ks[246] = 0.00035      # GluR1_memb_S845_S831_PP1 --> GluR1_memb_S831 + PP1 (forward)
ks[247] = 0.875        # GluR1_memb_S831 + PP1 <-> GluR1_memb_S831_PP1 (forward)
ks[248] = 0.0014       # GluR1_memb_S831 + PP1 <-> GluR1_memb_S831_PP1 (backward)
ks[249] = 0.00035      # GluR1_memb_S831_PP1 --> GluR1_memb + PP1 (forward)
ks[250] = 2.01         # GluR1_memb_S845 + PP2BCaMCa4 <-> GluR1_memb_S845_PP2B (forward)
ks[251] = 0.008        # GluR1_memb_S845 + PP2BCaMCa4 <-> GluR1_memb_S845_PP2B (backward)
ks[252] = 0.002        # GluR1_memb_S845_PP2B --> GluR1_memb + PP2BCaMCa4 (forward)
ks[253] = 2.01         # GluR1_memb_S845_S831 + PP2BCaMCa4 <-> GluR1_memb_S845_S831_PP2B (forward)
ks[254] = 0.008        # GluR1_memb_S845_S831 + PP2BCaMCa4 <-> GluR1_memb_S845_S831_PP2B (backward)
ks[255] = 0.002        # GluR1_memb_S845_S831_PP2B --> GluR1_memb_S831 + PP2BCaMCa4 (forward)
ks[256] = 2e-07        # GluR1 <-> GluR1_memb (forward)
ks[257] = 8e-07        # GluR1 <-> GluR1_memb (backward)
ks[258] = 2e-07        # GluR1_PKAc <-> GluR1_memb_PKAc (forward)
ks[259] = 8e-07        # GluR1_PKAc <-> GluR1_memb_PKAc (backward)
ks[260] = 2e-07        # GluR1_CKCam <-> GluR1_memb_CKCam (forward)
ks[261] = 8e-07        # GluR1_CKCam <-> GluR1_memb_CKCam (backward)
ks[262] = 2e-07        # GluR1_CKpCam <-> GluR1_memb_CKpCam (forward)
ks[263] = 8e-07        # GluR1_CKpCam <-> GluR1_memb_CKpCam (backward)
ks[264] = 2e-07        # GluR1_CKp <-> GluR1_memb_CKp (forward)
ks[265] = 8e-07        # GluR1_CKp <-> GluR1_memb_CKp (backward)
ks[266] = 2e-07        # GluR1_PKCt <-> GluR1_memb_PKCt (forward)
ks[267] = 8e-07        # GluR1_PKCt <-> GluR1_memb_PKCt (backward)
ks[268] = 2e-07        # GluR1_PKCp <-> GluR1_memb_PKCp (forward)
ks[269] = 8e-07        # GluR1_PKCp <-> GluR1_memb_PKCp (backward)
ks[270] = 2e-07        # GluR1_S831 <-> GluR1_memb_S831 (forward)
ks[271] = 8e-07        # GluR1_S831 <-> GluR1_memb_S831 (backward)
ks[272] = 2e-07        # GluR1_S831_PKAc <-> GluR1_memb_S831_PKAc (forward)
ks[273] = 8e-07        # GluR1_S831_PKAc <-> GluR1_memb_S831_PKAc (backward)
ks[274] = 2e-07        # GluR1_S831_PP1 <-> GluR1_memb_S831_PP1 (forward)
ks[275] = 8e-07        # GluR1_S831_PP1 <-> GluR1_memb_S831_PP1 (backward)
ks[276] = 3.28e-05     # GluR1_S845 <-> GluR1_memb_S845 (forward)
ks[277] = 8e-06        # GluR1_S845 <-> GluR1_memb_S845 (backward)
ks[278] = 3.28e-05     # GluR1_S845_CKCam <-> GluR1_memb_S845_CKCam (forward)
ks[279] = 8e-06        # GluR1_S845_CKCam <-> GluR1_memb_S845_CKCam (backward)
ks[280] = 3.28e-05     # GluR1_S845_CKpCam <-> GluR1_memb_S845_CKpCam (forward)
ks[281] = 8e-06        # GluR1_S845_CKpCam <-> GluR1_memb_S845_CKpCam (backward)
ks[282] = 3.28e-05     # GluR1_S845_CKp <-> GluR1_memb_S845_CKp (forward)
ks[283] = 8e-06        # GluR1_S845_CKp <-> GluR1_memb_S845_CKp (backward)
ks[284] = 3.28e-05     # GluR1_S845_PKCt <-> GluR1_memb_S845_PKCt (forward)
ks[285] = 8e-06        # GluR1_S845_PKCt <-> GluR1_memb_S845_PKCt (backward)
ks[286] = 3.28e-05     # GluR1_S845_PKCp <-> GluR1_memb_S845_PKCp (forward)
ks[287] = 8e-06        # GluR1_S845_PKCp <-> GluR1_memb_S845_PKCp (backward)
ks[288] = 3.28e-05     # GluR1_S845_S831 <-> GluR1_memb_S845_S831 (forward)
ks[289] = 8e-06        # GluR1_S845_S831 <-> GluR1_memb_S845_S831 (backward)
ks[290] = 3.28e-05     # GluR1_S845_PP1 <-> GluR1_memb_S845_PP1 (forward)
ks[291] = 8e-06        # GluR1_S845_PP1 <-> GluR1_memb_S845_PP1 (backward)
ks[292] = 3.28e-05     # GluR1_S845_S831_PP1 <-> GluR1_memb_S845_S831_PP1 (forward)
ks[293] = 8e-06        # GluR1_S845_S831_PP1 <-> GluR1_memb_S845_S831_PP1 (backward)
ks[294] = 3.28e-05     # GluR1_S845_PP2B <-> GluR1_memb_S845_PP2B (forward)
ks[295] = 8e-06        # GluR1_S845_PP2B <-> GluR1_memb_S845_PP2B (backward)
ks[296] = 3.28e-05     # GluR1_S845_S831_PP2B <-> GluR1_memb_S845_S831_PP2B (forward)
ks[297] = 8e-06        # GluR1_S845_S831_PP2B <-> GluR1_memb_S845_S831_PP2B (backward)
ks[298] = 100.0        # PDE1 + CaMCa4 <-> PDE1CaMCa4 (forward)
ks[299] = 0.001        # PDE1 + CaMCa4 <-> PDE1CaMCa4 (backward)
ks[300] = 4.6          # PDE1CaMCa4 + cAMP <-> PDE1CaMCa4cAMP (forward)
ks[301] = 0.044        # PDE1CaMCa4 + cAMP <-> PDE1CaMCa4cAMP (backward)
ks[302] = 0.011        # PDE1CaMCa4cAMP --> PDE1CaMCa4 + AMP (forward)
ks[303] = 0.001        # AMP --> ATP (forward)
ks[304] = 21.66        # PDE4 + cAMP <-> PDE4cAMP (forward)
ks[305] = 0.0034656    # PDE4 + cAMP <-> PDE4cAMP (backward)
ks[306] = 0.017233     # PDE4cAMP --> PDE4 + AMP (forward)
ks[307] = 0.25         # PKAc + PDE4 <-> PKAcPDE4 (forward)
ks[308] = 8e-05        # PKAc + PDE4 <-> PKAcPDE4 (backward)
ks[309] = 2e-05        # PKAcPDE4 --> pPDE4 + PKAc (forward)
ks[310] = 2.5e-06      # pPDE4 --> PDE4 (forward)
ks[311] = 433.175      # pPDE4 + cAMP <-> pPDE4cAMP (forward)
ks[312] = 0.069308     # pPDE4 + cAMP <-> pPDE4cAMP (backward)
ks[313] = 0.3446674    # pPDE4cAMP --> pPDE4 + AMP (forward)
ks[314] = 0.25         # PDE4cAMP + PKAc <-> PKAc_PDE4_cAMP (forward)
ks[315] = 8e-05        # PDE4cAMP + PKAc <-> PKAc_PDE4_cAMP (backward)
ks[316] = 2e-05        # PKAc_PDE4_cAMP --> pPDE4cAMP + PKAc (forward)
ks[317] = 0.00024      # PKAcAMP4 <-> PKAr + PKAc*2 (forward)
ks[318] = 25.5         # PKAcAMP4 <-> PKAr + PKAc*2 (backward)
ks[319] = 400.0        # Ca + fixedbuffer <-> fixedbufferCa (forward)
ks[320] = 20.0         # Ca + fixedbuffer <-> fixedbufferCa (backward)
ks[321] = 0.0005       # Glu <-> GluOut (forward)
ks[322] = 2e-10        # Glu <-> GluOut (backward)
ks[323] = 0.4          # Ca + PLC <-> PLCCa (forward)
ks[324] = 0.001        # Ca + PLC <-> PLCCa (backward)
ks[325] = 0.7          # GqaGTP + PLC <-> PLCGqaGTP (forward)
ks[326] = 0.0007       # GqaGTP + PLC <-> PLCGqaGTP (backward)
ks[327] = 80.0         # Ca + PLCGqaGTP <-> PLCCaGqaGTP (forward)
ks[328] = 0.04         # Ca + PLCGqaGTP <-> PLCCaGqaGTP (backward)
ks[329] = 100.0        # GqaGTP + PLCCa <-> PLCCaGqaGTP (forward)
ks[330] = 0.01         # GqaGTP + PLCCa <-> PLCCaGqaGTP (backward)
ks[331] = 0.03         # PLCCa + Pip2 <-> PLCCaPip2 (forward)
ks[332] = 0.01         # PLCCa + Pip2 <-> PLCCaPip2 (backward)
ks[333] = 0.0003       # PLCCaPip2 --> PLCCaDAG + Ip3 (forward)
ks[334] = 0.2          # PLCCaDAG --> PLCCa + DAG (forward)
ks[335] = 15.0         # PLCCaGqaGTP + Pip2 <-> PLCCaGqaGTPPip2 (forward)
ks[336] = 0.075        # PLCCaGqaGTP + Pip2 <-> PLCCaGqaGTPPip2 (backward)
ks[337] = 0.25         # PLCCaGqaGTPPip2 --> PLCCaGqaGTPDAG + Ip3 (forward)
ks[338] = 1.0          # PLCCaGqaGTPDAG --> PLCCaGqaGTP + DAG (forward)
ks[339] = 2.0          # Ip3degrad + PIkinase <-> Ip3degPIk (forward)
ks[340] = 0.001        # Ip3degrad + PIkinase <-> Ip3degPIk (backward)
ks[341] = 0.001        # Ip3degPIk --> PIkinase + Pip2 (forward)
ks[342] = 0.012        # PLCGqaGTP --> PLC + GqaGDP (forward)
ks[343] = 0.012        # PLCCaGqaGTP --> PLCCa + GqaGDP (forward)
ks[344] = 0.001        # GqaGTP --> GqaGDP (forward)
ks[345] = 0.01         # GqaGDP --> Gqabg (forward)
ks[346] = 125.0        # Ca + DGL <-> CaDGL (forward)
ks[347] = 0.05         # Ca + DGL <-> CaDGL (backward)
ks[348] = 0.5          # DAG + CaDGL <-> DAGCaDGL (forward)
ks[349] = 0.001        # DAG + CaDGL <-> DAGCaDGL (backward)
ks[350] = 0.00025      # DAGCaDGL --> CaDGL + _2AG (forward)
ks[351] = 0.01         # Ip3 --> Ip3degrad (forward)
ks[352] = 0.005        # _2AG --> _2AGdegrad (forward)
ks[353] = 0.07         # DAG + DAGK <-> DAGKdag (forward)
ks[354] = 0.0008       # DAG + DAGK <-> DAGKdag (backward)
ks[355] = 0.0002       # DAGKdag --> DAGK + PA (forward)
ks[356] = 13.3         # Ca + PKC <-> PKCCa (forward)
ks[357] = 0.05         # Ca + PKC <-> PKCCa (backward)
ks[358] = 0.015        # PKCCa + DAG <-> PKCt (forward)
ks[359] = 0.00015      # PKCCa + DAG <-> PKCt (backward)
ks[360] = 0.0168       # Glu + MGluR <-> MGluR_Glu (forward)
ks[361] = 0.0001       # Glu + MGluR <-> MGluR_Glu (backward)
ks[362] = 6.25e-05     # MGluR_Glu <-> MGluR_Glu_desens (forward)
ks[363] = 1e-06        # MGluR_Glu <-> MGluR_Glu_desens (backward)
ks[364] = 9.0          # Gqabg + MGluR_Glu <-> MGluR_Gqabg_Glu (forward)
ks[365] = 0.00136      # Gqabg + MGluR_Glu <-> MGluR_Gqabg_Glu (backward)
ks[366] = 0.0015       # MGluR_Gqabg_Glu --> GqaGTP + MGluR_Glu (forward)
ks[367] = 0.4          # GluR2 + PKCt <-> GluR2_PKCt (forward)
ks[368] = 0.0008       # GluR2 + PKCt <-> GluR2_PKCt (backward)
ks[369] = 0.0047       # GluR2_PKCt --> GluR2_S880 + PKCt (forward)
ks[370] = 0.4          # GluR2 + PKCp <-> GluR2_PKCp (forward)
ks[371] = 0.0008       # GluR2 + PKCp <-> GluR2_PKCp (backward)
ks[372] = 0.0047       # GluR2_PKCp --> GluR2_S880 + PKCp (forward)
ks[373] = 0.5          # GluR2_S880 + PP2A <-> GluR2_S880_PP2A (forward)
ks[374] = 0.005        # GluR2_S880 + PP2A <-> GluR2_S880_PP2A (backward)
ks[375] = 0.00015      # GluR2_S880_PP2A --> GluR2 + PP2A (forward)
ks[376] = 0.4          # GluR2_memb + PKCt <-> GluR2_memb_PKCt (forward)
ks[377] = 0.0008       # GluR2_memb + PKCt <-> GluR2_memb_PKCt (backward)
ks[378] = 0.0047       # GluR2_memb_PKCt --> GluR2_memb_S880 + PKCt (forward)
ks[379] = 0.4          # GluR2_memb + PKCp <-> GluR2_memb_PKCp (forward)
ks[380] = 0.0008       # GluR2_memb + PKCp <-> GluR2_memb_PKCp (backward)
ks[381] = 0.0047       # GluR2_memb_PKCp --> GluR2_memb_S880 + PKCp (forward)
ks[382] = 0.5          # GluR2_memb_S880 + PP2A <-> GluR2_memb_S880_PP2A (forward)
ks[383] = 0.005        # GluR2_memb_S880 + PP2A <-> GluR2_memb_S880_PP2A (backward)
ks[384] = 0.00015      # GluR2_memb_S880_PP2A --> GluR2_memb + PP2A (forward)
ks[385] = 0.00024545   # GluR2 <-> GluR2_memb (forward)
ks[386] = 0.0003       # GluR2 <-> GluR2_memb (backward)
ks[387] = 0.00024545   # GluR2_PKCt <-> GluR2_memb_PKCt (forward)
ks[388] = 0.0003       # GluR2_PKCt <-> GluR2_memb_PKCt (backward)
ks[389] = 0.00024545   # GluR2_PKCp <-> GluR2_memb_PKCp (forward)
ks[390] = 0.0003       # GluR2_PKCp <-> GluR2_memb_PKCp (backward)
ks[391] = 0.0055       # GluR2_S880 <-> GluR2_memb_S880 (forward)
ks[392] = 0.07         # GluR2_S880 <-> GluR2_memb_S880 (backward)
ks[393] = 0.0055       # GluR2_S880_PP2A <-> GluR2_memb_S880_PP2A (forward)
ks[394] = 0.07         # GluR2_S880_PP2A <-> GluR2_memb_S880_PP2A (backward)
ks[395] = 0.095        # ACh + M1R <-> AChM1R (forward)
ks[396] = 0.0025       # ACh + M1R <-> AChM1R (backward)
ks[397] = 24.0         # Gqabg + AChM1R <-> AChM1RGq (forward)
ks[398] = 0.00042      # Gqabg + AChM1R <-> AChM1RGq (backward)
ks[399] = 0.576        # Gqabg + M1R <-> M1RGq (forward)
ks[400] = 0.00042      # Gqabg + M1R <-> M1RGq (backward)
ks[401] = 3.96         # ACh + M1RGq <-> AChM1RGq (forward)
ks[402] = 0.0025       # ACh + M1RGq <-> AChM1RGq (backward)
ks[403] = 0.0005       # AChM1RGq --> GqaGTP + AChM1R (forward)
ks[404] = 0.006        # ACh --> ACh*0 (forward)
ks[405] = 0.6          # Ca + PLA2 <-> CaPLA2 (forward)
ks[406] = 0.003        # Ca + PLA2 <-> CaPLA2 (backward)
ks[407] = 22.0         # CaPLA2 + Pip2 <-> CaPLA2Pip2 (forward)
ks[408] = 0.444        # CaPLA2 + Pip2 <-> CaPLA2Pip2 (backward)
ks[409] = 0.111        # CaPLA2Pip2 --> CaPLA2 + AA (forward)
ks[410] = 0.001        # AA --> Pip2 (forward)
ks[411] = 0.005        # PKCt + AA <-> PKCp (forward)
ks[412] = 1.76e-07     # PKCt + AA <-> PKCp (backward)

for ialteredk in range(0,len(alteredks)):
  ks[alteredks[ialteredk]] = alteredk_factors[ialteredk]*ks[alteredks[ialteredk]]
reaction000 = rxd.Reaction(specs[0] + specs[9] != specs[11], ks[0], ks[1])
reaction001 = rxd.Reaction(specs[11] > specs[9] + specs[1], ks[2])
reaction002 = rxd.Reaction(specs[0] + specs[10] != specs[12], ks[3], ks[4])
reaction003 = rxd.Reaction(specs[12] > specs[10] + specs[1], ks[5])
reaction004 = rxd.Reaction(specs[1] + specs[3] != specs[2], ks[6], ks[7])
reaction005 = rxd.Reaction(specs[2] > specs[0] + specs[3], ks[8])
reaction006 = rxd.Reaction(specs[0] + specs[4] != specs[5], ks[9], ks[10])
reaction007 = rxd.Reaction(specs[13] != specs[6], ks[11], ks[12])
reaction008 = rxd.Reaction(specs[13] + specs[14] != specs[17], ks[13], ks[14])
reaction009 = rxd.Reaction(specs[17] + specs[15] != specs[18], ks[15], ks[16])
reaction010 = rxd.Reaction(specs[15] + specs[14] != specs[39], ks[17], ks[18])
reaction011 = rxd.Reaction(specs[39] + specs[13] != specs[18], ks[19], ks[20])
reaction012 = rxd.Reaction(specs[18] > specs[46] + specs[40], ks[21])
reaction013 = rxd.Reaction(specs[46] > specs[17] + specs[45], ks[22])
reaction014 = rxd.Reaction(specs[17] + specs[90] != specs[19], ks[23], ks[24])
reaction015 = rxd.Reaction(specs[19] > specs[23] + specs[90], ks[25])
reaction016 = rxd.Reaction(specs[23] + specs[90] != specs[20], ks[26], ks[27])
reaction017 = rxd.Reaction(specs[20] > specs[24] + specs[90], ks[28])
reaction018 = rxd.Reaction(specs[24] + specs[90] != specs[21], ks[29], ks[30])
reaction019 = rxd.Reaction(specs[21] > specs[25] + specs[90], ks[31])
reaction020 = rxd.Reaction(specs[25] + specs[90] != specs[22], ks[32], ks[33])
reaction021 = rxd.Reaction(specs[22] > specs[26] + specs[90], ks[34])
reaction022 = rxd.Reaction(specs[26] + specs[16] != specs[27], ks[35], ks[36])
reaction023 = rxd.Reaction(specs[27] > specs[28] + specs[42], ks[37])
reaction024 = rxd.Reaction(specs[28] > specs[26] + specs[44], ks[38])
reaction025 = rxd.Reaction(specs[23] > specs[17], ks[39])
reaction026 = rxd.Reaction(specs[24] > specs[23], ks[40])
reaction027 = rxd.Reaction(specs[25] > specs[24], ks[41])
reaction028 = rxd.Reaction(specs[26] > specs[25], ks[42])
reaction029 = rxd.Reaction(specs[14] + specs[90] != specs[29], ks[43], ks[44])
reaction030 = rxd.Reaction(specs[29] > specs[33] + specs[90], ks[45])
reaction031 = rxd.Reaction(specs[33] + specs[90] != specs[30], ks[46], ks[47])
reaction032 = rxd.Reaction(specs[30] > specs[34] + specs[90], ks[48])
reaction033 = rxd.Reaction(specs[34] + specs[90] != specs[31], ks[49], ks[50])
reaction034 = rxd.Reaction(specs[31] > specs[35] + specs[90], ks[51])
reaction035 = rxd.Reaction(specs[35] + specs[90] != specs[32], ks[52], ks[53])
reaction036 = rxd.Reaction(specs[32] > specs[36] + specs[90], ks[54])
reaction037 = rxd.Reaction(specs[36] + specs[16] != specs[37], ks[55], ks[56])
reaction038 = rxd.Reaction(specs[37] > specs[38] + specs[42], ks[57])
reaction039 = rxd.Reaction(specs[38] > specs[36] + specs[44], ks[58])
reaction040 = rxd.Reaction(specs[33] > specs[14], ks[59])
reaction041 = rxd.Reaction(specs[34] > specs[33], ks[60])
reaction042 = rxd.Reaction(specs[35] > specs[34], ks[61])
reaction043 = rxd.Reaction(specs[36] > specs[35], ks[62])
reaction044 = rxd.Reaction(specs[40] > specs[41], ks[63])
reaction045 = rxd.Reaction(specs[41] + specs[45] > specs[15], ks[64])
reaction046 = rxd.Reaction(specs[42] > specs[43], ks[65])
reaction047 = rxd.Reaction(specs[43] + specs[44] > specs[16], ks[66])
reaction048 = rxd.Reaction(specs[40] + specs[47] != specs[48], ks[67], ks[68])
reaction049 = rxd.Reaction(specs[48] + specs[73] != specs[49], ks[69], ks[70])
reaction050 = rxd.Reaction(specs[49] + specs[57] != specs[50], ks[71], ks[72])
reaction051 = rxd.Reaction(specs[50] > specs[58] + specs[49], ks[73])
reaction052 = rxd.Reaction(specs[42] + specs[48] != specs[54], ks[74], ks[75])
reaction053 = rxd.Reaction(specs[54] + specs[73] != specs[55], ks[76], ks[77])
reaction054 = rxd.Reaction(specs[55] + specs[57] != specs[56], ks[78], ks[79])
reaction055 = rxd.Reaction(specs[56] > specs[58] + specs[55], ks[80])
reaction056 = rxd.Reaction(specs[42] + specs[59] != specs[52], ks[81], ks[82])
reaction057 = rxd.Reaction(specs[52] + specs[57] != specs[53], ks[83], ks[84])
reaction058 = rxd.Reaction(specs[53] > specs[58] + specs[52], ks[85])
reaction059 = rxd.Reaction(specs[47] + specs[73] != specs[59], ks[86], ks[87])
reaction060 = rxd.Reaction(specs[59] + specs[57] != specs[60], ks[88], ks[89])
reaction061 = rxd.Reaction(specs[60] > specs[58] + specs[59], ks[90])
reaction062 = rxd.Reaction(specs[51] + specs[40] != specs[54], ks[91], ks[92])
reaction063 = rxd.Reaction(specs[61] + specs[73] != specs[62], ks[93], ks[94])
reaction064 = rxd.Reaction(specs[62] + specs[57] != specs[63], ks[95], ks[96])
reaction065 = rxd.Reaction(specs[63] > specs[58] + specs[62], ks[97])
reaction066 = rxd.Reaction(specs[70] + specs[0]*2 != specs[71], ks[98], ks[99])
reaction067 = rxd.Reaction(specs[71] + specs[0] != specs[72], ks[100], ks[101])
reaction068 = rxd.Reaction(specs[72] + specs[0] != specs[73], ks[102], ks[103])
reaction069 = rxd.Reaction(specs[70] + specs[68] != specs[69], ks[104], ks[105])
reaction070 = rxd.Reaction(specs[70] + specs[74] != specs[75], ks[106], ks[107])
reaction071 = rxd.Reaction(specs[71] + specs[74] != specs[76], ks[108], ks[109])
reaction072 = rxd.Reaction(specs[73] + specs[74] != specs[78], ks[110], ks[111])
reaction073 = rxd.Reaction(specs[75] + specs[0]*2 != specs[76], ks[112], ks[113])
reaction074 = rxd.Reaction(specs[76] + specs[0] != specs[77], ks[114], ks[115])
reaction075 = rxd.Reaction(specs[77] + specs[0] != specs[78], ks[116], ks[117])
reaction076 = rxd.Reaction(specs[73] + specs[79] != specs[80], ks[118], ks[119])
reaction077 = rxd.Reaction(specs[80]*2 != specs[83], ks[120], ks[121])
reaction078 = rxd.Reaction(specs[81] + specs[80] != specs[84], ks[122], ks[123])
reaction079 = rxd.Reaction(specs[81] + specs[83] > specs[81] + specs[84], ks[124])
reaction080 = rxd.Reaction(specs[80] + specs[83] > specs[80] + specs[84], ks[125])
reaction081 = rxd.Reaction(specs[83]*2 > specs[83] + specs[84], ks[126])
reaction082 = rxd.Reaction(specs[83] + specs[84] > specs[84]*2, ks[127])
reaction083 = rxd.Reaction(specs[81] != specs[73] + specs[82], ks[128], ks[129])
reaction084 = rxd.Reaction(specs[82] + specs[94] != specs[85], ks[130], ks[131])
reaction085 = rxd.Reaction(specs[85] > specs[94] + specs[79], ks[132])
reaction086 = rxd.Reaction(specs[81] + specs[94] != specs[86], ks[133], ks[134])
reaction087 = rxd.Reaction(specs[86] > specs[94] + specs[80], ks[135])
reaction088 = rxd.Reaction(specs[87] + specs[58]*4 != specs[88], ks[136], ks[137])
reaction089 = rxd.Reaction(specs[7] + specs[58] != specs[8], ks[138], ks[139])
reaction090 = rxd.Reaction(specs[91] + specs[90] != specs[92], ks[140], ks[141])
reaction091 = rxd.Reaction(specs[92] > specs[93] + specs[90], ks[142])
reaction092 = rxd.Reaction(specs[93] + specs[94] != specs[95], ks[143], ks[144])
reaction093 = rxd.Reaction(specs[93] + specs[78] != specs[96], ks[145], ks[146])
reaction094 = rxd.Reaction(specs[96] > specs[91] + specs[78], ks[147])
reaction095 = rxd.Reaction(specs[95] + specs[78] != specs[97], ks[148], ks[149])
reaction096 = rxd.Reaction(specs[97] > specs[91] + specs[98], ks[150])
reaction097 = rxd.Reaction(specs[98] > specs[94] + specs[78], ks[151])
reaction098 = rxd.Reaction(specs[99] + specs[90] != specs[103], ks[152], ks[153])
reaction099 = rxd.Reaction(specs[103] > specs[100] + specs[90], ks[154])
reaction100 = rxd.Reaction(specs[99] + specs[80] != specs[104], ks[155], ks[156])
reaction101 = rxd.Reaction(specs[104] > specs[101] + specs[80], ks[157])
reaction102 = rxd.Reaction(specs[99] + specs[81] != specs[105], ks[158], ks[159])
reaction103 = rxd.Reaction(specs[105] > specs[101] + specs[81], ks[160])
reaction104 = rxd.Reaction(specs[99] + specs[82] != specs[106], ks[161], ks[162])
reaction105 = rxd.Reaction(specs[106] > specs[101] + specs[82], ks[163])
reaction106 = rxd.Reaction(specs[99] + specs[172] != specs[107], ks[164], ks[165])
reaction107 = rxd.Reaction(specs[107] > specs[101] + specs[172], ks[166])
reaction108 = rxd.Reaction(specs[99] + specs[173] != specs[108], ks[167], ks[168])
reaction109 = rxd.Reaction(specs[108] > specs[101] + specs[173], ks[169])
reaction110 = rxd.Reaction(specs[100] + specs[80] != specs[109], ks[170], ks[171])
reaction111 = rxd.Reaction(specs[109] > specs[102] + specs[80], ks[172])
reaction112 = rxd.Reaction(specs[100] + specs[81] != specs[110], ks[173], ks[174])
reaction113 = rxd.Reaction(specs[110] > specs[102] + specs[81], ks[175])
reaction114 = rxd.Reaction(specs[100] + specs[82] != specs[111], ks[176], ks[177])
reaction115 = rxd.Reaction(specs[111] > specs[102] + specs[82], ks[178])
reaction116 = rxd.Reaction(specs[100] + specs[172] != specs[112], ks[179], ks[180])
reaction117 = rxd.Reaction(specs[112] > specs[102] + specs[172], ks[181])
reaction118 = rxd.Reaction(specs[100] + specs[173] != specs[113], ks[182], ks[183])
reaction119 = rxd.Reaction(specs[113] > specs[102] + specs[173], ks[184])
reaction120 = rxd.Reaction(specs[101] + specs[90] != specs[114], ks[185], ks[186])
reaction121 = rxd.Reaction(specs[114] > specs[102] + specs[90], ks[187])
reaction122 = rxd.Reaction(specs[100] + specs[94] != specs[115], ks[188], ks[189])
reaction123 = rxd.Reaction(specs[115] > specs[99] + specs[94], ks[190])
reaction124 = rxd.Reaction(specs[102] + specs[94] != specs[116], ks[191], ks[192])
reaction125 = rxd.Reaction(specs[116] > specs[100] + specs[94], ks[193])
reaction126 = rxd.Reaction(specs[116] > specs[101] + specs[94], ks[194])
reaction127 = rxd.Reaction(specs[101] + specs[94] != specs[117], ks[195], ks[196])
reaction128 = rxd.Reaction(specs[117] > specs[99] + specs[94], ks[197])
reaction129 = rxd.Reaction(specs[100] + specs[78] != specs[118], ks[198], ks[199])
reaction130 = rxd.Reaction(specs[118] > specs[99] + specs[78], ks[200])
reaction131 = rxd.Reaction(specs[102] + specs[78] != specs[119], ks[201], ks[202])
reaction132 = rxd.Reaction(specs[119] > specs[101] + specs[78], ks[203])
reaction133 = rxd.Reaction(specs[120] + specs[90] != specs[124], ks[204], ks[205])
reaction134 = rxd.Reaction(specs[124] > specs[121] + specs[90], ks[206])
reaction135 = rxd.Reaction(specs[120] + specs[80] != specs[125], ks[207], ks[208])
reaction136 = rxd.Reaction(specs[125] > specs[122] + specs[80], ks[209])
reaction137 = rxd.Reaction(specs[120] + specs[81] != specs[126], ks[210], ks[211])
reaction138 = rxd.Reaction(specs[126] > specs[122] + specs[81], ks[212])
reaction139 = rxd.Reaction(specs[120] + specs[82] != specs[127], ks[213], ks[214])
reaction140 = rxd.Reaction(specs[127] > specs[122] + specs[82], ks[215])
reaction141 = rxd.Reaction(specs[120] + specs[172] != specs[128], ks[216], ks[217])
reaction142 = rxd.Reaction(specs[128] > specs[122] + specs[172], ks[218])
reaction143 = rxd.Reaction(specs[120] + specs[173] != specs[129], ks[219], ks[220])
reaction144 = rxd.Reaction(specs[129] > specs[122] + specs[173], ks[221])
reaction145 = rxd.Reaction(specs[121] + specs[80] != specs[130], ks[222], ks[223])
reaction146 = rxd.Reaction(specs[130] > specs[123] + specs[80], ks[224])
reaction147 = rxd.Reaction(specs[121] + specs[81] != specs[131], ks[225], ks[226])
reaction148 = rxd.Reaction(specs[131] > specs[123] + specs[81], ks[227])
reaction149 = rxd.Reaction(specs[121] + specs[82] != specs[132], ks[228], ks[229])
reaction150 = rxd.Reaction(specs[132] > specs[123] + specs[82], ks[230])
reaction151 = rxd.Reaction(specs[121] + specs[172] != specs[133], ks[231], ks[232])
reaction152 = rxd.Reaction(specs[133] > specs[123] + specs[172], ks[233])
reaction153 = rxd.Reaction(specs[121] + specs[173] != specs[134], ks[234], ks[235])
reaction154 = rxd.Reaction(specs[134] > specs[123] + specs[173], ks[236])
reaction155 = rxd.Reaction(specs[122] + specs[90] != specs[135], ks[237], ks[238])
reaction156 = rxd.Reaction(specs[135] > specs[123] + specs[90], ks[239])
reaction157 = rxd.Reaction(specs[121] + specs[94] != specs[136], ks[240], ks[241])
reaction158 = rxd.Reaction(specs[136] > specs[120] + specs[94], ks[242])
reaction159 = rxd.Reaction(specs[123] + specs[94] != specs[137], ks[243], ks[244])
reaction160 = rxd.Reaction(specs[137] > specs[121] + specs[94], ks[245])
reaction161 = rxd.Reaction(specs[137] > specs[122] + specs[94], ks[246])
reaction162 = rxd.Reaction(specs[122] + specs[94] != specs[138], ks[247], ks[248])
reaction163 = rxd.Reaction(specs[138] > specs[120] + specs[94], ks[249])
reaction164 = rxd.Reaction(specs[121] + specs[78] != specs[139], ks[250], ks[251])
reaction165 = rxd.Reaction(specs[139] > specs[120] + specs[78], ks[252])
reaction166 = rxd.Reaction(specs[123] + specs[78] != specs[140], ks[253], ks[254])
reaction167 = rxd.Reaction(specs[140] > specs[122] + specs[78], ks[255])
reaction168 = rxd.Reaction(specs[99] != specs[120], ks[256], ks[257])
reaction169 = rxd.Reaction(specs[103] != specs[124], ks[258], ks[259])
reaction170 = rxd.Reaction(specs[104] != specs[125], ks[260], ks[261])
reaction171 = rxd.Reaction(specs[105] != specs[126], ks[262], ks[263])
reaction172 = rxd.Reaction(specs[106] != specs[127], ks[264], ks[265])
reaction173 = rxd.Reaction(specs[107] != specs[128], ks[266], ks[267])
reaction174 = rxd.Reaction(specs[108] != specs[129], ks[268], ks[269])
reaction175 = rxd.Reaction(specs[101] != specs[122], ks[270], ks[271])
reaction176 = rxd.Reaction(specs[114] != specs[135], ks[272], ks[273])
reaction177 = rxd.Reaction(specs[117] != specs[138], ks[274], ks[275])
reaction178 = rxd.Reaction(specs[100] != specs[121], ks[276], ks[277])
reaction179 = rxd.Reaction(specs[109] != specs[130], ks[278], ks[279])
reaction180 = rxd.Reaction(specs[110] != specs[131], ks[280], ks[281])
reaction181 = rxd.Reaction(specs[111] != specs[132], ks[282], ks[283])
reaction182 = rxd.Reaction(specs[112] != specs[133], ks[284], ks[285])
reaction183 = rxd.Reaction(specs[113] != specs[134], ks[286], ks[287])
reaction184 = rxd.Reaction(specs[102] != specs[123], ks[288], ks[289])
reaction185 = rxd.Reaction(specs[115] != specs[136], ks[290], ks[291])
reaction186 = rxd.Reaction(specs[116] != specs[137], ks[292], ks[293])
reaction187 = rxd.Reaction(specs[118] != specs[139], ks[294], ks[295])
reaction188 = rxd.Reaction(specs[119] != specs[140], ks[296], ks[297])
reaction189 = rxd.Reaction(specs[64] + specs[73] != specs[65], ks[298], ks[299])
reaction190 = rxd.Reaction(specs[65] + specs[58] != specs[66], ks[300], ks[301])
reaction191 = rxd.Reaction(specs[66] > specs[65] + specs[67], ks[302])
reaction192 = rxd.Reaction(specs[67] > specs[57], ks[303])
reaction193 = rxd.Reaction(specs[141] + specs[58] != specs[142], ks[304], ks[305])
reaction194 = rxd.Reaction(specs[142] > specs[141] + specs[67], ks[306])
reaction195 = rxd.Reaction(specs[90] + specs[141] != specs[143], ks[307], ks[308])
reaction196 = rxd.Reaction(specs[143] > specs[144] + specs[90], ks[309])
reaction197 = rxd.Reaction(specs[144] > specs[141], ks[310])
reaction198 = rxd.Reaction(specs[144] + specs[58] != specs[145], ks[311], ks[312])
reaction199 = rxd.Reaction(specs[145] > specs[144] + specs[67], ks[313])
reaction200 = rxd.Reaction(specs[142] + specs[90] != specs[146], ks[314], ks[315])
reaction201 = rxd.Reaction(specs[146] > specs[145] + specs[90], ks[316])
reaction202 = rxd.Reaction(specs[88] != specs[89] + specs[90]*2, ks[317]*specs[88], ks[318]*specs[89]*specs[90], custom_dynamics=True)
reaction203 = rxd.Reaction(specs[0] + specs[147] != specs[148], ks[319], ks[320])
reaction204 = rxd.Reaction(specs[149] != specs[154], ks[321], ks[322])
reaction205 = rxd.Reaction(specs[0] + specs[158] != specs[159], ks[323], ks[324])
reaction206 = rxd.Reaction(specs[156] + specs[158] != specs[161], ks[325], ks[326])
reaction207 = rxd.Reaction(specs[0] + specs[161] != specs[160], ks[327], ks[328])
reaction208 = rxd.Reaction(specs[156] + specs[159] != specs[160], ks[329], ks[330])
reaction209 = rxd.Reaction(specs[159] + specs[162] != specs[163], ks[331], ks[332])
reaction210 = rxd.Reaction(specs[163] > specs[166] + specs[165], ks[333])
reaction211 = rxd.Reaction(specs[166] > specs[159] + specs[174], ks[334])
reaction212 = rxd.Reaction(specs[160] + specs[162] != specs[164], ks[335], ks[336])
reaction213 = rxd.Reaction(specs[164] > specs[167] + specs[165], ks[337])
reaction214 = rxd.Reaction(specs[167] > specs[160] + specs[174], ks[338])
reaction215 = rxd.Reaction(specs[183] + specs[168] != specs[169], ks[339], ks[340])
reaction216 = rxd.Reaction(specs[169] > specs[168] + specs[162], ks[341])
reaction217 = rxd.Reaction(specs[161] > specs[158] + specs[157], ks[342])
reaction218 = rxd.Reaction(specs[160] > specs[159] + specs[157], ks[343])
reaction219 = rxd.Reaction(specs[156] > specs[157], ks[344])
reaction220 = rxd.Reaction(specs[157] > specs[155], ks[345])
reaction221 = rxd.Reaction(specs[0] + specs[178] != specs[179], ks[346], ks[347])
reaction222 = rxd.Reaction(specs[174] + specs[179] != specs[180], ks[348], ks[349])
reaction223 = rxd.Reaction(specs[180] > specs[179] + specs[181], ks[350])
reaction224 = rxd.Reaction(specs[165] > specs[183], ks[351])
reaction225 = rxd.Reaction(specs[181] > specs[182], ks[352])
reaction226 = rxd.Reaction(specs[174] + specs[175] != specs[176], ks[353], ks[354])
reaction227 = rxd.Reaction(specs[176] > specs[175] + specs[177], ks[355])
reaction228 = rxd.Reaction(specs[0] + specs[170] != specs[171], ks[356], ks[357])
reaction229 = rxd.Reaction(specs[171] + specs[174] != specs[172], ks[358], ks[359])
reaction230 = rxd.Reaction(specs[149] + specs[150] != specs[151], ks[360], ks[361])
reaction231 = rxd.Reaction(specs[151] != specs[152], ks[362], ks[363])
reaction232 = rxd.Reaction(specs[155] + specs[151] != specs[153], ks[364], ks[365])
reaction233 = rxd.Reaction(specs[153] > specs[156] + specs[151], ks[366])
reaction234 = rxd.Reaction(specs[184] + specs[172] != specs[185], ks[367], ks[368])
reaction235 = rxd.Reaction(specs[185] > specs[187] + specs[172], ks[369])
reaction236 = rxd.Reaction(specs[184] + specs[173] != specs[186], ks[370], ks[371])
reaction237 = rxd.Reaction(specs[186] > specs[187] + specs[173], ks[372])
reaction238 = rxd.Reaction(specs[187] + specs[194] != specs[188], ks[373], ks[374])
reaction239 = rxd.Reaction(specs[188] > specs[184] + specs[194], ks[375])
reaction240 = rxd.Reaction(specs[189] + specs[172] != specs[190], ks[376], ks[377])
reaction241 = rxd.Reaction(specs[190] > specs[192] + specs[172], ks[378])
reaction242 = rxd.Reaction(specs[189] + specs[173] != specs[191], ks[379], ks[380])
reaction243 = rxd.Reaction(specs[191] > specs[192] + specs[173], ks[381])
reaction244 = rxd.Reaction(specs[192] + specs[194] != specs[193], ks[382], ks[383])
reaction245 = rxd.Reaction(specs[193] > specs[189] + specs[194], ks[384])
reaction246 = rxd.Reaction(specs[184] != specs[189], ks[385], ks[386])
reaction247 = rxd.Reaction(specs[185] != specs[190], ks[387], ks[388])
reaction248 = rxd.Reaction(specs[186] != specs[191], ks[389], ks[390])
reaction249 = rxd.Reaction(specs[187] != specs[192], ks[391], ks[392])
reaction250 = rxd.Reaction(specs[188] != specs[193], ks[393], ks[394])
reaction251 = rxd.Reaction(specs[195] + specs[196] != specs[197], ks[395], ks[396])
reaction252 = rxd.Reaction(specs[155] + specs[197] != specs[199], ks[397], ks[398])
reaction253 = rxd.Reaction(specs[155] + specs[196] != specs[198], ks[399], ks[400])
reaction254 = rxd.Reaction(specs[195] + specs[198] != specs[199], ks[401], ks[402])
reaction255 = rxd.Reaction(specs[199] > specs[156] + specs[197], ks[403])
reaction256 = rxd.Reaction(specs[195] > specs[195]*0, ks[404])
reaction257 = rxd.Reaction(specs[0] + specs[200] != specs[201], ks[405], ks[406])
reaction258 = rxd.Reaction(specs[201] + specs[162] != specs[202], ks[407], ks[408])
reaction259 = rxd.Reaction(specs[202] > specs[201] + specs[203], ks[409])
reaction260 = rxd.Reaction(specs[203] > specs[162], ks[410])
reaction261 = rxd.Reaction(specs[172] + specs[203] != specs[173], ks[411], ks[412])

reaction_Ca_flux = rxd.Rate(specs[0], Ca_flux_rate) # Ca
reaction_L_flux = rxd.Rate(specs[13], L_flux_rate) # L
reaction_Glu_flux = rxd.Rate(specs[149], Glu_flux_rate) # Glu
reaction_ACh_flux = rxd.Rate(specs[195], ACh_flux_rate) # ACh

vecs = []
vec_t = h.Vector()
vec_t.record(h._ref_t)
toRecord = [0]*len(species)

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
                     ['GluR1', 'GluR1_PKCt','GluR1_PKCp', 'GluR2'],
                     'syncond']

for ispec in range(0,len(species)):
  vecs.append(h.Vector())
  for imeas in range(0,len(Measured_species)):
    if species[ispec] in Measured_species[imeas]:
      toRecord[ispec] = 1+(species[ispec]=='Ca')
      break
  if toRecord[ispec] == 2:
    vecs[ispec].record(specs[ispec].nodes(dend)(0.5)[0]._ref_concentration)
  elif toRecord[ispec] == 1:
    vecs[ispec].record(specs[ispec].nodes(dend)(0.5)[0]._ref_concentration,10000)

cvode = h.CVode()
cvode.active(1)
hmax = cvode.maxstep(1000)
hmin = cvode.minstep(1e-6)
cvode.atol(tolerance)

h.finitialize(-65)
print('Simulation started!')
print('Duration: '+str(Duration))
print('\n')

def set_param(param, val):
    param.nodes.value = val
    h.cvode.re_init()

### Set on and off the inputs to the spine
# L and ACh:
h.cvode.event(L_input_onset, lambda: set_param(L_flux_rate, L_input_flux/6.022e23/my_volume*1e3))
h.cvode.event(L_input_onset, lambda: set_param(ACh_flux_rate, ACh_input_flux/6.022e23/my_volume*1e3))

# Ca and Glu:
T = 1000./Ca_input_freq
tnow = 0

for itrain in range(0,Ntrains):
    for istim in range(0,Ca_input_N):
      tnew = Ca_input_onset + istim*T + trainT*itrain                       
      h.cvode.event(tnew, lambda: set_param(Ca_flux_rate, Ca_input_flux/6.022e23/my_volume*1e3))
      h.cvode.event(tnew+Ca_input_dur, lambda: set_param(Ca_flux_rate, 0))
      h.cvode.event(tnew, lambda: set_param(Glu_flux_rate, Glu_input_flux/6.022e23/my_volume*1e3))
      h.cvode.event(tnew+Ca_input_dur, lambda: set_param(Glu_flux_rate, 0))
      tnow = tnew
timenow = time.time()
h.continuerun(Duration)
print("Simulation done in "+str(time.time()-timenow)+" seconds")

def isFlux(t):
  for itrain in range(0,Ntrains):
    for istim in range(0,Ca_input_N):
      tnew = Ca_input_onset + istim*T + trainT*itrain
      if t >= tnew and t < tnew+Ca_input_dur:
        return 1
  return 0

tvec = np.array(vec_t)
minDT_nonFlux = 20.0
minDT_Flux = 1.0
lastt = -(np.inf)
itvec2 = []
for it in range(0,len(tvec)):
  if tvec[it] - lastt > minDT_nonFlux or (isFlux(tvec[it]) and tvec[it] - lastt > minDT_Flux):
    itvec2.append(it)
    lastt = tvec[it]

headers = [ 'tvec', 'Ca', 'CaOut', 'CaOutLeak', 'Leak', 'Calbin', 'CalbinC', 'LOut', 'Epac1', 'Epac1cAMP', 'PMCA', 'NCX', 'PMCACa', 'NCXCa', 'L', 'R', 'Gs', 'Gi', 'LR', 'LRGs', 'PKAcLR', 'PKAcpLR', 'PKAcppLR', 'PKAcpppLR', 'pLR', 'ppLR', 'pppLR', 'ppppLR', 'ppppLRGi', 'ppppLRGibg', 'PKAcR', 'PKAcpR', 'PKAcppR', 'PKAcpppR', 'pR', 'ppR', 'pppR', 'ppppR', 'ppppRGi', 'ppppRGibg', 'GsR', 'GsaGTP', 'GsaGDP', 'GiaGTP', 'GiaGDP', 'Gibg', 'Gsbg', 'LRGsbg', 'AC1', 'AC1GsaGTP', 'AC1GsaGTPCaMCa4', 'AC1GsaGTPCaMCa4ATP', 'AC1GiaGTP', 'AC1GiaGTPCaMCa4', 'AC1GiaGTPCaMCa4ATP', 'AC1GsaGTPGiaGTP', 'AC1GsaGTPGiaGTPCaMCa4', 'AC1GsGiCaMCa4ATP', 'ATP', 'cAMP', 'AC1CaMCa4', 'AC1CaMCa4ATP', 'AC8', 'AC8CaMCa4', 'AC8CaMCa4ATP', 'PDE1', 'PDE1CaMCa4', 'PDE1CaMCa4cAMP', 'AMP', 'Ng', 'NgCaM', 'CaM', 'CaMCa2', 'CaMCa3', 'CaMCa4', 'PP2B', 'PP2BCaM', 'PP2BCaMCa2', 'PP2BCaMCa3', 'PP2BCaMCa4', 'CK', 'CKCaMCa4', 'CKpCaMCa4', 'CKp', 'Complex', 'pComplex', 'CKpPP1', 'CKpCaMCa4PP1', 'PKA', 'PKAcAMP4', 'PKAr', 'PKAc', 'I1', 'I1PKAc', 'Ip35', 'PP1', 'Ip35PP1', 'Ip35PP2BCaMCa4', 'Ip35PP1PP2BCaMCa4', 'PP1PP2BCaMCa4', 'GluR1', 'GluR1_S845', 'GluR1_S831', 'GluR1_S845_S831', 'GluR1_PKAc', 'GluR1_CKCam', 'GluR1_CKpCam', 'GluR1_CKp', 'GluR1_PKCt', 'GluR1_PKCp', 'GluR1_S845_CKCam', 'GluR1_S845_CKpCam', 'GluR1_S845_CKp', 'GluR1_S845_PKCt', 'GluR1_S845_PKCp', 'GluR1_S831_PKAc', 'GluR1_S845_PP1', 'GluR1_S845_S831_PP1', 'GluR1_S831_PP1', 'GluR1_S845_PP2B', 'GluR1_S845_S831_PP2B', 'GluR1_memb', 'GluR1_memb_S845', 'GluR1_memb_S831', 'GluR1_memb_S845_S831', 'GluR1_memb_PKAc', 'GluR1_memb_CKCam', 'GluR1_memb_CKpCam', 'GluR1_memb_CKp', 'GluR1_memb_PKCt', 'GluR1_memb_PKCp', 'GluR1_memb_S845_CKCam', 'GluR1_memb_S845_CKpCam', 'GluR1_memb_S845_CKp', 'GluR1_memb_S845_PKCt', 'GluR1_memb_S845_PKCp', 'GluR1_memb_S831_PKAc', 'GluR1_memb_S845_PP1', 'GluR1_memb_S845_S831_PP1', 'GluR1_memb_S831_PP1', 'GluR1_memb_S845_PP2B', 'GluR1_memb_S845_S831_PP2B', 'PDE4', 'PDE4cAMP', 'PKAcPDE4', 'pPDE4', 'pPDE4cAMP', 'PKAc_PDE4_cAMP', 'fixedbuffer', 'fixedbufferCa', 'Glu', 'MGluR', 'MGluR_Glu', 'MGluR_Glu_desens', 'MGluR_Gqabg_Glu', 'GluOut', 'Gqabg', 'GqaGTP', 'GqaGDP', 'PLC', 'PLCCa', 'PLCCaGqaGTP', 'PLCGqaGTP', 'Pip2', 'PLCCaPip2', 'PLCCaGqaGTPPip2', 'Ip3', 'PLCCaDAG', 'PLCCaGqaGTPDAG', 'PIkinase', 'Ip3degPIk', 'PKC', 'PKCCa', 'PKCt', 'PKCp', 'DAG', 'DAGK', 'DAGKdag', 'PA', 'DGL', 'CaDGL', 'DAGCaDGL', '2AG', '2AGdegrad', 'Ip3degrad', 'GluR2', 'GluR2_PKCt', 'GluR2_PKCp', 'GluR2_S880', 'GluR2_S880_PP2A', 'GluR2_memb', 'GluR2_memb_PKCt', 'GluR2_memb_PKCp', 'GluR2_memb_S880', 'GluR2_memb_S880_PP2A', 'PP2A', 'ACh', 'M1R', 'AChM1R', 'M1RGq', 'AChM1RGq', 'PLA2', 'CaPLA2', 'CaPLA2Pip2', 'AA' ]

myonset = 0
#myonset = Ca_input_onset
if myonset > max(tvec):
  myonset = 0

baseline_length = 5400000   # 90 min --> 30 min baseline if input at 120 min
interptimes = [baseline_length + 120000*i for i in range(0,int((max(tvec) - baseline_length)/120000)+1)]
#full_timeCourse = [myonset + 120000*i for i in range(0,int((max(tvec)-myonset)/120000+1))]
#print('INTERPTIMES: '+str(interptimes))

if interptimes[0] < 0:
  interptimes = interptimes[1:]
  
interpDATA = []
#ftcDATA = []

def interpolate(tref,vref,tint): #Assumes that the trefs come sorted!
  vint = len(tint)*[0.0]
  addedOne = False
  if tref[0] > tint[0] or tref[len(tref)-1] < tint[len(tint)-1]:
    print("Extrapolation needed!")
    return len(tint)*[-1]
  indvrecnow = 0  
  for j in range(0,len(tint)):
    while tref[indvrecnow+1] <= tint[j]:
      indvrecnow = indvrecnow + 1
      if indvrecnow == len(tref)-1: # It must be the last index if this happens
        vint[j:len(tint)] = [vref[indvrecnow]]*(len(tint)-j)
        return vint
    vint[j] = vref[indvrecnow] + 1.0*(tint[j]-tref[indvrecnow])/(tref[indvrecnow+1]-tref[indvrecnow])*(vref[indvrecnow+1]-vref[indvrecnow])
  return vint

for j in range(0,len(species)):
  if toRecord[j]==2:
    interpDATA.append(interpolate(tvec,vecs[j],interptimes))
    #ftcDATA.append(interpolate(tvec,vecs[j],full_timeCourse))
  elif toRecord[j]==1:
    interpDATA.append(interpolate([10000.0*x for x in range(0,len(vecs[j]))],vecs[j],interptimes))
    #ftcDATA.append(interpolate([10000.0*x for x in range(0,len(vecs[j]))],vecs[j],full_timeCourse))
  else:
    interpDATA.append([0 for x in interptimes])
    #ftcDATA.append([0 for x in full_timeCourse])

tcDATA = np.array([interptimes]+interpDATA)
#full_timeCourse_DATA = np.array([full_timeCourse]+ftcDATA)
maxDATA = [max(tvec)]+[0.0 for i in range(0,len(species))]

for ispec in range(0,len(species)):
  if toRecord[ispec]:
    maxDATA[1+ispec] = max(np.array(vecs[ispec]))
print('Filename: ' + str(filename) + str('.mat'))
scipy.io.savemat(filename+'.mat',{'DATA': tcDATA, 'maxDATA': maxDATA, 'headers': headers}, appendmat=True)  # 'fullDATA': full_timeCourse_DATA, 