from scipy.stats import norm, uniform, beta
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd
import gzip
from matplotlib import ticker
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import FuncFormatter


indir =  '../posterior_marginals_and_predictives/'
outdir = '../generated_figures/'

fittingdatadict = {
    'TKO':pd.read_csv('../cibersort_data/cibersort_data_Sage.csv'),
    'RPM':pd.read_csv('../cibersort_data/cibersort_data_Oliver.csv'),
    'cl_A':pd.read_csv('../cibersort_data/cibersort_data_cl_cluster_A.csv')
}

obs_list = ['NE_obs', 'NEv1_obs', 'NEv2_obs', 'NonNE_obs']

for j in fittingdatadict:
    dat = fittingdatadict[j]
    newcol = []
    for i in dat.columns:
        if i=='ML' or i=='NonNE':
            newcol.append('NonNE_obs')
        elif i=='MLH' or i=='NEv2':
            newcol.append('NEv2_obs')
        elif i=='NEH' or i=='NEv1':
            newcol.append('NEv1_obs')
        elif i=='NE':
            newcol.append('NE_obs')
        else:
            newcol.append(i)
    dat.columns = newcol
    if j == 'RPM':
        fittingdatadict[j] = dat.loc[dat['Input Sample'].str.startswith('PB',na=False)]

def beta_dist_from_mu_and_stdev(mu,std):
    nu_out = (mu*(1-mu)/(std**2)) - 1
    alpha_out = mu*nu_out
    beta_out = (1-mu)*nu_out
    return beta(alpha_out,beta_out)

def remove_empty_plots(fig, axs, dims_plotted, columns, rows):
    ## The plt.subplots() function puts a plot in every single row and column, so eliminate empty plots and replace them with empty space
    dims_plotted = list(set(dims_plotted))
    tot_plots = columns * rows
    to_del = []
    for i in range(0, tot_plots):
        if not i in dims_plotted:
            to_del.append(i)
    #
    for dim in to_del:
        ax = axs[int((dim - dim % columns) / columns), (dim % columns)]
        fig.delaxes(ax)

zerotoone = np.linspace(0,1,101)

obstonamedict={'NE_obs':'Subtype A',
    'NEv1_obs':'Subtype N',
    'NEv2_obs':'Subtype A2',
    'NonNE_obs':'Subtype Y'
}

# # if we want them all similar colors...? i think too confusing to look at though
# obstocolordict={'NonNE_obs':{'prior':'rosybrown','post':'darkred','post_indep':'red'},
#     'NEv1_obs':{'prior':'burlywood','post':'darkorange','post_indep':'orange'},
#     'NEv2_obs':{'prior':'darkseagreen','post':'darkgreen','post_indep':'green'},
#     'NE_obs':{'prior':'cadetblue','post':'darkblue','post_indep':'blue'},
#     'TKO':'purple',
#     'RPM':'turquoise',
#     'cl_A':'pink'
# }

# where the posterior independent parameter sampling is all gray
obstocolordict={'NonNE_obs':{'prior':'rosybrown','post':'red','post_indep':'gray'},
    'NEv1_obs':{'prior':'burlywood','post':'orange','post_indep':'gray'},
    'NEv2_obs':{'prior':'darkseagreen','post':'green','post_indep':'gray'},
    'NE_obs':{'prior':'cadetblue','post':'blue','post_indep':'gray'},
    'TKO':'purple',
    'RPM':'turquoise',
    'cl_A':'pink'
}

plt.rcParams.update({'font.size': 16})
element='step'

modselection_priorpred_alldata = {}
modselection_postpred_alldata = {}
modselection_postpred_indep_alldata = {}

for j in ['TKO','RPM','cl_A']:
    print(j,'prior')
    with gzip.open(indir+j+'_trajectories_as_priorpredictive_toptopologies.pklz','rb') as fp:
        modselection_priorpred_alldata[j] = pickle.load(fp)
    print(j,'post (joint)')
    with gzip.open(indir+j+'_trajectories_as_postpredictive_from_postequalweights_toptopologies.pklz','rb') as fp:
        modselection_postpred_alldata[j] = pickle.load(fp)
    print(j,'post (independent)')
    with gzip.open(indir+j+'_trajectories_as_postpredictive_from_independentsampling_toptopologies.pklz','rb') as fp:
        modselection_postpred_indep_alldata[j] = pickle.load(fp)

