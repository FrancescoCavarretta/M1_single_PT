import os

n = 2395

fmt = 'python3 mk_spike_trains.py --filename test_control_%d.pkl --output test_control_%d --seed %d --tstop 1000'

for i in range(10):
  os.system( fmt % (i, i, i * n) )
  
