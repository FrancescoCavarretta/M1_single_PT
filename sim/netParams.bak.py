
"""
netParams.py 

High-level specifications for M1 network model using NetPyNE

Contributors: salvadordura@gmail.com
"""

def create_syn_inputs(netParams, pre_name, post_section, n, rate, noise, start, weight, delay, syn_receptor, syn_weight_fraction=None, pulses=list(), syn_per_conn=5):
    netParams.popParams[pre_name] = {
        'cellModel': 'VecStim',
        'rate': rate,
        'noise': noise,
        'start': start,
        'pulses': pulses,
        'numCells': n }
    
    netParams.connParams['%s->PT5B_full' % pre_name] = {
        'preConds': {'pop': pre_name},
        'postConds': {'cellType': 'PT'},
        'synMech': syn_receptor,
        'weight': weight,
        'delay': delay,
        'synsPerConn': syn_per_conn,
        'synMechWeightFactor': syn_weight_fraction,
        'sec': post_section}
    

from netpyne import specs
import pickle, json

netParams = specs.NetParams()   # object of class NetParams to store the network parameters

netParams.version = 56

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg

from math import ceil

#------------------------------------------------------------------------------
#
# NETWORK PARAMETERS
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# General network parameters
#------------------------------------------------------------------------------
netParams.scale = cfg.scale # Scale factor for number of cells
netParams.sizeX = cfg.sizeX # x-dimension (horizontal length) size in um
netParams.sizeY = cfg.sizeY # y-dimension (vertical height or cortical depth) size in um
netParams.sizeZ = cfg.sizeZ # z-dimension (horizontal depth) size in um
netParams.shape = 'cylinder' # cylindrical (column-like) volume

#------------------------------------------------------------------------------
# General connectivity parameters
#------------------------------------------------------------------------------
netParams.defaultThreshold = 0.0 # spike threshold, 10 mV is NetCon default, lower it for all cells
netParams.defaultDelay = 2.0 # default conn delay (ms)
netParams.propVelocity = 500.0 # propagation velocity (um/ms)
netParams.probLambda = 100.0  # length constant (lambda) for connection probability decay (um)
netParams.defineCellShapes = True  # convert stylized geoms to 3d points

#------------------------------------------------------------------------------
# Cell parameters
#------------------------------------------------------------------------------
layer = {'1':[0.0, 0.1], '2/3': [0.1,0.37], '5A': [0.37,0.47], '24':[0.1,0.37], '5B': [0.47,0.8], '6': [0.8,1.0], 
'longTPO': [2.0,2.1], 'longTVL': [2.1,2.2], 'longS1': [2.2,2.3], 'longS2': [2.3,2.4], 'longcM1': [2.4,2.5], 'longM2': [2.5,2.6], 'longOC': [2.6,2.7]}  # normalized layer boundaries

netParams.correctBorder = {'threshold': [cfg.correctBorderThreshold, cfg.correctBorderThreshold, cfg.correctBorderThreshold, cfg.correctBorderThreshold], 
                        'yborders': [layer['1'][0], layer['2/3'][0], layer['5A'][0], layer['6'][0], layer['6'][1]]}  # correct conn border effect



cellRule = netParams.importCellParams(label='PT5B_full', conds={'cellType': 'PT', 'cellModel': 'HH_full'}, fileName='cells/PTcell.hoc', cellName='PTcell', somaAtOrigin=True)

netParams.addCellParamsSecList(label='PT5B_full', secListName='perisom', somaDist=[0, 50])  # sections within 50 um of soma
netParams.addCellParamsSecList(label='PT5B_full', secListName='below_soma', somaDistY=[-600, 0])  # sections within 0-300 um of soma
netParams.addCellParamsSecList(label='PT5B_full', secListName='tuftdenddend', somaDistY=[465, 100])  # sections within 0-300 um of soma

nonSpiny = ['apic_0', 'apic_1']

for sec in nonSpiny:
  cellRule['secLists']['perisom'].remove(sec)
  
cellRule['secLists']['alldend'] = [sec for sec in cellRule.secs if ('dend' in sec or 'apic' in sec)] # basal+apical
cellRule['secLists']['apicdend'] = [sec for sec in cellRule.secs if ('apic' in sec)] # apical
cellRule['secLists']['spiny'] = [sec for sec in cellRule['secLists']['alldend'] if sec not in  nonSpiny]


