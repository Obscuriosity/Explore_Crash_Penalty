'''
QLDataHandling for Q Learning programs
'''
import os.path
import numpy as np
from numpy import save
from numpy import load
import pickle
import matplotlib.pyplot as plt

NAME = 'QL_16_Explore_CP'
LOG = (f'{NAME}_log.txt')
STATES_LIST = (f'States_List_{NAME}.npy')
QTABLE = (f'Q_Table_{NAME}.npy')
DICTIONARY = (f'{NAME}_Stats.pkl')

def LoadLog():
    t = int(0) # Variable for timestep count

    tlog = open(LOG) # Open File for reading to retrieve data
    tlog.readline()        #Read first line and do nothing with it
    oldt = tlog.readline() # Read file and assign iteration data to variable
    tlog.close() # Close file
    print(oldt)
    t = int(oldt) # convert numeric data into int
    return t

def LoadQTable():
    Q = load(QTABLE)
    return Q

def LoadStatesList():    
    states = load(STATES_LIST)
    return states

def LoadDictionary():
    Dictionary = pickle.load(open(DICTIONARY, "rb"))
    return Dictionary

def SaveData(t, Q, DictData):
    save(QTABLE, Q)
    if t % 1000 == 0:
        save((f'QTables/{NAME}_{t}.npy'), Q)
    
    t = str(t) # convert back to string for writing
    tlog = open(LOG, "w+") # open file for writing
    tlog.write("Itteration Number :\n") # Lets write what the file is about
    tlog.write(t) # write new data to file              # insert variables after conversion to string
    tlog.close()  # Close file
    t = int(t)
    
    # Save Dictionary Data
    StatDict = open(DICTIONARY, "wb")
    pickle.dump(DictData, StatDict)
    StatDict.close
    
    print("Time Steps :", t)
    print("Data Saved.")

def SaveGraph(t, alpha, gamma):
    aggr_rewards = pickle.load(open(DICTIONARY, "rb"))
    title = (f'{NAME}, alpha, {alpha},  gamma, {gamma}')
    plt.figure(figsize=(22, 12))
    plt.plot(aggr_rewards['t'], aggr_rewards['eps'], 'r:', label="epsilon x 10")
    plt.plot(aggr_rewards['t'], aggr_rewards['min'], label="min rewards")
    plt.plot(aggr_rewards['t'], aggr_rewards['avg'], label="average rewards")
    plt.plot(aggr_rewards['t'], aggr_rewards['max'], label="max rewards")
    plt.xlabel('Iterations')
    plt.ylabel('Rewards')
    plt.title(title)
    plt.legend(loc=3)
    plt.savefig(f'QTables/Graph_{NAME}_{t}.png')
    print("Graph Saved")
    #plt.show()
    
def mapp(x, in_min, in_max, out_min, out_max):
    # Function to map reward values ie - r = round(mapp(a, 0, 75, 0, 10), 4)
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def CreateData():
    sonar_range = 2
    startVal = 20.0

    Q_table = np.array([[startVal, startVal, startVal]])
    States_List = []
    for i in range(0, sonar_range):
        for j in range(0, sonar_range):
            for k in range(0, sonar_range):
                for l in range(0, sonar_range):
                    newState = (i, j, k, l)
                    States_List.append(newState)
    print('states is ', len(States_List), " long.")
    for o in range(0, len(States_List)-1):
        newQ = np.array ([startVal, startVal, startVal])  # create new action value list
        Q_table = np.vstack((Q_table, newQ))
    print("Q Table is ", len(Q_table), " long.")

    log = open(LOG, "w")
    log.write("Itteration Number :\n") # Lets write what the file is about
    log.write("0\n")
    log.close()

    save(QTABLE, Q_table) # Added zeros so as not to overwrite current file if one in use. Delete '_0000' to use
    save(STATES_LIST, States_List)

    print("Q Table Created\nState List Created\nLog created")
    
    cwd = os.getcwd() # Get current working directory
    dir = os.path.join(cwd,'QTables') # Make directory path
    if not os.path.exists(dir) == True: # If path does not exist Create it
        os.mkdir(dir)
        print(dir, "- Made")
    t = 'EMPTY'
    save((f'QTables/{NAME}_{t}.npy'), Q_table)
    
    # Create and save new dictinary
    Dictionary = {'t': [], 'avg': [], 'max': [], 'min': [], 'eps': []}
    StatDict = open(DICTIONARY, "wb")
    pickle.dump(Dictionary, StatDict)
    StatDict.close
