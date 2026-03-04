I structured the metadata file into clearly separated sections so that each part of the analysis workflow is documented independently. The main sections are dataset, generation, observables, weights, unfolding, normalization, and event selection which directly correspond to the gaps identified in Part 1.

The dataset and samples sections describe what files exist and how they relate to each other. This is important because the three files (Nominal, Sherpa, NonDY) have different numbers of columns and events, so users need context.

The observables section clarifies which columns represent physical measurements, since the DataFrame itself does not distinguish observables from weights beyond naming conventions.

The weights section is structured carefully because it is the most critical part for reuse. I included the number of weight columns, examples of systematic variations, and an explicit combination rule (multiplicative). This prevents misuse and clarifies how the weights should be applied.

The unfolding section includes OmniFold related details, even though the current files do not provide them. Including placeholders such as “Not specified” highlights missing reproducibility information and shows what should be documented in future analyses.

I chose not to include very low-level machine learning hyperparameters because they are not always necessary for someone simply applying the weights. However, the schema is flexible and could be extended if full training reproducibility is required.

A user who did not run the original analysis would use this YAML file as a guide to understand:

What the dataset represents
Which columns are observables vs. weights
How to correctly combine weights
How normalization is handled