# Bayes-MMI

This repository contains code from 'Unified Tumor Growth Mechanisms from Multimodel Inference and Dataset Integration'.

There are empty directories in this repository, and these are for data referenced 
in the scripts to plot figures and other supporting plots for the publication. These
scripts, contained in plotting_incl_for_paper_figures/, will not be able to run 
without this data. The data is hosted on DropBox. To run the Bayes-MMI/plotting_incl_for_paper_figures/ 
scripts, go to the DropBox link and download the contents of the directories there and
place them in the identically-named but empty directories provided in Bayes-MMI.

DropBox link:
https://www.dropbox.com/sh/4fqzpvu9hgyjicm/AABdfFlCenEuiOPgiH0TT-xqa?dl=0

** Explain what the project does here **

Data-generating and analyzing code is in the multimodel_inference_SCLC directory,
where each script can be run in order. Scripts 01 through 05 generate all of the
PySB models that represent model candidates for the multimodel inference analysis,
as well as generate individual scripts that will run nested sampling (via PyMultiNest)
on each model to calculate posterior fitted parameter distributions and the marginal
likelihood (Bayesian evidence) value per model. 06_run_pymultinest_files.txt describes
running PyMultiNest on each model, which will be unique to the user wanting to
replicate the fitted parameters/evidence values for each SCLC candidate model.

Scripts 07 through 10 use the results of nested sampling and combine, per dataset, each model's evidence
value (scripts 07a-c and 08) and each model's posterior fitted parameters, generating
all model posterior marginal distributions (09) and all model posterior predictive
distributions. Helper functions (in helper_functions_and_files/) consolidate_posterior_marginal_distributions.py
and consolidate_posterior_predictive_distributions.py then make these files more accessible.

Plotting code is in the plotting_incl_for_paper_figures/ directory, named and commented within
each file for which figure is plotted using each script (e.g., script f03 plots each part of Figure 3,
and comments within the script indicate the code that plots Fig 3A-C, and the code that plots Fig 3D).
Files from the DropBox link above are required for running these scripts.


