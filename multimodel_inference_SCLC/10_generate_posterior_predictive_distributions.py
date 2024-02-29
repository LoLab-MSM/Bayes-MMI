## Need to run ../helper_functions_and_files/consolidate_posterior_marginal_distributions.py before
#   running this script (but after 09_generate_posterior_marginal_distributions.py)

from pysb.simulator import ScipyOdeSimulator
import sys
import pickle
import numpy as np
import pandas as pd
import signal
import os

# add this Bayes-MMI directory to the path to be able to import from helper_functions_and_files
sys.path.append('/home/beiksp/Bayes-MMI')
sys.path.append('/home/beiksp/maybe_pycharm_running/')

class TimeoutException(RuntimeError):
    """ Time out occurred! """
    pass

def handler(signum, frame):
    print('forever is over!')
    raise TimeoutException()

with open('../helper_functions_and_files/all_possible_sampled_params_dict.pickle','rb') as p:
    sampled_params_dict = pickle.load(p)

# Register the signal function handler
signal.signal(signal.SIGALRM, handler)

names_dict = {}
for n,i in enumerate([x for x in sampled_params_dict]):
    param_toprint = i
    ptp = param_toprint.split('sp_')[1]
    paramtoprint = ptp.split('_diff')
    if len(paramtoprint) == 1:
        paramtoprint = ptp.replace('cell_1kc','cell')
        finalparam = paramtoprint.replace('division_0_N', 'division_N').replace('die_0_N', 'die_N').replace(
                'cell_0', 'baseline').replace('cell_1', 'altered').replace('cell_2', 'equil_assn')
    else:
        paramtoprint = ptp.replace('_cell_1kf','_cell')
        altered_details = ''
        if '_1' in paramtoprint:
            altered_details = '_altered'
        elif '_2' in paramtoprint:
            altered_details = '_equil_assn'
        finalparam = paramtoprint.replace('uni_0_', '').replace('cell_N', 'to_N').replace(
                'diff_cell_0', 'baseline').replace('diff_cell_1', 'altered').replace('diff_cell_2', 'equil_assn')
    finalparam = finalparam.replace('NonNE', 'Y').replace('NEv2', 'A2').replace('NEv1', 'N').replace('NE', 'A')
    names_dict[i] = finalparam

#now just have to access the right stats object -- just add for any relevant new distributions
randomgen_dict = {
    'norm':np.random.default_rng().normal,
    'uniform':np.random.default_rng().uniform
}

def gen_priors_for_predictive(howmany,dist,loc,scale):
    # howmany = how many sets you want
    # dist = the scipy.stats distribution
    # loc and scale the way they are defined for scipy.stats distributions
    # for some reason loc and scale here represent the left and right bounds of the uniform distr
    #   (unlike in plotting_incl_for_paper_figures/plot_prior_and_posterior_marginals.py's plot_priors,
    #    where loc is the leftmost bound and loc+scale is the rightmost bound)
    return randomgen_dict[dist.name](loc,scale,size=howmany)

margfile_dir = "../posterior_marginals_and_predictives/"
outdir_prior = "../posterior_marginals_and_predictives/prior_posterior_predictives_all/prior_predictives_all/"
outdir_post = "../posterior_marginals_and_predictives/prior_posterior_predictives_all/posterior_predictives_all/"

obs_list = ['NE_obs', 'NEv1_obs', 'NEv2_obs', 'NonNE_obs']

