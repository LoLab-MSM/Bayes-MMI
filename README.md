Bayes-MMI
========

This is the repository for the Bayesian Multimodel Inference (Bayes-MMI) analysis of small cell lung cancer (SCLC) using 
several RNA-sequencing datasets integrated into one overall analysis, to be published as "Unified Tumor Growth 
Mechanisms from Multimodel Inference and Dataset Integration". Code in this repository represents the generation of
multiple candidate models of SCLC based on prior knowledge, followed by model selection and Bayesian evidence (marginal 
likelihood) value calculation via Nested Sampling. Evidence values are then used to determine posterior probabilities 
per model, which are model-averaged to 1) generate posterior parameter distributions across all candidate models, and 2) 
determine the probability of model features conditioned on the evaluated datasets. 

Why Bayesian Multimodel Inference of small cell lung cancer (SCLC)?
---------------------------------

Mathematical modeling aims to provide a mechanistic understanding of cellular processes, but model composition and 
comparison to the data represented continue to be a challenge. A single proposed model may represent only a subset of 
mechanistic hypotheses, and the data may not inform every aspect of the model – even after parameter calibration. 
Hypothesis exploration in biological processes via mechanistic modeling is a challenge in nearly every system, including 
the molecular biology of SCLC. We probe unanswered questions in the SCLC field about 
heterogeneity, lineage plasticity, and cell-cell interactions in the tumor system, using a Bayesian multimodel 
inference (MMI) approach to evaluate mathematical models of SCLC representing mechanistic hypotheses inferred from 
data. Integrating multiple existing datasets, our approach directly enables estimating how informative the data are 
for a given model hypothesis, and whether multiple hypotheses support the data equally well. Predictions from our 
application of Bayesian MMI support tumor evolution promoted by high lineage plasticity, rather than through expanding 
rare stem-like populations. This work yields a novel probabilistic understanding of SCLC tumor growth mechanisms, 
highlighting what mechanistic knowledge is supported by data and identifying which desired knowledge requires further 
experiments. These results highlight that given available data, any SCLC cellular subtype can contribute to tumor 
repopulation post-treatment, suggesting a mechanistic interpretation for tumor recalcitrance.
                                                                                                                    

Download
--------
To use this code, you can clone the repository with Git:
```bash
git clone https://github.com/LoLab-VU/Bayes-MMI.git
```

The code may be run from scratch, by running scripts in number-order in the multimodel_inference_SCLC/ directory. In
this usage, no downloads are necessary. Figures can then be generated after all multimodel_inference_SCLC/ scripts have 
been run and completed.

To run only the figure-generating code, with scripts in figure-number-order in the plotting_incl_for_paper_figures/ 
directory, files generated via the multimodel_inference_SCLC/ scripts, used in the publication, are hosted via Zenodo.
The following directories in this repository: files_generated_in_MMI_sclc/ and posterior_marginals_and_predictives/ are the
locations where Bayes-MMI code expects the data to be placed in order to generate figures.

To run the Bayes-MMI/plotting_incl_for_paper_figures/ scripts, go to the Zenodo links and download the contents of all three, and place them in the appropriate directories:

Place in files_generated_in_MMI_sclc/ : <br>
&emsp; results_fromNS_gathered_TKO_addlanalyses.pickle <br>
&emsp; results_fromNS_gathered_RPM_addlanalyses.pickle <br>
&emsp; results_fromNS_gathered_cl_A_addlanalyses.pickle <br>

Place in posterior_marginals_and_predictives/ : <br>
&emsp; All other files from the Zenodo repositories

Zenodo links: <br>
&emsp; https://doi.org/10.5281/zenodo.6671100 (TKO data files) <br>
&emsp;https://doi.org/10.5281/zenodo.8002484 (RPM data files) <br>
&emsp;https://doi.org/10.5281/zenodo.8002506 (SCLC-A cell line data files)

How to run Bayes-MMI (with SCLC data)
------------------------------------

