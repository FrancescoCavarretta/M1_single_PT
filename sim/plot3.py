import pickle
import matplotlib.pyplot as plt

data = pickle.load(open('../data/v56_manualTune/v56_tune3_data.pkl', 'rb'))
for k in data['simData'].keys():
  if k.startswith('iL') or k.startswith('iN'):
    plt.plot(data['simData']['t'], data['simData'][k]['cell_0'], label=k)

plt.legend()
plt.show()
