"""
cfg.py 

Simulation configuration for M1 model (using NetPyNE)

Contributors: salvadordura@gmail.com
"""

from netpyne import specs
import pickle

cfg = specs.SimConfig()  

#------------------------------------------------------------------------------
#
# SIMULATION CONFIGURATION
#
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
cfg.duration = 1*1e3 
cfg.dt = 0.025
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 34, 'v_init': -80}  
cfg.verbose = 0
cfg.createNEURONObj = 1
cfg.createPyStruct = 1
cfg.connRandomSecFromList = False  # set to false for reproducibility 
cfg.cvode_active = False
cfg.cvode_atol = 1e-6
cfg.cache_efficient = True
cfg.printRunTime = 0.1
cfg.oneSynPerNetcon = True  # only affects conns not in subconnParams; produces identical results

cfg.includeParamsLabel = False #True # needed for modify synMech False
cfg.printPopAvgRates = [1000., 5000.]

cfg.checkErrors = False

cfg.saveInterval = 100 # define how often the data is saved, this can be used with interval run if you want to update the weights more often than you save
cfg.intervalFolder = 'interval_saving'


#------------------------------------------------------------------------------
# Recording 
#------------------------------------------------------------------------------
allpops = ['PT5B_full']

cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc':0.5, 'var':'v'}}#,
					#'V_soma_ih': {'sec':'soma', 'loc':0.5, 'var':'gbar', 'mech':'hd', 'conds':{'pop': 'PT5B'}}}
					# 'V_apic_26': {'sec':'apic_26', 'loc':0.5, 'var':'v', 'conds':{'pop': 'PT5B'}},
					# 'V_dend_5': {'sec':'dend_5', 'loc':0.5, 'var':'v', 'conds':{'pop': 'PT5B'}}}
					#'I_AMPA_Adend2': {'sec':'Adend2', 'loc':0.5, 'synMech': 'AMPA', 'var': 'i'}}

cfg.recordLFP = [[150, y, 150] for y in range(200,1300,100)] # [[150, y, 150] for y in range(200,1300,100)]

cfg.saveLFPPops =  False # allpops 

cfg.recordDipoles = False # {'L2': ['IT2'], 'L4': ['IT4'], 'L5': ['IT5A', 'IT5B', 'PT5B']}

cfg.recordStim = False
cfg.recordTime = False  
cfg.recordStep = 0.025


#------------------------------------------------------------------------------
# Saving
#------------------------------------------------------------------------------
cfg.simLabel = 'v56_tune3'
cfg.saveFolder = '../data/v56_manualTune'
cfg.savePickle = True
cfg.saveJson = False
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams']#, 'net']
cfg.backupCfgFile = None #['cfg.py', 'backupcfg/'] 
cfg.gatherOnlySimData = False
cfg.saveCellSecs = False
cfg.saveCellConns = False
cfg.compactConnFormat = 0

#------------------------------------------------------------------------------
# Analysis and plotting 
#------------------------------------------------------------------------------
with open('cells/popColors.pkl', 'rb') as fileObj: popColors = pickle.load(fileObj)['popColors']

cfg.analysis['plotRaster'] = {'include': allpops, 'orderBy': ['pop', 'y'], 'timeRange': [0, cfg.duration], 'saveFig': True, 'showFig': False, 'popRates': True, 'orderInverse': True, 'popColors': popColors, 'figSize': (12,10), 'lw': 0.3, 'markerSize':3, 'marker': '.', 'dpi': 300} 


cfg.analysis['plotLFP'] = {'plots': ['timeSeries'], 'electrodes': list(range(len(cfg.recordLFP))), 'figSize': (12,10), 'timeRange': [1000,5000],  'saveFig': True, 'showFig':False} 


cfg.analysis['plotTraces'] = {'include': [], 'timeRange': [0, cfg.duration], 'oneFigPer': 'trace', 'figSize': (10,4), 'saveFig': True, 'showFig': False} 



#------------------------------------------------------------------------------
# Synapses
#------------------------------------------------------------------------------
cfg.synWeightFractionEE = [0.5, 0.5] # E->E AMPA to NMDA ratio
cfg.synWeightFractionSOME = [0.9, 0.1] # SOM -> E GABAASlow to GABAB ratio

cfg.synsperconn = 5
cfg.AMPATau2Factor = 1.0

#------------------------------------------------------------------------------
# Network 
#------------------------------------------------------------------------------
cfg.weightNorm = 1  # use weight normalization
cfg.weightNormThreshold = 4.0  # weight normalization factor threshold

cfg.scale = 0.3
cfg.sizeY = 1350.0
cfg.sizeX = 300.0
cfg.sizeZ = 300.0
cfg.correctBorderThreshold = 150.0

cfg.L5BrecurrentFactor = 1.0
cfg.ITinterFactor = 1.0
cfg.strengthFactor = 1.0

cfg.EEGain = 0.5

cfg.IEdisynapticBias = None  # increase prob of I->Ey conns if Ex->I and Ex->Ey exist 

#------------------------------------------------------------------------------
## I->E gains
cfg.PVEGain = 1.0
cfg.SOMEGain = 1.0
cfg.IEGain = (cfg.PVEGain+cfg.SOMEGain)/2.0

#------------------------------------------------------------------------------
## I->E/I layer weights (L2/3+4, L5, L6)
cfg.IEweights = [0.8, 0.8, 1.0]

cfg.IPTGain = 1.0
cfg.IFullGain = 1.0

#------------------------------------------------------------------------------
# Long range inputs
#------------------------------------------------------------------------------
cfg.numCellsLong = 1000 # num of cells per population
cfg.noiseLong = 1.0  # firing rate random noise
cfg.delayLong = 5.0  # (ms)
cfg.weightLong = 0.5  # corresponds to unitary connection somatic EPSP (mV)
cfg.startLong = 0  # start at 0 ms
cfg.ratesLong = {'TPO': [0,5], 'TVL': [0,2.5], 'S1': [0,5], 'S2': [0,5], 'cM1': [0,2.5], 'M2': [0,2.5], 'OC': [0,5]}

#------------------------------------------------------------------------------
# Short range inputs i.e. intracortical
#------------------------------------------------------------------------------
cfg.noiseShort = 1.0  # firing rate random noise
cfg.delayShort = 5.0  # (ms)
cfg.weightShort = 0.5  # corresponds to unitary connection somatic EPSP (mV)
cfg.startShort = 0  # start at 0 ms
cfg.ratesShort = {'IT2': [0,5], 'IT4': [0,2.5], 'IT5A': [0,5], 'IT5B': [0,5], 'IT6': [0,2.5], 'CT6': [0,2.5], 'PT5B': [0,2.5],
                  'SOM2': [0,2.5], 'SOM5A': [0,5], 'SOM5B': [0,5], 'SOM6': [0,5],
                  'PV2': [0,2.5], 'PV5A': [0,5], 'PV5B': [0,5], 'PV6': [0,5]}


## input pulses
cfg.addPulses = 1
cfg.pulse = {'pop': 'None', 'start': 1000, 'end': 1200, 'rate': [0, 20], 'noise': 0.8}
cfg.pulse2 = {'pop': 'None', 'start': 1000, 'end': 1200, 'rate': [0, 20], 'noise': 0.5, 'duration': 500}


#------------------------------------------------------------------------------
# Current inputs 
#------------------------------------------------------------------------------
cfg.addIClamp = 0

cfg.IClamp1 = {'pop': 'IT5B', 'sec': 'soma', 'loc': 0.5, 'start': 0, 'dur': 1000, 'amp': 0.50}


#------------------------------------------------------------------------------
# NetStim inputs 
#------------------------------------------------------------------------------
cfg.addNetStim = 0

 			   ## pop, sec, loc, synMech, start, interval, noise, number, weight, delay 
cfg.NetStim1 = {'pop': 'IT2', 'ynorm':[0,1], 'sec': 'soma', 'loc': 0.5, 'synMech': ['AMPA'], 'synMechWeightFactor': [1.0],
				'start': 500, 'interval': 1000.0/60.0, 'noise': 0.0, 'number': 60.0, 'weight': 30.0, 'delay': 0}
