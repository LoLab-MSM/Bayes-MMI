### Put together the posterior marginal simulations, which involves consolidating within each dataset and saving that
#

import pandas as pd
import gzip
import pickle
import sys

indirdict = {
    'TKO': '../posterior_marginals_and_predictives/posterior_marginals_all/TKO/',
    'RPM': '../posterior_marginals_and_predictives/posterior_marginals_all/RPM/',
    'cl_A': '../posterior_marginals_and_predictives/posterior_marginals_all/cl_A/'
}

outdir = '../posterior_marginals_and_predictives/'

###
#
# TKO
indir_TKO = indirdict['TKO']

post_picklelist_names = [
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_0_to_1004.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1004_to_2038.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2038_to_3054.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_3054_to_4084.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_4084_to_5134.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5134_to_5890.pickle']

post_picklelist = []
for f in post_picklelist_names:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist.append(p)

modselection_postmarg = pd.DataFrame()
for n, p in enumerate(post_picklelist):
    print(0, n)
    modselection_postmarg = pd.concat(
        [modselection_postmarg, p])

modselection_postmarg.to_pickle(
    outdir + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights.pklz',
            compression='gzip')
#
# RPM
indir_RPM = indirdict['RPM']

post_picklelist_names = [
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_0_to_1014.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1014_to_2080.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2080_to_3103.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_3103_to_4142.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_4142_to_5177.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5177_to_5890.pickle']

post_picklelist = []
for f in post_picklelist_names:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist.append(p)

modselection_postmarg = pd.DataFrame()
for n, p in enumerate(post_picklelist):
    print(0, n)
    modselection_postmarg = pd.concat(
        [modselection_postmarg, p])

modselection_postmarg.to_pickle(
    outdir + 'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights.pklz',
        compression='gzip')

# cell lines cluster A
indir_clA = indirdict['cl_A']

post_picklelist_names = [
    indir_clA+'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_0_to_1007.pickle',
    indir_clA+'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1007_to_2059.pickle',
    indir_clA+'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2059_to_3087.pickle',
    indir_clA+'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_3087_to_4131.pickle',
    indir_clA+'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_4131_to_5173.pickle',
    indir_clA+'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5173_to_5890.pickle']

post_picklelist = []
for f in post_picklelist_names:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist.append(p)

modselection_postmarg = pd.DataFrame()
for n, p in enumerate(post_picklelist):
    print(0, n)
    modselection_postmarg = pd.concat(
        [modselection_postmarg, p])

modselection_postmarg.to_pickle(
    outdir + 'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights.pklz',
            compression='gzip') #,protocol=4 ?


