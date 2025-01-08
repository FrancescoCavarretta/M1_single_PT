import pickle
import matplotlib.pyplot as plt
import sys
import efel
import numpy


def get_spike_count(data):
    # Now we will construct the datastructure that will be passed to eFEL

  # A 'trace' is a dictionary
  trace1 = {}

  idx = numpy.argwhere(numpy.array(data['simData']['t']) >= 5000)[:,0]


  # Set the 'T' (=time) key of the trace
  trace1['T'] = numpy.array(data['simData']['t'])[idx]

  # Set the 'V' (=voltage) key of the trace
  trace1['V'] = numpy.array(data['simData']['V_soma']['cell_0'])[idx]

  # Set the 'stim_start' (time at which a stimulus starts, in ms)
  # key of the trace
  # Warning: this need to be a list (with one element)
  trace1['stim_start'] = [5000]

  # Set the 'stim_end' (time at which a stimulus end) key of the trace
  # Warning: this need to be a list (with one element)
  trace1['stim_end'] = [10000]

  # Multiple traces can be passed to the eFEL at the same time, so the
  # argument should be a list
  traces = [trace1]

  # Now we pass 'traces' to the efel and ask it to calculate the feature
  # values
  return efel.get_feature_values(traces, ['Spikecount'])[0]['Spikecount'] / 5.0


nspk = [ get_spike_count(pickle.load(open('../data/%s/%s_data.pkl' % tuple(['test_control_%d' % i] * 2), 'rb'))) for i in range(1) ]
  
print(numpy.mean(nspk), numpy.std(nspk))
