## Below is plotting the prior marginal distributions (= the prior parameters you gave to multinest) and the posterior marginal distributions (the distributions you got back) -- this way you can compare them

from scipy.stats import norm, uniform
from matplotlib import ticker
import seaborn as sns
import sys
import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
import math
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def magnitude(value):
    if (value == 0): return 0
    if not np.isnan(value):
        return int(math.floor(math.log10(abs(value))))
    else:
        return np.NaN

indir = '../posterior_marginals_and_predictives/'
outdir = ''

with open('../helper_functions_and_files/all_possible_sampled_params.pickle', 'rb') as p:
    sampled_params_list = pickle.load(p)

dfdict = pd.read_pickle('../helper_functions_and_files/updatedinjune_all_9327_models_in_dataframe_with_subtype_starting_makeup_code.pickle')
updated_modelmakeups = np.load('../helper_functions_and_files/updatedinjune_apr_11_all_model_makeups_from_redo_ignoring_uneven_bidirtxns.npy')
upd_modnums = []
for j in dfdict.index:
    if dfdict.loc[j]['model_makeup'] in updated_modelmakeups:
        upd_modnums.append(j)

### much of ticks_format() is from https://stackoverflow.com/questions/19239297/matplotlib-bad-ticks-labels-for-loglog-twin-axis adapted for just the x axis
def ticks_format(value, index):
    """
    This function decompose the log value and returns a latex string.
    If 0<=value<99: return the value as it is.
    if 0.1<value<0: returns as it is rounded to the first decimal
    otherwise returns $base*10^{exp}$
    """
    exp = np.floor(value)
    base = abs(round(10 ** value / 10 ** exp))
    if exp == 0 or exp == 1:
        return '${0:.1f}$'.format(round(10 ** value, 1))
    if exp == -1:
        return '${0:.2f}$'.format(round(10 ** value, 2))
    else:
        return '${0:d}\\times10^{{{1:d}}}$'.format(int(base), int(exp))


names_dict = {}
for n, i in enumerate([x.name for x in sampled_params_list]):
    param_toprint = i
    ptp = param_toprint.split('sp_')[1]
    paramtoprint = ptp.split('_diff')
    if len(paramtoprint) == 1:
        paramtoprint = ptp.replace('cell_1kc', 'cell')
        finalparam = paramtoprint.replace('division_0_N', 'division_N').replace('die_0_N', 'die_N').replace(
            'cell_0', 'baseline').replace('cell_1', 'altered').replace('cell_2', 'equil_assn')
    else:
        paramtoprint = ptp.replace('_cell_1kf', '_cell')
        altered_details = ''
        if '_1' in paramtoprint:
            altered_details = '_altered'
        elif '_2' in paramtoprint:
            altered_details = '_equil_assn'
        finalparam = paramtoprint.replace('uni_0_', '').replace('cell_N', 'to_N').replace(
            'diff_cell_0', 'baseline').replace('diff_cell_1', 'altered').replace('diff_cell_2', 'equil_assn')
    finalparam = finalparam.replace('NonNE', 'Y').replace('NEv2', 'A2').replace('NEv1', 'N').replace('NE', 'A')
    names_dict[i] = finalparam


def plot_priors(ax, dist, loc, scale, plt_range):
    # ax = the matplotlib ax
    # dist = the scipy.stats distribution
    # loc and scale the way they are defined for scipy.stats distributions
    x = np.linspace(plt_range[0], plt_range[1], 1000)
    ax.plot(x, dist.pdf(x, loc=loc, scale=scale), linewidth=2, color='black')


def remove_empty_plots(fig, ax, dims_plotted):
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


# for later subplots_adjust
left = 0.05  # the value on the x axis where the left margin should be
right = 0.95
bottom = 0.075  # the value on the y axis where the bottom margin should be
top = 0.9
wspace = 0.5  # the proportion of the average of the left value and the right value -> for example, 0.2*((0.075+0.95)/2)
hspace = 0.8

####
# run code on ACCRE for marginals (reasonably quick... lol)
# ok gotta do it again so i can include them in the github
# i guess wait to try to rerun some models

####

