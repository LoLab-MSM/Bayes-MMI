import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
import math
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.stats import ttest_ind
from matplotlib import ticker
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import FuncFormatter
import sys

def magnitude(value):
    if (value == 0): return 0
    if not np.isnan(value):
        return int(math.floor(math.log10(abs(value))))
    else:
        return np.NaN

indir = '../posterior_marginals_and_predictives/'
outdir_fig =  '../generated_figures/'
outdir_file = '../files_generated_in_MMI_sclc/'

palette_dict = {
    'TKO':'Blues_r',
    'RPM':'Reds_r',
    'cl_A':'Greens_r'
}

topo_dict = {
    'TKO':['four_subtype','three_subtype_A_A2_Y','two_subtype_A_Y','two_subtype_A_A2'],
    'RPM':['four_subtype','three_subtype_A_N_Y','two_subtype_A_Y','two_subtype_A_N'],
    'cl_A':['four_subtype','three_subtype_A_N_A2','two_subtype_A_Y','two_subtype_A_N','two_subtype_A_A2']
}

topo_makeup_dict = {
    'four_subtype':'0',
    'three_subtype_A_N_Y':'1.',
    'three_subtype_A_A2_Y':'2',
    'three_subtype_A_N_A2':'4',
    'two_subtype_A_N':'5',
    'two_subtype_A_A2':'6',
    'two_subtype_A_Y':'7'
}

ordered_namelist = ['division_A_baseline',
                    'division_A_altered',
                    'division_A_equil_assn',
                    'division_N_baseline',
                    'division_N_altered',
                    'division_N_equil_assn',
                    'division_A2_baseline',
                    'division_A2_altered',
                    'division_A2_equil_assn',
                    'division_Y_baseline',
                    'division_Y_altered',
                    'division_Y_equil_assn',
                    'die_A_baseline',
                    'die_A_altered',
                    'die_A_equil_assn',
                    'die_N_baseline',
                    'die_N_altered',
                    'die_N_equil_assn',
                    'die_A2_baseline',
                    'die_A2_altered',
                    'die_A2_equil_assn',
                    'die_Y_baseline',
                    'die_Y_altered',
                    'die_Y_equil_assn',
                    'diff_A_to_N_baseline',
                    'diff_A_to_N_altered',
                    'diff_A_to_N_equil_assn',
                    'diff_N_to_A_baseline',
                    'diff_A_to_A2_baseline',
                    'diff_A_to_A2_altered',
                    'diff_A_to_A2_equil_assn',
                    'diff_A2_to_A_baseline',
                    'diff_N_to_Y_baseline',
                    'diff_N_to_Y_altered',
                    'diff_N_to_Y_equil_assn',
                    'diff_Y_to_N_baseline',
                    'diff_A2_to_Y_baseline',
                    'diff_A2_to_Y_altered',
                    'diff_A2_to_Y_equil_assn',
                    'diff_Y_to_A2_baseline',
                    'diff_N_to_A2_baseline',
                    'diff_A2_to_N_baseline',
                    'diff_A_to_Y_baseline',
                    'diff_Y_to_A_baseline']

alpha_val = 0.01

# for subplots_adjust later on
left = 0.2  # the value on the x axis where the left margin should be
right = 0.8
bottom = 0.2  # the value on the y axis where the bottom margin should be
top = 0.8
wspace = 1#0.5  # the proportion of the average of the left value and the right value -> for example, 0.2*((0.075+0.95)/2)
hspace = 1#0.8

## Fig 5B

