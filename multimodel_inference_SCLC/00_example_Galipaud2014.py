import pymultinest
import numpy as np
from scipy.stats import norm, uniform
import pandas as pd
from pymultinest.solve import solve
from pymultinest.analyse import Analyzer
import pickle
import sys
import copy
import os

# add this Bayes-MMI directory to the path to be able to import from helper_functions_and_files
sys.path.append('/home/beiksp/Bayes-MMI')
sys.path.append('/home/beiksp/maybe_pycharm_running')

from helper_functions_and_files.likelihood_fxns_for_galipaud_candidates import likelihood_beta, \
    likelihood_all, likelihood_x1, likelihood_x2, likelihood_x3, likelihood_x4, likelihood_x1x2, \
    likelihood_x1x3, likelihood_x1x4, likelihood_x2x3, likelihood_x2x4, likelihood_x3x4, \
    likelihood_x1x2x3, likelihood_x1x2x4, likelihood_x1x3x4, likelihood_x2x3x4
from helper_functions_and_files.calculations_for_galipaud_example import example_get_param_importance, \
    example_get_postprobs

# csv generated by R code provided in Galipaud et al., 2014
df = pd.read_csv('galipaud_sim_dat.csv')
df.drop('Unnamed: 0',axis=1,inplace=True)

chisquare_denom = np.var(df.y)  # np.std(df.y)**2

which_likelihood_dict = {
    'galipaud_intonly':likelihood_beta,
    'galipaud_uniformprior':likelihood_all,
    'galipaud_x1only':likelihood_x1,
    'galipaud_x2only':likelihood_x2,
    'galipaud_x3only':likelihood_x3,
    'galipaud_x4only':likelihood_x4,
    'galipaud_x1x2':likelihood_x1x2,
    'galipaud_x1x3':likelihood_x1x3,
    'galipaud_x1x4':likelihood_x1x4,
    'galipaud_x2x3':likelihood_x2x3,
    'galipaud_x2x4':likelihood_x2x4,
    'galipaud_x3x4':likelihood_x3x4,
    'galipaud_x1x2x3':likelihood_x1x2x3,
    'galipaud_x1x2x4':likelihood_x1x2x4,
    'galipaud_x1x3x4':likelihood_x1x3x4,
    'galipaud_x2x3x4':likelihood_x2x3x4
}

# def prior(hypercube):
#     return np.array([sp_list[i].ppf(value) for i, value in enumerate(hypercube)])
#
# for m in ['galipaud_intonly',
#          'galipaud_x1only', 'galipaud_x2only', 'galipaud_x3only', 'galipaud_x4only',
#          'galipaud_x1x2',   'galipaud_x1x3',   'galipaud_x1x4',   'galipaud_x2x3',   'galipaud_x2x4', 'galipaud_x3x4',
#          'galipaud_x1x2x3', 'galipaud_x1x2x4', 'galipaud_x1x3x4', 'galipaud_x2x3x4' ,
#          'galipaud_uniformprior']:
#     if m == 'galipaud_intonly':
#         sp_list = []
#         sp_list.append(uniform(loc=-10,scale=20))
#     elif m == 'galipaud_uniformprior':
#         sp_list = []
#         sp_list.append(uniform(loc=0, scale=1))
#         sp_list.append(uniform(loc=0, scale=1))
#         sp_list.append(uniform(loc=0, scale=1))
#         sp_list.append(uniform(loc=0, scale=1))
#         sp_list.append(uniform(loc=-10,scale=20))
#     elif m in ['galipaud_x1only', 'galipaud_x2only', 'galipaud_x3only', 'galipaud_x4only']:
#         sp_list = []
#         sp_list.append(uniform(loc=0, scale=1))
#         sp_list.append(uniform(loc=-10,scale=20))
#     elif m in ['galipaud_x1x2', 'galipaud_x1x3', 'galipaud_x1x4', 'galipaud_x2x3', 'galipaud_x2x4', 'galipaud_x3x4']:
#         sp_list = []
#         sp_list.append(uniform(loc=0, scale=1))
#         sp_list.append(uniform(loc=0, scale=1))
#         sp_list.append(uniform(loc=-10,scale=20))
#     elif m in ['galipaud_x1x2x3', 'galipaud_x1x2x4', 'galipaud_x1x3x4', 'galipaud_x2x3x4']:
#         sp_list = []
#         sp_list.append(uniform(loc=0, scale=1))
#         sp_list.append(uniform(loc=0, scale=1))
#         sp_list.append(uniform(loc=0, scale=1))
#         sp_list.append(uniform(loc=-10,scale=20))
#     else:
#         print('ATTN: wrong',m)
#         continue
#     if not os.path.exists(m):
#         os.mkdir(m)
#     sfr = m+'/'+m
#     print(sfr)
#     #
#     likelihood = which_likelihood_dict[m]
#     output = solve(LogLikelihood=likelihood, Prior=prior,
#                    n_dims = len(sp_list),
#                    n_live_points=3000,
#                    sampling_efficiency=0.05,
#                    outputfiles_basename=sfr,
#                    verbose=True)

