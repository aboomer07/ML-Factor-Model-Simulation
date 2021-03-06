import random
import numpy as np
import re
import os
import sys
import statsmodels.api as sm

def gen_params(sim_params, N, T):

	r = sim_params['r']
	r_max = sim_params['r_max']

	M = np.divide(np.ones((N, N)), np.array(range(1, (N + 1))).reshape((N, 1)))

	mean = np.zeros(r[2])
	covar = np.multiply(np.array([1, 2, 3, 3, 4]), np.identity(r[2]))

	params = {'DGP1' : {'theta' : np.ones((r[0], 1)), 'nu' : np.random.normal(0, 1, (T, 1)), 'xi' : np.random.normal(0, 1, (T, N)), 'F' : np.random.normal(0, 1, (T, r[0])), 'lambda' : np.random.normal(0, 1, (r[0], N))},
	'DGP2' : {'theta' : np.ones((r[1], 1)), 'nu' : np.random.normal(0, 1, (T, 1)), 'xi' : np.random.normal(0, 1, (T, N)), 'F' : np.random.normal(0, 1, (T, r[1])), 'lambda' : np.random.normal(0, 1, (r[1], N))},
	'DGP3' : {'theta' : np.array([1] + [0] * (r[2] - 1)).reshape((r[2], 1)), 'nu' : np.random.normal(0, 0.01, (T, 1)), 'xi' : np.random.normal(0, 1, (T, N)), 'F' : np.random.multivariate_normal(mean, covar, T), 'lambda' : np.random.normal(0, 1, (r[2], N))},
	'DGP4' : {'theta' : np.zeros((r[3], 1)), 'nu' : np.random.normal(0, 1, (T, 1)), 'xi' : np.random.normal(0, 1, (T, N)), 'F' : np.random.multivariate_normal(mean, covar, T), 'lambda' : np.random.normal(0, 1, (r[3], N))},
	'DGP5' : {'theta' : np.zeros((r[4], 1)), 'nu' : np.random.normal(0, 1, (T, 1)), 'xi' : np.random.normal(0, 1, (T, N)), 'F' : np.random.normal(0, 1, (T, r[4])), 'lambda' : np.multiply(M, np.random.normal(0, 1, (N, N)))},
	'DGP6' : {'theta' : np.ones((r[5], 1)), 'nu' : np.random.normal(0, 1, (T, 1)), 'xi' : np.random.normal(0, 1, (T, N)), 'F' : np.random.normal(0, 1, (T, r[5])), 'lambda' : (1 / np.sqrt(N)) * np.ones((r[5], N))}

	}

	return(params)

def gen_sim(sim_params, dgp, N, T):

	params = gen_params(sim_params, N, T)

	F = params[dgp]['F']
	Lambda = params[dgp]['lambda']
	theta = params[dgp]['theta']
	nu = params[dgp]['nu']
	xi = params[dgp]['xi']

	sim_output = {'y' : F @ theta + nu, 'X' : F @ Lambda + xi}

	if dgp in ['DGP3']:
		X = sim_output['X']
		T = F.shape[0]
		k = F.shape[1]
		lamb, psi = np.linalg.eig((X @ X.T) / T)
		F_hat = psi[:, :k]
		sim_output['y'] = F_hat @ theta + nu

	sim_output['r_max'] = sim_params['r_max'][int(dgp[-1]) - 1]

	return(sim_output)