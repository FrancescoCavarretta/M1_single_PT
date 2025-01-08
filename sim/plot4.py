import pickle
import matplotlib.pyplot as plt

data = pickle.load(open('../data/v56_manualTune/v56_tune3_data.pkl', 'rb'))

plt.plot(data['simData']['t'], data['simData']['caNL_apic_distal_62']['cell_0'], label='caNL_apic_distal_62')

plt.legend()
plt.show()