sampleparamsdict = {}
for i in sampled_params_list:
    sampleparamsdict[i.name] = i

colordict = {
    'TKO': {
        'distr': 'blue',
        'kdeline': 'blue'
    },
    'RPM': {
        'distr': 'red',
        'kdeline': 'darkred'
    },
    'cell_line_A': {
        'distr': 'green',
        'kdeline': 'darkgreen'
    },
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

# Plot prior distributions only (Figure S2)

plt.rcParams.update({'font.size': 12})
plt.rcParams.update({'axes.titlesize': 12})

ndims = len(ordered_namelist)
columns = 6
rows = int(np.ceil(ndims / 6))

fig, axs = plt.subplots(rows, columns, figsize=(20, 20))
dims_plotted = []
# don't need to go through the different datasets because priors are the same for all of them
# for resdir in ['TKO','RPM','cell_line_A']:
removeind = 0  # also unnecessary since everything in ordered_namelist has a prior
for n, i in enumerate(ordered_namelist):
    dims_plotted.append(n - removeind)
    ax = axs[int(((n - removeind) - (n - removeind) % columns) / columns), ((n - removeind) % columns)]
    try:
        currprior = sampleparamsdict[[k for k, v in names_dict.items() if v == i][0]]
        # with whatever scipy stats update i have, this is needed on Notch
        if currprior.prior_dist.a == -np.inf:
            # normal distribution
            plt_range = (currprior.prior_dist.ppf(0.001), currprior.prior_dist.ppf(0.999))
            plot_priors(ax, currprior.prior_dist.dist, currprior.prior_dist.mean(),
                        currprior.prior_dist.std(), plt_range)
        else:
            # uniform distribution
            # again, notch with update whatever
            plt_range = (-3.5, 3)
            plot_priors(ax, uniform,
                        currprior.prior_dist.ppf(0.00001),
                        abs(currprior.prior_dist.ppf(0.00001)) +
                        currprior.prior_dist.ppf(0.99999), plt_range)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(ticks_format))
        ax.get_yaxis().set_visible(True)
        ax.tick_params(labelsize=16)
        ax.set_xlabel('')
        ax.set_title(i, fontsize=20)
    except KeyError:
        removeind += 1
        pass

remove_empty_plots(fig, ax, dims_plotted)

# sizes don't look ideal with plt.show() but saving it as a pdf then opening that pdf in adobe reader looks good

fig.text(0.5, 0.02, 'Log parameter value', ha='center')
fig.text(0.01, 0.55, 'Probability', va='center', rotation='vertical')
plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)
plt.savefig('../generated_figures/prior_marginals_suppfig.pdf',
            format='pdf')

plt.show()

# Priors and posteriors per model (the posteriors are the same as in the boxplot from Fig 5F, but a diff view of them)

plt.rcParams.update({'font.size': 12})
plt.rcParams.update({'axes.titlesize': 12})

ndims = len(ordered_namelist)
columns = 6
rows = int(np.ceil(ndims / 6))

