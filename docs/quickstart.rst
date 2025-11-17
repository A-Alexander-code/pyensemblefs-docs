Quickstart
==========

A minimal workflow demonstrating how to run an ensemble feature selection
experiment using ``pyensemblefs``.

Basic usage
-----------

.. code-block:: python

   from pyensemblefs.ensemble.featureselector import FeatureSelector

   selector = FeatureSelector(method="variance", k=5)
   selector.fit(X, y)

   print("Selected features:", selector.selected_features_)

Next steps
----------

To learn more:

- Understanding ensembling: :doc:`tutorials/ensemble_basics`
- Using bootstrapping: :doc:`tutorials/bootstrap_pipeline`
- Measuring stability: :doc:`tutorials/stability_analysis`
- Visualization tools: :doc:`tutorials/visualization_tools`
