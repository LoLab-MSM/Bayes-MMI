import numpy as np
from scipy.stats import norm,uniform
import pickle

# All possible parameters for each candidate model, each with its corresponding prior (see Box 1, Fig S1, Fig S2)

sampled_params_dict = {}

## divs and deaths without effect option
# NE
sampled_params_dict['sp_division_0_NE_cell_1kc_0'] = norm(loc=np.log10(0.469), scale=0.026)
sampled_params_dict['sp_die_0_NE_cell_1kc_0'] = norm(loc=np.log10(0.081), scale=0.236)
# NEv1
sampled_params_dict['sp_division_0_NEv1_cell_1kc_0'] = norm(loc=np.log10(0.7831), scale=.481)
sampled_params_dict['sp_die_0_NEv1_cell_1kc_0'] = norm(loc=np.log10(0.081), scale=.236)
# NEv2
sampled_params_dict['sp_division_0_NEv2_cell_1kc_0'] = norm(loc=np.log10(0.1898), scale=0.1197)
sampled_params_dict['sp_die_0_NEv2_cell_1kc_0'] = norm(loc=np.log10(0.081), scale=0.236)
# NonNE
sampled_params_dict['sp_division_0_NonNE_cell_1kc_0'] = norm(loc=np.log10(0.769), scale=.079)
sampled_params_dict['sp_die_0_NonNE_cell_1kc_0'] = norm(loc=np.log10(0.081), scale=0.236)

## diffs without effect option
# NE to NEv2
sampled_params_dict['sp_diff_uni_0_NE_cell_NEv2_diff_cell_1kf_0'] = uniform(loc=np.log10(0.01), scale=3.5)
# NE to NEv1
sampled_params_dict['sp_diff_uni_0_NE_cell_NEv1_diff_cell_1kf_0'] = uniform(loc=np.log10(0.01), scale=3.5)
# NEv2 to NonNE
sampled_params_dict['sp_diff_uni_0_NEv2_cell_NonNE_diff_cell_1kf_0'] = uniform(loc=np.log10(0.01), scale=3.5)
# NEv1 to NonNE
sampled_params_dict['sp_diff_uni_0_NEv1_cell_NonNE_diff_cell_1kf_0'] = uniform(loc=np.log10(0.01), scale=3.5)

## No more effects for diff - all of these are optional rxns
sampled_params_dict['sp_diff_uni_0_NEv1_cell_NEv2_diff_cell_1kf_0'] = uniform(loc=np.log10(0.01), scale=3.5)
sampled_params_dict['sp_diff_uni_0_NE_cell_NonNE_diff_cell_1kf_0'] = uniform(loc=np.log10(0.01), scale=3.5)
sampled_params_dict['sp_diff_uni_0_NEv2_cell_NEv1_diff_cell_1kf_0'] = uniform(loc=np.log10(0.01), scale=3.5)
sampled_params_dict['sp_diff_uni_0_NonNE_cell_NE_diff_cell_1kf_0'] = uniform(loc=np.log10(0.01), scale=3.5)

# No more effects for diff - these are optional reactions (if a rxn is present, its other-direction rxn is always present - e.g. NE->NEv2, NEv2->NonNE, NE->NEv1, NEv1->NonNE)
sampled_params_dict['sp_diff_uni_0_NEv1_cell_NE_diff_cell_1kf_0'] = uniform(loc=np.log10(0.01), scale=3.5)
sampled_params_dict['sp_diff_uni_0_NonNE_cell_NEv1_diff_cell_1kf_0'] = uniform(loc=np.log10(0.01), scale=3.5)
sampled_params_dict['sp_diff_uni_0_NEv2_cell_NE_diff_cell_1kf_0'] = uniform(loc=np.log10(0.01), scale=3.5)
sampled_params_dict['sp_diff_uni_0_NonNE_cell_NEv2_diff_cell_1kf_0'] = uniform(loc=np.log10(0.01), scale=3.5)

## Divs, deaths with effect

# NE div
# baseline division rate
sampled_params_dict['sp_division_0_NE_cell_0'] = norm(loc=np.log10(0.469), scale=0.026)
# division rate in the presence of NonNE cells (either Y or A2&Y, depending on the model)
sampled_params_dict['sp_division_0_NE_cell_1'] = norm(loc=np.log10(.4925), scale=0.5)
# division rate equilibrium constant
sampled_params_dict['sp_division_0_NE_cell_2'] = norm(loc=np.log10(1000), scale=2)
# NE die
# baseline death rate
sampled_params_dict['sp_die_0_NE_cell_0'] = norm(loc=np.log10(0.081), scale=0.236)
# death rate in the presence of NonNE cells (either Y or A2&Y, depending on the model)
sampled_params_dict['sp_die_0_NE_cell_1'] = norm(loc=np.log10(0.077), scale=.5)
# death rate equilibrium constant
sampled_params_dict['sp_die_0_NE_cell_2'] = norm(loc=np.log10(1000), scale=2)

