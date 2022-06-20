from scipy.stats import norm, uniform, beta
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd
import gzip

indir = '../posterior_marginals_and_predictives/'
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

zerotoone = np.linspace(0,1,101)

obstonamedict={'NE_obs':'Subtype A',
    'NEv1_obs':'Subtype N',
    'NEv2_obs':'Subtype A2',
    'NonNE_obs':'Subtype Y'
}

obstocolordict={'NonNE_obs':{'prior':'rosybrown','post':'red'},
    'NEv1_obs':{'prior':'burlywood','post':'orange'},
    'NEv2_obs':{'prior':'darkseagreen','post':'green'},
    'NE_obs':{'prior':'cadetblue','post':'blue'},
    'TKO':'purple',
    'RPM':'turquoise',
    'cl_A':'pink'
}

plt.rcParams.update({'font.size': 16})
element='step'

modselection_priorpred_alldata = {}
modselection_postpred_alldata = {}

for j in ['TKO','RPM','cl_A']:
    print(j,'prior')
    with gzip.open(indir+j+'_trajectories_as_priorpredictive_allmodels_somemissing_6_10_22.pklz','rb') as fp:
        modselection_priorpred_alldata[j] = pickle.load(fp)
    print(j,'post')
    with gzip.open(indir+j+'_trajectories_as_postpredictive_from_postequalweights_allmodels_somemissing_6_10_22.pklz','rb') as fp:
        modselection_postpred_alldata[j] = pickle.load(fp)

for j in ['TKO','RPM','cl_A']:
    modselection_postpred = modselection_postpred_alldata[j]
    modselection_priorpred = modselection_priorpred_alldata[j]
    fig, axs = plt.subplots(2,2,figsize=(12,6))
    currdim = 0
    for obs in obs_list:
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
            ax.set_ylim(0,np.nanmax(getmax))
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
            ax.set_ylim(0,np.nanmax(getmax))
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
        #plt.plot(g.get_children()[1].get_paths()[0].vertices[:, 0], g.get_children()[1].get_paths()[0].vertices[:, 1])
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
    plt.tight_layout()
    plt.savefig(outdir+j+'_datadistr_prior_posterior_integral.pdf',format='pdf')
    plt.show()
