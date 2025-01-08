"""
cfg.py 

Simulation configuration for M1 model (using NetPyNE)

Contributors: salvadordura@gmail.com
"""

import argparse
from netpyne import specs

parser = argparse.ArgumentParser()

parser.add_argument('--duration', type=float, default=25000.0, help='simulated time')
parser.add_argument('-o', '--output', type=str, default='default', help='filename of output data')
parser.add_argument('--seed', type=int, default=0, help='indicate the simulation seed')

parser.add_argument('--dt', type=float, default=0.01, help='time step describing resolution of the spike time generator (ms)')
parser.add_argument('-r', '--refractory_period', type=float, default=3, help='refractory period length following an action potential (ms)')
parser.add_argument('--reg', type=float, default=5, help='regularity score of tonic firing')
parser.add_argument('--synapses', type=str, default='', help='modulated synapses')
parser.add_argument('--modlength', type=float, default=500, help='modulated epoch duration (ms)')
parser.add_argument('-f', '--factor', type=float, default=1, help='factor describing the change in firing rate compared to baseline')
parser.add_argument('--modstart', type=float, default=5000, help='start of modulation')
parser.add_argument('--modulation_rate', type=float, default=0.5, help='modulation occurrence rate')
parser.add_argument('--mod_reg_intra', type=float, default=50000, help='regularity of intra-epocal modulation occurrence')
parser.add_argument('--mod_reg_extra', type=float, default=50000, help='regularity of modulation occurrence (ie, synchrony)')

parser.add_argument('--parkinsonian', action='store_true', help='switch indicating parkinsonian state simulation')

args, _ = parser.parse_known_args()



cfg = specs.SimConfig()  

#------------------------------------------------------------------------------
#
# SIMULATION CONFIGURATION
#
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Run parameters
#------------------------------------------------------------------------------
cfg.duration = 25e3 
cfg.dt = 0.05
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 34, 'v_init': -80.1}  
cfg.verbose = 1
cfg.createNEURONObj = 1
cfg.createPyStruct = 1
cfg.connRandomSecFromList = True  # set to false for reproducibility 
#cfg.cvode_active = True
#cfg.cvode_atol = 1e-6
cfg.cache_efficient = True
cfg.printRunTime = 0.1
cfg.oneSynPerNetcon = True  # only affects conns not in subconnParams; produces identical results

cfg.includeParamsLabel = False #True # needed for modify synMech False
cfg.printPopAvgRates = [2000., 5000.]

cfg.checkErrors = False

cfg.saveInterval = 100 # define how often the data is saved, this can be used with interval run if you want to update the weights more often than you save
cfg.intervalFolder = 'interval_saving'


#------------------------------------------------------------------------------
# Recording 
#------------------------------------------------------------------------------
allpops = ['PT5B']
cfg.recordCells = [0]
cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc':0.5, 'var':'v'},
                               'iN_apic_distal_62': {'sec':'apic_62', 'loc':1, 'var':'iN_caN'},
                               'iL_apic_distal_62': {'sec':'apic_62', 'loc':1, 'var':'iL_caL'},
                               'P_apic_distal_62': {'sec':'apic_62', 'loc':1, 'var':'ica_hvaP'},
                               'NL_apic_distal_62': {'sec':'apic_62', 'loc':1, 'var':'ica_hvaNL'},
                               'lva_apic_distal_62': {'sec':'apic_62', 'loc':1, 'var':'ica_lva'},
                               'caNL_apic_distal_62': {'sec':'apic_62', 'loc':1, 'var':'ca_hvaNLi'},
##                               'iN_apic_distal_62': {'sec':'apic_62', 'loc':1, 'var':'iN_caN'},
##                               'iL_apic_distal_62': {'sec':'apic_62', 'loc':1, 'var':'iL_caL'},
##                               'P_apic_distal_62': {'sec':'apic_62', 'loc':1, 'var':'ica_hvaP'},
##                               'NL_apic_distal_62': {'sec':'apic_62', 'loc':1, 'var':'ica_hvaNL'},
##                               'lva_apic_distal_62': {'sec':'apic_62', 'loc':1, 'var':'ica_lva'},
                               'V_apic_distal_62': {'sec':'apic_62', 'loc':1, 'var':'v'},
                               'V_apic_distal_91': {'sec':'apic_91', 'loc':1, 'var':'v'},
                               'tau_apic_distal_62': {'sec':'apic_62', 'loc':1, 'var':'mtau_caN'},
                               'tau_apic_distal_91': {'sec':'apic_91', 'loc':1, 'var':'mtau_caN'},