#------------------------------------------------------------------------------
## load densities
with open('cells/cellDensity.pkl', 'rb') as fileObj: density = pickle.load(fileObj)['density']

## Local populations
noise = cfg.noiseShort
start = cfg.startShort

## Intracortical inputs
shortPops = [('ENGF', '1', 0.33, ('M1','I'), 0),
##             ('IT2/3', '2/3', 1, ('M1','E'), 0),
##             ('SOM2/3', '2/3', 1, ('M1','SOM'), 5),
##             ('PV2/3', '2/3', 1, ('M1','PV'), 5),
##             ('IT5A', '5A', 1, ('M1','E'), 2), 
##             ('SOM5A', '5A', 1, ('M1','SOM'), 2),
##             ('PV5A', '5A', 1, ('M1','PV'), 2),
##             ('IT5B', '5B', 0.5, ('M1','E'), 3),
##             ('PT5B', '5B', 0.5, ('M1','E'), 3),
##             ('SOM5B', '5B', 1, ('M1','SOM'), 3), 
##             ('PV5B', '5B', 1, ('M1','PV'), 3),
##             ('IT6', '6', 1, ('M1','E'), 4),
##             ('SOM6', '6', 1, ('M1','SOM'), 4),
##             ('PV6', '6', 1, ('M1','PV'), 4)
             ]

from math import pi
columnHeight = 1350.0
columnRadius = 500.0


def get_n_neurons(dens, height, radius, round_off_flag=False):
    vol = height * pi * (radius ** 2)
    n = vol * dens * 1e-9
    return round(n) if round_off_flag else n




## create populations with fixed 
for popName, popLayer, scaleFactor, popKey1, popKey2 in shortPops:
    print(popName, get_n_neurons(scaleFactor * density[popKey1][popKey2], (layer[popLayer][1] - layer[popLayer][0]) * columnHeight, columnRadius))
    #netParams.popParams[popName] = {'cellModel': 'VecStim', 'rate': cfg.ratesShort[popName], 'noise': noise, 'start': start, 'pulses': [], 'ynormRange': layer[popLayer], 'density': scaleFactor*density[popKey1][popKey2]}

netParams.popParams['PT5B_full'] =   {'cellModel': 'HH_full', 'cellType': 'PT', 'numCells':1, 'ynormRange': layer['5B']}

#------------------------------------------------------------------------------
## Long-range input populations (VecStims)
## load experimentally based parameters for long range inputs
with open('conn/conn_long.pkl', 'rb') as fileObj: connLongData = pickle.load(fileObj)
#ratesLong = connLongData['rates']

numCells = cfg.numCellsLong
noise = cfg.noiseLong
start = cfg.startLong

longPops = [] #'TPO', 'TVL', 'S1', 'S2', 'cM1', 'M2', 'OC']
## create populations with fixed 
for longPop in longPops:
    netParams.popParams[longPop] = {'cellModel': 'VecStim', 'numCells': numCells, 'rate': cfg.ratesLong[longPop], 
                                    'noise': noise, 'start': start, 'pulses': [], 'ynormRange': layer['long'+longPop]}
    if isinstance(cfg.ratesLong[longPop], str): # filename to load spikes from
        spikesFile = cfg.ratesLong[longPop]
        with open(spikesFile, 'r') as f: spks = json.load(f)
        netParams.popParams[longPop].pop('rate')
        netParams.popParams[longPop]['spkTimes'] = spks


#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------
netParams.synMechParams['NMDA'] = {'mod': 'MyExp2SynNMDABB', 'tau1NMDA': 15, 'tau2NMDA': 150, 'e': 0}
netParams.synMechParams['AMPA'] = {'mod':'MyExp2SynBB', 'tau1': 0.05, 'tau2': 5.3*cfg.AMPATau2Factor, 'e': 0}
netParams.synMechParams['GABAB'] = {'mod':'MyExp2SynBB', 'tau1': 3.5, 'tau2': 260.9, 'e': -93} 
netParams.synMechParams['GABAA'] = {'mod':'MyExp2SynBB', 'tau1': 0.07, 'tau2': 18.2, 'e': -80}
netParams.synMechParams['GABAASlow'] = {'mod': 'MyExp2SynBB','tau1': 2, 'tau2': 100, 'e': -80}
netParams.synMechParams['GABAASlowSlow'] = {'mod': 'MyExp2SynBB', 'tau1': 200, 'tau2': 400, 'e': -80}



