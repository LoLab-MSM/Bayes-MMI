from pysb.simulator import ScipyOdeSimulator
import numpy as np
from scipy.stats import norm, uniform, beta, expon
import copy
import pandas as pd
import pickle
import pymultinest
import sys
import signal

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

# remove any that haven't finished

# as of 6/20/22
notdone = [1128, 1281, 1282, 1334, 1335, 1336, 1337, 1338, 1438, 1439, 1446, 1546, 1567, 1568, 1570, 4409, 4472,
           4532, 4533, 4804, 4805, 4806, 4807, 4812, 4986, 4988, 5251, 5264, 5265, 5272, 5273, 5274, 5275, 5276,
           5277, 5285, 5286, 5287, 5288, 5289, 5301, 5361, 5362, 5363, 5364, 5365, 5379, 5380, 5381, 5382, 5383,
           5397, 5398, 5399, 5401, 5402, 5403, 5492, 5495, 5507, 5516, 5518, 5580, 5583, 5598, 5601, 5712, 5713,
           5714, 5718, 5719, 5720, 5725, 5726, 5727, 5730, 5731, 5734, 5735, 5736, 5740, 5741, 5742, 5756, 5757,
           5758, 5762, 5763, 5764, 5769, 5774, 5776, 5778, 5779, 5780, 5784, 5785, 5786, 5807, 5812, 5817, 5888,
           5889, 5890, 5891, 5892, 5893, 5894, 5895, 5902, 5903, 5906, 5907, 5916, 5930, 5931, 6510, 6511, 6512,
           6513, 6518, 6519, 6531, 6552, 6553, 6556, 6557, 6560, 6561, 6562, 6563, 6564, 6565, 6566, 6567, 6570,
           6594, 6595, 6613, 6614, 6615, 6616, 6617, 6625, 6633, 6634, 6641, 6657, 6659, 6661, 6666, 6667, 6670,
           6687, 6688, 6689, 6714, 6716, 6722, 6723, 6724, 6726, 6727, 6734, 6735, 6736, 6739, 6766, 6767, 6768,
           6778, 6779, 6780, 6810, 6811, 6812, 6813, 6814, 6815, 6828, 6829, 6830, 6831, 6832, 6833, 6846, 6848,
           6876, 6877, 6878, 6894, 6895, 6896, 6942, 6943, 6944, 6945, 6946, 6954, 6955, 6956, 6957, 6958, 6959,
           6966, 6967, 6968, 6969, 6971, 6972, 6973, 6974, 6986, 6987, 6988, 6998, 6999, 7000, 7030, 7031, 7032,
           7033, 7048, 7051, 7052, 7096, 7097, 7098, 7114, 7115, 7162, 7163, 7164, 7174, 7175, 7176, 7228, 7229,
           7230, 7240, 7241, 7242, 7378, 7379, 7380, 7381, 7394, 7395, 7396, 7397, 7398, 7399, 7400, 7401, 7402,
           7435, 7436, 7437, 7438, 7441, 7467, 7468, 7469, 7470, 7473, 7474, 7511, 7548, 7549, 7550, 7551, 7583,
           7596, 7597, 7598, 7599, 7613, 7614, 7615, 7659, 7660, 7691, 7700, 7705, 7706, 7707, 7708, 7721, 7722,
           7723, 7724, 7757, 7759, 7760, 7761, 7762, 7764, 7766, 7767, 7769, 7797, 7799, 7803, 7804, 7805, 7806,
           7807, 7808, 7829, 7831, 7832, 7834, 7835, 7837, 7838, 7839, 7840, 7841, 7848, 7854, 7857, 7864, 7871,
           7886, 7888, 7889, 7893, 7909, 7910, 7911, 7912, 7922, 7923, 7924, 7952, 7953, 7954, 7966, 7979, 7980,
           7981, 7998, 8083, 8084, 8096, 8097, 8098, 8115, 8127, 8128, 8129, 8130, 8144, 8145, 8178, 8179, 8191,
           8192, 8194, 8210, 8222, 8223, 8224, 8225, 8239, 8240, 8288, 8289, 8319, 8320, 8350, 8351, 8450, 8451,
           8452, 8453, 8454, 8455, 8460, 8461, 8534, 8535, 8536, 8537, 8538, 8539, 8540, 8541, 8542, 8543, 8544,
           8545, 8546, 8547, 8548, 8549, 8550, 8551, 8552, 8567, 8568, 8569, 8570, 8571, 8572, 8573, 8574, 8590,
           8591, 8592, 8593, 8594, 8595, 8596, 8597, 8598, 8599, 8600, 8601, 8602, 8603, 8604, 8605, 8606, 8607,
           8608, 8623, 8624, 8625, 8626, 8627, 8628, 8629, 8630, 8631, 8632, 8633, 8634, 8635, 8636, 8637, 8638,
           8639, 8640, 8641, 8642, 8643, 8644, 8645, 8646, 8647, 8648, 8649, 8650, 8651, 8652, 8653, 8699, 8700,
           8701, 8702, 8703, 8704, 8709, 8710, 8783, 8784, 8785, 8786, 8787, 8788, 8789, 8790, 8791, 8792, 8793,
           8794, 8795, 8796, 8797, 8798, 8799, 8800, 8801, 8816, 8817, 8818, 8819, 8820, 8821, 8822, 8823, 8839,
           8840, 8841, 8842, 8843, 8844, 8845, 8846, 8847, 8848, 8849, 8850, 8851, 8852, 8853, 8854, 8855, 8856,
           8857, 8872, 8873, 8874, 8875, 8876, 8877, 8878, 8879, 8880, 8881, 8882, 8883, 8884, 8885, 8886, 8887,
           8888, 8889, 8890, 8891, 8892, 8893, 8894, 8895, 8896, 8897, 8898, 8899, 8900, 8901, 8902, 8948, 8949,
           8950, 8951, 8952, 8953, 8958, 8959, 9006, 9007, 9008, 9009, 9010, 9062, 9063, 9064, 9065, 9066, 9067,
           9072, 9263, 9264, 9267, 9268, 9275, 9276, 9285, 9286, 9293, 9294, 9305, 9308, 9312, 9313, 9316, 9317,
           9320, 9321, 9324, 9325]

for i in notdone:
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
                continue
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


with open('../helper_functions_and_files/all_possible_sampled_params.pickle','rb') as p:
    sampled_params_list = pickle.load(p)

# per model

results_dict = {}

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
        rates_mask.append('sp_'+i.name in [y.name for y in sampled_params_list])
    #
    sp_list = []
    for i in [x for x in sampled_params_list]:
        if i.name.split('sp_')[1] in [y.name for y in model.parameters]:
            sp_list.append(i)
    #
    sfr = ""+indir+"/dir_model_"+str(m)+"/model_"+str(m)+"_"
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
        #
        #
        # AIC estimate
        k = len(sp_list)
        AIC = 2.*k - 2.*ml
        print (AIC)
        results_dict[m]['AIC'] = AIC
        #
        # BIC estimate
        k = len(sp_list)
        # n_data = number of observations in the data... so the number of cibersort bars per data
        n_data = 10
        BIC = np.log(n_data)*k - 2.*ml
        results_dict[m]['BIC'] = BIC
        #
        # Not currently using INS but why not save it in case
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
full_rez_dict.to_pickle(outdir+'compare_RPM_gleipnir_results_subset_betafit_to9264_somemissing_4_7_2022.pickle')


#with open(outdir+'compare_clA_gleipnir_results_subset_betafit_12_10_2020_DIC_calc_values_in_case.pickle','wb') as f:
#    pickle.dump(DIC_dict,f)