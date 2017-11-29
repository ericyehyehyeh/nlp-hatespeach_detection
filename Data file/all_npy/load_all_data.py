import numpy as np
all_races = np.load("all_races.npy")
fword = np.load("fword.npy")
gender = np.load("gender.npy")
# below are dict 
hate_All = np.load("hate_All.npy").item()
racial = np.load("racial.npy").item()
# this is a list of keys of hate_All
hate_keys = hate_All.keys()