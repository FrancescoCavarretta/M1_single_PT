from netpyne import specs
import pickle, json
import numpy as np
import mk_spike_trains as mkst

netParams = specs.NetParams()

netParams.version = 56

from cfg import cfg, args


#------------------------------------------------------------------------------
# General connectivity parameters
#------------------------------------------------------------------------------
netParams.defaultThreshold = 0.0 # spike threshold, 10 mV is NetCon default, lower it for all cells
netParams.defaultDelay = 2.0 # default conn delay (ms)
netParams.propVelocity = 500.0 # propagation velocity (um/ms)
netParams.probLambda = 200  # length constant (lambda) for connection probability decay (um)
netParams.defineCellShapes = True  # convert stylized geoms to 3d points

#------------------------------------------------------------------------------
# Cell parameters
#------------------------------------------------------------------------------
pt_cell_filename = 'PTcell_6OHDA.hoc' if args.parkinsonian else  'PTcell.hoc'

cellRule = netParams.importCellParams(label='PT5B_full', conds={'cellType': 'PT', 'cellModel': 'HH_full'}, fileName='cells/%s' % pt_cell_filename, cellName='PTcell', somaAtOrigin=True)

netParams.addCellParamsSecList(label='PT5B_full', secListName='perisom', somaDist=[0, 50])  # sections within 50 um of soma
netParams.addCellParamsSecList(label='PT5B_full', secListName='below_soma', somaDistY=[-600, 0])  # sections within 0-300 um of soma
netParams.addCellParamsSecList(label='PT5B_full', secListName='tuftdend', somaDistY=[465, 1000])  # sections further than 465 um of soma

netParams.addCellParamsSecList(label='PT5B_full', secListName='L1A_neurite',   somaDistY=[680, 740])  # sections further than 465 um of soma
netParams.addCellParamsSecList(label='PT5B_full', secListName='L1B_neurite',   somaDistY=[620, 680])  # sections further than 465 um of soma
netParams.addCellParamsSecList(label='PT5B_full', secListName='L1_neurite',   somaDistY=[620, 740])  # sections further than 465 um of soma
netParams.addCellParamsSecList(label='PT5B_full', secListName='L2/3/4_neurite', somaDistY=[300, 620])  # sections further than 465 um of soma

netParams.addCellParamsSecList(label='PT5B_full', secListName='L5A_neurite',  somaDistY=[190, 300])  # sections further than 465 um of soma
netParams.addCellParamsSecList(label='PT5B_full', secListName='L5B_neurite',  somaDistY=[-190, 190])  # sections further than 465 um of soma
netParams.addCellParamsSecList(label='PT5B_full', secListName='L5_neurite',  somaDistY=[-190, 300])  # sections further than 465 um of soma

netParams.addCellParamsSecList(label='PT5B_full', secListName='L6_neurite',   somaDistY=[-425, -190])  # sections further than 465 um of soma

nonSpiny = ['apic_0', 'apic_1']

for sec in nonSpiny:
  cellRule['secLists']['perisom'].remove(sec)
  
cellRule['secLists']['alldend'] = [sec for sec in cellRule.secs if ('dend' in sec or 'apic' in sec)] # basal+apical
cellRule['secLists']['apicdend'] = [sec for sec in cellRule.secs if ('apic' in sec)] # apical
cellRule['secLists']['spiny'] = [sec for sec in cellRule['secLists']['alldend'] if sec not in  nonSpiny]


#------------------------------------------------------------------------------
## Local populations
noise = cfg.noiseShort
start = cfg.startShort

## Intracortical inputs
netParams.popParams['PT5B_full'] =   {'cellModel': 'HH_full', 'cellType': 'PT', 'numCells':1}

