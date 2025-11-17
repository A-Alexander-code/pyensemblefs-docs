End-to-End Workflow: From Data to Stability and Visualization
=============================================================

This tutorial demonstrates a complete ``pyensemblefs`` workflow:

1. Load a dataset.
2. Apply a simple feature selection method on multiple bootstrap samples.
3. Aggregate feature selections via selection frequency.
4. Compute stability metrics across bootstrap runs.
5. Visualize selection frequencies.

The goal is to illustrate how ensemble feature selection, stability
analysis, and visualization fit together in a single pipeline.


Step 1 – Load a dataset
-----------------------

We use a standard classification dataset from ``scikit-learn``:

.. code-block:: python

   import numpy as np
   import pandas as pd
   from sklearn.datasets import load_breast_cancer

   data = load_breast_cancer(as_frame=True)
   X = data.data
   y = data.target

   print(X.shape, y.shape)


Step 2 – Bootstrap resampling + feature selection
-------------------------------------------------

We will use a simple subset-based filter from ``pyensemblefs.fsmethods``
to select features on different bootstrap samples of the same dataset.

.. code-block:: python

   from sklearn.utils import resample
   from pyensemblefs.fsmethods import SubsetFilter

   n_bootstraps = 30
   n_features = X.shape[1]

   # Store binary masks of selected features
   bootstrap_supports = []

   for b in range(n_bootstraps):
       X_b, y_b = resample(X, y, replace=True, random_state=42 + b)

       fs = SubsetFilter(rule="variance", k=10)
       fs.fit(X_b, y_b)

       # fs.selected_features_ is expected to be a boolean mask of shape (p,)
       support = np.asarray(fs.selected_features_, dtype=int)
       bootstrap_supports.append(support)

   bootstrap_supports = np.vstack(bootstrap_supports)
   print("Supports shape:", bootstrap_supports.shape)  # (n_bootstraps, p)


Step 3 – Aggregate selections via frequency
-------------------------------------------

A simple and interpretable aggregation rule is the *selection frequency*:
for each feature, count in how many bootstraps it was selected.

.. code-block:: python

   selection_frequency = bootstrap_supports.mean(axis=0)

   # Top-10 most frequently selected features
   top_indices = np.argsort(selection_frequency)[::-1][:10]

   print("Top-10 features by frequency:")
   for idx in top_indices:
       print(f"  Feature {idx}: freq = {selection_frequency[idx]:.2f}")


Step 4 – Compute stability metrics
----------------------------------

We now quantify how stable these selections are across bootstrap samples
using the stability utilities.

.. code-block:: python

   from pyensemblefs.stability.evaluator import StabilityEvaluator

   # bootstrap_supports has shape (B, p), values in {0,1}
   evaluator = StabilityEvaluator(
       metrics="all12",   # Jaccard, Dice, Ochiai, Hamming, Novovicova, Davis,
                          # Lustgarten, Phi, Kappa, Nogueira, Yu, Zucknick
       mode="subset",
   )

   result = evaluator.compute(bootstrap_supports)

   print("Stability metrics:")
   for name, value in result.values.items():
       print(f"  {name:10s}: {value:.4f}")

   print("Summary stability (mean over metrics):", result.summary)


Step 5 – Visualize selection frequencies
----------------------------------------

Finally, we use the visualization module to inspect how often each
feature is selected.

.. code-block:: python

   from pyensemblefs.viz.visualizer import Visualizer

   Visualizer.plot_topk_frequency(
       selection_frequency,
       feature_names=X.columns,
       top_k=20,
       title="Top-20 selection frequencies across bootstraps"
   )

This produces a bar plot showing the most frequently selected features.
