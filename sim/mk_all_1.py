import numpy as np
import pickle
import os

nseed = 2395
fmt = 'python3 mk_spike_trains_1.py --filename test_control_%d_%g_%s.pkl --output test_control_%d_%g_%s --seed %d --regularity_intra 5'


args = []
for syninput in ['IT6', 'SOM-T', 'ENGF', 'IT2/3/4', 'SOM-FO', 'SOM-NMC', 'IT5', 'PT5B', 'PV', 'CX', 'VM_L1', 'VM_L5']:
  for p in np.arange(-1, 1.2, 0.2):
    for iseed in range(10):
      seed = nseed * iseed

      os.system(fmt % (seed, p, syninput, seed, p, syninput, seed))
      args.append('test_control_%d_%g_%s.pkl' % (seed, p, syninput))

pickle.dump(args, open('all_args.pkl', 'wb'))
