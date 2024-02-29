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

indir = '../pymultinest_results/RPM/'
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

# this is rpm_retired (retired = job took more than 28 days without finishing)
# 15 + 12*10 + 6*10 = 195
failedjobs_models = [31, 46, 75, 378, 379, 458, 572, 573, 574, 575, 579, 670, 671, 672, 727, 1015, 1016, 1037, 1038, 1044, 1331,
                     1332, 1353, 1354, 1417, 1422, 1487, 1488, 1491, 1492, 1514, 1515, 1516, 1517, 1518, 1519, 1520, 1521, 1522,
                     1524, 1525, 1526, 1527, 1528, 1585, 1589, 1639, 1655, 1656, 1659, 1668, 1683, 1685, 1686, 1688, 1689, 1690,
                     1691, 1692, 1693, 1694, 1695, 1736, 1780, 1782, 1783, 1785, 1787, 1788, 1789, 1811, 1815, 1816, 1833, 1834,
                     1838, 1854, 1859, 1860, 1865, 2030, 2255, 2317, 2318, 2358, 2420, 2481, 2482, 2522, 2645, 2707, 2708, 2766,
                     2935, 2941, 2942, 2943, 3005, 3006, 3007, 3012, 3013, 3075, 3076, 3271, 3272, 3274, 3280, 3281, 3282, 3284,
                     3348, 3350, 3354, 3355, 3356, 3427, 3429, 3434, 3435, 3505, 3549, 3551, 3552, 3561, 3562, 3563, 3564, 3803,
                     3804, 3805, 3810, 3811, 3873, 3875, 3880, 3881, 3882, 3944, 3945, 4139, 4140, 4143, 4145, 4148, 4149, 4150,
                     4151, 4216, 4218, 4222, 4223, 4224, 4295, 4297, 4302, 4373, 4417, 4419, 4420, 4422, 4423, 4428, 4429, 4430,
                     4432, 4517, 4553, 4805, 4841, 4873, 4917, 4953, 5013, 5023, 5063, 5099, 5329, 5353, 5389, 5421, 5468, 5498,
                     5538, 5544, 5583, 5593, 5623, 5633, 5669, 5771, 5787, 5797, 5867, 5873]

for i in failedjobs_models:
    model_dict.pop(i)

# RPM data from cibersort csvs
Oliver_pct = {
'NE_obs':0.259122843833646,
'NEv1_obs':0.318704767383416,
'NEv2_obs':0.010548327444441,
'NonNE_obs':0.411624061338496
}

Oliver_stdev = {
'NE_obs':0.171187022711461,
'NEv1_obs':0.157524233180492,
'NEv2_obs':0.016363538701013,
'NonNE_obs':0.223000331826237
}

def beta_dist_from_mu_and_stdev(mu,std):
    nu_out = (mu*(1-mu)/(std**2)) - 1
    alpha_out = mu*nu_out
    beta_out = (1-mu)*nu_out
    return beta(alpha_out,beta_out)


# beta distrs for means near zero are U-shaped with the bottom left of the curve near zero
# if you try to get a y-value for an x-value too close to zero it'll just be inf
# so to avoid returning inf as the likelihood value, clip x-values to the lowest possible that won't return y=inf
# based on beta distr transformation using mu and sigma to generate alpha and beta (Kruschke, 2011; see Methods), requires sigma^2 < mu(1-mu)
# so if mu is otherwise zero for likelihood fxn, instead find the lowest value that fits sigma^2 < mu(1-mu)
lowest_allowed = {}
for i in Oliver_stdev:
    mu = 1e-5
    while not (Oliver_stdev[i]**2 < mu*(1-mu)):
        mu *= 1.00001
    lowest_allowed[i] = mu


TOLERANCE = 1e-4
def likelihood(position,obs_list,param_values,rates_mask,solver):
    tspan = np.linspace(0,60,1001)
    Y=np.copy(position)
    param_values[rates_mask] = 10 ** Y
    signal.alarm(30)
    try:
        sim = solver.run(param_values=param_values,tspan=tspan).all
    except TimeoutException as exc:
        return -np.inf
    else:
        signal.alarm(0)
    sim_data = {}
    all_lessthan1 = True
    for obs in obs_list:
        sim_data[obs] = sim[obs] #[:new_end]
        if sim[obs][-1] > 1:
            all_lessthan1 = False
    # if there aren't enough cells, or there are too many cells, or if the end of the sim gets to NaNs (because it grew too fast)
    if sim['total_cells'][-1] < 100:
        #print ('not enough cells ' + str(sim['total_cells'][-1]))
        return -np.inf
    elif np.isnan(sim['total_cells'][-1]):
        #print ('too many cells computer couldnt handle ' + str(sim['total_cells'][-1]))
        return -np.inf
    elif all_lessthan1: #smallest size in SCLC allografts (Lim et al) 1cm^3 (~10^8 cells), largest ~3.5cm^3 (~4*10^8)
        #print ('something crashed out at the end ')
        return np.inf*-1
    else:
        # get the percentages so you can check for equilibrium - first get the total # of cells
        sim_pct_run = {}
        for obs in obs_list:
            sim_pct_run[obs] = np.true_divide(sim[obs],sim['total_cells'])
        # is it in equilibrium?
        not_eq = False
        total_stack = (sim_pct_run[obs_list[0]],)
        for obs in obs_list[1:]:
            total_stack = total_stack + (sim_pct_run[obs],)
        y = np.column_stack(total_stack)
        for idx in range(y.shape[1]):
            try:
                derivative = (y[:,idx][-1]-y[:,idx][-75])/(tspan[-1]-tspan[-75])
                if abs(derivative)>TOLERANCE or np.isnan(derivative): #or np.isnan probably shouldnt happen but just in case
                    not_eq = True
            except IndexError:
                return -np.inf
        if not_eq:
            return -np.inf
        # Score
        total_cost_nonzeros = np.sum([
                            beta_dist_from_mu_and_stdev(
                                                        np.clip(sim_pct_run[obs][-1],lowest_allowed[obs],(1-lowest_allowed[obs])),
                                                        Oliver_stdev[obs]
                                                       )
                            .logpdf(Oliver_pct[obs]) for obs in obs_list[:-1]
                                if not np.all(sim_pct_run[obs]==0)
                           ])
        total_cost_zeros = np.sum([
                            expon(0,scale=Oliver_stdev[obs])
                            .logpdf(Oliver_pct[obs]) for obs in obs_list[:-1]
                                if np.all(sim_pct_run[obs]==0)
                           ])
        total_cost = np.sum([total_cost_nonzeros,total_cost_zeros])
        if np.isnan(total_cost):
            total_cost = np.inf*-1
        return total_cost