##import numpy as np
##freq = 20.0
##vm_spktimes_template = np.arange(0.0, cfg.duration + 1000.0 / freq, 1000.0 / freq)
##burst_template = np.arange(0.0, 100.0, 1000.0 / 150)
##
##def get_vm_spktimes():
##    vm_spktimes = vm_spktimes_template + (np.random.rand(vm_spktimes_template.size) - 0.5) / 0.5 * 1000.0 / freq / 2
##    vm_spktimes = vm_spktimes[vm_spktimes > 0]
##    i_init = np.argwhere(vm_spktimes >= 500)[0, 0]
##    i_end = np.argwhere(vm_spktimes <= (vm_spktimes[i_init] + 100))[-1, 0]
##    vm_spktimes = np.concatenate((vm_spktimes[:i_init], burst_template + vm_spktimes[i_init], vm_spktimes[i_end:]))
##    return vm_spktimes

#('SOM-OTHERS', 100),




# create input populations
for popName, spktimes in mkst.gen_spike_trains().items():
    spktimes = [[1,2,3],[4,5,6]]
    netParams.popParams[popName] = {'cellModel': 'VecStim', 'numCells':len(spktimes), 'cellType':popName, 'spkTimes':spktimes}


    
##    if popName.startswith('VM'):
##        rate_var = 'VM'
##    elif popName.startswith('SOM'):
##        rate_var = 'SOM'
##    else:
##        rate_var = popName
##
##    if popName == 'VM_L1':
##        netParams.popParams[popName] = {'cellModel': 'VecStim', 'numCells':int(n), 'cellType':popName, 'spkTimes':vm_tspk[:25]}
##    elif popName == 'VM_L5':
##        netParams.popParams[popName] = {'cellModel': 'VecStim', 'numCells':int(n), 'cellType':popName, 'spkTimes':vm_tspk[25:]}
##    else:
##        netParams.popParams[popName] = {'cellModel': 'VecStim', 'numCells':int(n), 'cellType':popName, 'rate':cfg.ratesShort[rate_var], 'noise':cfg.noiseShort, 'start':cfg.startShort}



##    if popName == 'VM_L5':
##        netParams.popParams[popName].update({'pulses': [{'start': 3000, 'end': 3150, 'rate': 20, 'noise': 0}, {'start': 4000, 'end': 4150, 'rate': 20, 'noise': 0}, {'start': 5000, 'end': 5150, 'rate': 20, 'noise': 0}, {'start': 6000, 'end': 6150, 'rate': 20, 'noise': 0}]})
    
    #if popName == 'VM_L5':
    #    netParams.popParams[popName].update({'pulses': [{'start': 3000, 'end': 3150, 'rate': 35, 'noise': 0}, {'start': 4000, 'end': 4150, 'rate': 35, 'noise': 0}, {'start': 5000, 'end': 5150, 'rate': 35, 'noise': 0}, {'start': 6000, 'end': 6150, 'rate': 35, 'noise': 0}]})
    #if popName == 'IT2/3/4':
    #    netParams.popParams[popName].update(
    #        {'pulses': [{'start': 3000, 'end': 3150, 'rate': 0.6, 'noise': 0}, {'start': 4000, 'end': 4150, 'rate': 0.6, 'noise': 0}, {'start': 5000, 'end': 5150, 'rate': 0.6, 'noise': 0}, {'start': 6000, 'end': 6150, 'rate': 0.6, 'noise': 0}]})
    #if popName == 'PV':
    #    netParams.popParams[popName].update({'pulses': [{'start': 3000, 'end': 3150, 'rate': 35, 'noise': 0}, {'start': 4000, 'end': 4150, 'rate': 35, 'noise': 0}, {'start': 5000, 'end': 5150, 'rate': 35, 'noise': 0}, {'start': 6000, 'end': 6150, 'rate': 35, 'noise': 0}]})

    #if popName == 'VM_L5':
    #    netParams.popParams[popName].update({'pulses': [{'start': 3000, 'end': 3150, 'rate': 35, 'noise': 0}, {'start': 4000, 'end': 4150, 'rate': 35, 'noise': 0}, {'start': 5000, 'end': 5150, 'rate': 35, 'noise': 0}, {'start': 6000, 'end': 6150, 'rate': 35, 'noise': 0}]})
    #if popName == 'VM_L1':
    #    netParams.popParams[popName].update({'pulses': [{'start': 3000, 'end': 3150, 'rate': 250, 'noise': 0}, {'start': 4000, 'end': 4150, 'rate': 250, 'noise': 0}, {'start': 5000, 'end': 5150, 'rate': 250, 'noise': 0}, {'start': 6000, 'end': 6150, 'rate': 250, 'noise': 0}]})        
