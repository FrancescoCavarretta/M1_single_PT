"""
init.py

Starting script to run NetPyNE-based M1 model.

Usage:
    python init.py # Run simulation, optionally plot a raster

MPI usage:
    mpiexec -n 4 nrniv -python -mpi init.py

Contributors: salvadordura@gmail.com
"""

import matplotlib; matplotlib.use('Agg')  # to avoid graphics error in servers
from netpyne import sim

#------------------------------------------------------------------------------
## Function to modify cell params during sim (e.g. modify PT ih)
def modifyMechsFunc(simTime):
    from netpyne import sim

    t = simTime

    if t >= 1000 and t <= 1100:
            for cell in sim.net.cells:
                if 'cellType' in cell.tags and cell.tags['cellType'] == 'VM':
                    cell.tags['rate'] = 150



# -----------------------------------------------------------
# Main code
cfg, netParams = sim.readCmdLineArgs()




sim.initialize(
    simConfig = cfg, 	
    netParams = netParams)  # create network object and set cfg and net params

sim.pc.timeout(300)                          # set nrn_timeout threshold to X sec (max time allowed without increasing simulation time, t; 0 = turn off)
sim.net.createPops()               			# instantiate network populations
sim.net.createCells()              			# instantiate network cells based on defined populations
sim.net.connectCells()            			# create connections between cells based on params
sim.net.addStims() 							# add network stimulation
sim.setupRecording()              			# setup variables to record for each cell (spikes, V traces, etc)

### Simulation option 1: standard

sim.runSim()                              # run parallel Neuron simulation (calling func to modify mechs)
##
##sim.runSimWithIntervalFunc(cfg.duration, modifyMechsFunc)
### Gather/save data option 1: standard
###sim.gatherData()
##
### Gather/save data option 2: distributed saving across nodes 
sim.saveDataInNodes()
sim.gatherDataFromFiles()

sim.saveData()                    			# save params, cell info and sim output to file (pickle,mat,txt,etc)#
#sim.analysis.plotData()         			# plot spike raster etc