with open('../helper_functions_and_files/all_possible_sampled_params_dict.pickle', 'rb') as p:
    sampled_params_dict = pickle.load(p)

results_dict = {}

# per model
for m in model_dict:
    model = model_dict[m]
    solver = ScipyOdeSimulator(model,integrator='lsoda',compiler='cython')
    param_values = np.array([p.value for p in model.parameters])
    #
    obs_list = []
    for i in [x.name for x in model.observables]:
        if i != 'NE_all_obs' and i!= 'total_cells' and i != 'Hes1_all_obs':
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
    a = pymultinest.Analyzer(len(sp_list),outputfiles_basename=sfr)
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
        log_ls = -0.5*mn_data[:,1]
        ml = log_ls.max()
        results_dict[m]['max_loglikelihood'] = ml
        #
        # DIC estimate
        params = mn_data[:,2:]
        prior_mass = mn_data[:,0]
        norm_weights = (prior_mass*np.exp(log_ls))/(np.exp(a.get_stats()['nested sampling global log-evidence']))
        nw_mask = np.isnan(norm_weights)
        if np.any(nw_mask):
            print ('cant calculate this bc there are NaNs')
        #
        results_dict[m]['DIC_calcs'] = {}
        D_of_theta = -2.*log_ls # or like mn_data[:,1] but whatever
        D_bar = np.average(D_of_theta, weights=norm_weights)
        theta_bar = np.average(params, axis=0, weights=norm_weights)
        #
        D_of_theta_bar = -2. * likelihood(theta_bar,obs_list,param_values,rates_mask,solver)
        p_D = D_bar - D_of_theta_bar
        DIC = p_D + D_bar
        print ('check likelihood of theta_bar worked: '+str(DIC))
        results_dict[m]['DIC_calcs']['D_bar'] = D_bar
        results_dict[m]['DIC_calcs']['theta_bar'] = theta_bar
        results_dict[m]['DIC_calcs']['D_of_theta_bar'] = D_of_theta_bar
        results_dict[m]['DIC_calcs']['p_D'] = p_D
        results_dict[m]['DIC_calcs']['DIC'] = DIC
        # AIC estimate
        k = len(sp_list)
        AIC = 2.*k - 2.*ml
        print (AIC)
        results_dict[m]['AIC'] = AIC
        # plus correction
        # n_data = number of observations in the data
        n_data = 11
        try:
            AIC_corr = ( (2. * k**2) + (2. * k) ) / (n_data - k - 1)
        except ZeroDivisionError:
            AIC_corr = np.inf
        results_dict[m]['AICc'] = AIC + AIC_corr
        #
        # BIC estimate
        k = len(sp_list)
        # n_data = number of observations in the data... so the number of cell line cibersort bars per data
        #n_data = 11
        BIC = np.log(n_data)*k - 2.*ml
        results_dict[m]['BIC'] = BIC
        #
        # log Z for INS
        results_dict[m]['INS_log_Z'] = a.get_stats()['nested importance sampling global log-evidence'] # equivalent to a.get_stats()['global evidence'] at least in this context
        # log Z err for INS
        results_dict[m]['INS_log_Z_err'] = a.get_stats()['nested importance sampling global log-evidence error']
    except ValueError:
        print ('Analyzer did not work for model '+str(m)+' so no values returned.')
        pass

DIC_dict = {}
df_list = []
for m in results_dict:
    try:
        DIC_dict[m] = results_dict[m].pop('DIC_calcs')
    except KeyError:
        print ('just another time this model did not get added to the final output: '+str(m))
        pass
    try:
        results_dict[m]['DIC'] = DIC_dict[m]['DIC']
    except KeyError:
        print ('likely another time the model didnt get added to final output: '+str(m))
        pass
    df_list.append(pd.DataFrame(results_dict[m],index=[m]))

full_rez_dict = pd.concat(df_list)
full_rez_dict.to_pickle(outdir+'results_fromNS_gathered_RPM.pickle')

#with open(outdir+'compare_RPM_gleipnir_results_subset_betafit_DIC_calc_values_in_case.pickle','wb') as f:
#    pickle.dump(DIC_dict,f)
