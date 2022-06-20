### Put together the posterior predictive simulations, which involves consolidating within each dataset and save

import pandas as pd
import gzip
import pickle

indirdict = {
    'TKO': {'prior':'../posterior_marginals_and_predictives/prior_posterior_predictives_all/priors_TKO/',
            'post':'../posterior_marginals_and_predictives/prior_posterior_predictives_all/posteriors_TKO/'},
    'RPM': {'prior':'../posterior_marginals_and_predictives/prior_posterior_predictives_all/priors_RPM/',
            'post':'../posterior_marginals_and_predictives/prior_posterior_predictives_all/posteriors_RPM/'},
    'cl_A': {'prior':'../posterior_marginals_and_predictives/prior_posterior_predictives_all/priors_cl_A/',
                    'post':'../posterior_marginals_and_predictives/prior_posterior_predictives_all/posteriors_cl_A/'}
}

outdir = '../posterior_marginals_and_predictives/'
###

# TKO
indir_TKO_post = indirdict['TKO']['post']

post_picklelist = []
for f in [indir_TKO_post
            +'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_0_to_264_onlyupdatedmodels.pickle',
          indir_TKO_post
            +'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_264_to_522_onlyupdatedmodels.pickle',
          indir_TKO_post
            +'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_522_to_788_onlyupdatedmodels.pickle',
          indir_TKO_post
            +'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_788_to_1038_onlyupdatedmodels.pickle',
          indir_TKO_post
            +'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_1038_to_1288_onlyupdatedmodels.pickle',
          indir_TKO_post
            +'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_1288_to_1541_onlyupdatedmodels.pickle',
          indir_TKO_post
            +'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_1541_to_1800_onlyupdatedmodels.pickle',
          indir_TKO_post
            +'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_1800_to_2067_onlyupdatedmodels.pickle',
          indir_TKO_post
            +'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_2067_to_2327_onlyupdatedmodels.pickle',
          indir_TKO_post
            +'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_2327_to_2587_onlyupdatedmodels.pickle',
          indir_TKO_post
            +'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_2587_to_2859_onlyupdatedmodels.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_2859_to_3199.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_3199_to_3866.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_3866_to_4454.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_4454_to_4708.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_4708_to_4967.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_4967_to_5230.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_5230_to_7306.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_7306_to_7572.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_7572_to_7866.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_7866_to_8147.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_8147_to_8449.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_8449_to_8806.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_8806_to_9151.pickle',
          indir_TKO_post+'TKO_trajectories_as_postpredictive_from_postequalweights_from_model_9151_to_9264.pickle']:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist.append(p)