##                               'iN_apic_distal_91': {'sec':'apic_91', 'loc':1, 'var':'iN_caN'},
##                               'iL_apic_distal_91': {'sec':'apic_91', 'loc':1, 'var':'iL_caL'},
##                               'P_apic_distal_91': {'sec':'apic_91', 'loc':1, 'var':'ica_hvaP'},
##                               'NL_apic_distal_91': {'sec':'apic_91', 'loc':1, 'var':'ica_hvaNL'},
##                               'lva_apic_distal_91': {'sec':'apic_91', 'loc':1, 'var':'ica_lva'},
##                               'iN_apic_distal_91': {'sec':'apic_91', 'loc':1, 'var':'iN_caN'},
##                               'iL_apic_distal_91': {'sec':'apic_91', 'loc':1, 'var':'iL_caL'},
##                               'P_apic_distal_91': {'sec':'apic_91', 'loc':1, 'var':'ica_hvaP'},
##                               'NL_apic_distal_91': {'sec':'apic_91', 'loc':1, 'var':'ica_hvaNL'},
##                               'lva_apic_distal_91': {'sec':'apic_91', 'loc':1, 'var':'ica_lva'},
                    
                               'V_dend_73': {'sec':'dend_73', 'loc':0.5, 'var':'v'},
##                               'iN_dend_73': {'sec':'dend_73', 'loc':1, 'var':'iN_caN'},
##                               'iL_dend_73': {'sec':'dend_73', 'loc':1, 'var':'iL_caL'},
##                               'P_dend_73': {'sec':'dend_73', 'loc':1, 'var':'ica_hvaP'},
##                               'NL_dend_73': {'sec':'dend_73', 'loc':1, 'var':'ica_hvaNL'},
##                               'lva_dend_73': {'sec':'dend_73', 'loc':1, 'var':'ica_lva'},
##                               'iN_dend_73': {'sec':'dend_73', 'loc':1, 'var':'iN_caN'},
##                               'iL_dend_73': {'sec':'dend_73', 'loc':1, 'var':'iL_caL'},
##                               'P_dend_73': {'sec':'dend_73', 'loc':1, 'var':'ica_hvaP'},
##                               'NL_dend_73': {'sec':'dend_73', 'loc':1, 'var':'ica_hvaNL'},
##                               'lva_dend_73': {'sec':'dend_73', 'loc':1, 'var':'ica_lva'},
                    
                               'V_dend_0': {'sec':'dend_0', 'loc':0.5, 'var':'v'},
##                               'iN_dend_0': {'sec':'dend_0', 'loc':1, 'var':'iN_caN'},
##                               'iL_dend_0': {'sec':'dend_0', 'loc':1, 'var':'iL_caL'},
##                               'P_dend_0': {'sec':'dend_0', 'loc':1, 'var':'ica_hvaP'},
##                               'NL_dend_0': {'sec':'dend_0', 'loc':1, 'var':'ica_hvaNL'},
##                               'lva_dend_0': {'sec':'dend_0', 'loc':1, 'var':'ica_lva'},
##                               'iN_dend_0': {'sec':'dend_0', 'loc':1, 'var':'iN_caN'},
##                               'iL_dend_0': {'sec':'dend_0', 'loc':1, 'var':'iL_caL'},
##                               'P_dend_0': {'sec':'dend_0', 'loc':1, 'var':'ica_hvaP'},
##                               'NL_dend_0': {'sec':'dend_0', 'loc':1, 'var':'ica_hvaNL'},
##                               'lva_dend_0': {'sec':'dend_0', 'loc':1, 'var':'ica_lva'},
                    
                               'V_dend_5': {'sec':'dend_5', 'loc':0.5, 'var':'v'},
