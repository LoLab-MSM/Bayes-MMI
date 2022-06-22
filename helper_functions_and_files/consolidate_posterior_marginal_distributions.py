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
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_0_to_527.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_527_to_1567.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1567_to_1797.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1797_to_1906.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1906_to_2015.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2015_to_2126.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2126_to_2232.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2232_to_2342.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2342_to_2448.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2448_to_2557.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2557_to_2669.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2669_to_2779.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2779_to_2888.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2888_to_2998.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2998_to_3107.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_3107_to_3219.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_3219_to_5360.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5360_to_5469.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5469_to_5590.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5590_to_5701.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5701_to_5805.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5805_to_6752.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_6752_to_6878.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_6878_to_6994.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_6994_to_7121.pickle',
    indir_TKO + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_7121_to_7161.pickle']

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
    outdir + 'TKO_betafit_postmarg_params_and_probabilities_from_postequalweights_somemissing_4_10_22.pklz',
            compression='gzip')


# RPM
indir_RPM = indirdict['RPM']

post_picklelist_names = [
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_0_to_517.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_517_to_859.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_859_to_1771.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1771_to_1871.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1871_to_1971.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1971_to_2071.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2071_to_2171.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2171_to_2271.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2271_to_2371.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2371_to_2471.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2471_to_2571.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2571_to_2671.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2671_to_2771.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2771_to_2871.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2871_to_2971.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2971_to_3071.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_3071_to_3171.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_3171_to_5315.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5315_to_5432.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5432_to_5537.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5537_to_5641.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5641_to_5761.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5761_to_5876.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5876_to_6795.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_6795_to_6915.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_6915_to_7044.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_7044_to_7152.pickle',
    indir_RPM+'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_7152_to_7161.pickle']

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
    outdir + 'RPM_betafit_postmarg_params_and_probabilities_from_postequalweights_somemissing_4_10_22.pickle',
        compression='gzip')

# cell lines cluster A
indir_clA = indirdict['cl_A']

post_picklelist_names = [
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_0_to_517.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_517_to_859.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_859_to_1772.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1772_to_1872.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1872_to_1975.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_1975_to_2075.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2075_to_2180.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2180_to_2280.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2280_to_2382.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2382_to_2485.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2485_to_2587.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2587_to_2687.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2687_to_2792.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2792_to_2896.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2896_to_2997.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_2997_to_3099.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_3099_to_3199.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_3199_to_5348.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5348_to_5460.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5460_to_5567.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5567_to_5680.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5680_to_5821.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_5821_to_6760.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_6760_to_6889.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_6889_to_7021.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_7021_to_7141.pickle',
    indir_clA+'clA_betafit_postmarg_params_and_probabilities_from_postequalweights_from_model_7141_to_7161.pickle']

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
    outdir + 'cl_A_betafit_postmarg_params_and_probabilities_from_postequalweights_somemissing_4_10_22.pklz',
            compression='gzip') #,protocol=4 ?


