Estimators and Evaluation Tools
===============================

The ``pyensemblefs.estimators`` module contains utility functions designed
to evaluate classifiers trained on subsets of features produced by ensemble
feature selection methods.  
These components are *experimental runners* rather than estimators in the
scikit-learn sense, and they are used to:

- Train classifiers with different numbers of selected features.
- Evaluate model performance across feature subsets.
- Compute classification metrics (binary and multiclass).
- Integrate results with ensemble-based feature selection pipelines.

This module complements the ``ensemble`` and ``stability`` modules by
linking selected features with predictive performance.

.. contents::
   :local:
   :depth: 2


Training Utilities
------------------

train_fs_clf_with_different_k_features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pyensemblefs.estimators.base.train_fs_clf_with_different_k_features

This function automates the evaluation of a classifier over a full range of
subset sizes, using ranked features from either:

- an individual selector, or  
- an ensemble voting/ranking method.

It returns performance metrics for each value of :math:`k`, enabling an
analysis of *predictive performance vs. number of features*.


select_optimal_features_ensemblefs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pyensemblefs.estimators.base.select_optimal_features_ensemblefs

This function determines the optimal number of selected features using an
ensemble-produced ranking.  
It evaluates percentages of the ranked list (10%–100%), identifying the
subset yielding the highest score according to a chosen metric.


Evaluation Metrics
------------------

The ``evaluator`` module provides a unified interface to evaluate binary and
multiclass classifiers.

get_metric_classification
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pyensemblefs.estimators.evaluator.get_metric_classification

Maps requested scoring metrics to their binary or multiclass variants.


compute_classification_prestations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pyensemblefs.estimators.evaluator.compute_classification_prestations

Computes a dictionary of classification metrics, including:

- accuracy  
- precision  
- recall / sensitivity  
- specificity  
- ROC-AUC  
- F1-score  


compute_multiclass_metrics
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pyensemblefs.estimators.evaluator.compute_multiclass_metrics


Example Usage
-------------

A minimal workflow integrating feature selection, classifier evaluation and
stability analysis:

.. code-block:: python

   import pandas as pd
   import numpy as np
   from pyensemblefs.datasets import load_breast_cancer_dataset
   from pyensemblefs.fsmethods.factory import get_fs_method
   from pyensemblefs.ensemble.bootstrapper import Bootstrapper
   from pyensemblefs.aggregators.rank import MeanRankAggregator
   from pyensemblefs.ensemble.featureselector import EnsembleFeatureSelector

   # Load data
   df = load_breast_cancer_dataset()
   X = df.drop(columns=["target"])
   y = df["target"]

   # Create the feature selection pipeline manually
   # 1. Create a base selector
   base_selector = get_fs_method("variance")

   # 2. Create bootstrapper with the selector
   bootstrapper = Bootstrapper(fs_method=base_selector, n_bootstraps=50)

   # 3. Create aggregator (concrete implementation)
   aggregator = MeanRankAggregator()

   # 4. Combine them with EnsembleFeatureSelector
   ensemble_fs = EnsembleFeatureSelector(
      bootstrapper=bootstrapper,
      aggregator=aggregator,
      k=20  # Select top 20 features
   )

   # Fit and transform
   ensemble_fs.fit(X, y)
   X_selected = ensemble_fs.transform(X)

   print(f"Original shape: {X.shape}")
   print(f"Selected shape: {X_selected.shape}")
   print(f"Selected features: {X_selected.columns.tolist()}")

API Reference
-------------

.. automodule:: pyensemblefs.estimators
   :members:
   :undoc-members:
   :show-inheritance:
