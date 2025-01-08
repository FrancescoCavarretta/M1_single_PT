import pickle
import matplotlib.pyplot as plt
import sys
print(sys.argv[-1:])
import efel
import numpy
for x in sys.argv[1:]:
  data = pickle.load(open('../data/%s/%s_data.pkl' % tuple([x] * 2), 'rb'))
  print(data['simData'].keys())
  plt.plot(data['simData']['t'], data['simData']['V_soma']['cell_0'])
##  plt.plot(data['simData']['t'], data['simData']['V_apic_distal_91']['cell_0'])
##  plt.plot(data['simData']['t'], data['simData']['V_apic_distal_62']['cell_0'])
##  plt.plot(data['simData']['t'], data['simData']['V_dend_0']['cell_0'])
##  plt.plot(data['simData']['t'], data['simData']['V_dend_5']['cell_0'])
#plt.legend()

##try:
##  data_bs = pickle.load(open('../data/%s/%s_data.pkl' % ('mydefault_0.pkl', 'mydefault_0.pkl'), 'rb'))['simData']
##  plt.plot(data_bs['t'], data_bs['V_soma']['cell_0'], color='gray')  
##except:
##  pass

plt.show()








### Now we will construct the datastructure that will be passed to eFEL
##
### A 'trace' is a dictionary
##trace1 = {}
##
##idx = numpy.argwhere(numpy.array(data['simData']['t'])>=5000)[:,0]
##
##print(idx)
##
### Set the 'T' (=time) key of the trace
##trace1['T'] = numpy.array(data['simData']['t'])[idx]
##
### Set the 'V' (=voltage) key of the trace
##trace1['V'] = numpy.array(data['simData']['V_soma']['cell_0'])[idx]
##
### Set the 'stim_start' (time at which a stimulus starts, in ms)
### key of the trace
### Warning: this need to be a list (with one element)
##trace1['stim_start'] = [5000]
##
### Set the 'stim_end' (time at which a stimulus end) key of the trace
### Warning: this need to be a list (with one element)
##trace1['stim_end'] = [15000]
##
### Multiple traces can be passed to the eFEL at the same time, so the
### argument should be a list
##traces = [trace1]
##
### Now we pass 'traces' to the efel and ask it to calculate the feature
### values
##traces_results = efel.get_feature_values(traces,
##                                       ['Spikecount'])
##
### The return value is a list of trace_results, every trace_results
### corresponds to one trace in the 'traces' list above (in same order)
##for trace_results in traces_results:
##    # trace_result is a dictionary, with as keys the requested eFeatures
##    for feature_name, feature_values in trace_results.items():
##        print("Feature %s has the following values: %s" % \
##            (feature_name, ', '.join([str(x/10) for x in feature_values])))