# I have this separated between running each of them and then getting the results all in a row,
# but could build results_dict one at a time

outdir = '../files_generated_in_MMI_sclc/'
results_dict = {}

for m in ['galipaud_intonly',
          'galipaud_x1only', 'galipaud_x2only', 'galipaud_x3only', 'galipaud_x4only',
          'galipaud_x1x2',   'galipaud_x1x3',   'galipaud_x1x4',   'galipaud_x2x3',   'galipaud_x2x4', 'galipaud_x3x4',
          'galipaud_x1x2x3', 'galipaud_x1x2x4', 'galipaud_x1x3x4', 'galipaud_x2x3x4' ,
          'galipaud_uniformprior']:
    if m == 'galipaud_intonly':
        sp_list = []
        sp_list.append(uniform(loc=-10,scale=20))
        columns = ['int']
    elif m == 'galipaud_uniformprior':
        sp_list = []
        sp_list.append(uniform(loc=0, scale=1))
        sp_list.append(uniform(loc=0, scale=1))
        sp_list.append(uniform(loc=0, scale=1))
        sp_list.append(uniform(loc=0, scale=1))
        sp_list.append(uniform(loc=-10,scale=20))
        columns = ['x1','x2','x3','x4','int']
    elif m in ['galipaud_x1only', 'galipaud_x2only', 'galipaud_x3only', 'galipaud_x4only']:
        sp_list = []
        sp_list.append(uniform(loc=0, scale=1))
        sp_list.append(uniform(loc=-10,scale=20))
        columns = [m.split('_')[-1].split('only')[0]]+['int']
    elif m in ['galipaud_x1x2', 'galipaud_x1x3', 'galipaud_x1x4', 'galipaud_x2x3', 'galipaud_x2x4', 'galipaud_x3x4']:
        sp_list = []
        sp_list.append(uniform(loc=0, scale=1))
        sp_list.append(uniform(loc=0, scale=1))
        sp_list.append(uniform(loc=-10,scale=20))
        columns = ['x'+y for y in m.split('_')[-1].split('x')[1:]]+['int']
    elif m in ['galipaud_x1x2x3', 'galipaud_x1x2x4', 'galipaud_x1x3x4', 'galipaud_x2x3x4']:
        sp_list = []
        sp_list.append(uniform(loc=0, scale=1))
        sp_list.append(uniform(loc=0, scale=1))
        sp_list.append(uniform(loc=0, scale=1))
        sp_list.append(uniform(loc=-10,scale=20))
        columns = ['x'+y for y in m.split('_')[-1].split('x')[1:]]+['int']
    else:
        print('ATTN: wrong',m)
        continue
    #sfr = '../galipaud_repeatedsims/'+m+'_1000/'+m+'_1000'
    sfr = m+'/'+m
    #print(m)
    #print(columns)
    #
    a = pymultinest.Analyzer(len(sp_list), outputfiles_basename=sfr)
    results_dict[m] = {}
    try:
        pos = pd.DataFrame(np.array([i for i in a.get_equal_weighted_posterior()]),
                           columns=columns + ['paramset_likelihood'])
        pos = pos.sort_values('paramset_likelihood', ascending=False)
    except ValueError:
        print('Analyzer did not work for model ' + str(m)+'_'+str(z) + ' so no values returned.')
        continue
    #
    try:
        # log Z and err
        results_dict[m]['log_Z'] = a.get_stats()['nested sampling global log-evidence']
        results_dict[m]['log_Z_err'] = a.get_stats()['nested sampling global log-evidence error']
        # Z and err
        results_dict[m]['Z'] = np.exp(a.get_stats()['nested sampling global log-evidence'])
        results_dict[m]['Z_err'] = np.exp(a.get_stats()['nested sampling global log-evidence error'])
        # INS log Z and err
        results_dict[m]['INS_log_Z'] = a.get_stats()[
            'nested importance sampling global log-evidence']  # equivalent to a.get_stats()['global evidence'] at least in this context
        results_dict[m]['INS_log_Z_err'] = a.get_stats()['nested importance sampling global log-evidence error']
        # INS Z and err
        results_dict[m]['INS_Z'] = np.exp(a.get_stats()['nested importance sampling global log-evidence'])
        results_dict[m]['INS_Z_err'] = np.exp(a.get_stats()['nested importance sampling global log-evidence error'])
        #
        try:
            results_dict[m]['x1_mean'] = np.mean(pos.x1)
            results_dict[m]['x1_mle'] = pos.x1.iloc[0]
        except AttributeError:
            pass
        try:
            results_dict[m]['x2_mean'] = np.mean(pos.x2)
            results_dict[m]['x2_mle'] = pos.x2.iloc[0]
        except AttributeError:
            pass
        try:
            results_dict[m]['x3_mean'] = np.mean(pos.x3)
            results_dict[m]['x3_mle'] = pos.x3.iloc[0]
        except AttributeError:
            pass
        try:
            results_dict[m]['x4_mean'] = np.mean(pos.x4)
            results_dict[m]['x4_mle'] = pos.x4.iloc[0]
        except AttributeError:
            pass
        results_dict[m]['int_mean'] = np.mean(pos.int)
        results_dict[m]['int_mle'] = pos.int.iloc[0]
        # max_loglikelihood (ml) & setting useful things
        mn_data = a.get_data()
        log_ls = -0.5 * mn_data[:, 1]
        ml = log_ls.max()
        results_dict[m]['max_loglikelihood'] = ml
        # AIC estimate
        k = len(sp_list)
        AIC = 2. * k - 2. * ml
        results_dict[m]['AIC'] = AIC
        # plus correction
        # n_data = number of observations in the data... used 100 simulated data points for this
        n_data = 100
        AIC_corr = ( (2. * k**2) + (2. * k) ) / (n_data - k - 1)
        results_dict[m]['AICc'] = AIC + AIC_corr
        #
        # BIC estimate
        k = len(sp_list)
        # n_data = number of observations in the data, assigned above
        #n_data = 100
        BIC = np.log(n_data) * k - 2. * ml
        results_dict[m]['BIC'] = BIC
        #
    except ValueError:
        print('Analyzer did not work for model ' + str(m) + ' so no values returned.')
        pass
    #break