for dset in ['TKO', 'RPM', 'cl_A']:
    fig, axs = plt.subplots(rows, columns, figsize=(20, 20))
    dims_plotted = []
    model_avgd = pd.read_pickle(
        indir + dset + '_betafit_postmarg_params_and_probabilities_from_postequalweights_somemissing_4_10_22.pickle')
    model_avgd = model_avgd.loc[~np.isnan(model_avgd.model_pp)]  # only models with a posterior probability can be used
    model_avgd = model_avgd.loc[model_avgd.from_model.isin(upd_modnums)]
    ## comment out for any initiating subtype, currently has A +/- others
    model_avgd = model_avgd.loc[model_avgd.model_starting_subtype_makeup_code.str.contains('\...1')]
    ##
    removeind = 0
    for n, i in enumerate(ordered_namelist):
        dims_plotted.append(n - removeind)
        ax = axs[int(((n - removeind) - (n - removeind) % columns) / columns), ((n - removeind) % columns)]
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
            vals = np.linspace(plt_range[0], plt_range[1], 100)
            ax.hist(model_avgd[i].values, bins=100,
                    weights=model_avgd.model_pp,
                    color=colordict[dset]['distr'],
                    alpha=0.2, histtype='stepfilled',
                    range=plt_range, density=True)
            ax.plot(vals, k.evaluate(vals), color=colordict[dset]['kdeline'],
                    linewidth=2)
            ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
            ax.get_shared_y_axes().join(ax, ax2)  # needs to share y-axis too
            currprior = sampleparamsdict[[k for k, v in names_dict.items() if v == i][0]]
            # with whatever scipy stats update i have, this is needed on Notch
            if currprior.prior_dist.a == -np.inf:
                plot_priors(ax2, currprior.prior_dist.dist, currprior.prior_dist.mean(),
                            currprior.prior_dist.std(), plt_range)
            else:
                # again, notch with update whatever
                plot_priors(ax2, uniform,
                            currprior.prior_dist.ppf(0.00001),
                            abs(currprior.prior_dist.ppf(0.00001)) +
                            currprior.prior_dist.ppf(0.99999), plt_range)
            ax.xaxis.set_major_formatter(ticker.FuncFormatter(ticks_format))
            ax.get_yaxis().set_visible(True)
            ax2.get_yaxis().set_visible(False)
            ax.tick_params(labelsize=16)
            ax.set_xlabel('')
            ax.set_title(i, fontsize=20)
        except KeyError:
            removeind += 1
            pass
    remove_empty_plots(fig, ax, dims_plotted)
    #
    # sizes don't look ideal with plt.show() but saving it as a pdf then opening that pdf in adobe reader looks good
    fig.text(0.5, 0.02, 'Log parameter value', ha='center')  # , fontsize=30)  ## need diff sizes for ACCRE
    fig.text(0.01, 0.55, 'Probability', va='center',
             rotation='vertical')  # , fontsize=30)  ## need diff sizes for ACCRE
    plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)
    plt.savefig('../generated_figures/priors_modelavg_posterior_marginals_5891update_' + str(dset) + '.pdf',
                format='pdf')
    plt.show()

# Priors and posteriors separated by initiating subtype (Figure S4)

ndims = len(ordered_namelist)
columns = 6
rows = int(np.ceil(ndims / 6))

for dset in ['TKO', 'RPM', 'cl_A']:
    fig, axs = plt.subplots(rows, columns, figsize=(20, 20))
    dims_plotted = []
    # below to look for 'starting with A +/- others', 'starting with N +/- others', etc
    # for starting in [(('1000','1200','1300','1400','1230','1240','1340','1234'),'blue','blue'),(('1200','1230','1240','1234','2000','2300','2400','2340'),'orange','goldenrod'),
    #                 (('1300','1230','1340','1234','2300','2340','3000','3400'),'green','darkgreen'),(('1400','1240','1340','1234','2400','2340','3400','4000'),'red','darkred')]:
    # below to look for 'starting with A only', 'starting with N only', etc
    for starting in [('1000', 'blue', 'blue'), (('2000'), 'orange', 'goldenrod'), ('3000', 'green', 'darkgreen'),
                     ('4000', 'red', 'darkred')]:
        removeind = 0
        model_avgd = pd.read_pickle(
            indir + dset + '_betafit_postmarg_params_and_probabilities_from_postequalweights_somemissing_4_10_22.pickle')
        model_avgd = model_avgd.loc[
            ~np.isnan(model_avgd.model_pp)]  # only models with a posterior probability can be used
        model_avgd = model_avgd.loc[model_avgd.from_model.isin(upd_modnums)]
        model_avgd = model_avgd.loc[model_avgd.model_starting_subtype_makeup_code.str.endswith(starting[0])]
        for n, i in enumerate(ordered_namelist):
            dims_plotted.append(n - removeind)
            ax = axs[int(((n - removeind) - (n - removeind) % columns) / columns), ((n - removeind) % columns)]
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
                vals = np.linspace(plt_range[0], plt_range[1], 100)
                ax.hist(model_avgd[i].values, bins=100,
                        weights=model_avgd.model_pp,
                        color=starting[1],
                        alpha=0.2, histtype='stepfilled',
                        range=plt_range, density=True)
                ax.plot(vals, k.evaluate(vals), color=starting[2],
                        linewidth=2)
                ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
                ax.get_shared_y_axes().join(ax, ax2)  # needs to share y-axis too
                currprior = sampleparamsdict[[k for k, v in names_dict.items() if v == i][0]]
                # with whatever scipy stats update i have, this is needed on Notch
                if currprior.prior_dist.a == -np.inf:
                    plot_priors(ax2, currprior.prior_dist.dist, currprior.prior_dist.mean(),
                                currprior.prior_dist.std(), plt_range)
                else:
                    # again, notch with update whatever
                    plot_priors(ax2, uniform,
                                currprior.prior_dist.ppf(0.00001),
                                abs(currprior.prior_dist.ppf(0.00001)) +
                                currprior.prior_dist.ppf(0.99999), plt_range)
                ax.xaxis.set_major_formatter(ticker.FuncFormatter(ticks_format))
                ax.get_yaxis().set_visible(True)
                ax2.get_yaxis().set_visible(False)
                ax.tick_params(labelsize=16)
                ax.set_xlabel('')
                ax.set_title(i, fontsize=20)
            except KeyError:
                removeind += 1
                pass
    remove_empty_plots(fig, ax, dims_plotted)
    #
    fig.text(0.5, 0.02, 'Log parameter value', ha='center')  # , fontsize=30)  ## need diff sizes for ACCRE
    fig.text(0.01, 0.55, 'Probability', va='center',
             rotation='vertical')  # , fontsize=30)  ## need diff sizes for ACCRE
    plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)
    plt.savefig('../generated_figures/priors_modelavg_posterior_marginals_' + str(dset) + '_bystarting_suppfig.pdf',
                format='pdf')
    plt.show()

