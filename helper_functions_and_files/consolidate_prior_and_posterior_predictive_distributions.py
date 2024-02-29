### Put together the posterior predictive simulations, which involves consolidating within each dataset and save

import pandas as pd
import gzip
import pickle
import sys

indirdict = {
    'prior':'../posterior_marginals_and_predictives/prior_posterior_predictives_all/prior_predictives_all/',
    'post':'../posterior_marginals_and_predictives/prior_posterior_predictives_all/posterior_predictives_all/'
}

indir_post = indirdict['post']
indir_prior = indirdict['prior']
outdir = '../posterior_marginals_and_predictives/'
###

### Put together the posterior predictive (from joint posterior distribution) simulations, which
#   involves consolidating within each dataset and saving

# TKO

# top topologies
post_picklelist_top = []
for f in [indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_0_to_944_toptopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_944_to_1197_toptopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_1197_to_1449_toptopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_1449_to_1711_toptopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_1711_to_1863_toptopologies.pickle']:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist_top.append(p)

modselection_postpred_top = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist_top):
    print(n)
    modselection_postpred_top['NE_obs'] = pd.concat(
        [modselection_postpred_top['NE_obs'], p['NE_obs']])
    modselection_postpred_top['NEv1_obs'] = pd.concat(
        [modselection_postpred_top['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred_top['NEv2_obs'] = pd.concat(
        [modselection_postpred_top['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred_top['NonNE_obs'] = pd.concat(
        [modselection_postpred_top['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'TKO_trajectories_as_postpredictive_from_postequalweights_toptopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred_top,fp,protocol=4)

# all topologies
post_picklelist_all = []
for f in [indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_0_to_249_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_249_to_505_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_505_to_755_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_755_to_1005_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_1005_to_1258_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_1258_to_1511_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_1511_to_1773_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_1773_to_1863_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_1863_to_2042_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_2042_to_2294_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_2294_to_2552_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_2552_to_2803_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_2803_to_3060_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_3060_to_3318_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_3318_to_3582_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_3582_to_3836_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_3836_to_4090_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_4090_to_4353_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_4353_to_4618_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_4618_to_4876_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_4876_to_5140_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_5140_to_5400_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_5400_to_5668_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_5668_to_5890_alltopologies.pickle'
          ]:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist_all.append(p)

modselection_postpred_all = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist_all):
    print(n)
    modselection_postpred_all['NE_obs'] = pd.concat(
        [modselection_postpred_all['NE_obs'], p['NE_obs']])
    modselection_postpred_all['NEv1_obs'] = pd.concat(
        [modselection_postpred_all['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred_all['NEv2_obs'] = pd.concat(
        [modselection_postpred_all['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred_all['NonNE_obs'] = pd.concat(
        [modselection_postpred_all['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'TKO_trajectories_as_postpredictive_from_postequalweights_alltopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred_all,fp,protocol=4)


# RPM

# top topologies
post_picklelist_top = []
for f in [indirdict['post']+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_0_to_329_toptopologies.pickle',
          indirdict['post']+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_329_to_587_toptopologies.pickle',
          indirdict['post']+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_587_to_726_toptopologies.pickle']:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist_top.append(p)

modselection_postpred_top = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist_top):
    print(n)
    modselection_postpred_top['NE_obs'] = pd.concat(
        [modselection_postpred_top['NE_obs'], p['NE_obs']])
    modselection_postpred_top['NEv1_obs'] = pd.concat(
        [modselection_postpred_top['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred_top['NEv2_obs'] = pd.concat(
        [modselection_postpred_top['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred_top['NonNE_obs'] = pd.concat(
        [modselection_postpred_top['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'RPM_trajectories_as_postpredictive_from_postequalweights_toptopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred_top,fp,protocol=4)

# all topologies
post_picklelist_all = []
for f in [indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_0_to_252_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_252_to_505_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_505_to_726_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_726_to_764_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_764_to_1014_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_1014_to_1269_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_1269_to_1543_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_1543_to_1822_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_1822_to_2080_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_2080_to_2333_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_2333_to_2590_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_2590_to_2844_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_2844_to_3105_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_3105_to_3367_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_3367_to_3630_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_3630_to_3890_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_3890_to_4146_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_4146_to_4409_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_4409_to_4670_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_4670_to_4924_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_4924_to_5179_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_5179_to_5433_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_5433_to_5692_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_5692_to_5890_alltopologies.pickle'
          ]:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist_all.append(p)

modselection_postpred_all = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist_all):
    print(n)
    modselection_postpred_all['NE_obs'] = pd.concat(
        [modselection_postpred_all['NE_obs'], p['NE_obs']])
    modselection_postpred_all['NEv1_obs'] = pd.concat(
        [modselection_postpred_all['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred_all['NEv2_obs'] = pd.concat(
        [modselection_postpred_all['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred_all['NonNE_obs'] = pd.concat(
        [modselection_postpred_all['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'RPM_trajectories_as_postpredictive_from_postequalweights_alltopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred_all,fp,protocol=4)

#
# cell_line_A

# top topologies
post_picklelist_top = []
for f in [indirdict['post']+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_0_to_2078_toptopologies.pickle',
          indirdict['post']+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_2078_to_2193_toptopologies.pickle']:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist_top.append(p)

modselection_postpred_top = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist_top):
    print(n)
    modselection_postpred_top['NE_obs'] = pd.concat(
        [modselection_postpred_top['NE_obs'], p['NE_obs']])
    modselection_postpred_top['NEv1_obs'] = pd.concat(
        [modselection_postpred_top['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred_top['NEv2_obs'] = pd.concat(
        [modselection_postpred_top['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred_top['NonNE_obs'] = pd.concat(
        [modselection_postpred_top['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'cl_A_trajectories_as_postpredictive_from_postequalweights_toptopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred_top,fp,protocol=4)

# all topologies
post_picklelist_all = []
for f in [indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_0_to_252_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_252_to_504_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_504_to_757_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_757_to_1007_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_1007_to_1260_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_1260_to_1522_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_1522_to_1800_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_1800_to_2059_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_2059_to_2193_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_2193_to_2313_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_2313_to_2570_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_2570_to_2825_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_2825_to_3088_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_3088_to_3349_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_3349_to_3619_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_3619_to_3877_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_3877_to_4132_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_4132_to_4405_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_4405_to_4667_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_4667_to_4920_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_4920_to_5174_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_5174_to_5425_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_5425_to_5681_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_5681_to_5890_alltopologies.pickle'
          ]:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist_all.append(p)

modselection_postpred_all = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist_all):
    print(n)
    modselection_postpred_all['NE_obs'] = pd.concat(
        [modselection_postpred_all['NE_obs'], p['NE_obs']])
    modselection_postpred_all['NEv1_obs'] = pd.concat(
        [modselection_postpred_all['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred_all['NEv2_obs'] = pd.concat(
        [modselection_postpred_all['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred_all['NonNE_obs'] = pd.concat(
        [modselection_postpred_all['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'cl_A_trajectories_as_postpredictive_from_postequalweights_alltopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred_all,fp,protocol=4)

### Put together the prior predictive simulations, which involves consolidating within each dataset and saving

##
# TKO
# can't just for loop TKO, RPM, cl_A because the numbers ("from_model_x_to_y") are different for the pickle files

# TKO

# top topologies
prior_picklelist_top = []
for f in [indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_0_to_944_toptopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_944_to_1197_toptopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_1197_to_1449_toptopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_1449_to_1711_toptopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_1711_to_1863_toptopologies.pickle']:
    print(f)
    p = pd.read_pickle(f)
    prior_picklelist_top.append(p)

modselection_priorpred_top = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(prior_picklelist_top):
    print(n)
    modselection_priorpred_top['NE_obs'] = pd.concat(
        [modselection_priorpred_top['NE_obs'], p['NE_obs']])
    modselection_priorpred_top['NEv1_obs'] = pd.concat(
        [modselection_priorpred_top['NEv1_obs'], p['NEv1_obs']])
    modselection_priorpred_top['NEv2_obs'] = pd.concat(
        [modselection_priorpred_top['NEv2_obs'], p['NEv2_obs']])
    modselection_priorpred_top['NonNE_obs'] = pd.concat(
        [modselection_priorpred_top['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'TKO_trajectories_as_priorpredictive_toptopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_priorpred_top,fp,protocol=4)

# all topologies
prior_picklelist_all = []
for f in [indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_0_to_249_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_249_to_505_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_505_to_755_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_755_to_1005_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_1005_to_1258_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_1258_to_1511_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_1511_to_1773_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_1773_to_1863_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_1863_to_2042_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_2042_to_2294_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_2294_to_2552_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_2552_to_2803_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_2803_to_3060_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_3060_to_3318_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_3318_to_3582_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_3582_to_3836_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_3836_to_4090_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_4090_to_4353_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_4353_to_4618_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_4618_to_4876_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_4876_to_5140_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_5140_to_5400_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_5400_to_5668_alltopologies.pickle',
          indirdict['prior'] + 'TKO_trajectories_as_priorpredictive_from_model_5668_to_5890_alltopologies.pickle'
          ]:
    print(f)
    p = pd.read_pickle(f)
    prior_picklelist_all.append(p)

modselection_priorpred_all = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(prior_picklelist_all):
    print(n)
    modselection_priorpred_all['NE_obs'] = pd.concat(
        [modselection_priorpred_all['NE_obs'], p['NE_obs']])
    modselection_priorpred_all['NEv1_obs'] = pd.concat(
        [modselection_priorpred_all['NEv1_obs'], p['NEv1_obs']])
    modselection_priorpred_all['NEv2_obs'] = pd.concat(
        [modselection_priorpred_all['NEv2_obs'], p['NEv2_obs']])
    modselection_priorpred_all['NonNE_obs'] = pd.concat(
        [modselection_priorpred_all['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'TKO_trajectories_as_priorpredictive_alltopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_priorpred_all,fp,protocol=4)


# RPM

# top topologies
prior_picklelist_top = []
for f in [indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_0_to_329_toptopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_329_to_587_toptopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_587_to_726_toptopologies.pickle']:
    print(f)
    p = pd.read_pickle(f)
    prior_picklelist_top.append(p)

modselection_priorpred_top = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(prior_picklelist_top):
    print(n)
    modselection_priorpred_top['NE_obs'] = pd.concat(
        [modselection_priorpred_top['NE_obs'], p['NE_obs']])
    modselection_priorpred_top['NEv1_obs'] = pd.concat(
        [modselection_priorpred_top['NEv1_obs'], p['NEv1_obs']])
    modselection_priorpred_top['NEv2_obs'] = pd.concat(
        [modselection_priorpred_top['NEv2_obs'], p['NEv2_obs']])
    modselection_priorpred_top['NonNE_obs'] = pd.concat(
        [modselection_priorpred_top['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'RPM_trajectories_as_priorpredictive_toptopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_priorpred_top,fp,protocol=4)

# all topologies
prior_picklelist_all = []
for f in [indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_0_to_252_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_252_to_505_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_505_to_726_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_726_to_764_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_764_to_1014_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_1014_to_1269_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_1269_to_1543_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_1543_to_1822_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_1822_to_2080_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_2080_to_2333_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_2333_to_2590_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_2590_to_2844_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_2844_to_3105_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_3105_to_3367_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_3367_to_3630_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_3630_to_3890_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_3890_to_4146_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_4146_to_4409_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_4409_to_4670_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_4670_to_4924_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_4924_to_5179_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_5179_to_5433_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_5433_to_5692_alltopologies.pickle',
          indirdict['prior'] + 'RPM_trajectories_as_priorpredictive_from_model_5692_to_5890_alltopologies.pickle'
          ]:
    print(f)
    p = pd.read_pickle(f)
    prior_picklelist_all.append(p)

modselection_priorpred_all = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(prior_picklelist_all):
    print(n)
    modselection_priorpred_all['NE_obs'] = pd.concat(
        [modselection_priorpred_all['NE_obs'], p['NE_obs']])
    modselection_priorpred_all['NEv1_obs'] = pd.concat(
        [modselection_priorpred_all['NEv1_obs'], p['NEv1_obs']])
    modselection_priorpred_all['NEv2_obs'] = pd.concat(
        [modselection_priorpred_all['NEv2_obs'], p['NEv2_obs']])
    modselection_priorpred_all['NonNE_obs'] = pd.concat(
        [modselection_priorpred_all['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'RPM_trajectories_as_priorpredictive_alltopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_priorpred_all,fp,protocol=4)

#
# cl_A

# top topologies
prior_picklelist_top = []
for f in [indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_0_to_2078_toptopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_2078_to_2193_toptopologies.pickle']:
    print(f)
    p = pd.read_pickle(f)
    prior_picklelist_top.append(p)



modselection_priorpred_top = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(prior_picklelist_top):
    print(n)
    modselection_priorpred_top['NE_obs'] = pd.concat(
        [modselection_priorpred_top['NE_obs'], p['NE_obs']])
    modselection_priorpred_top['NEv1_obs'] = pd.concat(
        [modselection_priorpred_top['NEv1_obs'], p['NEv1_obs']])
    modselection_priorpred_top['NEv2_obs'] = pd.concat(
        [modselection_priorpred_top['NEv2_obs'], p['NEv2_obs']])
    modselection_priorpred_top['NonNE_obs'] = pd.concat(
        [modselection_priorpred_top['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'cl_A_trajectories_as_priorpredictive_toptopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_priorpred_top,fp,protocol=4)

# all topologies
prior_picklelist_all = []
for f in [indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_0_to_252_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_252_to_504_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_504_to_757_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_757_to_1007_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_1007_to_1260_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_1260_to_1522_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_1522_to_1800_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_1800_to_2059_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_2059_to_2193_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_2193_to_2313_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_2313_to_2570_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_2570_to_2825_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_2825_to_3088_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_3088_to_3349_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_3349_to_3619_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_3619_to_3877_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_3877_to_4132_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_4132_to_4405_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_4405_to_4667_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_4667_to_4920_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_4920_to_5174_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_5174_to_5425_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_5425_to_5681_alltopologies.pickle',
          indirdict['prior'] + 'cl_A_trajectories_as_priorpredictive_from_model_5681_to_5890_alltopologies.pickle'
          ]:
    print(f)
    p = pd.read_pickle(f)
    prior_picklelist_all.append(p)

modselection_priorpred_all = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(prior_picklelist_all):
    print(n)
    modselection_priorpred_all['NE_obs'] = pd.concat(
        [modselection_priorpred_all['NE_obs'], p['NE_obs']])
    modselection_priorpred_all['NEv1_obs'] = pd.concat(
        [modselection_priorpred_all['NEv1_obs'], p['NEv1_obs']])
    modselection_priorpred_all['NEv2_obs'] = pd.concat(
        [modselection_priorpred_all['NEv2_obs'], p['NEv2_obs']])
    modselection_priorpred_all['NonNE_obs'] = pd.concat(
        [modselection_priorpred_all['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'cl_A_trajectories_as_priorpredictive_alltopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_priorpred_all,fp,protocol=4)

## Put together the posterior independently-sampled param simulations, which involves consolidating within each dataset and saving

# TKO

# top topologies
post_picklelist_top = []
for f in [indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_0_to_944_toptopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_944_to_1197_toptopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_1197_to_1449_toptopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_1449_to_1711_toptopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_1711_to_1863_toptopologies.pickle']:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist_top.append(p)

modselection_postpred_top = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist_top):
    print(n)
    modselection_postpred_top['NE_obs'] = pd.concat(
        [modselection_postpred_top['NE_obs'], p['NE_obs']])
    modselection_postpred_top['NEv1_obs'] = pd.concat(
        [modselection_postpred_top['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred_top['NEv2_obs'] = pd.concat(
        [modselection_postpred_top['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred_top['NonNE_obs'] = pd.concat(
        [modselection_postpred_top['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'TKO_trajectories_as_postpredictive_from_independentsampling_toptopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred_top,fp,protocol=4)

# all topologies
post_picklelist_all = []
for f in [indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_0_to_249_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_249_to_505_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_505_to_755_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_755_to_1005_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_1005_to_1258_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_1258_to_1511_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_1511_to_1773_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_1773_to_1863_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_1863_to_2042_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_2042_to_2294_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_2294_to_2552_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_2552_to_2803_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_2803_to_3060_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_3060_to_3318_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_3318_to_3582_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_3582_to_3836_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_3836_to_4090_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_4090_to_4353_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_4353_to_4618_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_4618_to_4876_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_4876_to_5140_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_5140_to_5400_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_5400_to_5668_alltopologies.pickle',
          indirdict['post'] + 'TKO_trajectories_as_postpredictive_from_independentsampling_from_model_5668_to_5890_alltopologies.pickle'
          ]:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist_all.append(p)

modselection_postpred_all = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist_all):
    print(n)
    modselection_postpred_all['NE_obs'] = pd.concat(
        [modselection_postpred_all['NE_obs'], p['NE_obs']])
    modselection_postpred_all['NEv1_obs'] = pd.concat(
        [modselection_postpred_all['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred_all['NEv2_obs'] = pd.concat(
        [modselection_postpred_all['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred_all['NonNE_obs'] = pd.concat(
        [modselection_postpred_all['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'TKO_trajectories_as_postpredictive_from_independentsampling_alltopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred_all,fp,protocol=4)

#
# RPM

# top topologies
post_picklelist_top = []
for f in [indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_0_to_329_toptopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_329_to_587_toptopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_587_to_726_toptopologies.pickle']:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist_top.append(p)

modselection_postpred_top = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist_top):
    print(n)
    modselection_postpred_top['NE_obs'] = pd.concat(
        [modselection_postpred_top['NE_obs'], p['NE_obs']])
    modselection_postpred_top['NEv1_obs'] = pd.concat(
        [modselection_postpred_top['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred_top['NEv2_obs'] = pd.concat(
        [modselection_postpred_top['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred_top['NonNE_obs'] = pd.concat(
        [modselection_postpred_top['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'RPM_trajectories_as_postpredictive_from_independentsampling_toptopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred_top,fp,protocol=4)

# all topologies
post_picklelist_all = []
for f in [indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_0_to_252_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_252_to_505_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_505_to_726_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_726_to_764_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_764_to_1014_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_1014_to_1269_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_1269_to_1543_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_1543_to_1822_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_1822_to_2080_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_2080_to_2333_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_2333_to_2590_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_2590_to_2844_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_2844_to_3105_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_3105_to_3367_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_3367_to_3630_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_3630_to_3890_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_3890_to_4146_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_4146_to_4409_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_4409_to_4670_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_4670_to_4924_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_4924_to_5179_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_5179_to_5433_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_5433_to_5692_alltopologies.pickle',
          indirdict['post'] + 'RPM_trajectories_as_postpredictive_from_independentsampling_from_model_5692_to_5890_alltopologies.pickle'
          ]:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist_all.append(p)

modselection_postpred_all = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist_all):
    print(n)
    modselection_postpred_all['NE_obs'] = pd.concat(
        [modselection_postpred_all['NE_obs'], p['NE_obs']])
    modselection_postpred_all['NEv1_obs'] = pd.concat(
        [modselection_postpred_all['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred_all['NEv2_obs'] = pd.concat(
        [modselection_postpred_all['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred_all['NonNE_obs'] = pd.concat(
        [modselection_postpred_all['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'RPM_trajectories_as_postpredictive_from_independentsampling_alltopologies_new.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred_all,fp,protocol=4)

#
# cell_line_A

# top topologies
post_picklelist_top = []
for f in [indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_0_to_2078_toptopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_2078_to_2193_toptopologies.pickle']:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist_top.append(p)

modselection_postpred_top = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist_top):
    print(n)
    modselection_postpred_top['NE_obs'] = pd.concat(
        [modselection_postpred_top['NE_obs'], p['NE_obs']])
    modselection_postpred_top['NEv1_obs'] = pd.concat(
        [modselection_postpred_top['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred_top['NEv2_obs'] = pd.concat(
        [modselection_postpred_top['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred_top['NonNE_obs'] = pd.concat(
        [modselection_postpred_top['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'cl_A_trajectories_as_postpredictive_from_independentsampling_toptopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred_top,fp,protocol=4)

# all topologies
post_picklelist_all = []
for f in [indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_0_to_252_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_252_to_504_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_504_to_757_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_757_to_1007_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_1007_to_1260_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_1260_to_1522_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_1522_to_1800_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_1800_to_2059_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_2059_to_2193_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_2193_to_2313_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_2313_to_2570_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_2570_to_2825_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_2825_to_3088_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_3088_to_3349_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_3349_to_3619_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_3619_to_3877_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_3877_to_4132_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_4132_to_4405_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_4405_to_4667_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_4667_to_4920_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_4920_to_5174_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_5174_to_5425_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_5425_to_5681_alltopologies.pickle',
          indirdict['post'] + 'cl_A_trajectories_as_postpredictive_from_independentsampling_from_model_5681_to_5890_alltopologies.pickle'
          ]:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist_all.append(p)

modselection_postpred_all = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist_all):
    print(n)
    modselection_postpred_all['NE_obs'] = pd.concat(
        [modselection_postpred_all['NE_obs'], p['NE_obs']])
    modselection_postpred_all['NEv1_obs'] = pd.concat(
        [modselection_postpred_all['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred_all['NEv2_obs'] = pd.concat(
        [modselection_postpred_all['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred_all['NonNE_obs'] = pd.concat(
        [modselection_postpred_all['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'cl_A_trajectories_as_postpredictive_from_independentsampling_alltopologies.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred_all,fp,protocol=4)