##                               'iN_dend_5': {'sec':'dend_5', 'loc':1, 'var':'iN_caN'},
##                               'iL_dend_5': {'sec':'dend_5', 'loc':1, 'var':'iL_caL'},
##                               'P_dend_5': {'sec':'dend_5', 'loc':1, 'var':'ica_hvaP'},
##                               'NL_dend_5': {'sec':'dend_5', 'loc':1, 'var':'ica_hvaNL'},
##                               'lva_dend_5': {'sec':'dend_5', 'loc':1, 'var':'ica_lva'},
##                               'iN_dend_5': {'sec':'dend_5', 'loc':1, 'var':'iN_caN'},
##                               'iL_dend_5': {'sec':'dend_5', 'loc':1, 'var':'iL_caL'},
##                               'P_dend_5': {'sec':'dend_5', 'loc':1, 'var':'ica_hvaP'},
##                               'NL_dend_5': {'sec':'dend_5', 'loc':1, 'var':'ica_hvaNL'},
##                               'lva_dend_5': {'sec':'dend_5', 'loc':1, 'var':'ica_lva'},
                    }
##,
##                    
##                    
##                    'V_apic_distal': {'sec':'apic_95', 'loc':0.2222, 'var':'v'},
##                    'BK_apic_distal': {'sec':'apic_95', 'loc':0.2222, 'var':'minf_kBK'}, 
##                    'P_apic_distal': {'sec':'apic_95', 'loc':0.2222, 'var':'minf_caP'}, 
##                    'L_apic_distal': {'sec':'apic_95', 'loc':0.2222, 'var':'minf_caL'},
##                    'L2_apic_distal': {'sec':'apic_95', 'loc':0.2222, 'var':'linf_caL'},
##                    'N_apic_distal': {'sec':'apic_95', 'loc':0.2222, 'var':'minf_caN'},
##                    'CaP_apic_distal': {'sec':'apic_95', 'loc':0.2222, 'var':'ca_hvaPi'}, 
##                    'CaNL_apic_distal': {'sec':'apic_95', 'loc':0.2222, 'var':'ca_hvaNLi'},
##                    'CaT_apic_distal': {'sec':'apic_95', 'loc':0.2222, 'var':'ca_lvai'}}
##                    'V_apic_distal_68': {'sec':'apic_68', 'loc':0.1009, 'var':'v'},
##                    'V_apic_distal_77': {'sec':'apic_77', 'loc':0.9708, 'var':'v'},
##                    'V_apic_distal_95': {'sec':'apic_95', 'loc':0.2222, 'var':'v'},
##                    'V_apic_distal_101': {'sec':'apic_101', 'loc':0.7173, 'var':'v'},
##                    'V_apic_distal_110': {'sec':'apic_110', 'loc':0.9225, 'var':'v'}}

cfg.recordLFP = [[150, y, 150] for y in range(200,1300,100)] # [[150, y, 150] for y in range(200,1300,100)]

cfg.saveLFPPops =  False # allpops 

cfg.recordDipoles = False # {'L2': ['IT2'], 'L4': ['IT4'], 'L5': ['IT5A', 'IT5B', 'PT5B']}

cfg.recordStim = False
cfg.recordTime = True  
cfg.recordStep = 0.025


#------------------------------------------------------------------------------
# Saving
#------------------------------------------------------------------------------
cfg.simLabel = 'default'
cfg.saveFolder = '../data/' + cfg.simLabel
cfg.savePickle = True
cfg.saveJson = False
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams'] #, 'net']
cfg.backupCfgFile = None #['cfg.py', 'backupcfg/'] 
cfg.gatherOnlySimData = True
cfg.saveCellSecs = False
cfg.saveCellConns = False
cfg.compactConnFormat = 0

