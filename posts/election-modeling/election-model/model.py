import numpy as np
import theano.tensor as tt
import pymc3 as pm

import seaborn as sns
import matplotlib.pyplot as plt

# import csv

# states = ['Washington', 'Delaware', 'Ohio', 'New Jersey', 'Connecticut',
#           'California', 'Nebraska', 'Pennsylvania', 'Michigan',
#           'New Mexico', 'Virginia', 'Maine', 'Hawaii', 'Arizona', 'Texas',
#           'Kentucky', 'Colorado', 'District of Columbia', 'New Hampshire',
#           'Oregon', 'Alabama', 'North Dakota', 'Iowa', 'Rhode Island',
#           'Tennessee', 'Massachusetts', 'Florida', 'Arkansas',
#           'South Dakota', 'Montana', 'North Carolina', 'Wyoming',
#           'West Virginia', 'Kansas', 'Wisconsin', 'Georgia', 'Vermont',
#           'Louisiana', 'Oklahoma', 'Mississippi', 'Idaho', 'Indiana',
#           'Maryland', 'Alaska', 'South Carolina', 'New York', 'Minnesota',
#           'Nevada', 'Missouri', 'Illinois', 'Utah']

# n_dem = np.zeros((51, 5),)
# n_rep = np.zeros((51, 5))

# with open("countypres_2000-2016.csv") as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:

#         state_index = states.index(row['state'])
#         year_index = (int(row['year'])-2000)//4
#         try:
#             votes = float(row['candidatevotes'])
#         except:
#             votes = 0
#             # raise ValueError
#         if row['party'] == 'democrat':
#             n_dem[state_index, year_index] += votes
#         if row['party'] == 'republican':
#             n_rep[state_index, year_index] += votes

# Code to save the vote totals for each state so we don't recompute
# np.save('n_dem.npy', n_dem)
# np.save('n_rep.npy', n_rep)

n_dem = np.load('n_dem.npy')
n_rep = np.load('n_rep.npy')

n = n_dem + n_rep

print(n_rep/n)

with pm.Model() as model:
    # This parameter indicates how much influence the state a voter lives in
    # has on their vote.
    sigma_state = pm.Uniform('sigma_state', lower=0.1, upper=10)
    # This parameter indicates how much influence the specific candidate pair
    # has on their vote.
    sigma_year = pm.Uniform('sigma_year', lower=0.1, upper=10)
    # This represents the bias of each state
    z_state = pm.Normal('z_state', mu=0, sigma=sigma_state, shape=51)
    # This represents the bias in a particular year
    z_year = pm.Normal('z_year', mu=0, sigma=sigma_year, shape=5)
    # Combined table of biases for each state, each year
    z = z_state.reshape((51, 1)) + z_year.reshape((1, 5))

    p = 1/2 + 1/2 * pm.math.erf(z)

    n_rep = pm.Binomial('n_rep', n=n, p=p, observed=n_rep)

    # Predicted values for the year 2020
    z_year_2020 = pm.Normal('z_year_2020', mu=0, sigma=sigma_year, shape=1)

    print(z_year_2020.shape)

    z_2020 = z_state + z_year_2020

    p_2020 = 1/2 + 1/2 * pm.math.erf(z_2020)

    n_2020 = np.average(n, axis=1)

    print(n_2020.shape, p_2020.shape)

    n_rep_2020 = pm.Binomial('n_rep_2020', n=n_2020, p=p_2020, shape=51)

    # Simulated percentage votes for republican in 2020
    p_hat_2020 = n_rep_2020/n_2020
    # Republican states won in 2020
    rep_states_won_2020 = p_hat_2020 > 0.5
    # Republican electoral college vote 2020
    rep_electoral_votes = pm.Deterministic(
        "rep_electoral_votes", pm.math.sum(electors * states_won_2020))

    approx = pm.fit()

    trace = approx.sample(500)

    pm.traceplot(trace["rep_electoral_votes"])
    plt.show()