# Priors and posteriors per structural topology (not a figure, but could be useful)

topodict = {
    'TKO': [('0.', 'gray', 'black'), ('2.', 'blue', 'blue'), ('6.', 'orange', 'goldenrod'),
            ('7.', 'green', 'darkgreen')],
    'RPM': [('0.', 'gray', 'black'), ('1.', 'blue', 'blue'), ('5.', 'orange', 'goldenrod'),
            ('7.', 'green', 'darkgreen'), ('9.', 'red', 'darkred')],
    'cl_A': [('0.', 'gray', 'black'), ('1.', 'pink', 'deeppink'), ('2.', 'blue', 'blue'),
                    ('4.', 'orange', 'goldenrod'),
                    ('5.', 'red', 'darkred'), ('6.', 'cyan', 'turquoise'), ('7.', 'green', 'darkgreen')]
}

ndims = len(ordered_namelist)
columns = 6
rows = int(np.ceil(ndims / 6))

for dset in ['TKO', 'RPM', 'cl_A']:
    fig, axs = plt.subplots(rows, columns, figsize=(20, 20))
    dims_plotted = []
    for topo in topodict[dset]:
        removeind = 0
        model_avgd = pd.read_pickle(
            indir + dset + '_betafit_postmarg_params_and_probabilities_from_postequalweights_somemissing_4_10_22.pickle')
        model_avgd = model_avgd.loc[~np.isnan(model_avgd.model_pp)]
        model_avgd = model_avgd.loc[model_avgd.from_model.isin(upd_modnums)]
        # this is only per structure, not initiating subtype
        model_avgd = model_avgd.loc[model_avgd.model_starting_subtype_makeup_code.str.startswith(topo[0])]
        #
        for n, i in enumerate(ordered_namelist):
            dims_plotted.append(n - removeind)
            ax = axs[int(((n - removeind) - (n - removeind) % columns) / columns), ((n - removeind) % columns)]
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
                vals = np.linspace(plt_range[0], plt_range[1], 100)
                ax.hist(model_avgd[i].values, bins=100,
                        weights=model_avgd.model_pp,
                        color=topo[1],
                        alpha=0.2, histtype='stepfilled',
                        range=plt_range, density=True)
                ax.plot(vals, k.evaluate(vals), color=topo[2],
                        linewidth=2)
                ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
                ax.get_shared_y_axes().join(ax, ax2)  # needs to share y-axis too
                currprior = sampleparamsdict[[k for k, v in names_dict.items() if v == i][0]]
                # with whatever scipy stats update i have, this is needed on Notch
                if currprior.prior_dist.a == -np.inf:
                    plot_priors(ax2, currprior.prior_dist.dist, currprior.prior_dist.mean(),
                                currprior.prior_dist.std(), plt_range)
                else:
                    # again, notch with update whatever
                    plot_priors(ax2, uniform,
                                currprior.prior_dist.ppf(0.00001),
                                abs(currprior.prior_dist.ppf(0.00001)) +
                                currprior.prior_dist.ppf(0.99999), plt_range)
                ax.xaxis.set_major_formatter(ticker.FuncFormatter(ticks_format))
                ax.get_yaxis().set_visible(True)
                ax2.get_yaxis().set_visible(False)
                ax.tick_params(labelsize=16)
                ax.set_xlabel('')
                ax.set_title(i, fontsize=20)
            except KeyError:
                removeind += 1
                pass
    remove_empty_plots(fig, ax, dims_plotted)
    #
    fig.text(0.5, 0.02, 'Log parameter value', ha='center')  # , fontsize=30)  ## need diff sizes for ACCRE
    fig.text(0.01, 0.55, 'Probability', va='center',
             rotation='vertical')  # , fontsize=30)  ## need diff sizes for ACCRE
    plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)
    # plt.savefig('priors_modelavg_posterior_marginals_'+str(resdir)+'_bytopology.pdf',
    #          format='pdf')
    plt.show()