##for popName, n in [ ('ENGF', 1) ]: #, ('PT5B', 362), ('PV', 46), ]: #, ('CX', 20), ('VM_L1', 20), ('VM_L5', 20)]:
##    if popName.startswith('VM'):
##        rate_var = 'VM'
##    elif popName.startswith('SOM'):
##        rate_var = 'SOM'
##    else:
##        rate_var = popName
##    netParams.popParams[popName] = {'cellModel': 'VecStim', 'numCells':int(n), 'cellType':popName, 'rate':1, 'noise':0, 'start':2000}

#------------------------------------------------------------------------------
#### Long-range input populations (VecStims)
#### load experimentally based parameters for long range inputs
##with open('conn/conn_long.pkl', 'rb') as fileObj: connLongData = pickle.load(fileObj)
###ratesLong = connLongData['rates']
##
##numCells = cfg.numCellsLong
##noise = cfg.noiseLong
##start = cfg.startLong
##
##longPops = [] #'TPO', 'TVL', 'S1', 'S2', 'cM1', 'M2', 'OC']
#### create populations with fixed 
##for longPop in longPops:
##    netParams.popParams[longPop] = {'cellModel': 'VecStim', 'numCells': numCells, 'rate': cfg.ratesLong[longPop], 
##                                    'noise': noise, 'start': start, 'pulses': [], 'ynormRange': layer['long'+longPop]}
##    if isinstance(cfg.ratesLong[longPop], str): # filename to load spikes from
##        spikesFile = cfg.ratesLong[longPop]
##        with open(spikesFile, 'r') as f: spks = json.load(f)
##        netParams.popParams[longPop].pop('rate')
##        netParams.popParams[longPop]['spkTimes'] = spks


#------------------------------------------------------------------------------
# Synaptic mechanism parameters
#------------------------------------------------------------------------------
netParams.synMechParams['NMDA'] = {'mod': 'NMDA', 'tau1': 8.7, 'tau2': 40}
netParams.synMechParams['AMPA'] = {'mod':'AMPA', 'tau1': 0.5, 'tau2': 3.5}
netParams.synMechParams['GABAB'] = {'mod':'MySyn', 'tau1': 45.4, 'tau2': 173.2, 'e': -100} 
netParams.synMechParams['GABAA'] = {'mod':'MySyn', 'tau1': 1.2, 'tau2': 9, 'e': -85}
netParams.synMechParams['GABAASlow'] = {'mod': 'MySyn','tau1': 1.2, 'tau2': 50, 'e': -85}



#------------------------------------------------------------------------------
# Local connectivity parameters
#------------------------------------------------------------------------------
##with open('conn/conn.pkl', 'rb') as fileObj: connData = pickle.load(fileObj)
##pmat = connData['pmat']
##wmat = connData['wmat']
##bins = connData['bins']
#import conn_param
# pmat = conn_param.pmat
# wmat = conn_param.wmat
# bins = conn_param.bins

#------------------------------------------------------------------------------
## E -> E
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

##netParams.connParams['IT->PT5B_full[%d,%d]' % (0, 0)] = { 
##    'preConds': {'pop': ['IT2/3','IT4','IT5A','IT5B','PT5B','IT6']}, 
##    'postConds': {'cellModel': 'HH_full', 'cellType': 'PT'},
##    'synMech': ['AMPA','NMDA'],
##    #'probability': pmat[('W+AS_norm', 'PT', 'L5B')][ipost,ipre],
##    'weight': 0.01, #wmat[('W+AS_norm', 'PT', 'L5B')][ipost,ipre] * cfg.EEGain / cfg.synsperconn, 
##    'synMechWeightFactor': [0.485, 0.515],
##    'delay': 'defaultDelay+dist_3D/propVelocity',
##    'synsPerConn': 1, #cfg.synsperconn,
##    'sec': 'spiny'}            




