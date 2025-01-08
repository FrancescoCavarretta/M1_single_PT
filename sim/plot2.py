import pickle
import matplotlib.pyplot as plt

data = pickle.load(open('../data/v56_manualTune/v56_tune3_data.pkl', 'rb'))
##for k in data['simData'].keys():
##  if k.startswith('iL'):
##    plt.plot(data['simData']['t'], data['simData'][k]['cell_0'], label=k)

plt.plot(data['simData']['t'], data['simData']['tau_apic_distal_62']['cell_0'], label='62')
plt.plot(data['simData']['t'], data['simData']['tau_apic_distal_91']['cell_0'], label='91')
plt.legend()
plt.show()
