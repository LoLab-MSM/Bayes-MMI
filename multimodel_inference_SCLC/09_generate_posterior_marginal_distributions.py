import pickle
import numpy as np
import pandas as pd
import pymultinest
import sys
import os

# add this Bayes-MMI directory to the path to be able to import from helper_functions_and_files
sys.path.append('/home/beiksp/Bayes-MMI')
sys.path.append('/home/beiksp/maybe_pycharm_running/')

with open('../helper_functions_and_files/all_possible_sampled_params_dict.pickle', 'rb') as p:
    sampled_params_dict = pickle.load(p)

analyzed_file_dir = "../files_generated_in_MMI_sclc/"
mmi_indir = "../pymultinest_results/"
outdir = "../posterior_marginals_and_predictives/posterior_marginals_all/"

names_dict = {}
for n, i in enumerate([x for x in sampled_params_dict]):
    param_toprint = i
    ptp = param_toprint.split('sp_')[1]
    paramtoprint = ptp.split('_diff')
    if len(paramtoprint) == 1:
        paramtoprint = ptp.replace('cell_1kc', 'cell')
        finalparam = paramtoprint.replace('division_0_N', 'division_N').replace('die_0_N', 'die_N').replace(
            'cell_0', 'baseline').replace('cell_1', 'altered').replace('cell_2', 'equil_assn')
    else:
        paramtoprint = ptp.replace('_cell_1kf', '_cell')
        altered_details = ''
        if '_1' in paramtoprint:
            altered_details = '_altered'
        elif '_2' in paramtoprint:
            altered_details = '_equil_assn'
        finalparam = paramtoprint.replace('uni_0_', '').replace('cell_N', 'to_N').replace(
            'diff_cell_0', 'baseline').replace('diff_cell_1', 'altered').replace('diff_cell_2', 'equil_assn')
    finalparam = finalparam.replace('NonNE', 'Y').replace('NEv2', 'A2').replace('NEv1', 'N').replace('NE', 'A')
    names_dict[i] = finalparam

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

# this job finished but couldn't be read by pymultinest.Analyzer,
# so maybe pymultinest experienced an error in saving it...
tko_retired.extend([1013])

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

# this job finished but couldn't be read by pymultinest.Analyzer,
# so maybe pymultinest experienced an error in saving it...
rpm_retired.extend([3432])

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

retireddict = {
    'TKO': tko_retired,
    'RPM': rpm_retired,
    'cl_A': cla_retired
}

from helper_functions_and_files.modeldict_generator import generate_modeldict

modeldict = generate_modeldict()

res_dict = {
    'TKO': pd.read_pickle(
        analyzed_file_dir+'/results_fromNS_gathered_TKO_addlanalyses.pickle'),
    'RPM': pd.read_pickle(
        analyzed_file_dir+'/results_fromNS_gathered_RPM_addlanalyses.pickle'),
    'cl_A': pd.read_pickle(
        analyzed_file_dir+'/results_fromNS_gathered_clA_addlanalyses.pickle')
}

modselection_postmarg = {
    'TKO': pd.DataFrame(),
    'RPM': pd.DataFrame(),
    'cl_A': pd.DataFrame()
}

dfdict = pd.read_pickle('../helper_functions_and_files/all_5891_models_in_dataframe_with_subtype_starting_makeup_code.pickle')

for dset in ['TKO', 'RPM', 'cl_A']:
    old_m = 0  # this will be different if you have to restart the code because it exceeded memory or failed for some reason
    # to figure out, check what the last saved file is for the appropriate dataset (and then will have to change the for loop as well)
    ind = 1
    for m in modeldict:
        print(m)
        if old_m == 0:      #first run (old_m == 0) should be m < old_m; anything past the first time this needs to be <=
            if m < old_m:
                continue
        else:
            if m <= old_m:  #first run should be <; anything past the first time this needs to be <=
                continue
        if m in retireddict[dset]:
            print(str(m) + ' is marked as not finished so will not be included')
            continue
        ##
        model = modeldict[m]
        param_values = np.array([p.value for p in model.parameters])
        sp_list = []
        for i in [x for x in sampled_params_dict]:
            if i.split('sp_')[1] in [y.name for y in model.parameters]:
                # need the tuples here to include the names and not just the scipy stats object
                sp_list.append((i,sampled_params_dict[i]))
        modeldir = mmi_indir +'/' + dset + '/'
        sfr = "" + modeldir + "/dir_model_" + str(m) + "/model_" + str(m) + "_"
        a = pymultinest.Analyzer(len(sp_list), outputfiles_basename=sfr)
        pos = pd.DataFrame(np.array([i for i in a.get_equal_weighted_posterior()]),
                           columns=[names_dict[i[0]] for i in sp_list] + ['paramset_likelihood'])
        pos = pos.sort_values('paramset_likelihood', ascending=False)[:1000]  # get the top 1000
        pos.reset_index(inplace=True, drop=True)
        # bc multiple paramsets per model
        pos['from_model'] = m
        # posterior model probabilities
        pos['model_pp'] = res_dict[dset].loc[m].posterior_prob
        #
        pos['model_starting_subtype_makeup_code'] = dfdict.loc[m].subtype_starting_and_makeup_code
        modselection_postmarg[dset] = pd.concat([modselection_postmarg[dset], pos], ignore_index=True)
        print('adding m ' + str(m))
        if (ind % 1000 == 0 and not ind == 0) or m == 5890:
            print('saving ' + str(dset) + ' ' + str(old_m) + ' to ' + str(m) + '...')
            if not os.path.exists(outdir + '/' + dset + '/'):
                os.makedirs(outdir + '/' + dset + '/')
            with open(
                    outdir + '/' + dset + '/' + dset +
                    '_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_'
                    + str(old_m) + '_to_' + str(m) + '.pickle', 'wb') as fp:
                pickle.dump(modselection_postmarg[dset], fp)
            ## restart for new ones to save
            modselection_postmarg[dset] = pd.DataFrame()
            old_m = m
        ind += 1