# I think this is Figure 5F

sampledict = {}
for dset in ['TKO', 'RPM', 'cl_A']:
    sampledict[dset] = {}
    model_avgd = pd.read_pickle(
        indir + dset + '_betafit_postmarg_params_and_probabilities_from_postequalweights_somemissing_4_10_22.pickle')
    model_avgd = model_avgd.loc[~np.isnan(model_avgd.model_pp)]
    model_avgd = model_avgd.loc[model_avgd.from_model.isin(upd_modnums)]
    model_avgd = model_avgd.loc[model_avgd.model_starting_subtype_makeup_code.str.contains('\...1')]
    model_avgd = model_avgd.loc[model_avgd.model_starting_subtype_makeup_code.str.startswith('0')]
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
            sampledict[dset][i] = k.resample(1000)
        except KeyError:
            print('UH OH')
            pass
        # break
    sampledict[dset]['dataset'] = dset

colpal = ['#4c72b0', '#dd8452', '#55a868']
# Hex values taken from the 'deep' color palette

all_datasets_all_params_df = pd.DataFrame()
for dset in ['TKO', 'RPM', 'cl_A']:
    one_dataset_all_params_df = pd.DataFrame()
    for i in sampledict[dset]:
        if not 'equil' in i and not 'die' in i and not 'alter' in i and not i=='dataset':
            df = pd.DataFrame(sampledict[dset][i]).T
            df.columns = [i]
            one_dataset_all_params_df = pd.concat([one_dataset_all_params_df, df], axis=1)
    one_dataset_all_params_df['dataset'] = dset
    all_datasets_all_params_df = pd.concat([all_datasets_all_params_df, one_dataset_all_params_df], ignore_index=True)
    one_dataset_all_params_df = pd.DataFrame()

all_datasets_all_params_df.columns = [x.split('_baseline')[0] for x in all_datasets_all_params_df.columns if not x == 'dataset'] + ['dataset']
df = pd.melt(all_datasets_all_params_df, id_vars=['dataset'], value_vars=[x for x in all_datasets_all_params_df.columns if not x == 'dataset'])

fig, ax = plt.subplots(figsize=(20, 10))
g = sns.boxplot(x='variable', y='value', hue='dataset', data=df, palette=colpal)
for n in range(len(g.lines)):
    l = g.lines[n]
    l.set_linewidth(.25)

plt.setp(ax.get_xticklabels(), rotation=90)
plt.title('Parameter values between datasets')
plt.subplots_adjust(left=left, right=right, bottom=bottom, top=top, wspace=wspace, hspace=hspace)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.xlabel('Parameter')
plt.ylabel('Log parameter value')
# plt.savefig('../generated_figures/parambarplot_updated5891.pdf',format='pdf')
plt.show()

