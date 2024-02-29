from pysb.simulator import ScipyOdeSimulator
import numpy as np
from scipy.stats import norm, uniform, beta, expon
import copy
import pandas as pd
import pickle
import pymultinest
import sys
import signal

# add this Bayes-MMI directory to the path to be able to import from helper_functions_and_files
sys.path.append('/home/beiksp/Bayes-MMI')
sys.path.append('/home/beiksp/maybe_pycharm_running/')

indir = '../pymultinest_results/cl_A/'
outdir = "../files_generated_in_MMI_sclc/"

class TimeoutException(RuntimeError):
    """ Time out occurred! """
    pass

def handler(signum, frame):
    print('forever is over!')
    raise TimeoutException()

# Register the signal function handler
signal.signal(signal.SIGALRM, handler)

from helper_functions_and_files.modeldict_generator import generate_modeldict

model_dict = generate_modeldict()

# this is cla_retired (retired = job took more than 28 days without finishing)
# 8 + 3*10 + 3*9 + 12*10 = 185
failedjobs_models = [68, 85, 91, 379, 412, 574, 580, 670, 1011, 1015, 1016, 1331, 1332, 1418, 1427, 1489, 1490, 1492, 1498, 1499,
                     1500, 1514, 1515, 1524, 1525, 1526, 1586, 1588, 1635, 1655, 1657, 1658, 1682, 1684, 1694, 1734, 1735, 1736,
                     1742, 1743, 1754, 1765, 1780, 1781, 1782, 1783, 1784, 1785, 1787, 1788, 1790, 1810, 1811, 1832, 1833, 1838,
                     1854, 1859, 1866, 2030, 2075, 2194, 2255, 2358, 2401, 2402, 2419, 2420, 2482, 2522, 2583, 2584, 2646, 2708,
                     2766, 2935, 2937, 2938, 2940, 2942, 2943, 3005, 3007, 3008, 3010, 3012, 3013, 3076, 3271, 3272, 3273, 3274,
                     3275, 3276, 3278, 3282, 3283, 3284, 3348, 3350, 3351, 3355, 3356, 3427, 3429, 3430, 3434, 3435, 3505, 3549,
                     3551, 3552, 3554, 3555, 3556, 3559, 3562, 3563, 3564, 3803, 3806, 3808, 3810, 3811, 3873, 3875, 3876, 3878,
                     3880, 3881, 3944, 3946, 4139, 4140, 4142, 4143, 4144, 4146, 4147, 4150, 4151, 4152, 4153, 4216, 4218, 4219,
                     4221, 4223, 4224, 4295, 4297, 4298, 4300, 4302, 4303, 4419, 4420, 4422, 4423, 4424, 4426, 4427, 4430, 4432,
                     4433, 4517, 4553, 4805, 4841, 4874, 4953, 5013, 5024, 5053, 5322, 5544, 5563, 5583, 5584, 5623, 5633, 5760,
                     5797, 5873, 5874]

for i in failedjobs_models:
    model_dict.pop(i)

# data for SCLC-A cell lines from cibersort csvs
cellline_pct = {
    'NE_obs': 0.82827978,
    'NEv1_obs': 0.071928499,
    'NEv2_obs': 0.0830788,
    'NonNE_obs': 0.016712921
}

cellline_stdev = {
    'NE_obs': 0.114751192,
    'NEv1_obs': 0.094443104,
    'NEv2_obs': 0.099794185,
    'NonNE_obs': 0.020277219
}


def beta_dist_from_mu_and_stdev(mu, std):
    nu_out = (mu * (1 - mu) / (std ** 2)) - 1
    alpha_out = mu * nu_out
    beta_out = (1 - mu) * nu_out
    return beta(alpha_out, beta_out)


# beta distrs for means near zero are U-shaped with the bottom left of the curve near zero
# if you try to get a y-value for an x-value too close to zero it'll just be inf
# so to avoid returning inf as the likelihood value, clip x-values to the lowest possible that won't return y=inf
# based on beta distr transformation using mu and sigma to generate alpha and beta (Kruschke, 2011; see Methods), requires sigma^2 < mu(1-mu)
# so if mu is otherwise zero for likelihood fxn, instead find the lowest value that fits sigma^2 < mu(1-mu)
lowest_allowed = {}
for i in cellline_stdev:
    mu = 1e-5
    while not (cellline_stdev[i] ** 2 < mu * (1 - mu)):
        mu *= 1.00001
    lowest_allowed[i] = mu

TOLERANCE = 1e-4
def likelihood(position, obs_list, param_values, rates_mask, solver):
    tspan = np.linspace(0, 60, 1001)
    Y = np.copy(position)
    param_values[rates_mask] = 10 ** Y
    signal.alarm(30)
    try:
        sim = solver.run(param_values=param_values, tspan=tspan).all
    except TimeoutException as exc:
        return -np.inf
    else:
        signal.alarm(0)
    sim_data = {}
    all_lessthan1 = True
    for obs in obs_list:
        sim_data[obs] = sim[obs]  # [:new_end]
        if sim[obs][-1] > 1:
            all_lessthan1 = False
    # if there aren't enough cells, or there are too many cells, or if the end of the sim gets to NaNs (because it grew too fast)
    if sim['total_cells'][-1] < 100:
        # print ('not enough cells ' + str(sim['total_cells'][-1]))
        return -np.inf
    elif np.isnan(sim['total_cells'][-1]):
        # print ('too many cells computer couldnt handle ' + str(sim['total_cells'][-1]))
        return -np.inf
    elif all_lessthan1:  # smallest size in SCLC allografts (Lim et al) 1cm^3 (~10^8 cells), largest ~3.5cm^3 (~4*10^8)
        # print ('something crashed out at the end ')
        # print (sim_data)
        return np.inf * -1
    else:
        # get the percentages so you can check for equilibrium - first get the total # of cells
        sim_pct_run = {}
        for obs in obs_list:
            sim_pct_run[obs] = np.true_divide(sim[obs], sim['total_cells'])
        # is it in equilibrium?
        not_eq = False
        total_stack = (sim_pct_run[obs_list[0]],)
        for obs in obs_list[1:]:
            total_stack = total_stack + (sim_pct_run[obs],)
        y = np.column_stack(total_stack)
        for idx in range(y.shape[1]):
            try:
                derivative = (y[:, idx][-1] - y[:, idx][-75]) / (tspan[-1] - tspan[-75])
                if abs(derivative) > TOLERANCE or np.isnan(
                        derivative):  # or np.isnan probably shouldnt happen but just in case
                    not_eq = True
            except IndexError:  # if tspan has less than 75 indices after the nanind process - not doing this anymore but leaving try/catch anyway...
                return -np.inf
        if not_eq:
            return -np.inf
        # Score
        total_cost_nonzeros = np.sum([
                            beta_dist_from_mu_and_stdev(
                                                        np.clip(sim_pct_run[obs][-1],lowest_allowed[obs],(1-lowest_allowed[obs])),
                                                        cellline_stdev[obs]
                                                       )
                            .logpdf(cellline_pct[obs]) for obs in obs_list[:-1]
                                if not np.all(sim_pct_run[obs]==0)
                           ])
        total_cost_zeros = np.sum([
                            expon(0,scale=cellline_stdev[obs])
                            .logpdf(cellline_pct[obs]) for obs in obs_list[:-1]
                                if np.all(sim_pct_run[obs]==0)
                           ])
        total_cost = np.sum([total_cost_nonzeros,total_cost_zeros])
        if np.isnan(total_cost):
            total_cost = np.inf * -1
        return total_cost

with open('../helper_functions_and_files/all_possible_sampled_params_dict.pickle', 'rb') as p:
    sampled_params_dict = pickle.load(p)

results_dict = {}

