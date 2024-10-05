import numpy as np
import scipy.io
from os.path import exists

# conductance calculations
def calcconds_nrn_withcas(filename_nrn):
  Measured_species = [ [ ['GluR1_S831', 'GluR1_S845_S831', 'GluR1_S831_PKAc', 'GluR1_S845_S831_PP1', 'GluR1_S831_PP1', 'GluR1_S845_S831_PP2B', 'GluR1_memb_S831', 'GluR1_memb_S845_S831', 'GluR1_memb_S831_PKAc', 'GluR1_memb_S845_S831_PP1', 'GluR1_memb_S831_PP1', 'GluR1_memb_S845_S831_PP2B'] ],
                   [ ['GluR1_memb_S831', 'GluR1_memb_S845_S831', 'GluR1_memb_S831_PKAc', 'GluR1_memb_S845_S831_PP1', 'GluR1_memb_S831_PP1', 'GluR1_memb_S845_S831_PP2B'] ],
                   [ ['GluR1_S845', 'GluR1_S845_S831', 'GluR1_S845_CKCam', 'GluR1_S845_CKpCam', 'GluR1_S845_CKp', 'GluR1_S845_PKCt', 'GluR1_S845_PKCp', 'GluR1_S845_PP1', 'GluR1_S845_S831_PP1', 'GluR1_S845_PP2B', 'GluR1_S845_S831_PP2B', 'GluR1_memb_S845', 'GluR1_memb_S845_S831', 'GluR1_memb_S845_CKCam', 'GluR1_memb_S845_CKpCam', 'GluR1_memb_S845_CKp', 'GluR1_memb_S845_PKCt', 'GluR1_memb_S845_PKCp', 'GluR1_memb_S845_PP1', 'GluR1_memb_S845_S831_PP1', 'GluR1_memb_S845_PP2B', 'GluR1_memb_S845_S831_PP2B'] ],
                   [ ['GluR1_memb', 'GluR1_memb_S845', 'GluR1_memb_S831', 'GluR1_memb_S845_S831', 'GluR1_memb_PKAc', 'GluR1_memb_CKCam', 'GluR1_memb_CKpCam', 'GluR1_memb_CKp', 'GluR1_memb_PKCt', 'GluR1_memb_PKCp', 'GluR1_memb_S845_CKCam', 'GluR1_memb_S845_CKpCam', 'GluR1_memb_S845_CKp', 'GluR1_memb_S845_PKCt', 'GluR1_memb_S845_PKCp', 'GluR1_memb_S831_PKAc', 'GluR1_memb_S845_PP1', 'GluR1_memb_S845_S831_PP1', 'GluR1_memb_S831_PP1', 'GluR1_memb_S845_PP2B', 'GluR1_memb_S845_S831_PP2B'] ],
                   [ ['GluR2_S880', 'GluR2_S880_PP2A', 'GluR2_memb_S880', 'GluR2_memb_S880_PP2A'] ],
                   [ ['GluR2_memb', 'GluR2_memb_PKCt', 'GluR2_memb_PKCp', 'GluR2_memb_S880', 'GluR2_memb_S880_PP2A'] ] ]

  conds_hom1 = [12.4, 18.9]
  conds_hom2 = 2.2
  conds_het = 2.5
  Nskip = 1
  my_volume = 0.50000*1e-15 #litres

  DATANRN_all = {}
  assert exists(filename_nrn)

  DATANRN_all_all = scipy.io.loadmat(filename_nrn)
  
  for ikey in range(0,len(DATANRN_all_all['headers'])):
    mykey = DATANRN_all_all['headers'][ikey][0:DATANRN_all_all['headers'][ikey].find(' ')]
    DATANRN_all[mykey] = DATANRN_all_all['DATA'][ikey]
    
  if len(DATANRN_all) > 0:
    times_nrn = DATANRN_all['tvec']

  TCs_nrn_all = []
  TCsN_nrn_all = []
  
  for iax in range(0,len(Measured_species)):
    for ispecgroup in range(0,len(Measured_species[iax])):
      specgroup = Measured_species[iax][ispecgroup]
      if len(DATANRN_all) > 0:
        mytimecourse_nrn = np.zeros(times_nrn.shape[0])
      if type(specgroup) is not list:
        specgroup = [specgroup]
      for ispec in range(0,len(specgroup)):
        specfactor = 1.0
        if len(specgroup[ispec]) > 24 and len(DATANRN_all) > 0:
          mytimecourse_nrn = mytimecourse_nrn + DATANRN_all[specgroup[ispec][:24]]
        elif len(DATANRN_all) > 0:
          mytimecourse_nrn = mytimecourse_nrn + DATANRN_all[specgroup[ispec]]

    factor = 1.0/6.022e23/my_volume*1e9
    nrnfactor = 1.0
    TCs_nrn_all.append(mytimecourse_nrn[::Nskip]*1e6*nrnfactor)
    TCsN_nrn_all.append(mytimecourse_nrn[::Nskip]*1e6*nrnfactor/factor)

  ENhom1_np_nrn = (TCsN_nrn_all[3] + TCsN_nrn_all[5])/4.0 * (TCsN_nrn_all[3]-TCsN_nrn_all[1])**4/(TCsN_nrn_all[3] + TCsN_nrn_all[5])**4                       
  ENhom1_p_nrn = (TCsN_nrn_all[3] + TCsN_nrn_all[5])/4.0 * (TCsN_nrn_all[3]**4 - (TCsN_nrn_all[3]-TCsN_nrn_all[1])**4)/(TCsN_nrn_all[3] + TCsN_nrn_all[5])**4 
  ENhom2_nrn = (TCsN_nrn_all[3] + TCsN_nrn_all[5])/4.0 * (TCsN_nrn_all[5]/(TCsN_nrn_all[3] + TCsN_nrn_all[5]))**4
  ENhet_nrn = (TCsN_nrn_all[3] + TCsN_nrn_all[5])/4.0 * (1 - (TCsN_nrn_all[3]/(TCsN_nrn_all[3] + TCsN_nrn_all[5]))**4 - (TCsN_nrn_all[5]/(TCsN_nrn_all[3] + TCsN_nrn_all[5]))**4)
  Egtot_nrn = ENhom1_np_nrn*conds_hom1[0] + ENhom1_p_nrn*conds_hom1[1] + ENhom2_nrn*conds_hom2 + ENhet_nrn*conds_het

  return Egtot_nrn, times_nrn, DATANRN_all['Ca']