#------------------------------------------------------------------------------
# Local connectivity parameters
#------------------------------------------------------------------------------
with open('conn/conn.pkl', 'rb') as fileObj: connData = pickle.load(fileObj)
pmat = connData['pmat']
wmat = connData['wmat']
bins = connData['bins']
#import conn_param
# pmat = conn_param.pmat
# wmat = conn_param.wmat
# bins = conn_param.bins

#------------------------------------------------------------------------------
## E -> E
for ipre, preBin in enumerate(bins['AS']):
    for ipost, postBin in enumerate(bins[('W+AS', 'PT', 'L5B')]):
        netParams.connParams['IT->PT5B_full[%d,%d]' % (ipre, ipost)] = { 
            'preConds': {'pop': ['IT2/3/3','IT4','IT5A','IT5B','PT5B','IT6'], 'ynorm': list(preBin)}, 
            'postConds': {'cellModel': 'HH_full', 'cellType': 'PT', 'ynorm': list(postBin)},
            'synMech': ['AMPA','NMDA'],
            'probability': pmat[('W+AS_norm', 'PT', 'L5B')][ipost,ipre],
            'weight': wmat[('W+AS_norm', 'PT', 'L5B')][ipost,ipre] * cfg.EEGain / cfg.synsperconn, 
            'synMechWeightFactor': cfg.synWeightFractionEE,
            'delay': 'defaultDelay+dist_3D/propVelocity',
            'synsPerConn': cfg.synsperconn,
            'sec': 'spiny'}
            




#------------------------------------------------------------------------------
# Local, intralaminar only; all-to-all but distance-based; high weights; L5A/B->L5A/B
prePopTypes = ['ENGF', 'SOM2/3','SOM5A', 'SOM5B', 'SOM6', 'PV2/3','PV5A', 'PV5B', 'PV6']
ynorms = [layer['1']] + [layer['2/3'], layer['5A'], layer['5B'], layer['6']] * 2

netParams.probLambda = 200
for i,(prePop, ynorm) in enumerate(zip(prePopTypes, ynorms)):
    if prePop.startswith('PV'):     # PV->E
        synMech = ['GABAA']
        sec = 'perisom'
        synWeightFraction = None
        probability = '1.0 * exp(-dist_3D_border/probLambda)'
    elif prePop.startswith('SOM'):  # SOM->E
        synMech = ['GABAASlow','GABAB']
        sec = 'spiny'
        synWeightFraction = cfg.synWeightFractionSOME
        probability = '1.0 * exp(-dist_3D_border/probLambda)'
    elif prePop.startswith('ENGF'):  # EBGF->E
        synMech = ['GABAASlow','GABAB']
        sec = 'tuftdend'
        synWeightFraction = cfg.synWeightFractionSOME
        probability = 0.0043
    else:
      continue

    netParams.connParams['%s->PT5B_full' % prePop] = {
        'preConds': {'pop': prePop, 'ynorm': ynorm},
        'postConds': {'cellModel': 'HH_full', 'cellType': 'PT', 'ynorm': layer['5B']},
        'synMech': synMech,
        'probability': probability,
        'weight': 1.0 / cfg.synsperconn,
        'delay': 'defaultDelay+dist_3D_border/propVelocity',
        'synsPerConn': cfg.synsperconn,
        'synMechWeightFactor': synWeightFraction,
        'sec': sec}

## ENGF inputs

    
#------------------------------------------------------------------------------
# Long-range  connectivity parameters
#------------------------------------------------------------------------------
# load load experimentally based parameters for long range inputs
cmatLong = connLongData['cmat']
binsLong = connLongData['bins']
longPops = ['TVL', 'S1', 'S2', 'cM1', 'M2'] #['TPO', 'TVL', 'S1', 'S2', 'cM1', 'M2', 'OC']