## Fig S4, posterior predictive using parameters sampled from the joint posterior distribution

for j in ['TKO','RPM','cl_A']:
    modselection_postpred = modselection_postpred_alldata[j]
    modselection_priorpred = modselection_priorpred_alldata[j]
    modselection_postpred_indep = modselection_postpred_indep_alldata[j]
    fig, axs = plt.subplots(2,2,figsize=(12,7))
    currdim = 0
    dims_plotted = []
    for n, obs in enumerate(obs_list):
        ## this is here for "top topology" models, which don't include 4 subtype
        if (j == 'TKO' and obs == 'NEv1_obs') or (j == 'RPM' and obs == 'NEv2_obs') or (j=='cl_A' and obs == 'NonNE_obs'):
            currdim += 1
            continue
        dims_plotted.append(n)
        print(obs)
        if modselection_priorpred[obs].iloc[-1].name != len(modselection_priorpred[obs])-1:
            modselection_priorpred[obs].reset_index(inplace=True, drop=True)
        if modselection_postpred[obs].iloc[-1].name != len(modselection_postpred[obs])-1:
            modselection_postpred[obs].reset_index(inplace=True, drop=True)
        ax = axs[int((currdim - currdim % 2) / 2), (currdim % 2)]
        # barplots don't show up well if all zeros / essentially zeros
        if len(np.where(abs(modselection_priorpred[obs][60.0])>1e-10)[0]) == 0:
            #print(obs)
            # calculate "true" binwidth before setting an erroneous value
            binwidth = np.max(modselection_priorpred[obs][60.0])-np.min(modselection_priorpred[obs][60.0]) \
                * 10**abs(np.floor(np.log10(np.max(modselection_priorpred[obs][60.0]) - np.min(
                modselection_priorpred[obs][60.0])))+2)
            # if that doesn't work:
            if binwidth == 0 or np.isnan(binwidth):
                binwidth = 0.03
            modselection_priorpred[obs][60.0].loc[0]=0.05
            getmax = np.where(
                beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).pdf(
                    zerotoone) == np.inf, np.nan,
                beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).pdf(zerotoone))
            ax.set_ylim(0,np.nanmax(getmax)+5)
            g = sns.histplot(modselection_priorpred[obs][60.0], binwidth=0.025, stat='density',
                     color=obstocolordict[obs]['prior'], element=element, fill=True, alpha=0.25,
                     label='subtype prior predictive', ax=ax)
        else:
            g = sns.histplot(modselection_priorpred[obs][60.0], binwidth=0.025, stat='density',
                             color=obstocolordict[obs]['prior'], element=element, fill=True, alpha=0.25,
                             label='subtype prior predictive', ax=ax)
        if len(np.where(abs(modselection_postpred[obs][60.0])>1e-10)[0]) == 0:
            # calculate "true" binwidth before setting an erroneous value
            binwidth = np.max(modselection_postpred[obs][60.0]) - np.min(
                modselection_postpred[obs][60.0]) \
                       * 10 ** abs(
                np.floor(np.log10(np.max(modselection_postpred[obs][60.0]) - np.min(
                    modselection_postpred[obs][60.0])))+2)
            if binwidth == 0 or np.isnan(binwidth):
                binwidth = 0.03
            modselection_postpred[obs][60.0].loc[0]=0.05
            getmax = np.where(
                beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).pdf(
                    zerotoone) == np.inf, np.nan,
                beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).pdf(zerotoone))
            ax.set_ylim(0,np.nanmax(getmax)+5)
            # if you only plot posteriors, needs to be g =
            sns.histplot(x=modselection_postpred[obs][60.0], binwidth=binwidth, stat='density',
                         weights=modselection_postpred[obs]['post_prob'],
                         color=obstocolordict[obs]['post'],
                         element=element, fill=True, alpha=0.25, label='subtype posterior predictive', ax=ax)
        else:
            # if you only plot posteriors, needs to be g =
            sns.histplot(x=modselection_postpred[obs][60.0], binwidth=0.025, stat='density',
                         weights=modselection_postpred[obs]['post_prob'],
                         color=obstocolordict[obs]['post'],
                         element=element, fill=True, alpha=0.25, label='subtype posterior predictive', ax=ax)
        #plt.plot(g.get_children()[0].get_paths()[0].vertices[:, 0], g.get_children()[0].get_paths()[0].vertices[:, 1])
        x_pre = g.get_children()[0].get_paths()[0].vertices[:, 0]
        x_pre = np.flip(x_pre)
        fx_pre = g.get_children()[0].get_paths()[0].vertices[:, 1]
        fx_pre = np.flip(fx_pre)
        x_post = g.get_children()[1].get_paths()[0].vertices[:, 0]
        # if you only plot posteriors, (thus commenting out "x_pre =" and "fx_pre =" lines) the following needs to be:
        #x_post = g.get_children()[0].get_paths()[0].vertices[:, 0]
        x_post = np.flip(x_post)
        fx_post = g.get_children()[1].get_paths()[0].vertices[:, 1]
        # if you only plot posteriors, needs to be:
        #fx_post = g.get_children()[0].get_paths()[0].vertices[:, 1]
        fx_post = np.flip(fx_post)
        ax.plot(zerotoone,beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(),
                                                      fittingdatadict[j][obs].std()).pdf(zerotoone),
                color=obstocolordict[j])
        ax.fill_between(zerotoone,0,beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(),fittingdatadict[j][obs].std()).pdf(zerotoone),color=obstocolordict[j],alpha=0.25,label='probabilistic representation, '+j+' data')
        lower = beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).ppf(.05/2)
        lower_pre = np.where(x_pre==min(x_pre, key=lambda i:abs(i-lower)))[0][0]
        lower_post = np.where(x_post==min(x_post, key=lambda i:abs(i-lower)))[0][0]
        upper = beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).ppf(1-(0.05/2))
        upper_pre = np.where(x_pre==min(x_pre, key=lambda i:abs(i-upper)))[0][0]+1
        upper_post = np.where(x_post==min(x_post, key=lambda i:abs(i-upper)))[0][0]+1
        ax.plot(x_pre[lower_pre:upper_pre], fx_pre[lower_pre:upper_pre], color=obstocolordict[obs]['prior'])
        ax.plot(x_post[lower_post:upper_post], fx_post[lower_post:upper_post], color=obstocolordict[obs]['post'])
        ax.fill_between(x_post[lower_post:upper_post],0,fx_post[lower_post:upper_post], color='turquoise', alpha=0.5,
                        label='integral under posterior: '+format(np.trapz(fx_post[lower_post:upper_post], x_post[lower_post:upper_post]) / np.trapz(fx_post, x_post),'.2f'))
        ax.fill_between(x_pre[lower_pre:upper_pre],0,fx_pre[lower_pre:upper_pre], color='oldlace', alpha=0.5,
                        label='integral under prior: '+format(np.trapz(fx_pre[lower_pre:upper_pre],x_pre[lower_pre:upper_pre])/np.trapz(fx_pre,x_pre), '.2f'))
        print('posterior predictive 95 CI integral',np.trapz(fx_post[lower_post:upper_post],x_post[lower_post:upper_post])/np.trapz(fx_post,x_post))
        ax.legend(prop={'size':12})
        ax.set_title(obstonamedict[obs])
        ax.set_xlabel('')
        currdim += 1
    remove_empty_plots(fig, axs, dims_plotted, 2, 2)
    plt.tight_layout()
    plt.savefig(outdir+j+'_datadistr_prior_posterior_integral.pdf',format='pdf')
    plt.show()

