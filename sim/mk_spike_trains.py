import cfg
import sys
import MeMo.compiler.neuron as mcn
import pickle
import numpy as np
#import matplotlib.pyplot as plt

filename = sys.argv[sys.argv.index('--filename')+1]
output = sys.argv[sys.argv.index('--output')+1]

try:
  seed = int(sys.argv[sys.argv.index('--seed')+1])
except:
  seed = 0

try:
  regularity = float(sys.argv[sys.argv.index('--regularity')+1])
except:
  regularity = 5.0

try:
  regularity2 = float(sys.argv[sys.argv.index('--regularity2')+1])
except:
  regularity2 = 50000.0

try:
  regularity3 = float(sys.argv[sys.argv.index('--regularity3')+1])
except:
  regularity3 = 50000.0
  
try:
  refractory_period = float(sys.argv[sys.argv.index('--refractory_period')+1])
except:
  refractory_period = 3.0

try:
  tstop = float(sys.argv[sys.argv.index('--tstop')+1])
except:
  tstop = 10000.0

try:
  dt = float(sys.argv[sys.argv.index('--dt')+1])
except:
  dt = 0.01
  
def CV(tspk):
  isi = tspk[1:] - tspk[:-1]
  return np.std(isi) / np.mean(isi)


cfgret = {}

cfgret['tstop'] = tstop
cfgret['seed'] = seed
cfgret['output'] = output


seed += 3
ispk = 0

spikes = {}
for name, n in sorted(cfg.cfg.numCells.items()):
  if name.startswith('SOM'):
    fr_name = 'SOM'
  elif name.startswith('VM'):
    fr_name = 'VM'
  else:
    fr_name = name
    
  spikes[name] = []

  rates = []
  CVs = []
  for i in range(n):
        
    o = mcn.SpikeTrain('abbasi')
    
    o.time_unit = 'ms'
    o.time = np.arange(0, tstop, dt)
    o.rate = np.zeros(o.time.size) + cfg.cfg.ratesShort[fr_name]
    o.refractory_period = refractory_period
    o.tstop = tstop
    
    o.distribution = mcn.Distribution((seed, 1), 'gamma')
    o.distribution.k = regularity
    o.distribution.theta = 1 / regularity
    seed += 1
    

    
    o.make()
    ispk += 1  
    spikes[name].append(o.product.tolist())
    


    CVs.append(CV(o.product))
    rates.append(o.product.size / tstop * 1000)

#    if '--plot' in sys.argv:
#      plt.eventplot(o.product, lineoffsets=ispk)

    


  print(name, '\t', round(np.mean(CVs), 2), round(np.std(CVs), 2), '\t', round(np.mean(rates), 1), round(np.std(rates), 1))
#plt.show()

cfgret['spiketrains'] = spikes

with open(filename, 'wb') as fo:
  pickle.dump(cfgret, fo)

print('seed', seed)