resdf = pd.DataFrame(results_dict).T
# get a marginal likelihood estimation from BIC (Wiki)
resdf['BIC_marglik_est'] = np.exp(-resdf['BIC']/2)

# save the df to get a subset of (Supplemental Table S4)
resdf_partial = copy.deepcopy(resdf)

# get posterior probability (from evidence / marginal likelihood / Z)
resdf['post_prob_Z'] = resdf.Z/np.sum(resdf.Z)
resdf['post_prob_INS_Z'] = resdf.INS_Z/np.sum(resdf.INS_Z)
# posterior prob estimate using BIC
resdf['BIC_pp_est'] = resdf.BIC_marglik_est/np.sum(resdf.BIC_marglik_est)

#
# then get SWs, posterior probs
print('param importance AICc')
example_get_param_importance(resdf)
print('param importance BIC')
example_get_param_importance(resdf,which_IC='BIC')
print('post probs BIC estimator')
example_get_postprobs(resdf,which_evidence='BIC_marglik_est')
print('post probs')
example_get_postprobs(resdf)

resdf.to_pickle(outdir+'galipaud_results_pp_AIC_BIC_test.pickle')

sys.exit(0)

# subset (Supplemental table S4)

resdf_partial = resdf_partial.loc[['galipaud_intonly', 'galipaud_x1only', 'galipaud_x2only',
       'galipaud_x3only', 'galipaud_x4only', 'galipaud_x1x2', 'galipaud_x1x3',
       'galipaud_x1x4', 'galipaud_x2x3', 'galipaud_x2x4',
       'galipaud_x1x2x3', 'galipaud_x1x2x4']]

# get posterior probability (from evidence / marginal likelihood / Z)
#resdf_partial['post_prob_Z'] = resdf_partial.Z/np.sum(resdf_partial.Z)
#resdf_partial['post_prob_INS_Z'] = resdf_partial.INS_Z/np.sum(resdf_partial.INS_Z)
#resdf_partial['BIC_pp_est'] = resdf_partial.BIC_marglik_est/np.sum(resdf_partial.BIC_marglik_est)
# then get SWs, posterior probs
print('param importance AICc')
example_get_param_importance(resdf_partial)
print('param importance BIC')
example_get_param_importance(resdf_partial,which_IC='BIC')
print('post probs BIC estimator')
example_get_postprobs(resdf_partial,which_evidence='BIC_marglik_est')
print('post probs')
example_get_postprobs(resdf_partial)

resdf_partial.to_pickle(outdir+'galipaud_results_nox3x4_pp_and_AIC_3_9_23.pickle')

