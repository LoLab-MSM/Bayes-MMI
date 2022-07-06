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

tko_notdone = [24, 26, 34, 36, 39, 40, 41, 136, 138, 141, 143, 156, 158, 161, 163, 268, 270, 271, 274, 288, 290, 293, 295,
           542, 547, 549, 562, 564, 613, 615, 628, 630, 631, 679, 681, 682, 689, 694, 696, 1336, 1337, 1441, 1638, 1640,
           1666, 1668, 1728, 1731, 1733, 1736, 1738, 1826, 1828, 1841, 1843, 1941, 1943, 1947, 1951, 1953, 1954, 1956,
           1958, 2046, 2048, 2049, 2061, 2063, 2129, 2171, 2173, 2176, 2178, 2266, 2268, 2278, 2281, 2283, 2386, 2391,
           2393, 2396, 2398, 2486, 2488, 2501, 2503, 2563, 2601, 2603, 2607, 2611, 2613, 2616, 2618, 2701, 2703, 2706,
           2707, 2708, 2716, 2718, 2721, 2723, 2812, 2823, 2831, 2833, 2836, 2838, 2921, 2923, 2926, 2928, 2936, 2938,
           2941, 2943, 3004, 3041, 3044, 3051, 3053, 3056, 3058, 3141, 3143, 3146, 3148, 3156, 3158, 3161, 3163, 3285,
           3287, 3290, 3292, 3305, 3307, 3310, 3312, 3390, 3405, 3407, 3410, 3412, 3420, 3422, 3425, 3427, 3528, 3549,
           3551, 3554, 3556, 3569, 3571, 3574, 3576, 3669, 3671, 3674, 3676, 3684, 3686, 3689, 3691, 3792, 3813, 3815,
           3818, 3820, 3833, 3835, 3838, 3840, 3945, 3947, 3948, 3950, 3953, 3965, 3967, 3970, 3972, 4065, 4067, 4070,
           4072, 4080, 4082, 4085, 4087, 4125, 4131, 4133, 4136, 4137, 4138, 4139, 4146, 4148, 4151, 4153, 4323, 4329,
           4330, 4331, 4334, 4335, 4336, 4337, 4344, 4346, 4349, 4351, 4352, 4643, 4647, 4694, 4695, 4756, 4757, 4762,
           4807, 4867, 4872, 4914, 4916, 4917, 4989, 5127, 5132, 5134, 5155, 5160, 5162, 5183, 5188, 5190, 5211, 5216,
           5218, 5251, 5296, 5298, 5301, 5303, 5311, 5313, 5396, 5398, 5493, 5497, 5505, 5508, 5509, 5523, 5580, 5581,
           5584, 5585, 5599, 5600, 5602, 5622, 5636, 5638, 5731, 5800, 5801, 5806, 5808, 5812, 5822, 5824, 5828, 5829,
           5845, 5846, 5850, 5851, 5852, 5856, 5857, 5858, 5859, 5888, 5889, 5890, 5891, 5892, 5893, 5894, 5895, 5896,
           5898, 5899, 5901, 5902, 5903, 5906, 5907, 5930, 5931, 5982, 5983, 5984, 5986, 5987, 5988, 5989, 6001, 6003,
           6006, 6008, 6106, 6108, 6109, 6121, 6123, 6216, 6217, 6288, 6289, 6290, 6292, 6293, 6294, 6295, 6312, 6314,
           6419, 6421, 6436, 6482, 6485, 6510, 6511, 6514, 6515, 6518, 6519, 6534, 6536, 6552, 6553, 6555, 6556, 6557,
           6562, 6563, 6564, 6566, 6567, 6570, 6571, 6594, 6595, 6596, 6613, 6614, 6615, 6618, 6642, 6649, 6657, 6659,
           6661, 6677, 6687, 6688, 6690, 6691, 6694, 6695, 6701, 6703, 6712, 6748, 6751, 6753, 6754, 6846, 6944, 6955,
           6956, 6981, 6982, 6983, 6984, 6986, 6987, 6988, 6998, 6999, 7000, 7030, 7031, 7032, 7034, 7048, 7049, 7050,
           7053, 7075, 7096, 7098, 7114, 7115, 7116, 7162, 7163, 7164, 7174, 7175, 7176, 7330, 7331, 7332, 7333, 7362,
           7363, 7364, 7365, 7379, 7380, 7381, 7395, 7396, 7397, 7487, 7490, 7596, 7597, 7598, 7599, 7612, 7613, 7614,
           7615, 7616, 7617, 7618, 7619, 7620, 7706, 7707, 7708, 7721, 7722, 7723, 7724, 7725, 7726, 7727, 7728, 7729,
           7757, 7761, 7762, 7767, 7769, 7799, 7802, 7806, 7807, 7829, 7830, 7834, 7835, 7838, 7839, 7840, 7841, 7854,
           7857, 7870, 7880, 7881, 7882, 7886, 7889, 7890, 7891, 7892, 7893, 7894, 7964, 7965, 7966, 7976, 7977, 7978,
           7979, 7980, 7981, 8063, 8064, 8084, 8098, 8099, 8115, 8130, 8142, 8143, 8144, 8145, 8157, 8158, 8159, 8160,
           8161, 8162, 8163, 8179, 8193, 8194, 8210, 8224, 8225, 8232, 8234, 8235, 8237, 8238, 8239, 8240, 8250, 8252,
           8254, 8255, 8256, 8257, 8258, 8274, 8282, 8284, 8285, 8305, 8312, 8313, 8314, 8315, 8316, 8346, 8358, 8359,
           8361, 8362, 8366, 8373, 8374, 8375, 8376, 8377, 8391, 8392, 8396, 8405, 8451, 8452, 8453, 8454, 8455, 8534,
           8535, 8536, 8537, 8538, 8539, 8540, 8541, 8542, 8543, 8544, 8545, 8546, 8547, 8548, 8549, 8550, 8551, 8552,
           8567, 8568, 8569, 8570, 8571, 8572, 8573, 8574, 8590, 8591, 8592, 8593, 8594, 8595, 8596, 8597, 8598, 8599,
           8600, 8601, 8602, 8603, 8604, 8605, 8606, 8607, 8608, 8623, 8624, 8625, 8626, 8627, 8628, 8629, 8630, 8631,
           8632, 8633, 8634, 8635, 8636, 8637, 8638, 8639, 8640, 8641, 8642, 8643, 8644, 8645, 8646, 8647, 8648, 8649,
           8650, 8651, 8652, 8653, 8699, 8700, 8701, 8702, 8703, 8704, 8783, 8784, 8785, 8786, 8787, 8788, 8789, 8790,
           8791, 8792, 8793, 8794, 8795, 8796, 8797, 8798, 8799, 8800, 8801, 8816, 8817, 8818, 8819, 8820, 8821, 8822,
           8823, 8839, 8840, 8841, 8842, 8843, 8844, 8845, 8846, 8847, 8848, 8849, 8850, 8851, 8852, 8853, 8854, 8855,
           8856, 8857, 8872, 8873, 8874, 8875, 8876, 8877, 8878, 8879, 8880, 8881, 8882, 8883, 8884, 8885, 8886, 8887,
           8888, 8889, 8890, 8891, 8892, 8893, 8894, 8895, 8896, 8897, 8898, 8899, 8900, 8901, 8902, 8918, 8920, 8922,
           8923, 8924, 8933, 8951, 8975, 8978, 8980, 8981, 8989, 8990, 8992, 9031, 9066, 9089, 9090, 9091, 9092, 9093,
           9094, 9102, 9103, 9104, 9105, 9106, 9107, 9122, 9129, 9145, 9146, 9147, 9148, 9149, 9150, 9158, 9159, 9160,
           9161, 9162, 9163, 9178, 9185, 9201, 9202, 9203, 9205, 9215, 9216, 9217, 9218, 9219, 9252, 9267, 9268, 9275,
           9276, 9285, 9286, 9293, 9294, 9317, 9318, 9319, 9320]