#------------------------------------------------------------------------------
# Local, intralaminar only; all-to-all but distance-based; high weights; L5A/B->L5A/B
##prePopTypes = ['ENGF', 'SOM2/3','SOM5A', 'SOM5B', 'SOM6', 'PV2/3','PV5A', 'PV5B', 'PV6']
##ynorms = [layer['1']] + [layer['2/3'], layer['5A'], layer['5B'], layer['6']] * 2
##
##
##for i,(prePop, ynorm) in enumerate(zip(prePopTypes, ynorms)):
##    if prePop.startswith('PV'):     # PV->E
##        synMech = ['GABAA']
##        sec = 'perisom'
##        synWeightFraction = None
##        probability = '1.0 * exp(-dist_3D_border/probLambda)'
##        
##    elif prePop.startswith('SOM'):  # SOM->E
##        synMech = ['GABAASlow','GABAB']
##        sec = 'spiny'
##        synWeightFraction = cfg.synWeightFractionIE
##        probability = '1.0 * exp(-dist_3D_border/probLambda)'
##        
##    elif prePop.startswith('ENGF'):  # ENGF->E
##        synMech = ['GABAASlow','GABAB']
##        sec = 'tuftdend'
##        synWeightFraction = cfg.synWeightFractionIE
##        probability = 0.0043
##        
##    else:
##      continue
##
##    netParams.connParams['%s->PT5B_full' % prePop] = {
##        'preConds': {'pop': prePop, 'ynorm': ynorm},
##        'postConds': {'cellModel': 'HH_full', 'cellType': 'PT', 'ynorm': layer['5B']},
##        'synMech': synMech,
##        'probability': probability,
##        'weight': 0.15 / cfg.synsperconn,
##        'delay': 'defaultDelay+dist_3D_border/propVelocity',
##        'synsPerConn': cfg.synsperconn,
##        'synMechWeightFactor': synWeightFraction,
##        'sec': sec}


# Local, intralaminar only; all-to-all but distance-based; high weights; L5A/B->L5A/B
prePopTypes = {
    'ENGF':{
        'synMech':['GABAASlow','GABAB'],
        'sec':'L1_neurite',
        'synMechWeightFactor':cfg.synWeightFractionIE,\
        },
    'SOM-T':{
        'synMech':['GABAASlow','GABAB'],
        'sec':'L1_neurite',
        'synMechWeightFactor':cfg.synWeightFractionIE,\
        },
    'SOM-FO':{
        'synMech':['GABAASlow','GABAB'],
        'sec':'L2/3/4_neurite',
        'synMechWeightFactor':cfg.synWeightFractionIE,\
        },
    'SOM-NMC':{
        'synMech':['GABAASlow','GABAB'],
        'sec':'L2/3/4_neurite',
        'synMechWeightFactor':cfg.synWeightFractionIE,
        },
    'PV':{
        'synMech':['GABAA'],
        'sec':'perisom',
        'synMechWeightFactor':None,
        },
    'IT2/3/4':{ 
        'preConds': {'pop': ['IT2/3/4']}, 
        'postConds': {'cellModel': 'HH_full', 'cellType': 'PT'},
        'synMech': ['AMPA','NMDA'],
        'synMechWeightFactor': cfg.synWeightFractionEE,
        'sec': 'spiny'
        },
    'IT6':{ 
        'preConds': {'pop': ['IT6']}, 
        'postConds': {'cellModel': 'HH_full', 'cellType': 'PT'},
        'synMech': ['AMPA','NMDA'],
        'synMechWeightFactor': cfg.synWeightFractionEE,
        'sec': 'spiny'
        },
    'IT5':{ 
        'preConds': {'pop': ['IT5']}, 
        'postConds': {'cellModel': 'HH_full', 'cellType': 'PT'},
        'synMech': ['AMPA','NMDA'],
        'synMechWeightFactor': cfg.synWeightFractionEE,
        'sec': 'spiny'
        },
    'PT5B':{ 
        'preConds': {'pop': ['PT5B']}, 
        'postConds': {'cellModel': 'HH_full', 'cellType': 'PT'},
        'synMech': ['AMPA','NMDA'],
        'synMechWeightFactor': cfg.synWeightFractionEE,
        'sec': 'spiny'
        },
    'CX':{ 
        'synMech': ['AMPA','NMDA'],
        'synMechWeightFactor': cfg.synWeightFractionEE,
        'sec': 'spiny'
        },
    'SOM-OTHERS':{
        'synMech':['GABAASlow','GABAB'],
        'sec':'L5_neurite',
        'synMechWeightFactor':cfg.synWeightFractionIE,
        },
    'VM_L1':{ 
        'synMech': ['AMPA','NMDA'],
        'synMechWeightFactor': cfg.synWeightFractionEE,
        'sec': 'L1_neurite'
        },
    'VM_L5':{ 
        'synMech': ['AMPA','NMDA'],
        'synMechWeightFactor': cfg.synWeightFractionEE,
        'sec': 'L5_neurite'
        }
    }

