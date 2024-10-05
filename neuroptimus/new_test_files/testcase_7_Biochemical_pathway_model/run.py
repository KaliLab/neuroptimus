import os
import sys
import time
import json
import random
import shutil
import scipy.io
import numpy as np
from os.path import exists
import matplotlib.pyplot as plt
import protocol_file as protocols_many

unique_ID = sys.argv[1]
params_file = 'params' + unique_ID + '.param'
params_v = np.genfromtxt(params_file)

parameters = {"Caflux": params_v[0],
             "Lflux": params_v[1],
             "Gluflux": params_v[2],
             "GluR1_ratio": params_v[3],
             "IC_MGluRM1RGqPLC": params_v[4],
             "IC_RGsAC1AC8": params_v[5],
             "IC_CaMCK":params_v[6],
             "IC_NCX": params_v[7],
             "IC_PKC": params_v[8],
             "IC_PKA": params_v[9],
             "IC_PP1PP2B": params_v[10],
             "IC_PDE1PDE4": params_v[11],} 
imeas = 0

Measurement_protocol = protocols_many.get_measurement_protocol()
MeasurementsAll =      Measurement_protocol[0]
Experiments =          Measurement_protocol[1]
protoparams_fixed =    Measurement_protocol[2]
protoparams_var =      Measurement_protocol[3]

#These are fixed across experiments:
Duration         = protoparams_fixed['Duration']
tolerance        = protoparams_fixed['tolerance']
Ca_input_onset   = protoparams_fixed['Ca_input_onset']

#These are indexed according to experiments:
Ca_input_NsAll    = protoparams_var['Ca_input_Ns']
Ca_input_freqsAll = protoparams_var['Ca_input_freqs']
Ca_input_dursAll  = protoparams_var['Ca_input_durs']
NtrainsAll        = protoparams_var['Ca_input_Ntrains']
trainTsAll        = protoparams_var['Ca_input_trainTs']

Measurements =     MeasurementsAll[imeas]
iExperiments =     Measurements[0]

