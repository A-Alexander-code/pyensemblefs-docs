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
   from pyensemblefs.ensemble.featureselector import FeatureSelector
   from pyensemblefs.estimators.base import train_fs_clf_with_different_k_features

   # Load data
   X = pd.DataFrame(...)
   y = np.array(...)

   # Feature selection
   fs = FeatureSelector(method="variance", k=20)
   fs.fit(X, y)
   df_selected, df_scores = fs.extract_features()

   # Evaluate classifier performance across k=1...p
   metrics, ranked_scores = train_fs_clf_with_different_k_features(
       df_features=X,
       y_label=y,
       fs_method_name="variance",
       bbdd_name="my_data",
       estimator_name="dt",
       scoring_estimator="roc_auc"
   )

   print(metrics[:5])

API Reference
-------------

.. automodule:: pyensemblefs.estimators
   :members:
   :undoc-members:
   :show-inheritance:
