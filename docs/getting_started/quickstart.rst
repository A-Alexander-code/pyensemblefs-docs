Quickstart
==========

Minimal example
---------------

.. code-block:: python

   from ensemble.featureselector import FeatureSelector
   from utils.datasets import loader

   X, y = load_dataset("sim_pow")  # as example data/sim_pow.csv
   fs = FeatureSelector(
       methods=["variance"],   # check fsmethods/
       n_features=10,
       n_bootstraps=50,
       n_jobs=-1,              # multiprocessing
   )
   ranking = fs.fit_rank(X, y)
   print(ranking[:10])