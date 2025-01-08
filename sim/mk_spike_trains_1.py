import cfg
import MeMo.compiler.neuron as mcn
import numpy as np

def gen_spike_trains():
  seed = cfg.args.seed+3

  spikes = {}

  for name, n in sorted(cfg.cfg.numCells.items()):
    spikes[name] = list()

    
    if name.startswith('SOM'):
      fr_name = 'SOM'
    elif name.startswith('VM'):
      fr_name = 'VM'
    else:
      fr_name = name
      
    for i in range(n):
      spikes[name].append(mcn.SpikeTrain('abbasi'))
      
      spikes[name][i].time_unit = 'ms'
      spikes[name][i].time = np.arange(0, cfg.args.duration, cfg.args.dt)
      spikes[name][i].rate = np.zeros(o.time.size) + cfg.cfg.ratesShort[fr_name]
      spikes[name][i].refractory_period = cfg.args.r
      spikes[name][i].tstop = cfg.args.duration
      
      spikes[name][i].distribution = mcn.Distribution((seed, 1), 'gamma')
      spikes[name][i].distribution.k = cfg.args.reg
      spikes[name][i].distribution.theta = 1 / cfg.args.reg
      
      seed += 1



  for name, n in sorted(cfg.cfg.numCells.items()):    
    if name.startswith('SOM'):
      fr_name = 'SOM'
    elif name.startswith('VM'):
      fr_name = 'VM'
    else:
      fr_name = name
      
    for i in range(n):      
      if name in cfg.args.synapses.split(' '):
        
        burst_model = mcn.SpikeTrain('burst')
        burst_model.time_unit = 'ms'
        burst_model.time = np.arange(0, cfg.args.modlength, 0.01)
        burst_model.rate = np.zeros(burst_model.time.size) + cfg.cfg.ratesShort[fr_name] * cfg.args.f

        burst_model.refractory_period = cfg.args.r
        burst_model.tinit = cfg.args.modstart - (1000 / cfg.args.v)
        burst_model.tstop = cfg.args.duration
        burst_model.Tdur = cfg.args.modlength

        burst_model.inter_time = np.arange(burst_model.tinit, burst_model.tstop, dt)
        burst_model.inter_rate = np.zeros(burst_model.inter_time.size) + cfg.args.modulation_rate
        burst_model.min_inter_period = cfg.args.modlength

        burst_model.intra_distribution = mcn.Distribution((seed, 1), 'gamma')
        burst_model.intra_distribution.k = cfg.args.mod_reg_intra
        burst_model.intra_distribution.theta = 1/cfg.args.mod_reg_intra

        seed += 1
        
        burst_model.inter_distribution = mcn.Distribution((seed, 1), 'gamma')
        burst_model.inter_distribution.k = cfg.args.mod_reg_extra
        burst_model.inter_distribution.theta = 1/cfg.args.mod_reg_extra

        seed += 1
        
        spikes[name][i].burst_model = burst_model
      

  for name, n in sorted(cfg.cfg.numCells.items()):         
    for i in range(n):
      spikes[name][i].make()
      spikes[name][i] = spikes[name][i].product.tolist()

  return spikes
    

