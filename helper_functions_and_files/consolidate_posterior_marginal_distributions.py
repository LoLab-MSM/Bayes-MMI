### Put together the posterior marginal simulations, which involves consolidating within each dataset and saving that
#

import pandas as pd
import gzip
import pickle

indirdict = {
    'TKO': '../posterior_marginals_and_predictives/posterior_marginals_all/TKO/',
    'RPM': '../posterior_marginals_and_predictives/posterior_marginals_all/RPM/',
    'cl_A': '../posterior_marginals_and_predictives/posterior_marginals_all/cl_A/'
}

outdir = '../posterior_marginals_and_predictives/'

###

# TKO
indir_TKO = indirdict['TKO']

post_picklelist_names = [
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_0_to_1651.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1651_to_2933.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2933_to_4766.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_4766_to_7640.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_7640_to_8921.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_8921_to_9327.pickle']

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
    outdir + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_somemissing_6_23_22.pklz',
            compression='gzip')


# RPM
indir_RPM = indirdict['RPM']

post_picklelist_names = [
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_0_to_1652.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1652_to_2872.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2872_to_4690.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_4690_to_7546.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_7546_to_8744.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_8744_to_9327.pickle']



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
    outdir + 'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_somemissing_6_23_22.pklz',
        compression='gzip')

# cell lines cluster A
indir_clA = indirdict['cl_A']

post_picklelist_names = [
    indir_clA+'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_0_to_1650.pickle',
    indir_clA+'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1650_to_2877.pickle',
    indir_clA+'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2877_to_4718.pickle',
    indir_clA+'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_4718_to_7602.pickle',
    indir_clA+'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_7602_to_8825.pickle',
    indir_clA+'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_8825_to_9327.pickle']

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
    outdir + 'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_somemissing_6_23_22.pklz',
            compression='gzip') #,protocol=4 ?


