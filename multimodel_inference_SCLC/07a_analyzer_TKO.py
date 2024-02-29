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
sys.path.append('/home/beiksp/maybe_pycharm_running')

indir = '../pymultinest_results/TKO/'
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

# this is tko_retired (retired = job took more than 28 days without finishing)
# 5 + 4*9 + 6*10 + 8*9 = 173
failedjobs_models = [263, 264, 383, 384, 406, 1044, 1360, 1490, 1514, 1520, 1524, 1526, 1585, 1655, 1657, 1660, 1667, 1688, 1694,
                     1754, 1780, 1781, 1782, 1786, 1787, 1793, 1811, 1832, 1838, 1854, 1855, 1859, 1864, 1865, 1866, 2009, 2025,
                     2026, 2335, 2336, 2353, 2354, 2499, 2500, 2517, 2518, 2608, 2935, 2937, 2938, 2942, 3005, 3007, 3012, 3076,
                     3271, 3272, 3274, 3275, 3281, 3282, 3283, 3348, 3350, 3351, 3355, 3356, 3427, 3429, 3434, 3435, 3549, 3551,
                     3552, 3554, 3562, 3803, 3805, 3810, 3811, 3873, 3875, 3880, 3944, 4139, 4140, 4142, 4149, 4150, 4151, 4216,
                     4218, 4219, 4223, 4295, 4297, 4302, 4417, 4419, 4420, 4422, 4423, 4429, 4430, 4431, 4509, 4510, 4518, 4520,
                     4545, 4546, 4556, 4777, 4780, 4787, 4788, 4798, 4808, 4834, 4844, 4889, 4892, 4909, 4910, 4920, 4945, 4946,
                     4956, 5016, 5026, 5054, 5056, 5064, 5066, 5217, 5286, 5317, 5318, 5322, 5334, 5346, 5356, 5382, 5392, 5438,
                     5441, 5448, 5449, 5461, 5471, 5501, 5511, 5563, 5566, 5569, 5573, 5585, 5586, 5596, 5597, 5626, 5636, 5702,
                     5759, 5760, 5764, 5774, 5776, 5790, 5800, 5830, 5833, 5840]

for i in failedjobs_models:
    model_dict.pop(i)

# data (mean and stdev taken from CIBERSORT output csvs)
TKO_pct = {
    'NE_obs': 0.670866848446898,
    'NEv1_obs': 0.001011170766988,
    'NEv2_obs': 0.294235217878072,
    'NonNE_obs': 0.033886762908045
}

TKO_stdev = {
    'NE_obs': 0.152576600276884,
    'NEv1_obs': 0.005730133430503,
    'NEv2_obs': 0.147927688661517,
    'NonNE_obs': 0.031684600453998
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
for i in TKO_stdev:
    mu = 1e-5
    while not (TKO_stdev[i] ** 2 < mu * (1 - mu)):
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
            except IndexError:
                return -np.inf
        if not_eq:
            return -np.inf
        # Score
        total_cost_nonzeros = np.sum([
                            beta_dist_from_mu_and_stdev(
                                                        np.clip(sim_pct_run[obs][-1],lowest_allowed[obs],(1-lowest_allowed[obs])),
                                                        TKO_stdev[obs]
                                                       )
                            .logpdf(TKO_pct[obs]) for obs in obs_list[:-1]
                                if not np.all(sim_pct_run[obs]==0)
                           ])
        total_cost_zeros = np.sum([
                            expon(0,scale=TKO_stdev[obs])
                            .logpdf(TKO_pct[obs]) for obs in obs_list[:-1]
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
        # max_loglikelihood (ml) & setting useful things - from Gleipnir

        mn_data = a.get_data()
        # From Multinest and PyMultinest Githubs:
        # ... 2 + nPar columns. Columns have sample probability, -2*loglikehood, parameter values.
        # [Not important for be but for completeness: Sample probability is the sample prior mass multiplied by its
        #   likelihood & normalized by the evidence.]
        # So! mn_data[:,1] is the column with -2*loglikelihood
        #     multiply that by -.5: -2*loglikelihood * -.5 = (1)*loglikelihood = loglikelihood
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
        n_data = 45
        try:
            AIC_corr = ( (2. * k**2) + (2. * k) ) / (n_data - k - 1)
        except ZeroDivisionError:
            AIC_corr = np.inf
        results_dict[m]['AICc'] = AIC + AIC_corr
        #
        # BIC estimate
        k = len(sp_list)
        # n_data already set
        #n_data = 45
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
full_rez_dict.to_pickle(outdir+'results_fromNS_gathered_TKO.pickle')

# with open(outdir+'compare_TKO_gleipnir_results_subset_betafit_DIC_calc_values_in_case.pickle','wb') as f:
#    pickle.dump(DIC_dict,f)