modselection_postpred = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist):
    print(n)
    modselection_postpred['NE_obs'] = pd.concat(
        [modselection_postpred['NE_obs'], p['NE_obs']])
    modselection_postpred['NEv1_obs'] = pd.concat(
        [modselection_postpred['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred['NEv2_obs'] = pd.concat(
        [modselection_postpred['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred['NonNE_obs'] = pd.concat(
        [modselection_postpred['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'TKO_trajectories_as_postpredictive_from_postequalweights_allmodels_somemissing_6_10_22.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred,fp,protocol=4)

#
# RPM
indir_RPM_post = indirdict['RPM']['post']

post_picklelist = []
for f in [indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_0_to_552.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_552_to_1138.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_1138_to_1395.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_1395_to_1652.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_1652_to_1946.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_1946_to_2249.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_2249_to_2578.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_2578_to_2859.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_2859_to_3178.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_3178_to_3745.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_3745_to_4424.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_4424_to_4677.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_4677_to_4932.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_4932_to_5184.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_5184_to_6681.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_6681_to_7533.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_7533_to_7824.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_7824_to_8113.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_8113_to_8336.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_8336_to_8565.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_8565_to_8908.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_8908_to_9128.pickle',
          indir_RPM_post+'RPM_trajectories_as_postpredictive_from_postequalweights_from_model_9128_to_9262.pickle']:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist.append(p)

modselection_postpred = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist):
    print(n)
    modselection_postpred['NE_obs'] = pd.concat(
        [modselection_postpred['NE_obs'], p['NE_obs']])
    modselection_postpred['NEv1_obs'] = pd.concat(
        [modselection_postpred['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred['NEv2_obs'] = pd.concat(
        [modselection_postpred['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred['NonNE_obs'] = pd.concat(
        [modselection_postpred['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'RPM_trajectories_as_postpredictive_from_postequalweights_allmodels_somemissing_6_10_22.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred,fp,protocol=4)

#
# cell_line_A
indir_clA_post = indirdict['cl_A']['post']

post_picklelist = []
for f in [indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_0_to_552.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_552_to_1137.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_1137_to_1392.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_1392_to_1650.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_1650_to_1949.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_1949_to_2252.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_2252_to_2581.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_2581_to_2877.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_2877_to_3205.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_3205_to_3861.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_3861_to_4445.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_4445_to_4718.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_4718_to_4979.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_4979_to_5000.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_5000_to_5257.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_5257_to_7293.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_7293_to_7568.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_7568_to_7859.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_7859_to_8141.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_8141_to_8426.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_8426_to_8768.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_8768_to_9133.pickle',
          indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_from_model_9133_to_9262.pickle']:
    print(f)
    p = pd.read_pickle(f)
    post_picklelist.append(p)

modselection_postpred = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(post_picklelist):
    print(n)
    modselection_postpred['NE_obs'] = pd.concat(
        [modselection_postpred['NE_obs'], p['NE_obs']])
    modselection_postpred['NEv1_obs'] = pd.concat(
        [modselection_postpred['NEv1_obs'], p['NEv1_obs']])
    modselection_postpred['NEv2_obs'] = pd.concat(
        [modselection_postpred['NEv2_obs'], p['NEv2_obs']])
    modselection_postpred['NonNE_obs'] = pd.concat(
        [modselection_postpred['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+indir_clA_post+'cl_A_trajectories_as_postpredictive_from_postequalweights_allmodels_somemissing_6_10_22.pklz',
          'wb') as fp:
    pickle.dump(modselection_postpred,fp,protocol=4)

### Put together the prior predictive simulations, which involves consolidating within each dataset and saving

##
# TKO
# can't just for loop TKO, RPM, cl_A because the numbers ("from_model_x_to_y") are different for the pickle files

indir_TKO_prior = indirdict['TKO']['prior']

prior_picklelist = []
for f in [indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_0_to_560.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_560_to_1146.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_1146_to_1288.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_1288_to_1541.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_1541_to_1650.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_1650_to_1959.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_1959_to_2274.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_2274_to_2604.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_2604_to_2859.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_2859_to_3199.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_3199_to_3866.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_3866_to_4454.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_4454_to_4708.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_4708_to_4967.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_4967_to_5230.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_5230_to_7306.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_7306_to_7572.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_7572_to_7866.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_7866_to_8147.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_8147_to_8449.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_8449_to_8806.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_8806_to_9151.pickle',
          indir_TKO_prior+'TKO_trajectories_as_priorpredictive_from_model_9151_to_9264.pickle']:
    print(f)
    p = pd.read_pickle(f)
    prior_picklelist.append(p)

modselection_priorpred = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(prior_picklelist):
    print(n)
    modselection_priorpred['NE_obs'] = pd.concat(
        [modselection_priorpred['NE_obs'], p['NE_obs']])
    modselection_priorpred['NEv1_obs'] = pd.concat(
        [modselection_priorpred['NEv1_obs'], p['NEv1_obs']])
    modselection_priorpred['NEv2_obs'] = pd.concat(
        [modselection_priorpred['NEv2_obs'], p['NEv2_obs']])
    modselection_priorpred['NonNE_obs'] = pd.concat(
        [modselection_priorpred['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'TKO_trajectories_as_priorpredictive_allmodels_somemissing_6_10_22.pklz',
          'wb') as fp:
    pickle.dump(modselection_priorpred,fp,protocol=4)

#
# RPM
indir_RPM_prior = indirdict['RPM']['prior']

prior_picklelist = []
for f in [indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_0_to_552.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_552_to_1138.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_1138_to_1395.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_1395_to_1652.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_1652_to_1946.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_1946_to_2249.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_2249_to_2578.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_2578_to_2859.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_2859_to_3178.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_3178_to_3745.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_3745_to_4424.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_4424_to_4677.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_4677_to_4932.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_4932_to_5184.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_5184_to_6681.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_6681_to_7533.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_7533_to_7824.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_7824_to_8113.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_8113_to_8336.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_8336_to_8565.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_8565_to_8908.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_8908_to_9128.pickle',
          indir_RPM_prior+'RPM_trajectories_as_priorpredictive_from_model_9128_to_9262.pickle']:
    print(f)
    p = pd.read_pickle(f)
    prior_picklelist.append(p)

modselection_priorpred = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(prior_picklelist):
    print(n)
    modselection_priorpred['NE_obs'] = pd.concat(
        [modselection_priorpred['NE_obs'], p['NE_obs']])
    modselection_priorpred['NEv1_obs'] = pd.concat(
        [modselection_priorpred['NEv1_obs'], p['NEv1_obs']])
    modselection_priorpred['NEv2_obs'] = pd.concat(
        [modselection_priorpred['NEv2_obs'], p['NEv2_obs']])
    modselection_priorpred['NonNE_obs'] = pd.concat(
        [modselection_priorpred['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'RPM_trajectories_as_priorpredictive_allmodels_somemissing_6_10_22.pklz',
          'wb') as fp:
    pickle.dump(modselection_priorpred,fp,protocol=4)

#
# cl_A
indir_clA_prior = indirdict['cl_A']['prior']

prior_picklelist = []
for f in [indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_0_to_552.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_552_to_1137.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_1137_to_1392.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_1392_to_1650.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_1650_to_1949.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_1949_to_2252.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_2252_to_2581.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_2581_to_2877.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_2877_to_3205.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_3205_to_3861.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_3861_to_4445.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_4445_to_4718.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_4718_to_4979.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_4979_to_5000.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_5000_to_5257.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_5257_to_7293.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_7293_to_7568.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_7568_to_7859.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_7859_to_8141.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_8141_to_8426.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_8426_to_8768.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_8768_to_9133.pickle',
          indir_clA_prior+'cl_A_trajectories_as_priorpredictive_from_model_9133_to_9262.pickle']:
    print(f)
    p = pd.read_pickle(f)
    prior_picklelist.append(p)



modselection_priorpred = {
    'NE_obs': pd.DataFrame(),
    'NEv1_obs': pd.DataFrame(),
    'NEv2_obs': pd.DataFrame(),
    'NonNE_obs': pd.DataFrame()
    }

for n,p in enumerate(prior_picklelist):
    print(n)
    modselection_priorpred['NE_obs'] = pd.concat(
        [modselection_priorpred['NE_obs'], p['NE_obs']])
    modselection_priorpred['NEv1_obs'] = pd.concat(
        [modselection_priorpred['NEv1_obs'], p['NEv1_obs']])
    modselection_priorpred['NEv2_obs'] = pd.concat(
        [modselection_priorpred['NEv2_obs'], p['NEv2_obs']])
    modselection_priorpred['NonNE_obs'] = pd.concat(
        [modselection_priorpred['NonNE_obs'], p['NonNE_obs']])

with gzip.open(outdir+'cl_A_trajectories_as_priorpredictive_allmodels_somemissing_6_10_22.pklz',
          'wb') as fp:
    pickle.dump(modselection_priorpred,fp,protocol=4)

