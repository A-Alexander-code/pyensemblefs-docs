Quickstart
==========

Minimal example
---------------

.. code-block:: python

    import pyensemblefs
    from pyensemblefs.datasets import load_pima_dataset

    # Load dataset
    df = load_pima_dataset()

    # Retrieve a pre-defined configuration (e.g., Relief filter)
    cfg = pyensemblefs.get_config('relief', n_bootrap=100, fnc_aggregation='voting')

    # Compute feature scores
    df_feature_scores = pyensemblefs.compute_scores(cfg, df)

    # Extract the most relevant features
    df_filtered = pyensemblefs.extract_features(n_max_features=10)