rpm_notdone = [1128, 1281, 1282, 1334, 1335, 1336, 1337, 1338, 1438, 1439, 1446, 1546, 1567, 1568, 1570, 4409, 4472,
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


cla_notdone = [643, 1279, 1281, 1282, 1337, 1338, 1439, 1442, 1553, 1579, 1583, 1633, 1638, 1640, 1657, 1659, 1661,
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


notdonedict = {
    'TKO':tko_notdone,
    'RPM':rpm_notdone,
    'cl_A':cla_notdone
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

# prior predictive should go for the same models as posterior predictive for optimal comparison (lol)
modselection_priorpred = {}
for i in ['TKO','cl_A','RPM']:
    modselection_priorpred[i] = {
            'NE_obs': pd.DataFrame(),
            'NEv1_obs': pd.DataFrame(),
            'NEv2_obs': pd.DataFrame(),
            'NonNE_obs': pd.DataFrame()
        }

dfdict = pd.read_pickle('../helper_functions_and_files/updatedinjune_all_9327_models_in_dataframe_with_subtype_starting_makeup_code.pickle')
updated_modelmakeups = np.load('../helper_functions_and_files/updatedinjune_apr_11_all_model_makeups_from_redo_ignoring_uneven_bidirtxns.npy')
upd_modnums = []
for j in dfdict.index:
    if dfdict.loc[j]['model_makeup'] in updated_modelmakeups:
        upd_modnums.append(j)

# print(upd_modnums)

TOLERANCE = 1e-4
for dset in ['TKO', 'RPM', 'cl_A']:
    old_m = 5000
    ind = 1
    #postparamstosim only need to load once as long as it's for the correct dataset
    postparamstosim = pd.read_pickle(margfile_dir + dset + '_betafit_postmarg_params_and_probabilities_from_postequalweights_somemissing_6_23_22.pklz',
                                     compression='gzip')
    for m in modeldict:
        if m <= old_m: #first run should be <; anything past the first time this needs to be <=
            continue
        if m in notdonedict[dset]:
            continue
        if m not in upd_modnums:
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
                priors_to_simulate = gen_priors_for_predictive(1000, thisprior.dist,
                                        thisprior.mean(), thisprior.std())
            else:
                priors_to_simulate = gen_priors_for_predictive(1000, thisprior.dist,
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
            if sim['total_cells'][-1] < 1000000:
                print('not enough cells ' + str(sim['total_cells'][-1]))
            elif np.isnan(sim['total_cells'][-1]):
                print('too many cells computer couldnt handle ' + str(sim['total_cells'][-1]))
            elif all_lessthan1:  # smallest size in SCLC allografts (Lim et al) 1cm^3 (~10^8 cells), largest ~3.5cm^3 (~4*10^8)
                print('something crashed out at the end ')
            else:
                sim_pct_run = {}
                for obs in ['NE_obs', 'NEv1_obs', 'NEv2_obs', 'NonNE_obs']:
                    sim_pct_run[obs] = np.true_divide(sim[obs], sim['total_cells'])
                not_eq = False
                y = np.column_stack(
                    (sim_pct_run['NE_obs'], sim_pct_run['NEv1_obs'], sim_pct_run['NEv2_obs'], sim_pct_run['NonNE_obs']))
                for idx in range(y.shape[1]):
                    derivative = (y[:, idx][-1] - y[:, idx][-50]) / (tspan[
                                                                         -1] - tspan[-50])
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
        ## Posterior predictive
        to_sim = postparamstosim.loc[postparamstosim.from_model==m]
        pweight = to_sim.iloc[0].model_pp                       # will be the same no matter the index so just look at 0 to get one weight value
        makeup_code = to_sim.iloc[0].model_starting_subtype_makeup_code
        #
        pnamesandorder = [names_dict['sp_'+p.name] for p in model.parameters if not p.name in ['NE_0','NEv1_0','NEv2_0','NonNE_0']]
        #
        NE = pd.DataFrame(columns=tspan)
        NEv1 = pd.DataFrame(columns=tspan)
        NEv2 = pd.DataFrame(columns=tspan)
        NonNE = pd.DataFrame(columns=tspan)
        #
        for i in range(0,len(to_sim[pnamesandorder])):
            if i % 500 == 0:
                print('model '+str(m)+', '+str(i))
            Y = np.copy(to_sim[pnamesandorder].iloc[i])
            param_values[rates_mask] = 10 ** Y
            signal.alarm(60)
            try:
                sim = solver.run(param_values=param_values,tspan=tspan).all
            except TimeoutException as exc:
                # this should not add anything to to the df
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
        if (ind % 250 == 0 and not ind == 0) or m == 9264 or m == 9262 or m == 5000:   #7293 #for clA high, now #5000 #for cla low, now
            # within one dataset (e.g., TKO), but any structure, and all observables
            print('saving ' + str(old_m) + ' to ' + str(m) + ', ' + str(ind) + ' models...')
            print(outdir_prior + dset + '_trajectories_as_priorpredictive_from_model_'
                  + str(old_m) + '_to_' + str(m) + '.pickle')
            if not os.path.exists(outdir_prior):
                os.makedirs(outdir_prior)
            with open(outdir_prior + dset + '_trajectories_as_priorpredictive_from_model_'
                      + str(old_m) + '_to_' + str(m) + '.pickle','wb') as fp:
                pickle.dump(modselection_priorpred[dset], fp)
            print(outdir_post + dset + '_trajectories_as_postpredictive_from_postequalweights_from_model_'
                  + str(old_m) + '_to_' + str(m) + '.pickle')
            if not os.path.exists(outdir_post):
                os.makedirs(outdir_post)
            with open(outdir_post + dset + '_trajectories_as_postpredictive_from_postequalweights_from_model_'
                      + str(old_m) + '_to_' + str(m) + '.pickle','wb') as fp:
                pickle.dump(modselection_postpred[dset], fp)
            # restart for new ones to save
            modselection_postpred[dset] = {
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