num_to_sample = 1000
for dset in ['TKO', 'RPM', 'cl_A']:
    kde_dict = {dset:{}}
    df = pd.read_pickle(indir+dset+'_betafit_postmarg_params_and_probabilities_from_postequalweights.pklz',
                        compression='gzip')
    # starting with A (+/- others) subtype
    df = df[df['model_starting_subtype_makeup_code'].str.contains('\...1')]
    #
    for topo in topo_dict[dset]:
        kde_dict[dset][topo] = {}
        model_avgd = df[df['model_starting_subtype_makeup_code'].str.startswith(topo_makeup_dict[topo])]
        for n, i in enumerate(ordered_namelist):  # [i for i in list(set(names_dict.values()))]):
            try:
                if np.isnan(model_avgd[i]).all():
                    continue
                model_avgd[i][model_avgd[i] == np.inf] = np.nan
                model_avgd[i][model_avgd[i] == -np.inf] = np.nan
                plt_range = (
                    model_avgd[i].dropna().values.min(),
                    model_avgd[i].dropna().values.max())
                k = gaussian_kde(model_avgd.loc[~np.isnan(model_avgd[i])][i],
                                weights=model_avgd.loc[~np.isnan(model_avgd[i])].model_pp)
                kde_dict[dset][topo][i] = k
            except KeyError:
                print('UH OH')
                pass
            #break
    #
    all_topos_in_dset_all_params_df = pd.DataFrame()
    one_topology_all_params_df = pd.DataFrame()
    for topo in topo_dict[dset]:
        for i in kde_dict[dset][topo]:
            if not 'equil' in i and not 'die' in i and not 'alter' in i:
                samplefordf = kde_dict[dset][topo][i].resample(num_to_sample)
                df = pd.DataFrame(samplefordf).T
                df.columns = [i]
                one_topology_all_params_df = pd.concat([one_topology_all_params_df, df], axis=1)
        one_topology_all_params_df['topology'] = topo
        all_topos_in_dset_all_params_df = pd.concat([all_topos_in_dset_all_params_df, one_topology_all_params_df], ignore_index=True)
        one_topology_all_params_df = pd.DataFrame()
    #
    all_topos_in_dset_all_params_df.columns = [x.split('_baseline')[0] for x in all_topos_in_dset_all_params_df.columns if not x == 'topology'] + ['topology']
    df = pd.melt(all_topos_in_dset_all_params_df, id_vars=['topology'], value_vars=[x for x in all_topos_in_dset_all_params_df.columns if not x == 'topology'])
    #
    fig,ax=plt.subplots(figsize=(20,10))
    g = sns.boxplot(x='variable',y='value',hue='topology',data=df,palette=palette_dict[dset])
    for n in range(len(g.lines)):
       l = g.lines[n]
       l.set_linewidth(.25)
    #
    plt.setp(ax.get_xticklabels(), rotation=90)
    plt.title('Parameter values between TKO structures')
    plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    plt.xlabel('Parameter')
    plt.ylabel('Log parameter value')
    plt.savefig(outdir_fig + '/' + dset + '_comparison_across_highscoring_topologies.pdf', format='pdf')
    plt.show()
    for i in list(set(df.variable)):
        try:
            testsample = df.loc[~np.isnan(df.value)]
            testsample = testsample.loc[testsample.variable == i]
            topo_param_variances = {topo: np.var(testsample.loc[testsample.topology == topo]['value']) for topo in
                                    topo_dict[dset]}
            # check the variances - should be equal to do ANOVA + Tukey, also note if unequal for caught TypeError t-test
            eqvar = True
            if not np.all([magnitude(topo_param_variances[v]) for v in topo_param_variances]):  # np.all() ignores NaNs
                print('***************')
                print('variances are not the same (different order of magnitude) for param ' + str(i))
                for j in topo_param_variances:
                    print(j, topo_param_variances[j])
                print('***************')
                eqvar = False
            # now do ANOVA + Tukey (maybe)
            try:
                tukey = pairwise_tukeyhsd(endog=testsample['value'],
                                          groups=testsample['topology'],
                                          alpha=alpha_val)
            except TypeError:
                # this catches the statsmodels tukey test error thrown when there are only 2 topologies to compare
                #  and the p-value is "at bounds" (i assume this means too close to 0 or 1):
                #   error noted in https://github.com/statsmodels/statsmodels/issues/6132
                # since this isn't actually multiple comparisons, can run a t-test instead
                tukey = tuple(
                    (ttest_ind(testsample.loc[testsample.topology == list(set(testsample.topology))[0]]['value'],
                               testsample.loc[testsample.topology == list(set(testsample.topology))[1]]['value'],
                               equal_var=eqvar),
                     # ttest_ind doesn't return the names of the topologies it tests which i need for
                     #  building the results dict; tukey lists in alphabetical order so i will here too
                     sorted(list(set(testsample.topology)))[0], sorted(list(set(testsample.topology)))[1]))
                pass
            print(i)
            print(tukey)
        except ValueError:
            # this catches the tukey test error thrown when only one topology has a particular parameter distr
            #  (so nothing to compare)... leaving the print statement so the user can check that it's a parameter
            #  they'd expect to only be in one topology
            print('only one topo (no comparison possible)', i)