# this is tko_retired (retired = job took more than 28 days without finishing)
# 5 + 2*10 + 2*9 + 13*10 = 173
tko_retired = [263, 264, 383, 384, 406, 1044, 1360, 1490, 1514, 1520, 1524, 1526, 1585, 1655, 1657, 1660, 1667, 1688,
               1694, 1754, 1780, 1781, 1782, 1786, 1787, 1793, 1811, 1832, 1838, 1854, 1855, 1859, 1864, 1865, 1866,
               2009, 2025, 2026, 2335, 2336, 2353, 2354, 2499, 2500, 2517, 2518, 2608, 2935, 2937, 2938, 2942, 3005,
               3007, 3012, 3076, 3271, 3272, 3274, 3275, 3281, 3282, 3283, 3348, 3350, 3351, 3355, 3356, 3427, 3429,
               3434, 3435, 3549, 3551, 3552, 3554, 3562, 3803, 3805, 3810, 3811, 3873, 3875, 3880, 3944, 4139, 4140,
               4142, 4149, 4150, 4151, 4216, 4218, 4219, 4223, 4295, 4297, 4302, 4417, 4419, 4420, 4422, 4423, 4429,
               4430, 4431, 4509, 4510, 4518, 4520, 4545, 4546, 4556, 4777, 4780, 4787, 4788, 4798, 4808, 4834, 4844,
               4889, 4892, 4909, 4910, 4920, 4945, 4946, 4956, 5016, 5026, 5054, 5056, 5064, 5066, 5217, 5286, 5317,
               5318, 5322, 5334, 5346, 5356, 5382, 5392, 5438, 5441, 5448, 5449, 5461, 5471, 5501, 5511, 5563, 5566,
               5569, 5573, 5585, 5586, 5596, 5597, 5626, 5636, 5702, 5759, 5760, 5764, 5774, 5776, 5790, 5800, 5830,
               5833, 5840]

# these jobs finished but couldn't be read by pymultinest.Analyzer,
# so maybe pymultinest experienced an error in saving them...
tko_retired.extend([358, 1013, 1037, 1349, 2024, 2217, 2218]) #358, 1037, 1349, 2024, 2217, 2218 propagated from 09_generate_posterior_marginal_distributions.py

# this is rpm_retired
# 15 + 5*11 + 7*10 + 5*11 = 195
rpm_retired = [31, 46, 75, 378, 379, 458, 572, 573, 574, 575, 579, 670, 671, 672, 727, 1015, 1016, 1037, 1038, 1044,
               1331, 1332, 1353, 1354, 1417, 1422, 1487, 1488, 1491, 1492, 1514, 1515, 1516, 1517, 1518, 1519, 1520,
               1521, 1522, 1524, 1525, 1526, 1527, 1528, 1585, 1589, 1639, 1655, 1656, 1659, 1668, 1683, 1685, 1686,
               1688, 1689, 1690, 1691, 1692, 1693, 1694, 1695, 1736, 1780, 1782, 1783, 1785, 1787, 1788, 1789, 1811,
               1815, 1816, 1833, 1834, 1838, 1854, 1859, 1860, 1865, 2030, 2255, 2317, 2318, 2358, 2420, 2481, 2482,
               2522, 2645, 2707, 2708, 2766, 2935, 2941, 2942, 2943, 3005, 3006, 3007, 3012, 3013, 3075, 3076, 3271,
               3272, 3274, 3280, 3281, 3282, 3284, 3348, 3350, 3354, 3355, 3356, 3427, 3429, 3434, 3435, 3505, 3549,
               3551, 3552, 3561, 3562, 3563, 3564, 3803, 3804, 3805, 3810, 3811, 3873, 3875, 3880, 3881, 3882, 3944,
               3945, 4139, 4140, 4143, 4145, 4148, 4149, 4150, 4151, 4216, 4218, 4222, 4223, 4224, 4295, 4297, 4302,
               4373, 4417, 4419, 4420, 4422, 4423, 4428, 4429, 4430, 4432, 4517, 4553, 4805, 4841, 4873, 4917, 4953,
               5013, 5023, 5063, 5099, 5329, 5353, 5389, 5421, 5468, 5498, 5538, 5544, 5583, 5593, 5623, 5633, 5669,
               5771, 5787, 5797, 5867, 5873]

# these jobs finished but couldn't be read by pymultinest.Analyzer,
# so maybe pymultinest experienced an error in saving it...
rpm_retired.extend([2336, 2499, 3432])  #3432 propagated from 09_generate_posterior_marginal_distributions.py