# NEv1 div
# same as above
sampled_params_dict['sp_division_0_NEv1_cell_0'] = norm(loc=np.log10(0.7831), scale=.481)
sampled_params_dict['sp_division_0_NEv1_cell_1'] = norm(loc=np.log10(.8223), scale=.5)
sampled_params_dict['sp_division_0_NEv1_cell_2'] = norm(loc=np.log10(1000), scale=2)
# NEv1 die
sampled_params_dict['sp_die_0_NEv1_cell_0'] = norm(loc=np.log10(0.081), scale=0.236)
sampled_params_dict['sp_die_0_NEv1_cell_1'] = norm(loc=np.log10(0.077), scale=.5)
sampled_params_dict['sp_die_0_NEv1_cell_2'] = norm(loc=np.log10(1000), scale=2)

# NEv2 div
# baseline
sampled_params_dict['sp_division_0_NEv2_cell_0'] = norm(loc=np.log10(0.1898), scale=.1197)
# division rate in the presence of 'affecting cells' - NE cells, if NEv2 acts like NonNE, or NonNE (specifically Y) cells, if NEv2 acts like NE
sampled_params_dict['sp_division_0_NEv2_cell_1'] = norm(loc=np.log10(0.1803), scale=.5)     # for models where NEv2 acts like NonNE
#sampled_params_dict['sp_division_0_NEv2_cell_1'] = norm(loc=np.log10(0.1993),scale=.5)     # for models where NEv2 acts like NE
# eq constant
sampled_params_dict['sp_division_0_NEv2_cell_2'] = norm(loc=np.log10(1000), scale=2)

# NEv2 die
# baseline
sampled_params_dict['sp_die_0_NEv2_cell_0'] = norm(loc=np.log10(0.081), scale=0.236)
# division rate in the presence of 'affecting cells' - NE cells, if NEv2 acts like NonNE, or NonNE (specifically Y) cells, if NEv2 acts like NE
sampled_params_dict['sp_die_0_NEv2_cell_1'] = norm(loc=np.log10(0.085), scale=.5)       # for models where NEv2 acts like NonNE
#sampled_params_dict['sp_die_0_NEv2_cell_1'] = norm(loc=np.log10(0.077), scale=.5)      # for models where NEv2 acts like NE
sampled_params_dict['sp_die_0_NEv2_cell_2'] = norm(loc=np.log10(1000), scale=2)

# NonNE div
# baseline
sampled_params_dict['sp_division_0_NonNE_cell_0'] = norm(loc=np.log10(0.769), scale=0.079)
# division rate in the presence of NE cells (A and N, or A,N,A2 depending on whether A2 acts like NE or NonNE)
sampled_params_dict['sp_division_0_NonNE_cell_1'] = norm(loc=np.log10(.731), scale=0.5)
# eq constant
sampled_params_dict['sp_division_0_NonNE_cell_2'] = norm(loc=np.log10(1000), scale=2)
# NonNE die
# as above
sampled_params_dict['sp_die_0_NonNE_cell_0'] = norm(loc=np.log10(0.081), scale=0.236)
sampled_params_dict['sp_die_0_NonNE_cell_1'] = norm(loc=np.log10(0.085), scale=.5)
sampled_params_dict['sp_die_0_NonNE_cell_2'] = norm(loc=np.log10(1000), scale=2)

## Diffs with effect

# NE to NEv2
sampled_params_dict['sp_diff_uni_0_NE_cell_NEv2_diff_cell_0'] = uniform(loc=np.log10(0.01), scale=3.5)
sampled_params_dict['sp_diff_uni_0_NE_cell_NEv2_diff_cell_1'] = uniform(loc=np.log10(0.05), scale=4)
sampled_params_dict['sp_diff_uni_0_NE_cell_NEv2_diff_cell_2'] = norm(loc=np.log10(1000), scale=2)

# NE to NEv1
sampled_params_dict['sp_diff_uni_0_NE_cell_NEv1_diff_cell_0'] = uniform(loc=np.log10(0.01), scale=3.5)
sampled_params_dict['sp_diff_uni_0_NE_cell_NEv1_diff_cell_1'] = uniform(loc=np.log10(0.05), scale=4)
sampled_params_dict['sp_diff_uni_0_NE_cell_NEv1_diff_cell_2'] = norm(loc=np.log10(1000), scale=2)

# NEv2 to NonNE
sampled_params_dict['sp_diff_uni_0_NEv2_cell_NonNE_diff_cell_0'] = uniform(loc=np.log10(0.01), scale=3.5)
sampled_params_dict['sp_diff_uni_0_NEv2_cell_NonNE_diff_cell_1'] = uniform(loc=np.log10(0.05), scale=4)
sampled_params_dict['sp_diff_uni_0_NEv2_cell_NonNE_diff_cell_2'] = norm(loc=np.log10(1000), scale=2)

# NEv1 to NonNE
sampled_params_dict['sp_diff_uni_0_NEv1_cell_NonNE_diff_cell_0'] = uniform(loc=np.log10(0.01), scale=3.5)
sampled_params_dict['sp_diff_uni_0_NEv1_cell_NonNE_diff_cell_1'] = uniform(loc=np.log10(0.05), scale=4)
sampled_params_dict['sp_diff_uni_0_NEv1_cell_NonNE_diff_cell_2'] = norm(loc=np.log10(1000), scale=2)

with open('../helper_functions_and_files/all_possible_sampled_params_dict.pickle', 'wb') as p:
    pickle.dump(sampled_params_dict,p)
