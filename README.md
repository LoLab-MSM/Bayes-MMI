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
directory, files generated via the multimodel_inference_SCLC/ scripts, used in the publication, are hosted via DropBox.
The empty directories in this repository (files_generated_in_MMI_sclc/ and posterior_marginals_and_predictives/) are the
locations where Bayes-MMI code expects the data to be placed in order to generate figures; these are identical to 
directory names in DropBox where the data is located.

To run the Bayes-MMI/plotting_incl_for_paper_figures/ scripts, go to the DropBox link and download the contents of the 
directories, and place them in the identically-named but empty directories provided in Bayes-MMI.

DropBox link:
https://www.dropbox.com/sh/4fqzpvu9hgyjicm/AABdfFlCenEuiOPgiH0TT-xqa?dl=0

Bayes-MMI repository arrangement
--------------------

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