## Fig S4, posterior predictive using parameters sampled independently from each parameter marginal distribution
for j in ['TKO','RPM','cl_A']:
    modselection_postpred = modselection_postpred_alldata[j]
    modselection_priorpred = modselection_priorpred_alldata[j]
    modselection_postpred_indep = modselection_postpred_indep_alldata[j]
    fig, axs = plt.subplots(2,2,figsize=(12,7))
    currdim = 0
    dims_plotted = []
    for n, obs in enumerate(obs_list):
        ## this is here for "top topology" models, which don't include 4 subtype
        if (j == 'TKO' and obs == 'NEv1_obs') or (j == 'RPM' and obs == 'NEv2_obs') or (j=='cl_A' and obs == 'NonNE_obs'):
            currdim += 1
            continue
        dims_plotted.append(n)
        print(obs)
        if modselection_priorpred[obs].iloc[-1].name != len(modselection_priorpred[obs])-1:
            modselection_priorpred[obs].reset_index(inplace=True, drop=True)
        if modselection_postpred_indep[obs].iloc[-1].name != len(modselection_postpred_indep[obs])-1:
            modselection_postpred_indep[obs].reset_index(inplace=True, drop=True)
        if modselection_postpred[obs].iloc[-1].name != len(modselection_postpred[obs])-1:
            modselection_postpred[obs].reset_index(inplace=True, drop=True)
        ax = axs[int((currdim - currdim % 2) / 2), (currdim % 2)]
        ## plot prior predictive
        # barplots don't show up well if all zeros / essentially zeros
        if len(np.where(abs(modselection_priorpred[obs][60.0])>1e-10)[0]) == 0:
            #print(obs)
            # calculate "true" binwidth before setting an erroneous value
            binwidth = np.max(modselection_priorpred[obs][60.0])-np.min(modselection_priorpred[obs][60.0]) \
                * 10**abs(np.floor(np.log10(np.max(modselection_priorpred[obs][60.0]) - np.min(
                modselection_priorpred[obs][60.0])))+2)
            # if that doesn't work:
            if binwidth == 0 or np.isnan(binwidth):
                binwidth = 0.03
            modselection_priorpred[obs][60.0].loc[0]=0.05
            getmax = np.where(
                beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).pdf(
                    zerotoone) == np.inf, np.nan,
                beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).pdf(zerotoone))
            ax.set_ylim(0,np.nanmax(getmax)+5)
            g = sns.histplot(modselection_priorpred[obs][60.0], binwidth=0.025, stat='density',
                     color=obstocolordict[obs]['prior'], element=element, fill=True, alpha=0.25,
                     label='subtype prior predictive', ax=ax)
        else:
            g = sns.histplot(modselection_priorpred[obs][60.0], binwidth=0.025, stat='density',
                             color=obstocolordict[obs]['prior'], element=element, fill=True, alpha=0.25,
                             label='subtype prior predictive', ax=ax)
        ## plot post independent-sampling predictive
        if len(np.where(abs(modselection_postpred_indep[obs][60.0])>1e-10)[0]) == 0:
            # calculate "true" binwidth before setting an erroneous value
            binwidth = np.max(modselection_postpred_indep[obs][60.0]) - np.min(
                modselection_postpred_indep[obs][60.0]) \
                       * 10 ** abs(
                np.floor(np.log10(np.max(modselection_postpred_indep[obs][60.0]) - np.min(
                    modselection_postpred_indep[obs][60.0])))+2)
            if binwidth == 0 or np.isnan(binwidth):
                binwidth = 0.03
            #modselection_postpred[obs][60.0].loc[0]=0.05
            getmax = np.where(
                beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).pdf(
                    zerotoone) == np.inf, np.nan,
                beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).pdf(zerotoone))
            ax.set_ylim(0,np.nanmax(getmax)+5)
            # if you only plot posteriors, needs to be g =
            sns.histplot(x=modselection_postpred_indep[obs][60.0], binwidth=binwidth, stat='density',
                         weights=modselection_postpred_indep[obs]['post_prob'],
                         color=obstocolordict[obs]['post_indep'],
                         element=element, fill=True, alpha=0.25, label='subtype independent posterior predictive', ax=ax)
        else:
            # if you only plot posteriors, needs to be g =
            sns.histplot(x=modselection_postpred_indep[obs][60.0], binwidth=0.025, stat='density',
                         weights=modselection_postpred_indep[obs]['post_prob'],
                         color=obstocolordict[obs]['post_indep'],
                         element=element, fill=True, alpha=0.25, label='subtype independent posterior predictive', ax=ax)
        ## plot joint posterior predictive
        if len(np.where(abs(modselection_postpred[obs][60.0])>1e-10)[0]) == 0:
            # calculate "true" binwidth before setting an erroneous value
            binwidth = np.max(modselection_postpred[obs][60.0]) - np.min(
                modselection_postpred[obs][60.0]) \
                       * 10 ** abs(
                np.floor(np.log10(np.max(modselection_postpred[obs][60.0]) - np.min(
                    modselection_postpred[obs][60.0])))+2)
            if binwidth == 0 or np.isnan(binwidth):
                binwidth = 0.03
            #modselection_postpred[obs][60.0].loc[0]=0.05
            getmax = np.where(
                beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).pdf(
                    zerotoone) == np.inf, np.nan,
                beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).pdf(zerotoone))
            ax.set_ylim(0,np.nanmax(getmax)+5)
            # if you only plot posteriors, needs to be g =
            sns.histplot(x=modselection_postpred[obs][60.0], binwidth=binwidth, stat='density',
                         weights=modselection_postpred[obs]['post_prob'],
                         color=obstocolordict[obs]['post'],
                         element=element, fill=True, alpha=0.25, label='subtype joint posterior predictive', ax=ax)
        else:
            # if you only plot posteriors, needs to be g =
            sns.histplot(x=modselection_postpred[obs][60.0], binwidth=0.025, stat='density',
                         weights=modselection_postpred[obs]['post_prob'],
                         color=obstocolordict[obs]['post'],
                         element=element, fill=True, alpha=0.25, label='subtype joint posterior predictive', ax=ax)
        ## Currently not calculating integrals or using the data distributions for this part of the figure
        # x_pre = g.get_children()[0].get_paths()[0].vertices[:, 0]
        # x_pre = np.flip(x_pre)
        # fx_pre = g.get_children()[0].get_paths()[0].vertices[:, 1]
        # fx_pre = np.flip(fx_pre)
        # x_post = g.get_children()[1].get_paths()[0].vertices[:, 0]
        # # if you only plot posteriors, (thus commenting out "x_pre =" and "fx_pre =" lines) the following needs to be:
        # #x_post = g.get_children()[0].get_paths()[0].vertices[:, 0]
        # x_post = np.flip(x_post)
        # fx_post = g.get_children()[1].get_paths()[0].vertices[:, 1]
        # # if you only plot posteriors, needs to be:
        # #fx_post = g.get_children()[0].get_paths()[0].vertices[:, 1]
        # fx_post = np.flip(fx_post)
        # ax.plot(zerotoone,beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(),
        #                                               fittingdatadict[j][obs].std()).pdf(zerotoone),
        #         color=obstocolordict[j])
        # ax.fill_between(zerotoone,0,beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(),fittingdatadict[j][obs].std()).pdf(zerotoone),color=obstocolordict[j],alpha=0.25,label='probabilistic representation, '+j+' data')
        # lower = beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).ppf(.05/2)
        # lower_pre = np.where(x_pre==min(x_pre, key=lambda i:abs(i-lower)))[0][0]
        # lower_post = np.where(x_post==min(x_post, key=lambda i:abs(i-lower)))[0][0]
        # upper = beta_dist_from_mu_and_stdev(fittingdatadict[j][obs].mean(), fittingdatadict[j][obs].std()).ppf(1-(0.05/2))
        # upper_pre = np.where(x_pre==min(x_pre, key=lambda i:abs(i-upper)))[0][0]+1
        # upper_post = np.where(x_post==min(x_post, key=lambda i:abs(i-upper)))[0][0]+1
        # ax.plot(x_pre[lower_pre:upper_pre], fx_pre[lower_pre:upper_pre], color=obstocolordict[obs]['prior'])
        # ax.plot(x_post[lower_post:upper_post], fx_post[lower_post:upper_post], color=obstocolordict[obs]['post'])
        # ax.fill_between(x_post[lower_post:upper_post],0,fx_post[lower_post:upper_post], color='turquoise', alpha=0.5,
        #                 label='integral under posterior: '+format(np.trapz(fx_post[lower_post:upper_post], x_post[lower_post:upper_post]) / np.trapz(fx_post, x_post),'.2f'))
        # ax.fill_between(x_pre[lower_pre:upper_pre],0,fx_pre[lower_pre:upper_pre], color='oldlace', alpha=0.5,
        #                 label='integral under prior: '+format(np.trapz(fx_pre[lower_pre:upper_pre],x_pre[lower_pre:upper_pre])/np.trapz(fx_pre,x_pre), '.2f'))
        # print('posterior predictive 95 CI integral',np.trapz(fx_post[lower_post:upper_post],x_post[lower_post:upper_post])/np.trapz(fx_post,x_post))
        ax.legend(prop={'size':12})
        ax.set_title(obstonamedict[obs])
        ax.set_xlabel('')
        currdim += 1
    remove_empty_plots(fig, axs, dims_plotted, 2, 2)
    plt.tight_layout()
    plt.savefig(outdir+j+'_prior_postindep_jointposterior_nointegralordatadistr.pdf',format='pdf')
    plt.show()

