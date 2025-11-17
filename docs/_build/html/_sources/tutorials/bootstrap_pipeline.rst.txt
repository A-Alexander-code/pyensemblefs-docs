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

   from pyensemblefs.ensemble.bootstrapper import Bootstrapper

   boot = Bootstrapper(method="variance", n_bootstraps=50)
   results = boot.run(X, y)

   aggregated = boot.aggregate(results)