**Python libraries required for Bayes-MMI with SCLC data**:
```angular2html
library                   versions used for the publication
-------                   ---------------------------------
matplotlib                3.0.3
*multinest                3.10
networkx                  2.3
numpy                     1.17.2
pandas                    1.2.2
*pymultinest              2.9
pysb                      1.11.0
python                    3.7.3
scipy                     1.5.0
seaborn                   0.11.1
statsmodels               0.10.1
```

*starred libraries:
- To install PyMultinest/Multinest, please follow instructions at: http://johannesbuchner.github.io/PyMultiNest/index.html#

**Running Bayes-MMI with SCLC data**

Data-generating and analyzing code is in the multimodel_inference_SCLC directory,
where each script can be run in order. 
- Scripts 01 through 05: these generate all of the
PySB models that represent model candidates for the multimodel inference analysis,
as well as generate individual scripts that will run nested sampling (via PyMultiNest)
on each model to calculate posterior fitted parameter distributions and the marginal
likelihood (Bayesian evidence) value per model. 
- 06_run_pymultinest_files.txt: this file describes
running PyMultiNest on each model, which will be unique to the user wanting to
replicate the fitted parameters/evidence values for each SCLC candidate model.
- Scripts 07 through 10: these use the results of nested sampling and combine, per dataset, each model's evidence
value (scripts 07a-c and 08) and each model's posterior fitted parameters, generating
all model posterior marginal distributions (09) and all model posterior predictive
distributions (10). Scripts 09 and 10 result in multiple files as-written.
  - Helper function (located in helper_functions_and_files/) modeldict_generator.py is used in scripts 07a-c, 09, and 10
  to access the features of all PySB candidate models.
  - Helper functions (helper_functions_and_files/) consolidate_posterior_marginal_distributions.py and
  consolidate_posterior_predictive_distributions.py must be called by the user, and will make the multiple files of
  analyzed data from scripts 09 and 10 into one consolidated file each, enabling scripts used for plotting to easily
  access these analyzed data.

Plotting code, including for plotting-specific helper functions, is in the plotting_incl_for_paper_figures/ directory, 
named and commented within each file for which figure is plotted using each script (e.g., script f03 plots each part of 
Figure 3, and comments within the script indicate the code that plots Fig 3A-C, and the code that plots Fig 3D). Files 
from the DropBox link above are required for running these scripts.
- Script f03: this plots the Bayesian evidence (marginal likelihood) values per candidate model in order, per dataset, 
corresponding to Figures 3A-C in the publication, and plots the total numbers of candidate models in and out of 
confidence intervals per dataset, corrseponding to Figure 3D.
- Script f04a: this plots the Bayesian model-averaged probabilities of each model structure compared to each dataset, 
corresponding to Figure 4A.
  - Helper function posterior_probability_calculations.py is called by this script to calculate these probabilities.
- Script f04b: this plots the Bayesian model-averaged posterior parameter distributions per highest-scoring model 
structures (seen in Figure 4A) per dataset, corresponding to Figure 4B.
- Script f05: this plots the Bayesian model-averaged probabilities of each feature in the highest-scoring three-subtype
models, as a heatmap, corresponding to Figure 5A, and as model topology representations, corresponding to Figures 5B-D.
  - Helper function posterior_probability_calculations.py (in helper_functions_and_files/) is called by this script to 
  calculate the model-averaged probabilities for each model structure.
  - Plotting-specific helper function plotting_incl_for_paper_figures/posterior_prob_networkgraph_plotting.py is called
  by this script to generate model topology representations using posterior probabilities to determine edge color.
- Scripts plot_prior_and_posterior_marginals.py and plot_prior_and_posterior_predictives.py: these plot model-averaged 
posterior parameter distributions (posterior marginals), and simulate candidate models using model-averaged posterior 
marginal distributions (posterior predictives). Part of plot_prior_and_posterior_marginals.py corresponds to
Figure 5F, and the remainder of the script, as well as plot_prior_and_posterior_predictives.py, correspond to 
supplementary figures.