# this is cla_retired
# 8 + 6*10 + 7*11 + 4*10 = 185
cla_retired = [68, 85, 91, 379, 412, 574, 580, 670, 1011, 1015, 1016, 1331, 1332, 1418, 1427, 1489, 1490, 1492, 1498,
               1499, 1500, 1514, 1515, 1524, 1525, 1526, 1586, 1588, 1635, 1655, 1657, 1658, 1682, 1684, 1694, 1734,
               1735, 1736, 1742, 1743, 1754, 1765, 1780, 1781, 1782, 1783, 1784, 1785, 1787, 1788, 1790, 1810, 1811,
               1832, 1833, 1838, 1854, 1859, 1866, 2030, 2075, 2194, 2255, 2358, 2401, 2402, 2419, 2420, 2482, 2522,
               2583, 2584, 2646, 2708, 2766, 2935, 2937, 2938, 2940, 2942, 2943, 3005, 3007, 3008, 3010, 3012, 3013,
               3076, 3271, 3272, 3273, 3274, 3275, 3276, 3278, 3282, 3283, 3284, 3348, 3350, 3351, 3355, 3356, 3427,
               3429, 3430, 3434, 3435, 3505, 3549, 3551, 3552, 3554, 3555, 3556, 3559, 3562, 3563, 3564, 3803, 3806,
               3808, 3810, 3811, 3873, 3875, 3876, 3878, 3880, 3881, 3944, 3946, 4139, 4140, 4142, 4143, 4144, 4146,
               4147, 4150, 4151, 4152, 4153, 4216, 4218, 4219, 4221, 4223, 4224, 4295, 4297, 4298, 4300, 4302, 4303,
               4419, 4420, 4422, 4423, 4424, 4426, 4427, 4430, 4432, 4433, 4517, 4553, 4805, 4841, 4874, 4953, 5013,
               5024, 5053, 5322, 5544, 5563, 5583, 5584, 5623, 5633, 5760, 5797, 5873, 5874]

# this job finished but couldn't be read by pymultinest.Analyzer,
# so maybe pymultinest experienced an error in saving it...
cla_retired.extend([2256])

retireddict = {
    'TKO':tko_retired,
    'RPM':rpm_retired,
    'cl_A':cla_retired
}

from helper_functions_and_files.modeldict_generator import generate_modeldict

modeldict = generate_modeldict()

modselection_postpred = {}
for i in ['TKO','RPM','cl_A']:
    modselection_postpred[i] = {
                        'NE_obs':pd.DataFrame(),
                        'NEv1_obs':pd.DataFrame(),
                        'NEv2_obs':pd.DataFrame(),
                        'NonNE_obs':pd.DataFrame()
                        }

modselection_sampledmarginals = {}
for i in ['TKO','RPM','cl_A']:
    modselection_sampledmarginals[i] = {
                        'NE_obs':pd.DataFrame(),
                        'NEv1_obs':pd.DataFrame(),
                        'NEv2_obs':pd.DataFrame(),
                        'NonNE_obs':pd.DataFrame()
                        }

# prior predictive
modselection_priorpred = {}
for i in ['TKO','cl_A','RPM']:
    modselection_priorpred[i] = {
            'NE_obs': pd.DataFrame(),
            'NEv1_obs': pd.DataFrame(),
            'NEv2_obs': pd.DataFrame(),
            'NonNE_obs': pd.DataFrame()
        }

topo_dict = {
    'TKO':('2','6','7'),
    'RPM':('1.','5','7'),
    'cl_A':('4','5','6','7')
}

# final model for each dataset's top topology
finalmodel = {'TKO':  1863,
              'RPM':  726,
              'cl_A': 2193
              }

# Generate posterior predictive (based on full parameter sets, called "manifold sampling" in Eydgahi et al 2013),
# posterior predictive based on independent sampling from posterior marginal distributions (called "independent sampling" in Eydgahi)
# and prior predictive (based on independent sampling from prior marginal distributions)

TOLERANCE = 1e-4
DOING_ALL = False #True     ## IF TRUE, DOING ALL TOPOLOGIES
old_m = 0   # this will be different if you have to restart the code because it exceeded memory or failed for some reason
            # to figure out, check what the last saved file is for the dataset (then will have to change the for loop as well)
