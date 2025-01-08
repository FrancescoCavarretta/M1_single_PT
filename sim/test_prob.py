import pickle
import numpy as np
layer = {'1':[0.0, 0.1], '2': [0.1,0.29], '4': [0.29,0.37], '5A': [0.37,0.47], '24':[0.1,0.37], '5B': [0.47,0.8], '6': [0.8,1.0],}


with open('conn/conn.pkl', 'rb') as fileObj:
  connData = pickle.load(fileObj)
  
pmat = connData['pmat']
wmat = connData['wmat']
bins = connData['bins']


print( 'L2', np.mean(pmat[('W+AS_norm', 'PT', 'L5B')][:, :2]) )
print( 'L3', np.mean(pmat[('W+AS_norm', 'PT', 'L5B')][:, 2:5]) )
print( 'L4', np.mean(pmat[('W+AS_norm', 'PT', 'L5B')][:, 5:7]) )
print( 'L5A', np.mean(pmat[('W+AS_norm', 'PT', 'L5B')][:, 7:8]) )
print( 'L5B', np.mean(pmat[('W+AS_norm', 'PT', 'L5B')][:, 8:13]) )
print( 'L6', np.mean(pmat[('W+AS_norm', 'PT', 'L5B')][:, 13:]) )
##for ipre, preBin in enumerate(bins['AS']):
##    for ipost, postBin in enumerate(bins[('W+AS', 'PT', 'L5B')]):
##        netParams.connParams['IT->PT5B_full[%d,%d]' % (ipre, ipost)] = { 
##            'preConds': {'pop': ['IT2/3','IT5A','IT5B','PT5B','IT6'], 'ynorm': list(preBin)}, 
##            'postConds': {'cellModel': 'HH_full', 'cellType': 'PT', 'ynorm': list(postBin)},
##            'synMech': ['AMPA','NMDA'],
##            'probability': pmat[('W+AS_norm', 'PT', 'L5B')][ipost,ipre],
##            'weight': 0.01 / cfg.synsperconn, #wmat[('W+AS_norm', 'PT', 'L5B')][ipost,ipre] * cfg.EEGain / cfg.synsperconn, 
##            'synMechWeightFactor': cfg.synWeightFractionEE,
##            'delay': 'defaultDelay+dist_3D/propVelocity',
##            'synsPerConn': cfg.synsperconn,
##            'sec': 'spiny'}