for prePop, pars in prePopTypes.items():
    if prePop in cfg.g:
        netParams.connParams['%s->PT5B_full' % prePop] = {
            'preConds': {'pop': prePop},
            'postConds': {'cellModel': 'HH_full', 'cellType': 'PT'},
            'synsPerConn':1,
            'loc':None,
            'weight': cfg.g[prePop], 
            }
        
        netParams.connParams['%s->PT5B_full' % prePop].update(pars)
    




    
###------------------------------------------------------------------------------
### Long-range  connectivity parameters
###------------------------------------------------------------------------------
### load load experimentally based parameters for long range inputs
##cmatLong = connLongData['cmat']
##binsLong = connLongData['bins']
##longPops = [] #'TVL', 'S1', 'S2', 'cM1', 'M2'] #['TPO', 'TVL', 'S1', 'S2', 'cM1', 'M2', 'OC']
##
##for longPop in longPops:
##            for i, (binRange, convergence) in enumerate(zip(binsLong[(longPop, 'PT')], cmatLong[(longPop, 'PT', 'exc')])):
##                netParams.connParams['%s[%s]->PT5B_full[%d]' % (longPop, 'exc', i)] = { 
##                    'preConds': {'pop': longPop}, 
##                    'postConds': {'cellModel': 'HH_full', 'cellType': 'PT', 'ynorm': list(binRange)},
##                    'synMech': ['AMPA', 'NMDA'],
##                    'convergence': convergence,
##                    'weight': cfg.weightLong / cfg.synsperconn, 
##                    'synMechWeightFactor': cfg.synWeightFractionEE,
##                    'delay': 'defaultDelay+dist_3D/propVelocity',
##                    'synsPerConn': cfg.synsperconn,
##                    'sec': 'spiny'}


#------------------------------------------------------------------------------
# Subcellular connectivity (synaptic distributions)
#------------------------------------------------------------------------------         
with open('conn/conn_dend_PT.json', 'r') as fileObj:
    connDendPTData = json.load(fileObj)
##with open('conn/conn_dend_IT.json', 'r') as fileObj: connDendITData = json.load(fileObj)

#------------------------------------------------------------------------------
# L2/3,TVL,S2,cM1,M2 -> PT (Suter, 2015)
synDens, gridY, fixedSomaY = connDendPTData['synDens'], connDendPTData['gridY'], connDendPTData['fixedSomaY']

netParams.subConnParams['IT2/3/4->PT5B_full'] = {
    'preConds': {'pop': 'IT2/3/4'},
    'postConds': {'cellType': 'PT'},
    'sec': 'spiny',
    'groupSynMechs': ['AMPA', 'NMDA'],
    'density': {'type': '1Dmap', 'gridX': None, 'gridY': gridY['L2_PT'], 'gridValues': synDens['L2_PT'], 'fixedSomaY': fixedSomaY}}
        
