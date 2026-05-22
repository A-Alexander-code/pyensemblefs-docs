Quickstart
==========

Minimal example
---------------

.. code-block:: python

    from sklearn.datasets import load_breast_cancer
    from pyensemblefs.ensemble.featureselector import FeatureSelector

    # Load a dataset
    X, y = load_breast_cancer(return_X_y=True)

    # Create and fit a simple selector
    selector = FeatureSelector(method="variance", k=10)
    selector.fit(X, y)

    # Inspect the selected features
    print("Selected features:", selector.selected_features_)