# calculate significance for Fig 5B (see Fig 5 legend / Methods)
num_to_sample = 1000
results_acrossdatasets = {}
for dset in ['TKO', 'RPM', 'cl_A']:
    kde_dict = {dset:{}}
    df = pd.read_pickle(indir+dset+'_betafit_postmarg_params_and_probabilities_from_postequalweights.pklz',
                        compression='gzip')
    # starting with A (+/- others) subtype
    df = df[df['model_starting_subtype_makeup_code'].str.contains('\...1')]
    #
    for topo in topo_dict[dset]:
        kde_dict[dset][topo] = {}
        model_avgd = df[df['model_starting_subtype_makeup_code'].str.startswith(topo_makeup_dict[topo])]
        for n, i in enumerate(ordered_namelist):  # [i for i in list(set(names_dict.values()))]):
            try:
                if np.isnan(model_avgd[i]).all():
                    continue
                model_avgd[i][model_avgd[i] == np.inf] = np.nan
                model_avgd[i][model_avgd[i] == -np.inf] = np.nan
                plt_range = (
                    model_avgd[i].dropna().values.min(),
                    model_avgd[i].dropna().values.max())
                k = gaussian_kde(model_avgd.loc[~np.isnan(model_avgd[i])][i],
                                weights=model_avgd.loc[~np.isnan(model_avgd[i])].model_pp)
                kde_dict[dset][topo][i] = k
            except KeyError:
                print('UH OH')
                pass
    results_from_topology_comparisons = {}
    y = 0
    while y < 10:
        # not using y, just want to run this 10 times
        print(y)
        all_topos_in_dset_all_params_df = pd.DataFrame()
        one_topology_all_params_df = pd.DataFrame()
        for topo in topo_dict[dset]:
            for i in kde_dict[dset][topo]:
                if not 'equil' in i and not 'die' in i and not 'alter' in i:
                    samplefordf = kde_dict[dset][topo][i].resample(num_to_sample)
                    df = pd.DataFrame(samplefordf).T
                    df.columns = [i]
                    one_topology_all_params_df = pd.concat([one_topology_all_params_df, df], axis=1)
            one_topology_all_params_df['topology'] = topo
            all_topos_in_dset_all_params_df = pd.concat([all_topos_in_dset_all_params_df, one_topology_all_params_df], ignore_index=True)
            one_topology_all_params_df = pd.DataFrame()
        #
        all_topos_in_dset_all_params_df.columns = [x.split('_baseline')[0] for x in all_topos_in_dset_all_params_df.columns if not x == 'topology'] + ['topology']
        df = pd.melt(all_topos_in_dset_all_params_df, id_vars=['topology'], value_vars=[x for x in all_topos_in_dset_all_params_df.columns if not x == 'topology'])
        #
        for i in list(set(df.variable)):
            if i not in results_from_topology_comparisons: # the first of 10 samples need to add the key
                results_from_topology_comparisons[i] = {}
            try:
                tukey_returned = True
                testsample = df.loc[~np.isnan(df.value)]
                testsample = testsample.loc[testsample.variable==i]
                topo_param_variances = {topo:np.var(testsample.loc[testsample.topology == topo]['value']) for topo in topo_dict[dset]}
                # check the variances - should be equal to do ANOVA + Tukey
                eqvar = True
                if not np.all([magnitude(topo_param_variances[v]) for v in topo_param_variances]): # np.all() ignores NaNs
                    print('***************')
                    print('variances are not the same (different order of magnitude) for param ' + str(i))
                    for j in topo_param_variances:
                        print(j,topo_param_variances[j])
                    print('***************')
                    eqvar = False
                # now do ANOVA + Tukey (maybe)
                try:
                    tukey = pairwise_tukeyhsd(endog=testsample['value'],
                                          groups=testsample['topology'],
                                          alpha=alpha_val)
                except TypeError:
                    # this catches the statsmodels tukey test error thrown when there are only 2 topologies to compare
                    #  and the p-value is "at bounds" (i assume this means too close to 0 or 1):
                    #   error noted in https://github.com/statsmodels/statsmodels/issues/6132
                    # since this isn't actually multiple comparisons, can run a t-test instead
                    tukey = tuple((np.mean(testsample.loc[testsample.topology==list(set(testsample.topology))[1]]['value'])-np.mean(testsample.loc[testsample.topology==list(set(testsample.topology))[0]]['value']),
                                    # ttest_ind doesn't return differences in means which i need for the results dict;
                                    # statsmodels tukeyhsd lists mean differences (pairwise_tukeyhsd.meandiffs)
                                    # subtracting the alphabetically earlier group from the alphabetically later group
                                    # so i do the same above
                                    ttest_ind(testsample.loc[testsample.topology == list(set(testsample.topology))[0]]['value'],
                                    testsample.loc[testsample.topology == list(set(testsample.topology))[1]]['value'],
                                    equal_var=eqvar),
                                    # ttest_ind doesn't return the names of the topologies it tests which i need for
                                    #  building the results dict; statsmodels tukeyhsd lists in alphabetical order so
                                    #  i will here too
                                    sorted(list(set(testsample.topology)))[0],sorted(list(set(testsample.topology)))[1]))
                    tukey_returned = False
                    pass
                #print(y,i)
                #print(tukey)
                if tukey_returned:
                    ind = 0
                    for n,j in enumerate(tukey.groupsunique):
                        for m,k in enumerate(tukey.groupsunique):
                            if m>n: # tukey lists the groups and also compares them in alphabetical order
                                try:
                                    results_from_topology_comparisons[i][j + ' vs ' + k].append((tukey.meandiffs[ind], tukey.pvalues[ind], tukey.reject[ind]))
                                except KeyError:
                                    results_from_topology_comparisons[i][j + ' vs ' + k] = [(tukey.meandiffs[ind], tukey.pvalues[ind], tukey.reject[ind])]
                                ind += 1
                else:
                    try:
                        results_from_topology_comparisons[i][tukey[2] + ' vs ' + tukey[3]].append(
                            (tukey[0], tukey[1].pvalue, tukey[1].pvalue < alpha_val))
                    except KeyError:
                        results_from_topology_comparisons[i][tukey[2] + ' vs ' + tukey[3]] = [(tukey[0], tukey[1].pvalue, tukey[1].pvalue < alpha_val)]
            except ValueError:
                # this catches the tukey test error thrown when only one topology has a particular parameter distr
                #  (so nothing to compare)... leaving the print statement so the user can check that it's a parameter
                #  they'd expect to only be in one topology
                print('only one topo (no comparison possible)',i)
        y += 1
    print(dset)
    for i in results_from_topology_comparisons:
        print(i)
        for j in results_from_topology_comparisons[i]:
            print('\t'+j)
            print('\t\t' + str(np.mean([x[2] for x in results_from_topology_comparisons[i][j]])))
    results_acrossdatasets[dset] = results_from_topology_comparisons