##for k in synDens.keys():
##    prePop,postType = k.split('_')  # eg. split 'M2_PT'
##
##    if postType == 'PT':
##        if prePop == 'L2':
##            prePop = 'IT2/3'  # include conns from layer 2/3 and 4
##        
##        netParams.subConnParams['%s->PT5B_full' % prePop] = {
##        'preConds': {'pop': prePop}, 
##        'postConds': {'cellType': postType},  
##        'sec': 'spiny',
##        'groupSynMechs': ['AMPA', 'NMDA'], 
##        'density': {'type': '1Dmap', 'gridX': None, 'gridY': gridY[k], 'gridValues': synDens[k], 'fixedSomaY': fixedSomaY}} 


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
netParams.subConnParams['IT5->PT5B_full'] = {
    'preConds': {'pop': 'IT5'}, 
    'postConds': {'cellType': 'PT'},
    'sec': 'L5_neurite',
    'groupSynMechs': ['AMPA', 'NMDA'], 
    'density': 'uniform'}

netParams.subConnParams['PT5B->PT5B_full'] = {
    'preConds': {'pop': 'PT5B'}, 
    'postConds': {'cellType': 'PT'},
    'sec': 'L5_neurite',
    'groupSynMechs': ['AMPA', 'NMDA'], 
    'density': 'uniform'}

netParams.subConnParams['IT6->PT5B_full'] = {
    'preConds': {'pop': 'IT6'}, 
    'postConds': {'cellType': 'PT'},
    'sec': 'L1_neurite',
    'groupSynMechs': ['AMPA', 'NMDA'], 
    'density': 'uniform'}

netParams.subConnParams['ENGF->PT5B_full'] = {
    'preConds': {'pop': 'ENGF'}, 
    'postConds': {'cellType': 'PT'},  
    'sec': 'L1_neurite', 
    'groupSynMechs': ['GABAASlow','GABAB'],
    'density': 'uniform'}

netParams.subConnParams['PV->PT5B_full'] = {
    'preConds': {'pop': ['PV']}, 
    'postConds': {'cellType': 'PT'},  
    'sec': 'perisom', 
    'density': 'uniform'} 

netParams.subConnParams['SOM-T->PT5B_full'] = {
    'preConds': {'pop': ['SOM-T']}, 
    'postConds': {'cellType': 'PT'},  
    'sec': 'L1_neurite',
    'groupSynMechs': ['GABAASlow','GABAB'],
    'density': 'uniform'}

netParams.subConnParams['SOM-FO&NMC->PT5B_full'] = {
    'preConds': {'pop': ['SOM-FO', 'SOM-NMC']}, 
    'postConds': {'cellType': 'PT'},  
    'sec': 'L2/3/4_neurite',
    'groupSynMechs': ['GABAASlow','GABAB'],
    'density': 'uniform'}

netParams.subConnParams['SOM-OTHERS->PT5B_full'] = {
    'preConds': {'pop':'SOM-OTHERS'}, 
    'postConds': {'cellType': 'PT'},  
    'sec': 'L5_neurite',
    'groupSynMechs': ['GABAASlow','GABAB'],
    'density': 'uniform'}

netParams.subConnParams['CX->PT5B_full'] = {
    'preConds': {'pop': 'CX'}, 
    'postConds': {'cellType': 'PT'},  
    'sec': 'spiny', 
    'groupSynMechs': ['AMPA', 'NMDA'],
    'density': 'uniform'}

netParams.subConnParams['VM_L1->PT5B_full'] = {
    'preConds': {'pop': 'VM_L1'}, 
    'postConds': {'cellType': 'PT'},  
    'sec': 'L1_neurite', 
    'groupSynMechs': ['AMPA', 'NMDA'],
    'density': 'uniform'}

netParams.subConnParams['VM_L5->PT5B_full'] = {
    'preConds': {'pop': 'VM_L5'}, 
    'postConds': {'cellType': 'PT'},  
    'sec': 'L5_neurite', 
    'groupSynMechs': ['AMPA', 'NMDA'],
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
    pass
    #print(len(netParams.connParams))
    #print(len(netParams.subConnParams))
    #print(cellRule['secLists'])