for dset in ['TKO','RPM','cl_A']:#'TKO']:#, 'RPM']:#, 'cl_A']:
    ind = 1
    #postparamstosim only need to load once as long as it's for the correct dataset
    postparamstosim = pd.read_pickle(margfile_dir + dset + '_betafit_postmarg_params_and_probabilities_from_postequalweights.pklz',
                                     compression='gzip')
    ###
    # for top topologies
    if not DOING_ALL:
        # this code filters for only top topologies
        postparamstosim = postparamstosim[postparamstosim['model_starting_subtype_makeup_code'].str.startswith(topo_dict[dset])]
    ###
    for m in modeldict:
        if old_m == 0:      #first run (old_m == 0) should be m < old_m; anything past the first time this needs to be <=
            if m < old_m:
                continue
        else:
            if m <= old_m:  #first run should be <; anything past the first time this needs to be <=
                continue
        if m in retireddict[dset]:
            print(str(m) + ' is marked as not finished so will not be included')
            continue
        if not DOING_ALL:
            if len(np.where(postparamstosim.from_model==m)[0]) == 0:    # then it's not in the top topologies for this dset
                continue
        print('analyzing model ' + str(m) +' for dir ' + str(dset))
        model = modeldict[m]
        print(model)
        solver = ScipyOdeSimulator(model,integrator='lsoda',compiler='cython')
        param_values = np.array([p.value for p in model.parameters])
        #
        obs_list = ['NE_obs', 'NEv1_obs', 'NEv2_obs', 'NonNE_obs']
        #
        rates_mask = []
        for i in [x for x in model.parameters]:
            rates_mask.append('sp_' + i.name in [y for y in sampled_params_dict])
        #
        ### Prior predictive
        # "get" parameter sets
        parameters_idxs = [n for n, p in enumerate(model.parameters) if
                           not p.name in ['NEv2_0', 'NonNE_0', 'NEv1_0',
                                          'NE_0']]  # ok fine i had to hardcode initials sorry
        ndims = len(parameters_idxs)
        pddict = {}
        for dim in range(ndims):
            thisprior = [sampled_params_dict[i] for i in sampled_params_dict if i == 'sp_' + model.parameters[parameters_idxs[dim]].name][0]
            priors_to_simulate = []
            if thisprior.a == np.inf or thisprior.a == -np.inf: #normal distribution
                priors_to_simulate = gen_priors_for_predictive(500, thisprior.dist,
                                        thisprior.mean(), thisprior.std())
            else:
                priors_to_simulate = gen_priors_for_predictive(500, thisprior.dist,
                                        thisprior.ppf(0.00001),
                                        thisprior.ppf(0.99999)
                                        )
            if len(priors_to_simulate)==0:
                print ('Error: no priors returned for parameter '+model.parameters[parameters_idxs[dim]].name
                       +', check and there will likely be errors due to this')
            pddict[parameters_idxs[dim]] = priors_to_simulate
        df_x = pd.DataFrame(pddict)
        #
        tspan = np.linspace(0, 60, 101)
        #
        priorNE = pd.DataFrame(columns=tspan)
        priorNEv1 = pd.DataFrame(columns=tspan)
        priorNEv2 = pd.DataFrame(columns=tspan)
        priorNonNE = pd.DataFrame(columns=tspan)
        for i in range(0, len(df_x)):
            if i % 100 == 0:
                print(str(dset) + ', model ' + str(m) + ', ' + str(i))
            Y = np.copy(df_x.iloc[i])
            param_values[rates_mask] = 10 ** Y
            signal.alarm(30)
            try:
                sim = solver.run(param_values=param_values, tspan=tspan).all
            except TimeoutException as exc:
                continue
            else:
                signal.alarm(0)
            sim_data = {}
            all_lessthan1 = True
            for obs in ['NE_obs', 'NEv1_obs', 'NEv2_obs', 'NonNE_obs']:
                sim_data[obs] = sim[obs]  # [:new_end]
                if sim[obs][-1] > 1:
                    all_lessthan1 = False
            if sim['total_cells'][-1] < 100:
                print('not enough cells ' + str(sim['total_cells'][-1]))
            elif np.isnan(sim['total_cells'][-1]):
                print('too many cells computer couldnt handle ' + str(sim['total_cells'][-1]))
            elif all_lessthan1:
                print('something crashed out at the end ')
            else:
                sim_pct_run = {}
                for obs in ['NE_obs', 'NEv1_obs', 'NEv2_obs', 'NonNE_obs']:
                    sim_pct_run[obs] = np.true_divide(sim[obs], sim['total_cells'])
                not_eq = False
                y = np.column_stack(
                    (sim_pct_run['NE_obs'], sim_pct_run['NEv1_obs'], sim_pct_run['NEv2_obs'], sim_pct_run['NonNE_obs']))
                for idx in range(y.shape[1]):
                    derivative = (y[:, idx][-1] - y[:, idx][-75]) / (tspan[
                                                                         -1] - tspan[-75])
                    if abs(derivative) > TOLERANCE:
                        not_eq = True
                if not_eq:
                    print('not_eq')
                else:
                    priorNE.loc[i] = sim['NE_obs'] / sim['total_cells']
                    priorNEv1.loc[i] = sim['NEv1_obs'] / sim['total_cells']
                    priorNEv2.loc[i] = sim['NEv2_obs'] / sim['total_cells']
                    priorNonNE.loc[i] = sim['NonNE_obs'] / sim['total_cells']
        priorNE['from_model'] = m
        priorNEv1['from_model'] = m
        priorNEv2['from_model'] = m
        priorNonNE['from_model'] = m
        modselection_priorpred[dset]['NE_obs'] = pd.concat([modselection_priorpred[dset]['NE_obs'], priorNE])
        modselection_priorpred[dset]['NEv1_obs'] = pd.concat([modselection_priorpred[dset]['NEv1_obs'], priorNEv1])
        modselection_priorpred[dset]['NEv2_obs'] = pd.concat([modselection_priorpred[dset]['NEv2_obs'], priorNEv2])
        modselection_priorpred[dset]['NonNE_obs'] = pd.concat([modselection_priorpred[dset]['NonNE_obs'], priorNonNE])
        #  #
        ## Posterior predictive: setup
        to_sim = postparamstosim.loc[postparamstosim.from_model==m]
        pweight = to_sim.iloc[0].model_pp                       # will be the same no matter the index so just look at 0 to get one weight value
        makeup_code = to_sim.iloc[0].model_starting_subtype_makeup_code
        #
        pnamesandorder = [names_dict['sp_'+p.name] for p in model.parameters if not p.name in ['NE_0','NEv1_0','NEv2_0','NonNE_0']]
        # Posterior predictive: independent sampling
        #
        NE = pd.DataFrame(columns=tspan)
        NEv1 = pd.DataFrame(columns=tspan)
        NEv2 = pd.DataFrame(columns=tspan)
        NonNE = pd.DataFrame(columns=tspan)
        #
        # ok so instead sample 500x from each param (so first sample could be, index 0 for division_A, index 10 for division_A2, index 154 for die_A...)
        sampled_dict = {}
        for i in pnamesandorder:
            sampled_dict[i] = list(to_sim[i].sample(500,replace=True))
        sampleddf = pd.DataFrame(sampled_dict)
        for i in range(0,len(sampleddf)):
            if i % 500 == 0:
                print('model '+str(m)+', '+str(i))
            Y = np.copy(sampleddf.iloc[i])
            param_values[rates_mask] = 10 ** Y
            signal.alarm(60)
            try:
                sim = solver.run(param_values=param_values,tspan=tspan).all
            except TimeoutException as exc:
                # this should not add anything to the df
                continue
            else:
                signal.alarm(0)
            NE.loc[i] = sim['NE_obs']/sim['total_cells']
            NEv1.loc[i] = sim['NEv1_obs']/sim['total_cells']
            NEv2.loc[i] = sim['NEv2_obs']/sim['total_cells']
            NonNE.loc[i] = sim['NonNE_obs']/sim['total_cells']
        NE['post_prob'] = pweight
        NE['from_model'] = m
        NE['model_starting_subtype_makeup_code'] = makeup_code
        NEv1['post_prob'] = pweight
        NEv1['from_model'] = m
        NEv1['model_starting_subtype_makeup_code'] = makeup_code
        NEv2['post_prob'] = pweight
        NEv2['from_model'] = m
        NEv2['model_starting_subtype_makeup_code'] = makeup_code
        NonNE['post_prob'] = pweight
        NonNE['from_model'] = m
        NonNE['model_starting_subtype_makeup_code'] = makeup_code
        modselection_sampledmarginals[dset]['NE_obs'] = pd.concat([modselection_sampledmarginals[dset]['NE_obs'], NE])
        modselection_sampledmarginals[dset]['NEv1_obs'] = pd.concat([modselection_sampledmarginals[dset]['NEv1_obs'], NEv1])
        modselection_sampledmarginals[dset]['NEv2_obs'] = pd.concat([modselection_sampledmarginals[dset]['NEv2_obs'], NEv2])
        modselection_sampledmarginals[dset]['NonNE_obs'] = pd.concat([modselection_sampledmarginals[dset]['NonNE_obs'], NonNE])
        # Posterior predictive: parameter set / manifold sampling
        #
        NE = pd.DataFrame(columns=tspan)
        NEv1 = pd.DataFrame(columns=tspan)
        NEv2 = pd.DataFrame(columns=tspan)
        NonNE = pd.DataFrame(columns=tspan)
        #
        for i in range(0,500):  #len(to_sim[pnamesandorder]) #is 1000, but i only want 500
            if i % 500 == 0:
                print('model '+str(m)+', '+str(i))
            Y = np.copy(to_sim[pnamesandorder].iloc[i])
            param_values[rates_mask] = 10 ** Y
            signal.alarm(60)
            try:
                sim = solver.run(param_values=param_values,tspan=tspan).all
            except TimeoutException as exc:
                # this should not add anything to the df
                continue
            else:
                signal.alarm(0)
            NE.loc[i] = sim['NE_obs']/sim['total_cells']
            NEv1.loc[i] = sim['NEv1_obs']/sim['total_cells']
            NEv2.loc[i] = sim['NEv2_obs']/sim['total_cells']
            NonNE.loc[i] = sim['NonNE_obs']/sim['total_cells']
        NE['post_prob'] = pweight
        NE['from_model'] = m
        NE['model_starting_subtype_makeup_code'] = makeup_code
        NEv1['post_prob'] = pweight
        NEv1['from_model'] = m
        NEv1['model_starting_subtype_makeup_code'] = makeup_code
        NEv2['post_prob'] = pweight
        NEv2['from_model'] = m
        NEv2['model_starting_subtype_makeup_code'] = makeup_code
        NonNE['post_prob'] = pweight
        NonNE['from_model'] = m
        NonNE['model_starting_subtype_makeup_code'] = makeup_code
        modselection_postpred[dset]['NE_obs'] = pd.concat([modselection_postpred[dset]['NE_obs'], NE])
        modselection_postpred[dset]['NEv1_obs'] = pd.concat([modselection_postpred[dset]['NEv1_obs'], NEv1])
        modselection_postpred[dset]['NEv2_obs'] = pd.concat([modselection_postpred[dset]['NEv2_obs'], NEv2])
        modselection_postpred[dset]['NonNE_obs'] = pd.concat([modselection_postpred[dset]['NonNE_obs'], NonNE])
        if (ind % 250 == 0 and not ind == 0) or (m == finalmodel[dset] and DOING_ALL) or m == 5890:
            if not DOING_ALL:   # i.e. if only doing top topologies
                print('saving ' + str(old_m) + ' to ' + str(m) + ', ' + str(ind) + ' models...')
                # prior predictives
                print(outdir_prior + dset + '_trajectories_as_priorpredictive_from_model_'
                      + str(old_m) + '_to_' + str(m) + '_toptopologies.pickle')
                if not os.path.exists(outdir_prior):
                    os.makedirs(outdir_prior)
                with open(outdir_prior + dset + '_trajectories_as_priorpredictive_from_model_'
                          + str(old_m) + '_to_' + str(m) + '_toptopologies.pickle','wb') as fp:
                    pickle.dump(modselection_priorpred[dset], fp)
                # predictives from sampled parameter sets (independent sampling)
                print(outdir_post + dset + '_trajectories_as_postpredictive_from_independentsampling_from_model_'
                      + str(old_m) + '_to_' + str(m) + '_toptopologies.pickle')
                if not os.path.exists(outdir_post):
                    os.makedirs(outdir_post)
                with open(outdir_post + dset + '_trajectories_as_postpredictive_from_independentsampling_from_model_'
                          + str(old_m) + '_to_' + str(m) + '_toptopologies.pickle','wb') as fp:
                    pickle.dump(modselection_sampledmarginals[dset], fp)
                # predictives from parameter sets (manifold sampling)
                print(outdir_post + dset + '_trajectories_as_postpredictive_from_postequalweights_from_model_'
                      + str(old_m) + '_to_' + str(m) + '_toptopologies.pickle')
                with open(outdir_post + dset + '_trajectories_as_postpredictive_from_postequalweights_from_model_'
                          + str(old_m) + '_to_' + str(m) + '_toptopologies.pickle','wb') as fp:
                    pickle.dump(modselection_postpred[dset], fp)
            else:   #so, if DOING_ALL
                print('saving ' + str(old_m) + ' to ' + str(m) + ', ' + str(ind) + ' models...')
                # prior predictives
                print(outdir_prior + dset + '_trajectories_as_priorpredictive_from_model_'
                      + str(old_m) + '_to_' + str(m) + '_alltopologies.pickle')
                if not os.path.exists(outdir_prior):
                    os.makedirs(outdir_prior)
                with open(outdir_prior + dset + '_trajectories_as_priorpredictive_from_model_'
                          + str(old_m) + '_to_' + str(m) + '_alltopologies.pickle','wb') as fp:
                    pickle.dump(modselection_priorpred[dset], fp)
                # predictives from sampled parameter sets (independent sampling)
                print(outdir_post + dset + '_trajectories_as_postpredictive_from_independentsampling_from_model_'
                      + str(old_m) + '_to_' + str(m) + '_alltopologies.pickle')
                if not os.path.exists(outdir_post):
                    os.makedirs(outdir_post)
                with open(outdir_post + dset + '_trajectories_as_postpredictive_from_independentsampling_from_model_'
                          + str(old_m) + '_to_' + str(m) + '_alltopologies.pickle','wb') as fp:
                    pickle.dump(modselection_sampledmarginals[dset], fp)
                # predictives from parameter sets (manifold sampling)
                print(outdir_post + dset + '_trajectories_as_postpredictive_from_postequalweights_from_model_'
                      + str(old_m) + '_to_' + str(m) + '_alltopologies.pickle')
                with open(outdir_post + dset + '_trajectories_as_postpredictive_from_postequalweights_from_model_'
                          + str(old_m) + '_to_' + str(m) + '_alltopologies.pickle','wb') as fp:
                    pickle.dump(modselection_postpred[dset], fp)
            # restart for new ones to save
            modselection_postpred[dset] = {
                    'NE_obs': pd.DataFrame(),
                    'NEv1_obs': pd.DataFrame(),
                    'NEv2_obs': pd.DataFrame(),
                    'NonNE_obs': pd.DataFrame()
                }
            modselection_sampledmarginals[dset] = {
                    'NE_obs': pd.DataFrame(),
                    'NEv1_obs': pd.DataFrame(),
                    'NEv2_obs': pd.DataFrame(),
                    'NonNE_obs': pd.DataFrame()
                }
            modselection_priorpred[dset] = {
                    'NE_obs': pd.DataFrame(),
                    'NEv1_obs': pd.DataFrame(),
                    'NEv2_obs': pd.DataFrame(),
                    'NonNE_obs': pd.DataFrame()
                }
            old_m = m
            print('old_m is now '+str(old_m))
        ind += 1
    print('moving on to new dataset')
    old_m = 0
