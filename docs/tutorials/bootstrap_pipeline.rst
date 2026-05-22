Bootstrapping Pipeline
======================

This tutorial explains how to perform repeated subsampling and combine
feature rankings or masks across multiple runs.

Contents
--------

- Bootstrapping strategies
- Aggregation methods
- Combining multiple feature selectors

Example
-------

.. code-block:: python

   from sklearn.datasets import load_breast_cancer
   from sklearn.feature_selection import SelectKBest, f_classif
   from pyensemblefs.ensemble.bootstrapper import Bootstrapper

   X, y = load_breast_cancer(return_X_y=True)

   base_fs = SelectKBest(score_func=f_classif, k=10)
   boot = Bootstrapper(fs_method=base_fs, n_bootstraps=50)
   results = boot.run(X, y)

   aggregated = boot.aggregate(results)