# # to see TKO tumor trajectories as proportions of a whole tumor
#
# j = 'TKO'
#
# df = pd.read_pickle('../files_generated_in_MMI_sclc/results_fromNS_gathered_'+j+'_addlanalyses.pickle')
# df.sort_values('posterior_prob',ascending=False,inplace=True)
# # get 'top' models
# df = df.loc[df.INS_Z > (np.max(df.INS_Z) / 10 ** .5)]
#
# ## choosing the TKO 3-subtype top model from this, structure 2
#
# modselection_postpred = modselection_postpred_alldata[j]
#
# tspan = np.linspace(0,60,101)
#
# newmod = {}
# for obs in ['NE_obs','NEv2_obs','NonNE_obs']:
#     newmod[obs] = modselection_postpred[obs].loc[modselection_postpred[obs].from_model.isin(df.loc[df.subtype_starting_and_makeup_code.str.startswith('2')].index)]
#
# titledict = {
#     '2\.0010.':'TKO 3 subtype (A,A2,Y) no effects',
#     '2\.1010.':'TKO 3 subtype (A,A2,Y) division effects from Y'
# }
#
# for modmakeup_code in ['2\.0010.', '2\.1010.']:
#     plt.figure(figsize=(8,6))
#     obs = 'NE_obs'
#     plt.fill_between(tspan, np.mean(
#         newmod[obs].loc[newmod[obs].model_starting_subtype_makeup_code.str.contains(modmakeup_code)].sample(
#             250, random_state=42)[[x for x in newmod[obs].columns if isinstance(x, float)]]),
#                      color=obstocolordict[obs]['post'], label=obstonamedict[obs])
#     sum_prev = np.mean(newmod[obs].loc[newmod[obs].model_starting_subtype_makeup_code.str.contains(modmakeup_code)].sample(
#         250, random_state=42))[[x for x in newmod[obs].columns if isinstance(x, float)]]
#     for obs in ['NEv2_obs','NonNE_obs']:
#         plt.fill_between(tspan, np.mean(
#             newmod[obs].loc[newmod[obs].model_starting_subtype_makeup_code.str.contains(modmakeup_code)].sample(
#                 250, random_state=42)[[x for x in newmod[obs].columns if isinstance(x, float)]]) + sum_prev, sum_prev,
#                          color=obstocolordict[obs]['post'], label=obstonamedict[obs])
#         sum_prev += np.mean(newmod[obs].loc[newmod[obs].model_starting_subtype_makeup_code.str.contains(modmakeup_code)].sample(
#             250, random_state=42)[[x for x in newmod[obs].columns if isinstance(x, float)]])
#         plt.fill_between(tspan, np.mean(
#             newmod[obs].loc[newmod[obs].model_starting_subtype_makeup_code.str.contains(modmakeup_code)].sample(
#                 250)[[x for x in newmod[obs].columns if isinstance(x, float)]]) + sum_prev, sum_prev,
#                          color=obstocolordict[obs]['post'], label=obstonamedict[obs])
#     plt.ylim(0,1)
#     plt.legend(loc='lower right')
#     plt.ylabel('Proportion of tumor population')
#     plt.xlabel('Time')
#     plt.title(titledict[modmakeup_code])
#     plt.savefig(outdir + j + '_3subtype_code'+modmakeup_code.split('.')[1]+'.pdf', format='pdf')
#     plt.show()