def run_model(parameters, deleteFiles=False, rankID=0):

  paramkeys = list(parameters.keys())

  Ca_input_flux  = parameters['Caflux'] if 'Caflux' in list(parameters.keys()) else 0.0
  L_input_flux   = parameters['Lflux'] if 'Lflux' in list(parameters.keys()) else 0.0
  Glu_input_flux = parameters['Gluflux'] if 'Gluflux' in list(parameters.keys()) else 0.0
  ACh_input_flux = parameters['AChflux'] if 'AChflux' in list(parameters.keys()) else 0.0
  GluR1_ratio = parameters['GluR1_ratio'] if 'GluR1_ratio' in list(parameters.keys()) else 0.5

  addition_IC = ''
  addition_IC_values = ''
  addition_ks = ''
  addition_ks_values = ''

  for iparam in range(0,len(paramkeys)):
    if paramkeys[iparam] == 'IC_MGluRM1RGqPLC':
      addition_IC = addition_IC + '~MGluR~M1R~Gqabg~PLC'
      addition_IC_values = addition_IC_values + '~'+str(parameters[paramkeys[iparam]]) + '~'+str(parameters[paramkeys[iparam]]) + '~'+str(parameters[paramkeys[iparam]]) + '~'+str(parameters[paramkeys[iparam]])
    elif paramkeys[iparam] == 'IC_RGsAC1AC8':
      addition_IC = addition_IC + '~R~Gs~AC1~AC8'
      addition_IC_values = addition_IC_values + '~'+str(parameters[paramkeys[iparam]]) + '~'+str(parameters[paramkeys[iparam]]) + '~'+str(parameters[paramkeys[iparam]]) + '~'+str(parameters[paramkeys[iparam]])
    elif paramkeys[iparam] == 'IC_CaMCK':
      addition_IC = addition_IC + '~CaM~CK'
      addition_IC_values = addition_IC_values + '~'+str(parameters[paramkeys[iparam]]) + '~'+str(parameters[paramkeys[iparam]])
    elif paramkeys[iparam] == 'IC_NCX':
      addition_IC = addition_IC + '~NCX'
      addition_IC_values = addition_IC_values + '~'+str(parameters[paramkeys[iparam]])
    elif paramkeys[iparam] == 'IC_PKC':
      addition_IC = addition_IC + '~PKC'
      addition_IC_values = addition_IC_values + '~'+str(parameters[paramkeys[iparam]])
    elif paramkeys[iparam] == 'IC_PKA':
      addition_IC = addition_IC + '~PKA'
      addition_IC_values = addition_IC_values + '~'+str(parameters[paramkeys[iparam]])
    elif paramkeys[iparam] == 'IC_PP1PP2B':
      addition_IC = addition_IC + '~PP1~PP2B'
      addition_IC_values = addition_IC_values + '~'+str(parameters[paramkeys[iparam]]) + '~'+str(parameters[paramkeys[iparam]])
    elif paramkeys[iparam] == 'IC_PDE1PDE4':
      addition_IC = addition_IC + '~PDE1~PDE4'
      addition_IC_values = addition_IC_values + '~'+str(parameters[paramkeys[iparam]]) + '~'+str(parameters[paramkeys[iparam]])
    elif paramkeys[iparam][0:3] == 'ks[':
      ks_ids = paramkeys[iparam][3:paramkeys[iparam].find(']')].split(',')
      for ik in range(0,len(ks_ids)):
        addition_ks = addition_ks + '-'+ks_ids[ik]
        addition_ks_values = addition_ks_values + '-'+str(parameters[paramkeys[iparam]])
    elif paramkeys[iparam].find('flux') == -1 and paramkeys[iparam].find('GluR1_ratio') == -1:
      print('Param '+paramkeys[iparam]+' not recognized, rankID='+str(rankID))
    
  addition_IC = addition_IC + '~GluR1~GluR1_memb~GluR2~GluR2_memb'
  addition_IC_values = addition_IC_values + '~'+str(2.*np.asarray(GluR1_ratio))+'~'+str(2.*np.asarray(GluR1_ratio))+'~'+str(2*np.asarray(1-(np.asarray(GluR1_ratio))))+'~'+str(2*np.asarray(1-(np.asarray(GluR1_ratio))))

  if len(addition_IC) > 0:
    addition_IC = addition_IC[1:]
    addition_IC_values = addition_IC_values[1:]
  else:
    addition_IC = 'Ca'
    addition_IC_values = '1.0'
  if len(addition_ks) > 0:
    addition_ks = addition_ks[1:]
    addition_ks_values = addition_ks_values[1:]

  timesAll = []
  timeCoursesAll = []
  maxValsAll = []
  filenames = []
  timenow = time.time()
  timetmp = time.time()

  for iiexperiment in range(0,len(iExperiments)):
    iexperiment = iExperiments[iiexperiment]
    iStimulusProtocol = Experiments[iexperiment][0]
    Ca_input_flux_coeff = Experiments[iexperiment][1]
    L_input_flux_coeff = Experiments[iexperiment][2]
    Glu_input_flux_coeff = Experiments[iexperiment][3]
    ACh_input_flux_coeff = Experiments[iexperiment][4]
    Blocked = Experiments[iexperiment][5]
    Altered = Experiments[iexperiment][6]

    Ca_input_N    = Ca_input_NsAll[iStimulusProtocol]
    Ca_input_freq = Ca_input_freqsAll[iStimulusProtocol]
    Ca_input_dur  = Ca_input_dursAll[iStimulusProtocol]
    Ntrains       = NtrainsAll[iStimulusProtocol]
    trainT        = trainTsAll[iStimulusProtocol]

    addition_IC_this = addition_IC
    addition_IC_values_this = addition_IC_values
    addition_ks_this = addition_ks
    addition_ks_values_this = addition_ks_values

    if Blocked != 'None':
      xInd = Blocked.rfind('x')
      if xInd == -1:
        print("Something's wrong with the Blocked!!")
        time.sleep(5)
      addition_IC_this = addition_IC_this + '-' + Blocked[0:xInd]
      addition_IC_values_this = addition_IC_values_this + '-' + Blocked[xInd+1:]

    if len(Altered) > 0:
      for ialtered in range(0,len(Altered[0])):
        addition_ks_this = addition_ks_this + '-'*(ialtered != 0 or len(addition_ks_this) > 0) + str(Altered[0][ialtered])
        addition_ks_values_this = addition_ks_values_this + '-'*(ialtered != 0 or len(addition_ks_values_this) > 0) + str(Altered[1])

    randomString = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for _ in range(0,10))+'_'+str(rankID)+'_'+str(iiexperiment)
    print('\n')
    print('Running model file..')
    print('python3 model_file_simulation.py'+' '+str(Duration)+' '+str(tolerance)+' '+str(Ca_input_onset)+' '+str(Ca_input_N)+' '+str(Ca_input_freq)+' '+str(Ca_input_dur)+' '+
           str(Ca_input_flux*Ca_input_flux_coeff)+' '+str(Ca_input_onset-600000)+' '+str(L_input_flux*L_input_flux_coeff)+' '+str(Glu_input_flux*Glu_input_flux_coeff)+' '+str(ACh_input_flux*ACh_input_flux_coeff)+' '+
           str(Ntrains)+' '+str(trainT)+' None fit'+randomString+' '+addition_IC_this+' '+addition_IC_values_this+' '+addition_ks_this+' '+addition_ks_values_this)
    os.system('python3 model_file_simulation.py '+str(Duration)+' '+str(tolerance)+' '+str(Ca_input_onset)+' '+str(Ca_input_N)+' '+str(Ca_input_freq)+' '+str(Ca_input_dur)+' '+
           str(Ca_input_flux*Ca_input_flux_coeff)+' '+str(Ca_input_onset-600000)+' '+str(L_input_flux*L_input_flux_coeff)+' '+str(Glu_input_flux*Glu_input_flux_coeff)+' '+str(ACh_input_flux*ACh_input_flux_coeff)+' '+
           str(Ntrains)+' '+str(trainT)+' None fit'+randomString+' '+addition_IC_this+' '+addition_IC_values_this+' '+addition_ks_this+' '+addition_ks_values_this)
    print(('Exp. '+str(iiexperiment)+' ('+str(iexperiment)+'), ID='+str(rankID)+' done in '+str(time.time()-timenow)+' sec'))

    timetmp = time.time()
    filename = 'fit'+randomString
    filenames.append(filename)
    
    if not exists(filename+'.mat'):
      print('Error: filename = '+filename+'.mat does not exists, Exp. ='+str(iiexperiment))
      timesAll.append([])
      timeCoursesAll.append([])
      maxValsAll.append([])
      continue
     
    import calcconds                 
    conds, times, cas = calcconds.calcconds_nrn_withcas(filename+'.mat')
    A = scipy.io.loadmat(filename+'.mat')
    timesAll.append(times[:])
    timeCoursesAll.append(conds[:])
    if A['maxDATA'].shape[0] == 1:
      maxValsAll.append(A['maxDATA'][0][1])
    else:
      maxValsAll.append(A['maxDATA'][1][0])
    
    Ca_input_onset_index = ((np.ndarray.tolist(times)).index(Ca_input_onset))
    #Saving traces into trace file.
    if iiexperiment == 0:
      control_trace = [conds[k]/conds[Ca_input_onset_index-1] for k in range(Ca_input_onset_index,len(conds))]
      tf = open('trace'+unique_ID+'.dat', 'a')
      print('Saving experiment_0 trace..')
      np.savetxt(tf, np.array([times[Ca_input_onset_index:], control_trace]).T, delimiter=' ')
      tf.close()
    elif iiexperiment == 1:
      blocked = [conds[k]/conds[Ca_input_onset_index-1] for k in range(Ca_input_onset_index,len(conds))]
      tf = open('trace'+unique_ID+'.dat', 'a')
      tf = np.genfromtxt('trace'+unique_ID+'.dat')
      print('Saving experiment_1 trace..')
      blocked_trace = np.array([times[Ca_input_onset_index:], blocked]).T
      tf = np.append(tf,  blocked_trace, 0)
      np.savetxt('trace'+unique_ID+'.dat', tf, delimiter=" ", fmt="%s")
    else:
      print('Something is wrong with experiment index!')

  if deleteFiles:
    print('Deleting .mat files')
    for filename in filenames:
      os.remove(filename + '.mat')
  
  return [timesAll, timeCoursesAll, maxValsAll]

run_model(parameters, deleteFiles=True, rankID=0)