#------------------------------------------------------------------------------
# Analysis and plotting 
#------------------------------------------------------------------------------
##with open('cells/popColors.pkl', 'rb') as fileObj: popColors = pickle.load(fileObj)['popColors']
##
##cfg.analysis['plotRaster'] = {'include': allpops, 'orderBy': ['pop', 'y'], 'timeRange': [0, cfg.duration], 'saveFig': True, 'showFig': False, 'popRates': True, 'orderInverse': True, 'popColors': popColors, 'figSize': (12,10), 'lw': 0.3, 'markerSize':3, 'marker': '.', 'dpi': 300} 
##
##
##cfg.analysis['plotLFP'] = {'plots': ['timeSeries'], 'electrodes': list(range(len(cfg.recordLFP))), 'figSize': (12,10), 'timeRange': [1000,5000],  'saveFig': True, 'showFig':False} 
##
##
##cfg.analysis['plotTraces'] = {'include': [], 'timeRange': [0, cfg.duration], 'oneFigPer': 'trace', 'figSize': (10,4), 'saveFig': True, 'showFig': False} 



#------------------------------------------------------------------------------
# Synapses
#------------------------------------------------------------------------------
cfg.synWeightFractionEE = [0.485, 0.515] # E->E AMPA to NMDA ratio
cfg.synWeightFractionIE = [0.747, 0.253] # SOM -> E GABAASlow to GABAB ratio

cfg.synsperconn = 5
cfg.AMPATau2Factor = 1.0

#------------------------------------------------------------------------------
# Network 
#------------------------------------------------------------------------------
cfg.weightNorm = 1  # use weight normalization
cfg.weightNormThreshold = 4.0  # weight normalization factor threshold

cfg.scale = 1
cfg.sizeY = 930.0
cfg.sizeX = 1000.0
cfg.sizeZ = 1000.0
#cfg.correctBorderThreshold = 150.0

cfg.L5BrecurrentFactor = 1.0
cfg.ITinterFactor = 1.0
cfg.strengthFactor = 1.0

cfg.EEGain = 0.5

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
cfg.ratesShort = {'ENGF':10, 'IT2/3/4':0.6, 'IT5':4, 'IT6':0.6, 'PT5B':6.4,
                  'SOM':10, 'PV':10, 'VM':20, 'CX':5}



#cfg.numCells = {'IT6':262, 'SOM-T':336, 'ENGF':17, 'IT2/3/4':288, 'SOM-FO':45, 'SOM-NMC':17, 'IT5':119+542, 'PT5B':362, 'PV':46, 'CX':271, 'SOM-OTHERS':150, 'VM_L1':25, 'VM_L5':25}
##vm_n = 8

#cfg.numCells = {'IT6':262, 'SOM-T':336, 'ENGF':17, 'IT2/3/4':288, 'SOM-FO':45, 'SOM-NMC':17, 'IT5':119+542, 'PT5B':362, 'PV':46, 'CX':271, 'SOM-OTHERS':175, 'VM_L1':8, 'VM_L5':20 }

cfg.numCells = {'IT6':2, 'SOM-T':2, 'ENGF':2, 'IT2/3/4':2, 'SOM-FO':2, 'SOM-NMC':2, 'IT5':2, 'PT5B':2, 'PV':2, 'CX':2, 'SOM-OTHERS':2, 'VM_L1':2, 'VM_L5':2 }

ginh1 = 0.0002
ginh4 = 0.00095
ginh2 = ginh4 * 4
ginh3 = 0.0002

gexc1 = 0.0025
gexc2 = 0.001

cfg.g = {'IT6':gexc1, 'SOM-T':ginh1, 'ENGF':ginh1, 'IT2/3/4':(gexc1 + gexc2) / 2, 'SOM-FO':ginh3, 'SOM-NMC':ginh3, 'IT5':gexc2, 'PT5B':gexc2, 'PV':ginh2, 'CX':(gexc1 + gexc2) / 2, 'SOM-OTHERS':ginh4, 'VM_L1':gexc1, 'VM_L5':gexc2}


if args.parkinsonian:
    cfg.numCells['VM_L1'] = int(round(cfg.numCells['VM_L1'] * 0.73))
    cfg.numCells['VM_L5'] = int(round(cfg.numCells['VM_L5'] * 0.65))
    cfg.g['VM_L1'] = cfg.g['VM_L1'] / 0.73
    cfg.g['VM_L5'] = cfg.g['VM_L5'] / 0.65

    
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



cfg.duration = args.duration
cfg.simLabel = args.output
cfg.saveFolder = '../data/' + args.output
cfg.seeds = {'conn':args.seed, 'stim':args.seed+1, 'loc':args.seed+2} 

