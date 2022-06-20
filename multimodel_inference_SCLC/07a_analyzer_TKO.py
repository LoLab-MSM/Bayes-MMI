from pysb.simulator import ScipyOdeSimulator
import numpy as np
from scipy.stats import norm, uniform, beta
import copy
import pandas as pd
import pickle
import pymultinest
import sys
import signal

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

# remove any that haven't finished

# as of 4/7/22
notdone = [24, 26, 34, 36, 39, 40, 41, 136, 138, 141, 143, 156, 158, 161, 163, 268, 270, 271, 274, 288, 290,
           293, 295, 542, 547, 549, 562, 564, 613, 615, 628, 630, 631, 679, 681, 682, 689, 694, 696, 1336, 1337,
           1441, 1638, 1640, 1666, 1668, 1728, 1731, 1733, 1736, 1738, 1826, 1828, 1841, 1843, 1941, 1943, 1947,
           1951, 1953, 1954, 1956, 1958, 2046, 2048, 2049, 2061, 2063, 2129, 2171, 2173, 2176, 2178, 2266, 2268,
           2278, 2281, 2283, 2386, 2391, 2393, 2396, 2398, 2486, 2488, 2501, 2503, 2563, 2601, 2603, 2607, 2611,
           2613, 2616, 2618, 2701, 2703, 2706, 2707, 2708, 2716, 2718, 2721, 2723, 2812, 2823, 2831, 2833, 2836,
           2838, 2921, 2923, 2926, 2928, 2936, 2938, 2941, 2943, 3004, 3041, 3044, 3051, 3053, 3056, 3058, 3141,
           3143, 3146, 3148, 3156, 3158, 3161, 3163, 3285, 3287, 3290, 3292, 3305, 3307, 3310, 3312, 3390, 3405,
           3407, 3410, 3412, 3420, 3422, 3425, 3427, 3528, 3549, 3551, 3554, 3556, 3569, 3571, 3574, 3576, 3669,
           3671, 3674, 3676, 3684, 3686, 3689, 3691, 3792, 3813, 3815, 3818, 3820, 3833, 3835, 3838, 3840, 3945,
           3947, 3948, 3950, 3953, 3965, 3967, 3970, 3972, 4065, 4067, 4070, 4072, 4080, 4082, 4085, 4087, 4125,
           4131, 4133, 4136, 4137, 4138, 4139, 4146, 4148, 4151, 4153, 4323, 4329, 4330, 4331, 4334, 4335, 4336,
           4337, 4344, 4346, 4349, 4351, 4352, 4643, 4647, 4694, 4695, 4756, 4757, 4762, 4807, 4867, 4872, 4914,
           4916, 4917, 4989, 5127, 5132, 5134, 5155, 5160, 5162, 5183, 5188, 5190, 5211, 5216, 5218, 5251, 5296,
           5298, 5301, 5303, 5311, 5313, 5396, 5398, 5493, 5497, 5505, 5508, 5509, 5523, 5580, 5581, 5584, 5585,
           5599, 5600, 5602, 5622, 5636, 5638, 5731, 5800, 5801, 5806, 5808, 5812, 5822, 5824, 5828, 5829, 5845,
           5846, 5850, 5851, 5852, 5856, 5857, 5858, 5859, 5888, 5889, 5890, 5891, 5892, 5893, 5894, 5895, 5896,
           5898, 5899, 5901, 5902, 5903, 5906, 5907, 5930, 5931, 5982, 5983, 5984, 5986, 5987, 5988, 5989, 6001,
           6003, 6006, 6008, 6106, 6108, 6109, 6121, 6123, 6216, 6217, 6288, 6289, 6290, 6292, 6293, 6294, 6295,
           6312, 6314, 6419, 6421, 6436, 6482, 6485, 6510, 6511, 6514, 6515, 6518, 6519, 6534, 6536, 6552, 6553,
           6555, 6556, 6557, 6562, 6563, 6564, 6566, 6567, 6570, 6571, 6594, 6595, 6596, 6613, 6614, 6615, 6618,
           6642, 6649, 6657, 6659, 6661, 6677, 6687, 6688, 6690, 6691, 6694, 6695, 6701, 6703, 6712, 6748, 6751,
           6753, 6754, 6846, 6944, 6955, 6956, 6981, 6982, 6983, 6984, 6986, 6987, 6988, 6998, 6999, 7000, 7030,
           7031, 7032, 7034, 7048, 7049, 7050, 7053, 7075, 7096, 7098, 7114, 7115, 7116, 7162, 7163, 7164, 7174,
           7175, 7176, 7330, 7331, 7332, 7333, 7362, 7363, 7364, 7365, 7379, 7380, 7381, 7395, 7396, 7397, 7487,
           7490, 7596, 7597, 7598, 7599, 7612, 7613, 7614, 7615, 7616, 7617, 7618, 7619, 7620, 7706, 7707, 7708,
           7721, 7722, 7723, 7724, 7725, 7726, 7727, 7728, 7729, 7757, 7761, 7762, 7767, 7769, 7799, 7802, 7806,
           7807, 7829, 7830, 7834, 7835, 7838, 7839, 7840, 7841, 7854, 7857, 7870, 7880, 7881, 7882, 7886, 7889,
           7890, 7891, 7892, 7893, 7894, 7964, 7965, 7966, 7976, 7977, 7978, 7979, 7980, 7981, 8063, 8064, 8084,
           8098, 8099, 8115, 8130, 8142, 8143, 8144, 8145, 8157, 8158, 8159, 8160, 8161, 8162, 8163, 8179, 8193,
           8194, 8210, 8224, 8225, 8232, 8234, 8235, 8237, 8238, 8239, 8240, 8250, 8252, 8254, 8255, 8256, 8257,
           8258, 8274, 8282, 8284, 8285, 8305, 8312, 8313, 8314, 8315, 8316, 8346, 8358, 8359, 8361, 8362, 8366,
           8373, 8374, 8375, 8376, 8377, 8391, 8392, 8396, 8405, 8451, 8452, 8453, 8454, 8455, 8534, 8535, 8536,
           8537, 8538, 8539, 8540, 8541, 8542, 8543, 8544, 8545, 8546, 8547, 8548, 8549, 8550, 8551, 8552, 8567,
           8568, 8569, 8570, 8571, 8572, 8573, 8574, 8590, 8591, 8592, 8593, 8594, 8595, 8596, 8597, 8598, 8599,
           8600, 8601, 8602, 8603, 8604, 8605, 8606, 8607, 8608, 8623, 8624, 8625, 8626, 8627, 8628, 8629, 8630,
           8631, 8632, 8633, 8634, 8635, 8636, 8637, 8638, 8639, 8640, 8641, 8642, 8643, 8644, 8645, 8646, 8647,
           8648, 8649, 8650, 8651, 8652, 8653, 8699, 8700, 8701, 8702, 8703, 8704, 8783, 8784, 8785, 8786, 8787,
           8788, 8789, 8790, 8791, 8792, 8793, 8794, 8795, 8796, 8797, 8798, 8799, 8800, 8801, 8816, 8817, 8818,
           8819, 8820, 8821, 8822, 8823, 8839, 8840, 8841, 8842, 8843, 8844, 8845, 8846, 8847, 8848, 8849, 8850,
           8851, 8852, 8853, 8854, 8855, 8856, 8857, 8872, 8873, 8874, 8875, 8876, 8877, 8878, 8879, 8880, 8881,
           8882, 8883, 8884, 8885, 8886, 8887, 8888, 8889, 8890, 8891, 8892, 8893, 8894, 8895, 8896, 8897, 8898,
           8899, 8900, 8901, 8902, 8918, 8920, 8922, 8923, 8924, 8933, 8951, 8975, 8978, 8980, 8981, 8989, 8990,
           8992, 9031, 9033, 9066, 9089, 9090, 9091, 9092, 9093, 9094, 9102, 9103, 9104, 9105, 9106, 9107, 9122,
           9129, 9145, 9146, 9147, 9148, 9149, 9150, 9158, 9159, 9160, 9161, 9162, 9163, 9178, 9185, 9201, 9202,
           9203, 9205, 9206, 9214, 9215, 9216, 9217, 9218, 9219, 9252]

for i in notdone:
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
                continue
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


with open('../helper_functions_and_files/all_possible_sampled_params.pickle', 'rb') as p:
    sampled_params_list = pickle.load(p)

# per model

results_dict = {}

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
        rates_mask.append('sp_' + i.name in [y.name for y in sampled_params_list])
    #
    sp_list = []
    for i in [x for x in sampled_params_list]:
        if i.name.split('sp_')[1] in [y.name for y in model.parameters]:
            sp_list.append(i)
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
        #
        # BIC estimate
        k = len(sp_list)
        # n_data = number of observations in the data... so the number of cibersort bars per data
        # i dont remember what that is so just putting 40
        n_data = 40
        BIC = np.log(n_data) * k - 2. * ml
        results_dict[m]['BIC'] = BIC
        #
        # Not currently using INS but why not save it in case
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
full_rez_dict.to_pickle(outdir+'compare_TKO_gleipnir_results_subset_betafit_to9264_somemissing_4_7_2022.pickle')

# with open(outdir+'compare_clA_gleipnir_results_subset_betafit_12_10_2020_DIC_calc_values_in_case.pickle','wb') as f:
#    pickle.dump(DIC_dict,f)