results_from_dataset_comparisons = {}
num_to_sample = 1000
for y in range(10):
    print(y)
    sampledict = {}
    for dset in ['TKO','RPM','cl_A']:
        model_avgd = pd.read_pickle(
            indir + dset + '_betafit_postmarg_params_and_probabilities_from_postequalweights_somemissing_4_10_22.pickle')
        model_avgd = model_avgd.loc[~np.isnan(model_avgd.model_pp)]
        model_avgd = model_avgd.loc[model_avgd.from_model.isin(upd_modnums)]
        model_avgd = model_avgd.loc[model_avgd.model_starting_subtype_makeup_code.str.contains('\...1')]
        model_avgd = model_avgd.loc[model_avgd.model_starting_subtype_makeup_code.str.startswith('0')]
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
                sampledict[dset][i] = k.resample(num_to_sample)
            except KeyError:
                print('UH OH')
                pass
        sampledict[dset]['dataset'] = dset
    #
    all_datasets_all_params_df = pd.DataFrame()
    #one_topology_all_params_df['dataset']
    one_dataset_all_params_df = pd.DataFrame()
    for i in sampledict[dset]:
        if not 'equil' in i and not 'die' in i and not 'alter' in i:
            df = pd.DataFrame(sampledict[dset][i]).T
            df.columns = [i]
            one_dataset_all_params_df = pd.concat([one_dataset_all_params_df, df], axis=1)
        one_dataset_all_params_df['dataset'] = dset
        all_datasets_all_params_df = pd.concat([all_datasets_all_params_df, one_dataset_all_params_df], ignore_index=True)
        one_dataset_all_params_df = pd.DataFrame()
    #
    all_datasets_all_params_df.columns = [x.split('_baseline')[0] for x in all_datasets_all_params_df.columns if not x == 'dataset'] + ['dataset']
    df = pd.melt(all_datasets_all_params_df, id_vars=['dataset'], value_vars=[x for x in all_datasets_all_params_df.columns if not x == 'dataset'])
    #
    results_from_dataset_comparisons = {}
    for i in list(set(df.variable)):
        if i not in results_from_dataset_comparisons:
            results_from_dataset_comparisons[i] = {}
        try:
            testsample = df.loc[~np.isnan(df.value)]
            testsample = testsample.loc[testsample.variable==i]
            tukey = pairwise_tukeyhsd(endog=testsample['value'],
                                  groups=testsample['dataset'],
                                  alpha=0.01)
            print(i)
            print(len(testsample))
            var_4sub = np.var(testsample.loc[testsample.dataset=='four_subtype']['value'])
            var_3sub = np.var(testsample.loc[testsample.dataset=='three_subtype_A_A2_Y']['value'])
            var_2subA2 = np.var(testsample.loc[testsample.dataset=='two_subtype_A_A2']['value'])
            var_2subY = np.var(testsample.loc[testsample.dataset=='two_subtype_A_Y']['value'])
            dset_param_variances = {dt: np.var(testsample.loc[testsample.dataset == dt]['value']) for dt in
                                    ['TKO','RPM','cl_A']}
            if not np.all([magnitude(v) for v in dset_param_variances]):  # np.all() ignores NaNs
                print('***************')
                print('variances are not the same (different order of magnitude)')
                for j in dset_param_variances:
                    print(j, dset_param_variances[j])
                print('***************')
            print(tukey)
            ind = 0
            for n,j in enumerate(tukey.groupsunique):
                for m,k in enumerate(tukey.groupsunique):
                    if m>n:
                        try:
                            results_from_dataset_comparisons[i][j + ' vs ' + k].append((tukey.pvalues[ind], tukey.reject[ind]))
                        except KeyError:
                            results_from_dataset_comparisons[i][j + ' vs ' + k] = [(tukey.pvalues[ind], tukey.reject[ind])]
                        ind += 1
    #        break
        except ValueError:
            # shouldnt happen in this case
            pass
    break

for i in results_from_dataset_comparisons:
    print(i)
    for j in results_from_dataset_comparisons[i]:
        print('\t' + j)
        print('\t\t' + str(np.mean([x[1] for x in results_from_dataset_comparisons[i][j]])))

