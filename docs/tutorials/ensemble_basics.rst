Ensemble Feature Selection Basics
=================================

This tutorial introduces the principles of ensemble feature selection (EFS)
and how ``pyensemblefs`` implements them.

Topics
------

- Why ensemble feature selection?
- Variance, ranking, frequency and score-based methods
- Basic usage examples

Example
-------

.. code-block:: python

   from pyensemblefs.ensemble.featureselector import FeatureSelector
   selector = FeatureSelector(method="variance", k=10)
   selector.fit(X, y)