# per model
for m in model_dict:
    model = model_dict[m]
    solver = ScipyOdeSimulator(model, integrator='lsoda', compiler='cython')
    param_values = np.array([p.value for p in model.parameters])
    #
    obs_list = []
    for i in [x.name for x in model.observables]:
        if i != 'NE_all_obs' and i != 'total_cells' and i != 'Hes1_all_obs':
            obs_list.append(i)
    #
    rates_mask = []
    for i in [x for x in model.parameters]:
        rates_mask.append('sp_' + i.name in [y for y in
                                             sampled_params_dict])  # list comprehension will give all the names for sampled params (keys in the dict)
    #
    sp_list = []
    for i in [x for x in sampled_params_dict]:
        if i.split('sp_')[1] in [y.name for y in model.parameters]:
            sp_list.append(sampled_params_dict[i])
    #
    sfr = "" + indir + "/dir_model_" + str(m) + "/model_" + str(m) + "_"
    #
    a = pymultinest.Analyzer(len(sp_list), outputfiles_basename=sfr)
    results_dict[m] = {}
    #
    try:
        # log Z
        results_dict[m]['log_Z'] = a.get_stats()['nested sampling global log-evidence']
        # log Z err
        results_dict[m]['log_Z_err'] = a.get_stats()['nested sampling global log-evidence error']
        #
        # Z
        results_dict[m]['Z'] = np.exp(a.get_stats()['nested sampling global log-evidence'])
        # Z err
        results_dict[m]['Z_err'] = np.exp(a.get_stats()['nested sampling global log-evidence error'])
        #
        # max_loglikelihood (ml) & setting useful things
        mn_data = a.get_data()
        log_ls = -0.5 * mn_data[:, 1]
        ml = log_ls.max()
        results_dict[m]['max_loglikelihood'] = ml
        #
        # DIC estimate
        params = mn_data[:, 2:]
        prior_mass = mn_data[:, 0]
        norm_weights = (prior_mass * np.exp(log_ls)) / (np.exp(a.get_stats()['nested sampling global log-evidence']))
        nw_mask = np.isnan(norm_weights)
        if np.any(nw_mask):
            print('cant calculate this bc there are NaNs')
        #
        results_dict[m]['DIC_calcs'] = {}
        D_of_theta = -2. * log_ls  # or like mn_data[:,1] but whatever
        D_bar = np.average(D_of_theta, weights=norm_weights)
        theta_bar = np.average(params, axis=0, weights=norm_weights)
        #
        D_of_theta_bar = -2. * likelihood(theta_bar, obs_list, param_values, rates_mask, solver)
        p_D = D_bar - D_of_theta_bar
        DIC = p_D + D_bar
        print('check likelihood of theta_bar worked: ' + str(DIC))
        results_dict[m]['DIC_calcs']['D_bar'] = D_bar
        results_dict[m]['DIC_calcs']['theta_bar'] = theta_bar
        results_dict[m]['DIC_calcs']['D_of_theta_bar'] = D_of_theta_bar
        results_dict[m]['DIC_calcs']['p_D'] = p_D
        results_dict[m]['DIC_calcs']['DIC'] = DIC
        #
        #
        # AIC estimate
        k = len(sp_list)
        AIC = 2. * k - 2. * ml
        print(AIC)
        results_dict[m]['AIC'] = AIC
        # plus correction
        # n_data = number of observations in the data
        n_data = 13
        try:
            AIC_corr = ( (2. * k**2) + (2. * k) ) / (n_data - k - 1)
        except ZeroDivisionError:
            AIC_corr = np.inf
        results_dict[m]['AICc'] = AIC + AIC_corr
        #
        # BIC estimate
        k = len(sp_list)
        # n_data = number of observations in the data... so the number of rpm datapoints to make the cibersort data.
        #n_data = 13
        BIC = np.log(n_data) * k - 2. * ml
        results_dict[m]['BIC'] = BIC
        #
        # log Z for INS
        results_dict[m]['INS_log_Z'] = a.get_stats()[
            'nested importance sampling global log-evidence']  # equivalent to a.get_stats()['global evidence'] at least in this context
        # log Z err for INS
        results_dict[m]['INS_log_Z_err'] = a.get_stats()['nested importance sampling global log-evidence error']
    except ValueError:
        print('Analyzer did not work for model ' + str(m) + ' so no values returned.')
        # line = f.readlines()
        # print (line)
        pass

DIC_dict = {}
df_list = []
for m in results_dict:
    try:
        DIC_dict[m] = results_dict[m].pop('DIC_calcs')
    except KeyError:
        print('just another time this model did not get added to the final output: ' + str(m))
        pass
    try:
        results_dict[m]['DIC'] = DIC_dict[m]['DIC']
    except KeyError:
        print('likely another time the model didnt get added to final output: ' + str(m))
        pass
    df_list.append(pd.DataFrame(results_dict[m], index=[m]))

full_rez_dict = pd.concat(df_list)
full_rez_dict.to_pickle(outdir+'results_fromNS_gathered_clA.pickle')

# with open(outdir+'compare_clA_gleipnir_results_subset_betafit_DIC_calc_values_in_case.pickle','wb') as f:
#    pickle.dump(DIC_dict,f)