for longPop in longPops:
            for i, (binRange, convergence) in enumerate(zip(binsLong[(longPop, 'PT')], cmatLong[(longPop, 'PT', 'exc')])):
                netParams.connParams['%s[%s]->PT5B_full[%d]' % (longPop, 'exc', i)] = { 
                    'preConds': {'pop': longPop}, 
                    'postConds': {'cellModel': 'HH_full', 'cellType': 'PT', 'ynorm': list(binRange)},
                    'synMech': ['AMPA', 'NMDA'],
                    'convergence': convergence,
                    'weight': cfg.weightLong / cfg.synsperconn, 
                    'synMechWeightFactor': cfg.synWeightFractionEE,
                    'delay': 'defaultDelay+dist_3D/propVelocity',
                    'synsPerConn': cfg.synsperconn,
                    'sec': 'spiny'}


#------------------------------------------------------------------------------
# Subcellular connectivity (synaptic distributions)
#------------------------------------------------------------------------------         
with open('conn/conn_dend_PT.json', 'r') as fileObj: connDendPTData = json.load(fileObj)
##with open('conn/conn_dend_IT.json', 'r') as fileObj: connDendITData = json.load(fileObj)

#------------------------------------------------------------------------------
# L2/3,TVL,S2,cM1,M2 -> PT (Suter, 2015)
synDens, gridY, fixedSomaY = connDendPTData['synDens'], connDendPTData['gridY'], connDendPTData['fixedSomaY']

for k in synDens.keys():
    prePop,postType = k.split('_')  # eg. split 'M2_PT'

    if postType == 'PT':
        if prePop == 'L2':
            prePop = 'IT2/3'  # include conns from layer 2/3 and 4
        
        netParams.subConnParams['%s->PT5B_full' % prePop] = {
        'preConds': {'pop': prePop}, 
        'postConds': {'cellType': postType},  
        'sec': 'spiny',
        'groupSynMechs': ['AMPA', 'NMDA'], 
        'density': {'type': '1Dmap', 'gridX': None, 'gridY': gridY[k], 'gridValues': synDens[k], 'fixedSomaY': fixedSomaY}} 


###------------------------------------------------------------------------------
### TPO, TVL, M2, OC  -> E (L2/3, L5A, L5B, L6) (Hooks 2013)
##synDens, gridY, fixedSomaY = connDendITData['synDens'], connDendITData['gridY'], connDendITData['fixedSomaY']
##for k in synDens.keys():
##    prePop,post = k.split('_')  # eg. split 'M2_L2'
##
##    if prePop in ['OC','TPO']:
##        postyRange = list(layer[post.split('L')[1]]) # get layer yfrac range 
##        if post == 'L2': postyRange[1] = layer['4'][1]  # apply L2 rule also to L4 
##        netParams.subConnParams['%s->PT5B_full' % prePop] = {
##        'preConds': {'pop': prePop}, 
##        'postConds': {'ynorm': postyRange , 'cellType': 'PT'},  
##        'sec': 'spiny',
##        'groupSynMechs': ['AMPA', 'NMDA'], 
##        'density': {'type': '1Dmap', 'gridX': None, 'gridY': gridY, 'gridValues': synDens[k], 'fixedSomaY': fixedSomaY}} 


#------------------------------------------------------------------------------
# rest of local E->E (exclude IT2/3->PT); uniform distribution over spiny      
netParams.subConnParams['IT5/6->PT5B_full'] = {
    'preConds': {'pop': ['IT4','IT5A','IT5B','PT5B','IT6']}, 
    'postConds': {'cellType': 'PT'},
    'sec': 'spiny',
    'groupSynMechs': ['AMPA', 'NMDA'], 
    'density': 'uniform'}

#------------------------------------------------------------------------------
# ENGF->E; perisomatic (no sCRACM)
netParams.subConnParams['ENGF->PT5B_full'] = {
    'preConds': {'pop': 'ENGF'}, 
    'postConds': {'cellType': 'PT'},  
    'sec': 'tuftdend', 
    'density': 'uniform'} 

#------------------------------------------------------------------------------
# PV->E; perisomatic (no sCRACM)
netParams.subConnParams['PV->PT5B_full'] = {
    'preConds': {'pop': ['PV2/3','PV5A', 'PV5B', 'PV6']}, 
    'postConds': {'cellType': 'PT'},  
    'sec': 'perisom', 
    'density': 'uniform'} 


