# Will take everything in the specified directory (in line 9) and make a run_model file for it

import os
import sys
import pandas as pd
# to determine whether A2 acts like NE or NonNE
dfdict = pd.read_pickle('../helper_functions_and_files/updatedinjune_all_9327_models_in_dataframe_with_subtype_starting_makeup_code.pickle')

candidate_model_dir = '../candidate_models/'
run_file_dir = '../run_files_for_candidate_models/'

for number in [x.split('_')[-1].split('.')[0] for x in os.listdir(candidate_model_dir) if
               'model_' in x and '.py' in x and not 'run' in x and not 'plot' in x and not 'posttx' in x and not 'testing' in x]:
    if int(number) < 87 or int(number) > 88:
        continue
    print(number)
    str_to_write_1 = """import os
import sys
sys.path.append('"""+candidate_model_dir+"""')

from pysb.simulator import ScipyOdeSimulator
import numpy as np
from scipy.stats import norm,uniform,beta,expon
from model_"""
    str_to_write_1 += str(number)
    str_to_write_2 = """ import model
import pickle
import copy
from itertools import chain
import pandas as pd

import pymultinest
from pymultinest.solve import solve
from pymultinest.analyse import Analyzer

import signal
from datetime import datetime

import argparse

parser = argparse.ArgumentParser()
# add this later
#parser.add_argument("dataset", help="Name of dataset the model selection run is using. Required to avoid confusion between runs.")
parser.add_argument("dirmodels", help="Directory where Multinest working files will be located (in directories \'dir_model_{int}\', as well as evidence printouts. Required.")
parser.add_argument("-iter", "--model_iteration", help="If doing multiple runs of the same model & Multinest implementation, provide this model's iteration number.",
                    type=int)
parser.add_argument("-imp", "--importance_nested_sampling", help="Use importance nested sampling in Multinest.",
                    action="store_true")
parser.add_argument("-ceff", "--constant_efficiency", help="Use constant efficiency mode in Multinest.",
                    action="store_true")
parser.add_argument("-f", "--sampling_efficiency", help="Target sampling efficiency in Multinest run. Default: 0.05",
                    type=float)
parser.add_argument("-p", "--population_size", help="Number of live points in the nested sampling population. Default: 3000",
                    type=int)
#parser.add_argument("-o", "--outfile_directory", help="Directory where .out files are located. Default: current working directory.")
#parser.add_argument("-w", "--write_job_completes", help="A filename which, if provided, test_joblib.py will write/append to when each job finishes, along with printing to STDOUT. Default: STDOUT only.")

args = parser.parse_args()

# maybe add later
#outdir = args.outfile_directory if args.outfile_directory else print ('Using current working directory '+os.getcwd()+' for outfiles')
#if outdir:
#    outdir = outdir if os.path.exists(outdir) else print('path \''+outdir+'\' does not exist, using current working directory '+os.getcwd()+' for outfiles')
#if not outdir:
#    outdir = os.getcwd()
#if args.write_job_completes:
#    print ('Writing to '+str(args.write_job_completes)+' when each model run finishes. Will include exit status.')
#    with open(args.write_job_completes,'w') as jobs_file:
#        jobs_file.write('Running '+__file__+'starting at '+str(datetime.now())+'.\\n')

modeliter = args.model_iteration if args.model_iteration else False
uses_modeliter = True if modeliter else False # False as default because more often i'm not using modeliter

INS = args.importance_nested_sampling
ceff = args.constant_efficiency
f = args.sampling_efficiency if args.sampling_efficiency else 0.05
popsize = args.population_size if args.population_size else 3000
paramdir = args.dirmodels
#paramdir = "/data/lola/beiksp/cl_A_betafit_"+str(f)+"_"+str(popsize)+"_inprogress"

if INS:
    fn_ins = "T"
else:
    fn_ins = "F"
if ceff:
    fn_ceff = "T"
else:
    fn_ceff = "F"

if not os.path.exists(paramdir):
    print ('\\n\\nNo destination directory in /data. Multinest will not run.\\n')
    print ('Likely you need to create '+str(paramdir)+'\\n')
    sys.exit(0)

class TimeoutException(RuntimeError):
    \""" Time out occurred! \"""
    pass

def handler(signum, frame):
    print('forever is over!')
    raise TimeoutException()

# Register the signal function handler
signal.signal(signal.SIGALRM, handler)

tspan = np.linspace(0,60,100)
solver = ScipyOdeSimulator(model,integrator='lsoda',compiler='cython')
param_values = np.array([p.value for p in model.parameters])
# make rates_mask later
#rates_mask = #np.concatenate((np.ones(9,dtype=bool),np.zeros(4,dtype=bool),np.ones(len(param_values[13:]),dtype=bool)))

cellline_pct = {
'NE_obs':0.82827978,
'NEv1_obs':0.071928499,
'NEv2_obs':0.0830788,
'NonNE_obs':0.016712921
}

cellline_stdev = {
'NE_obs':0.114751192,
'NEv1_obs':0.094443104,
'NEv2_obs':0.099794185,
'NonNE_obs':0.020277219
}

# TKO_pct = {
# 'NE_obs':0.670866848446898,
# 'NEv1_obs':0.001011170766988,
# 'NEv2_obs':0.294235217878072,
# 'NonNE_obs':0.033886762908045
# }
# 
# TKO_stdev = {
# 'NE_obs':0.152576600276884,
# 'NEv1_obs':0.005730133430503,
# 'NEv2_obs':0.147927688661517,
# 'NonNE_obs':0.031684600453998
# }

# Oliver_pct = {
# 'NE_obs':0.259122843833646,
# 'NEv1_obs':0.318704767383416,
# 'NEv2_obs':0.010548327444441,
# 'NonNE_obs':0.411624061338496
# }
# 
# 
# Oliver_stdev = {
# 'NE_obs':0.171187022711461,
# 'NEv1_obs':0.157524233180492,
# 'NEv2_obs':0.016363538701013,
# 'NonNE_obs':0.223000331826237
# }

# ok it really should be all 4, just some are zero and always zero
obs_list = ['NE_obs','NEv1_obs','NEv2_obs','NonNE_obs']

def beta_dist_from_mu_and_stdev(mu,std):
    nu_out = (mu*(1-mu)/(std**2)) - 1
    alpha_out = mu*nu_out
    beta_out = (1-mu)*nu_out
    return beta(alpha_out,beta_out)

# beta distrs for means near zero are U-shaped with the bottom left of the curve near zero
# if you try to get a y-value for an x-value too close to zero it'll just be inf
# so to avoid returning inf as the likelihood value, clip x-values to the lowest possible that won't return y=inf
# based on beta distr transformation using mu and sigma to generate alpha and beta (Kruschke, 2011; see Methods), requires sigma^2 < mu(1-mu)
# so if mu is otherwise zero for likelihood fxn, instead find the lowest value that fits sigma^2 < mu(1-mu)
lowest_allowed = {}
for i in cellline_stdev:
    mu = 1e-5
    while not (cellline_stdev[i]**2 < mu*(1-mu)):
        mu *= 1.00001
    lowest_allowed[i] = mu

TOLERANCE = 1e-4
def likelihood(position):
    tspan = np.linspace(0,60,1001)
    Y=np.copy(position)
    param_values[rates_mask] = 10 ** Y
    signal.alarm(30)
    try:
        sim = solver.run(param_values=param_values,tspan=tspan).all
    except TimeoutException as exc:
        #return -np.inf
        return -1e200
    else:
        signal.alarm(0)
    sim_data = {}
    all_lessthan1 = True
    for obs in obs_list:
        sim_data[obs] = sim[obs] #[:new_end]
        if sim[obs][-1] > 1:
            all_lessthan1 = False
    # if there aren't enough cells, or there are too many cells, or if the end of the sim gets to NaNs (because it grew too fast)
    if sim['total_cells'][-1] < 100:
        #print ('not enough cells ' + str(sim['total_cells'][-1]))
        #return -np.inf
        return -1e200
    elif np.isnan(sim['total_cells'][-1]):
        #print ('too many cells computer couldnt handle ' + str(sim['total_cells'][-1]))
        #return -np.inf
        return -1e200
    elif all_lessthan1: #smallest size in SCLC allografts (Lim et al) 1cm^3 (~10^8 cells), largest ~3.5cm^3 (~4*10^8)
        #print ('something crashed out at the end ')
        #print (sim_data)
        #return np.inf*-1
        return -1e200
    else:
        # get the percentages so you can check for equilibrium - first get the total # of cells
        sim_pct_run = {}
        for obs in obs_list:
            sim_pct_run[obs] = np.true_divide(sim[obs],sim['total_cells'])
        # is it in equilibrium?
        not_eq = False
        total_stack = (sim_pct_run[obs_list[0]],)
        for obs in obs_list[1:]:
            total_stack = total_stack + (sim_pct_run[obs],)                    
        y = np.column_stack(total_stack)
        for idx in range(y.shape[1]):
            try:
                derivative = (y[:,idx][-1]-y[:,idx][-75])/(tspan[-1]-tspan[-75])
                if abs(derivative)>TOLERANCE or np.isnan(derivative): #or np.isnan probably shouldnt happen but just in case
                    not_eq = True
            except IndexError: # if tspan has less than 75 indices after the nanind process - not doing this anymore but leaving try/catch anyway...
                #return -np.inf
                return -1e200
                continue
        if not_eq:
            #return -np.inf
            return -1e200
        # Score
        total_cost_nonzeros = np.sum([
                            beta_dist_from_mu_and_stdev(
                                                        np.clip(sim_pct_run[obs][-1],lowest_allowed[obs],(1-lowest_allowed[obs])),
                                                        cellline_stdev[obs]
                                                       )
                            .logpdf(cellline_pct[obs]) for obs in obs_list[:-1]
                                if not np.all(sim_pct_run[obs]==0)
                           ])
        total_cost_zeros = np.sum([
                            expon(0,scale=cellline_stdev[obs])
                            .logpdf(cellline_pct[obs]) for obs in obs_list[:-1]
                                if np.all(sim_pct_run[obs]==0)
                           ])
        total_cost = np.sum([total_cost_nonzeros,total_cost_zeros])
        if np.isnan(total_cost):
            #total_cost = #np.inf*-1
            total_cost = -1e200
        return total_cost

# Collect all sampled parameters to provide to the pymultinest run call
# saved this as a file previously
with open('../helper_functions_and_files/all_possible_sampled_params_dict.pickle','rb') as fp:
    sampled_params_dict = pickle.load(fp)
    
# sampled_params_dict is saved with A2-as-NonNE settings, but if this is a model where A2 acts like NE, change the values
"""
    # will the effect increase or decrease NEv2 division for this run?
    if int(number) in dfdict.loc[dfdict.subtype_starting_and_makeup_code.str.contains(
        '\.1.')].index: # contains some topologies without A2 subtype but in that case A2 sampled_params will be removed when building sp_list
        # these are for list 13s and 16s: NEv2 affected by NonNE_obs (i.e. it is considered neuroendocrine)
        str_to_write_3 = """# NEv2 acts like NE... NEv2 div should be:
sampled_params_dict['sp_division_0_NEv2_cell_1'] = norm(loc=np.log10(0.1993),scale=.5)"""
    else:
        # these are for list 14s and 17s: NEv2 affected by the neuroendocrine types (i.e. since it is Hes1+ it is considered non-neuroendocrine)
        # no change needed in this case - only write this comment once (i.e. not in the if-else statement below)
        str_to_write_3 = """# ***Not necessary here ***"""
    str_to_write_4 = """
"""
    # will the effect decrease or increase NEv2 death for this run?
    if int(number) in dfdict.loc[dfdict.subtype_starting_and_makeup_code.str.contains(
            '\.1.')].index: # contains some topologies without A2 subtype but in that case A2 sampled_params will be removed when building sp_list
        # these are for list 13s and 16s: NEv2 affected by NonNE_obs (i.e. it is considered neuroendocrine)
        str_to_write_5 = """# NEv2 acts like NE... NEv2 die should be:
sampled_params_dict['sp_die_0_NEv2_cell_1'] = norm(loc=np.log10(0.077),scale=.5)"""
    # 'not necessary' comment only written once (above) - only blank '' in the else statement
    else:
        str_to_write_5 = """"""
    str_to_write_6 = """

rates_mask = []
for i in [x for x in model.parameters]:
    rates_mask.append('sp_'+i.name in [y for y in sampled_params_dict]) # list comprehension will give all the names for sampled params (keys in the dict)

sp_list = []
for i in [x for x in sampled_params_dict]:
    if i.split('sp_')[1] in [y.name for y in model.parameters]:
        sp_list.append(sampled_params_dict[i])

# for checking that the parameters got in the right order
#for i in sp_list:
#    print(10**(i.mean()))
#sys.exit(0)

population_size=popsize

if uses_modeliter:
    sfr = paramdir+"/dir_model_"""+str(number)+"""_"+str(modeliter)+"/model_"""+str(number)+"""_"+str(modeliter)+"_"
else:
    sfr = paramdir+"/dir_model_"""+str(number)+"""/model_"""+str(number)+"""_"

# Make the prior function for PyMultiNest.
# adapted from https://github.com/LoLab-VU/Gleipnir/blob/master/gleipnir/multinest.py line 131-132
def prior(hypercube):
    return np.array([sp_list[i].ppf(value) for i, value in enumerate(hypercube)])

output = solve(LogLikelihood=likelihood, Prior=prior,
                       n_dims = len(sp_list),
                       n_live_points=population_size,
                       importance_nested_sampling=INS,
                       const_efficiency_mode=ceff,
                       sampling_efficiency=f,
                       outputfiles_basename=sfr,
                       verbose=True)

# don't need a print statement bc because all the info is in the outfiles... but print anyway i guess
print(output)

"""
    str_to_write_1+=str_to_write_2
    str_to_write_1+=str_to_write_3
    str_to_write_1+=str_to_write_4
    str_to_write_1+=str_to_write_5
    str_to_write_1+=str_to_write_6
    fname = run_file_dir+"/run_model_"+str(number)+"_clA_betafit.py"
    if not os.path.exists(run_file_dir):
        os.makedirs(run_file_dir)
    f = open(fname,"w")
    f.write(str_to_write_1)
    f.close()