# save the results of the 10-iteration sampling process to compare differences and significances across topologies
np.save(outdir_file + '/comparisons_across_highscoring_topologies_by_dataset.npy',results_acrossdatasets)

# # # ## If you want to load the above and examine the results
# # # results_acrossdatasets = np.load(outdir_file + '/comparisons_across_highscoring_topologies_by_dataset.npy',allow_pickle=True)[()]
# # #
# # # for dset in ['TKO', 'RPM', 'cl_A']:
# # #     print(dset)
# # #     for i in results_acrossdatasets[dset]:
# # #         print('\t' + i)
# # #         for j in results_acrossdatasets[dset][i]:
# # #             print('\t\t' + j)
# # #             print('\t\t\t' + str(np.mean([x[2] for x in results_acrossdatasets[dset][i][j]])))
# # #     print('')
# # #
#

## Fig S6, parameter values *within* each topology
# after plotting, need to consolidate barplots in Inkscape

plt.rcParams.update({'font.size': 12})
plt.rcParams.update({'axes.titlesize': 12})

import warnings
warnings.filterwarnings("ignore")

num_to_sample = 1000
for dset in ['TKO', 'RPM', 'cl_A']:
    kde_dict = {dset:{}}
    df = pd.read_pickle(indir+dset+'_betafit_postmarg_params_and_probabilities_from_postequalweights.pklz',
                        compression='gzip')
    df = df[df['model_starting_subtype_makeup_code'].str.contains('\...1')]
    #
    for topo in topo_dict[dset]:
        kde_dict[dset][topo] = {}
        model_avgd = df[df['model_starting_subtype_makeup_code'].str.startswith(topo_makeup_dict[topo])]
        for n, i in enumerate(ordered_namelist):
            try:
                if np.isnan(model_avgd[i]).all():
                    continue
                model_avgd[i][model_avgd[i] == np.inf] = np.nan
                model_avgd[i][model_avgd[i] == -np.inf] = np.nan
                plt_range = (
                    model_avgd[i].dropna().values.min(),
                    model_avgd[i].dropna().values.max())
                k = gaussian_kde(model_avgd.loc[~np.isnan(model_avgd[i])][i],
                                weights=model_avgd.loc[~np.isnan(model_avgd[i])].model_pp)
                kde_dict[dset][topo][i] = k
            except KeyError:
                print('UH OH')
                pass
    #
    all_topos_in_dset_all_params_df = pd.DataFrame()
    one_topology_all_params_df = pd.DataFrame()
    for topo in topo_dict[dset]:
        for i in kde_dict[dset][topo]:
            if not 'equil' in i and not 'die' in i and not 'alter' in i:
                samplefordf = kde_dict[dset][topo][i].resample(num_to_sample)
                df = pd.DataFrame(samplefordf).T
                df.columns = [i]
                one_topology_all_params_df = pd.concat([one_topology_all_params_df, df], axis=1)
        one_topology_all_params_df['topology'] = topo
        all_topos_in_dset_all_params_df = pd.concat([all_topos_in_dset_all_params_df, one_topology_all_params_df], ignore_index=True)
        one_topology_all_params_df = pd.DataFrame()
    #
    all_topos_in_dset_all_params_df.columns = [x.split('_baseline')[0] for x in all_topos_in_dset_all_params_df.columns if not x == 'topology'] + ['topology']
    df = pd.melt(all_topos_in_dset_all_params_df, id_vars=['topology'], value_vars=[x for x in all_topos_in_dset_all_params_df.columns if not x == 'topology'])
    #
    # only differentiation/transition params
    df = df.loc[df.variable.str.contains('diff_')]
    for strcontains in [('A_to_N|A_to_A2|N_to_Y|A2_to_Y|A_to_Y','fwd'),
                        ('N_to_A|A2_to_A|Y_to_N|Y_to_A2|Y_to_A|N_to_A2|A2_to_N','rev')]:
        df_byhier = df.loc[df.variable.str.contains(strcontains[0])]
        for m,topo in enumerate([x for x in topo_dict[dset] if not 'two' in x]):
            fig,ax=plt.subplots(figsize=(4,20))
            g = sns.boxplot(x='variable', y='value', data=df_byhier.loc[df_byhier.topology == topo],
                            color=sns.color_palette(palette_dict[dset], len(topo_dict[dset]))[m])
            for n in range(len(g.lines)):
                l = g.lines[n]
                l.set_linewidth(.25)
            plt.setp(ax.get_xticklabels(), rotation=90)
            ax.set_ylim(-4,3.5)
            plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)
            plt.title(dset + ' ' + topo + ' '+strcontains[1]+'-directions diffs')
            plt.savefig(outdir_fig + '/parambarplot_' + dset + '_struct' + topo_makeup_dict[topo] + '_' + strcontains[1] + 'diffs.pdf',
                        format='pdf')
            plt.show()
            try:
                testsample = df_byhier.loc[~np.isnan(df_byhier.value)]
                testsample = testsample.loc[testsample.topology == topo]
                topo_param_variances = {diff:np.var(testsample.loc[testsample.variable==diff]['value']) for diff in set(testsample.variable)}
                # check the variances - should be equal to do ANOVA + Tukey, also note if unequal for caught TypeError t-test
                eqvar = True
                if not np.all([magnitude(topo_param_variances[v]) for v in topo_param_variances]): # np.all() ignores NaNs
                    print('***************')
                    print('variances are not the same (different order of magnitude) for params in topology ' + str(topo))
                    for j in topo_param_variances:
                        print(j,topo_param_variances[j])
                    print('***************')
                # now do ANOVA + Tukey (maybe)
                try:
                    tukey = pairwise_tukeyhsd(endog=testsample['value'],
                                          groups=testsample['variable'],
                                          alpha=0.01)
                    print(i)
                    print(tukey)
                except TypeError:
                    # this catches the statsmodels tukey test error thrown when there are only 2 topologies to compare
                    #  and the p-value is "at bounds" (i assume this means too close to 0 or 1):
                    #   error noted in https://github.com/statsmodels/statsmodels/issues/6132
                    # since this isn't actually multiple comparisons, can run a t-test instead
                    rez = ttest_ind(testsample.loc[testsample.variable == list(set(testsample.variable))[0]]['value'],
                                    testsample.loc[testsample.variable == list(set(testsample.variable))[1]]['value'],
                                    equal_var=eqvar)
                    print('for 2 samples (equal var):') if eqvar else print('for 2 samples (unequal var):')
                    print(rez)
                    pass
            except ValueError:
                # this catches the tukey test error thrown when only one topology has a particular parameter distr
                #  (so nothing to compare)... leaving the print statement so the user can check that it's a parameter
                #  they'd expect to only be in one topology
                print('only one diff param (no comparison possible)',i)
    for m, topo in enumerate([x for x in topo_dict[dset] if 'two' in x]):
        fig,ax=plt.subplots(figsize=(8,20))
        j = sns.boxplot(x='variable',y='value',data=df.loc[df.topology == topo],
                        color=sns.color_palette(palette_dict[dset], len(topo_dict[dset]))[m+2])
        for n in range(len(j.lines)):
            l = j.lines[n]
            l.set_linewidth(.25)
        plt.setp(ax.get_xticklabels(), rotation=90)
        ax.set_ylim(-4,3.5)
        plt.title(dset+' '+topo+' both hierarchical-directions diffs')
        plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)
        plt.savefig(outdir_fig + '/parambarplot_' + dset + '_struct' + topo_makeup_dict[topo] + '_bothdiffs.pdf', format='pdf')
        plt.show()
        eqvar = True
        topo_param_variances = {diff: np.var(testsample.loc[testsample.variable == diff]['value']) for diff in
                                set(testsample.variable)}
        if not np.all([magnitude(topo_param_variances[v]) for v in topo_param_variances]):  # np.all() ignores NaNs
            print('***************')
            print('variances are not the same (different order of magnitude) for params in topology ' + str(topo))
            for j in topo_param_variances:
                print(j, topo_param_variances[j])
            print('***************')
            eqvar = False
        rez = ttest_ind(testsample.loc[testsample.variable == list(set(testsample.variable))[0]]['value'],
                        testsample.loc[testsample.variable == list(set(testsample.variable))[1]]['value'],
                        equal_var=eqvar)
        print('for 2 samples (equal var):') if eqvar else print('for 2 samples (unequal var):')
        print(rez)