#------------------------------------------------------------------------------
# SOM->E; apical dendrites (no sCRACM)
netParams.subConnParams['SOM->PT5B_full'] = {
    'preConds': {'pop': ['SOM2/3','SOM5A', 'SOM5B', 'SOM6']}, 
    'postConds': {'cellType': 'PT'},  
    'sec': 'apicdend',
    'groupSynMechs': ['GABAASlow','GABAB'],
    'density': 'uniform'} 



#------------------------------------------------------------------------------
# Description
#------------------------------------------------------------------------------
netParams.description = """ 
- M1 net, 6 layers, 7 cell types 
- NCD-based connectivity from  Weiler et al. 2008; Anderson et al. 2010; Kiritani et al. 2012; 
  Yamawaki & Shepherd 2015; Apicella et al. 2012
- Parametrized version based on Sam's code
- Updated cell models and mod files
- Added parametrized current inputs
- Fixed bug: prev was using cell models in /usr/site/nrniv/local/python/ instead of cells 
- Use 5 synsperconn for 5-comp cells (HH_reduced); and 1 for 1-comp cells (HH_simple)
- Fixed bug: made global h params separate for each cell model
- Fixed v_init for different cell models
- New IT cell with same geom as PT
- Cleaned cfg and moved background inputs here
- Set EIGain and IEGain for each inh cell type
- Added secLists for PT full
- Fixed reduced CT (wrong vinit and file)
- Added subcellular conn rules to distribute synapses
- PT full model soma centered at 0,0,0 
- Set cfg seeds here to ensure they get updated
- Added PVSOMGain and SOMPVGain
- PT subcellular distribution as a cfg param
- Cylindrical volume
- DefaultDelay (for local conns) = 2ms
- Added long range connections based on Yamawaki 2015a,b; Suter 2015; Hooks 2013; Meyer 2011
- Updated cell densities based on Tsai 2009; Lefort 2009; Katz 2011; Wall 2016; 
- Separated PV and SOM of L5A vs L5B
- Fixed bugs in local conn (PT, PV5, SOM5, L6)
- Added perisom secList including all sections 50um from soma
- Added subcellular conn rules (for both full and reduced models)
- Improved cell models, including PV and SOM fI curves
- Improved subcell conn rules based on data from Suter15, Hooks13 and others
- Adapted Bdend L of reduced cell models
- Made long pop rates a cfg param
- Set threshold to 0.0 mV
- Parametrized I->E/I layer weights
- Added missing subconn rules (IT6->PT; S1,S2,cM1->IT/CT; long->SOM/PV)
- Added threshold to weightNorm (PT threshold=10x)
- weightNorm threshold as a cfg parameter
- Separate PV->SOM, SOM->PV, SOM->SOM, PV->PV gains 
- Conn changes: reduced IT2/3->IT4, IT5B->CT6, IT5B,6->IT2/3,4,5A, IT2/3,4,5A,6->IT5B; increased CT->PV6+SOM6
- Parametrized PT ih gbar
- Added IFullGain parameter: I->E gain for full detailed cell models
- Replace PT ih with Migliore 2012
- Parametrized ihGbar, ihGbarBasal, dendNa, axonNa, axonRa, removeNa
- Replaced cfg list params with dicts
- Parametrized ihLkcBasal and AMPATau2Factor
- Fixed synMechWeightFactor
- Parametrized PT ih slope
- Added disynapticBias to I->E (Yamawaki&Shepherd,2015)
- Fixed E->CT bin 0.9-1.0
- Replaced GABAB with exp2syn and adapted synMech ratios
- Parametrized somaNa
- Added ynorm condition to NetStims
- Added option to play back recorded spikes into long-range inputs
- Fixed Bdend pt3d y location
- Added netParams.convertCellShapes = True to convert stylized geoms to 3d points
- New layer boundaries, cell densities, conn, FS+SOM L4 grouped with L2/3, low cortical input to L4
- Increased exc->L4 based on Yamawaki 2015 fig 5
- v54: Moved from NetPyNE v0.7.9 to v0.9.1 (v54_batch1-6)
- v54: Moved to NetPyNE v0.9.1 and py3 (v54_batch7 onwards)
- v56: Reduced dt from 0.05 to 0.025 (note this version follows from v54, i.e. without new cell types; branch 'paper2019_py3')
- v56: (included in prev version): Added cfg.KgbarFactor
"""

if __name__ == '__main__':
    print(len(netParams.connParams))
    print(len(netParams.subConnParams))
    print(cellRule['secLists'])
