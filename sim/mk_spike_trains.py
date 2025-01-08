import cfg
import MeMo.compiler.neuron as mcn
import numpy as np

def gen_spike_trains():
  seed = cfg.args.seed+3

  spikes = {}

  ncells = np.sum(cfg.cfg.numCells.values())

  for name, n in sorted(cfg.cfg.numCells.items()):
    spikes[name] = list()

    
    if name.startswith('SOM'):
      fr_name = 'SOM'
    elif name.startswith('VM'):
      fr_name = 'VM'
    else:
      fr_name = name
      
    for i in range(n):
      o = mcn.SpikeTrain('abbasi')
      
      o.time_unit = 'ms'
      o.time = np.arange(0, cfg.args.duration, cfg.args.dt)
      o.rate = np.zeros(o.time.size) + cfg.cfg.ratesShort[fr_name]
      o.refractory_period = cfg.args.refractory_period
      o.tstop = cfg.args.duration
      
      o.distribution = mcn.Distribution((seed, 1), 'gamma')
      o.distribution.k = cfg.args.reg
      o.distribution.theta = 1 / cfg.args.reg
      
      seed += 1
      
      if name in cfg.args.synapses.split(' '):
        
        burst_model = mcn.SpikeTrain('burst')
        burst_model.time_unit = 'ms'
        burst_model.time = np.arange(0, cfg.args.modlength, 0.01)
        burst_model.rate = np.zeros(burst_model.time.size) + cfg.cfg.ratesShort[fr_name] * cfg.args.f

        burst_model.refractory_period = cfg.args.refractory_period
        burst_model.tinit = cfg.args.modstart - (1000 / cfg.args.burst_rate)
        burst_model.tstop = cfg.args.duration
        burst_model.Tdur = cfg.args.modlength

        burst_model.inter_time = np.arange(burst_model.tinit, burst_model.tstop, dt)
        burst_model.inter_rate = np.zeros(burst_model.inter_time.size) + cfg.args.burst_rate
        burst_model.min_inter_period = cfg.args.modlength

        burst_model.intra_distribution = mcn.Distribution((seed+ncells, 1), 'gamma')
        burst_model.intra_distribution.k = cfg.args.burst_reg_intra
        burst_model.intra_distribution.theta = 1/cfg.args.burst_reg_intra
        
        burst_model.inter_distribution = mcn.Distribution((seed+ncells*2, 1), 'gamma')
        burst_model.inter_distribution.k = cfg.args.burst_reg_extra
        burst_model.inter_distribution.theta = 1/cfg.args.burst_reg_extra
        
        o.burst_model = burst_model

      o.make()
      spikes[name].append(o.product.tolist())

  return spikes
    
if __name__ == '__main__':
  import matplotlib.pyplot as plt
  for i, (n, v) in enumerate(gen_spike_trains().items()):
    plt.eventplot(v, lineoffsets=i+1)

  plt.show()
