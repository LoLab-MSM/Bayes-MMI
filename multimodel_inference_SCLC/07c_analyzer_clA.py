from pysb.simulator import ScipyOdeSimulator
import numpy as np
from scipy.stats import norm, uniform, beta, expon
import copy
import pandas as pd
import pickle
import pymultinest
import sys
import signal

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

# remove any that you dont have yet

# as of 6/20/22
notdone = [643, 1279, 1281, 1282, 1337, 1338, 1439, 1442, 1553, 1579, 1583, 1633, 1638, 1640, 1657, 1659, 1661,
           1666, 1668, 2823, 2841, 2888, 4410, 4412, 4436, 4439, 4469, 4470, 4496, 4499, 4529, 4530, 4556, 4559,
           4595, 4598, 4638, 4640, 4641, 4644, 4647, 4652, 4693, 4694, 4695, 4696, 4697, 4699, 4702, 4754, 4757,
           4804, 4806, 4863, 4872, 4913, 4914, 4916, 4917, 4922, 4985, 4987, 4989, 4993, 5049, 5053, 5065, 5069,
           5081, 5085, 5251, 5267, 5272, 5273, 5274, 5276, 5277, 5285, 5288, 5298, 5303, 5306, 5308, 5361, 5362,
           5365, 5379, 5380, 5381, 5382, 5383, 5396, 5398, 5401, 5403, 5493, 5494, 5523, 5526, 5528, 5581, 5582,
           5584, 5585, 5599, 5604, 5712, 5713, 5714, 5718, 5719, 5720, 5724, 5725, 5726, 5728, 5734, 5735, 5736,
           5740, 5741, 5742, 5756, 5757, 5758, 5762, 5763, 5764, 5770, 5772, 5778, 5779, 5780, 5784, 5785, 5786,
           5800, 5801, 5802, 5808, 5822, 5823, 5824, 5828, 5829, 5830, 5844, 5845, 5846, 5850, 5851, 5852, 5868,
           5874, 5888, 5889, 5891, 5892, 5893, 5895, 5896, 5901, 5902, 5903, 5906, 5907, 5916, 5917, 5918, 5919,
           5930, 5931, 6510, 6511, 6512, 6513, 6514, 6516, 6517, 6518, 6519, 6534, 6552, 6553, 6554, 6555, 6556,
           6557, 6559, 6561, 6562, 6563, 6564, 6565, 6566, 6567, 6570, 6571, 6586, 6595, 6596, 6613, 6614, 6615,
           6616, 6617, 6618, 6657, 6658, 6660, 6661, 6662, 6666, 6670, 6671, 6687, 6688, 6689, 6694, 6695, 6711,
           6712, 6716, 6718, 6719, 6720, 6722, 6723, 6724, 6725, 6726, 6739, 6746, 6751, 6753, 6766, 6767, 6768,
           6778, 6779, 6780, 6811, 6812, 6814, 6815, 6828, 6829, 6830, 6831, 6833, 6846, 6848, 6876, 6877, 6878,
           6894, 6895, 6896, 6944, 6946, 6947, 6967, 6970, 6971, 6972, 6974, 6975, 6986, 6987, 6988, 6998, 6999,
           7000, 7032, 7034, 7035, 7045, 7046, 7049, 7052, 7097, 7098, 7114, 7116, 7162, 7163, 7164, 7174, 7175,
           7176, 7228, 7229, 7230, 7240, 7241, 7242, 7378, 7379, 7380, 7381, 7394, 7395, 7396, 7397, 7398, 7399,
           7400, 7401, 7402, 7436, 7437, 7438, 7442, 7467, 7468, 7469, 7470, 7474, 7487, 7510, 7511, 7597, 7598,
           7599, 7612, 7613, 7614, 7615, 7616, 7617, 7618, 7619, 7620, 7706, 7707, 7708, 7722, 7723, 7724, 7725,
           7726, 7727, 7728, 7729, 7757, 7766, 7767, 7797, 7798, 7807, 7829, 7830, 7831, 7832, 7833, 7835, 7836,
           7838, 7839, 7840, 7841, 7854, 7870, 7886, 7889, 7891, 7893, 7894, 7922, 7923, 7924, 7952, 7953, 7954,
           7964, 7965, 7966, 7976, 7977, 7978, 7979, 7980, 7981, 8011, 8053, 8096, 8097, 8098, 8099, 8115, 8127,
           8128, 8129, 8130, 8142, 8143, 8144, 8145, 8157, 8158, 8159, 8160, 8162, 8163, 8179, 8191, 8192, 8193,
           8194, 8210, 8222, 8223, 8224, 8225, 8237, 8238, 8239, 8240, 8252, 8253, 8254, 8255, 8257, 8258, 8288,
           8289, 8320, 8350, 8351, 8450, 8451, 8452, 8453, 8454, 8455, 8460, 8461, 8534, 8535, 8536, 8537, 8538,
           8539, 8540, 8541, 8542, 8543, 8544, 8545, 8546, 8547, 8548, 8549, 8550, 8551, 8552, 8568, 8569, 8570,
           8571, 8572, 8573, 8574, 8590, 8591, 8592, 8593, 8594, 8595, 8596, 8597, 8598, 8599, 8600, 8601, 8602,
           8603, 8604, 8605, 8606, 8607, 8608, 8623, 8624, 8625, 8626, 8627, 8628, 8629, 8630, 8631, 8632, 8633,
           8634, 8635, 8636, 8637, 8638, 8639, 8640, 8641, 8642, 8643, 8644, 8645, 8646, 8647, 8648, 8649, 8650,
           8651, 8652, 8653, 8699, 8700, 8701, 8702, 8703, 8704, 8709, 8710, 8783, 8784, 8785, 8786, 8787, 8788,
           8789, 8790, 8791, 8792, 8793, 8794, 8795, 8796, 8797, 8798, 8799, 8800, 8801, 8817, 8818, 8819, 8820,
           8821, 8822, 8823, 8839, 8840, 8841, 8842, 8843, 8844, 8845, 8846, 8847, 8848, 8849, 8850, 8851, 8852,
           8853, 8854, 8855, 8856, 8857, 8872, 8873, 8874, 8875, 8876, 8877, 8878, 8879, 8880, 8881, 8882, 8883,
           8884, 8885, 8886, 8887, 8888, 8889, 8890, 8891, 8892, 8893, 8894, 8895, 8896, 8897, 8898, 8899, 8900,
           8901, 8902, 8923, 8934, 8935, 8948, 8949, 8950, 8951, 8952, 8953, 8959, 8978, 8979, 8980, 8981, 8992,
           9006, 9007, 9008, 9009, 9010, 9016, 9031, 9034, 9036, 9062, 9063, 9064, 9065, 9066, 9067, 9073, 9096,
           9098, 9100, 9101, 9102, 9106, 9122, 9129, 9154, 9159, 9178, 9214, 9215, 9263, 9264, 9267, 9268, 9275,
           9276, 9285, 9286, 9293, 9294, 9313, 9316, 9317, 9320, 9321, 9324, 9325]

for i in notdone:
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
                continue
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
        # n_data = number of observations in the data... so the number of sage datapoints to make the cibersort data.
        # i dont remember what that is so just putting 40 for now
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
full_rez_dict.to_pickle(outdir+'compare_clA_gleipnir_results_subset_betafit_to9264_somemissing_4_7_2022.pickle')

# with open(outdir+'compare_clA_gleipnir_results_subset_betafit_12_10_2020_DIC_calc_values_in_case.pickle','wb') as f:
#    pickle.dump(DIC_dict,f)