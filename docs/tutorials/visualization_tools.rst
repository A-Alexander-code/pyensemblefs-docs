Visualization Tools
===================

Use ``Visualizer`` to inspect feature frequencies, bootstrap selections and
aggregator rankings. The two heatmaps support styling and PNG/PDF export.

Bootstrap selection heatmap
---------------------------

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt
   from pyensemblefs.viz.visualizer import Visualizer

   supports = np.array([[1, 0, 1, 0], [1, 1, 0, 0], [0, 1, 1, 0]])
   names = ["age", "weight", "height", "pressure"]
   fig, ax = Visualizer.stability_heatmap(
       supports, n_features=4, feature_names=names,
       title=None, cmap="Blues", annotate=True,
       font_sizes={"x_ticks": 10, "y_ticks": 10, "colorbar_ticks": 9},
       output_dir="figures", filename="bootstrap_selections",
       save_png=True, save_pdf=True, dpi=300, show=False,
   )
   plt.close(fig)

NumPy matrices are interpreted as binary supports or scores; score rows select
the largest ``top_k`` values. A Python list is interpreted as a list of selected
feature-index arrays, not a nested binary matrix. Bootstrap heatmaps retain all
feature columns in their original order, including never-selected features.

Aggregator comparison heatmap
-----------------------------

.. code-block:: python

   # Per-feature ranks in the same column order; lower values rank first.
   ranks = {
       "mean": np.array([1, 3, 2, 4]),
       "median": np.array([2, 1, 3, 4]),
   }
   fig, ax = Visualizer.compare_aggregators_heatmap(
       ranks, top_k=2, feature_names=names,
       title="Top-2 ranks", annotate=True,
       output_dir="figures", filename="aggregators",
       save_png=True, save_pdf=True, show=False,
   )
   plt.close(fig)

Inputs are equal-length per-feature rank vectors, rather than ordered feature
indices. Each row displays the positions 1..k of its best features. Columns
outside every aggregator's top-k are removed from the rendered comparison;
partially populated columns remain, with masked cells for other aggregators.
Retained columns preserve original feature order and input rankings are unchanged.

Labels, styling and export
--------------------------

Both heatmaps return an open ``(fig, ax)`` for further customization. Use
``show=False`` for file generation without display and close the figure when done.
The colorbar is available through ``ax.collections[0].colorbar``.

- ``feature_names`` supplies one label per input column; defaults are f1..fn.
- ``title=None`` omits the title and its reserved space.
- ``font_sizes`` accepts ``title``, ``x_label``, ``y_label``, ``x_ticks``,
  ``y_ticks`` and ``colorbar_ticks``; unknown keys raise an error.
- ``max_tick_labels=32`` shows every label for short axes. Longer axes show
  every ``tick_interval=15`` cells, always including the last. This changes
  tick density, not the underlying cells, and applies to both axes.
- ``save_png`` and ``save_pdf`` enable either or both formats with white
  backgrounds and tight bounds; ``dpi`` defaults to 150.
- ``output_dir`` is created when saving. With export flags, ``filename`` is
  a base name; a PNG/PDF suffix is stripped before extensions are added.
  Defaults are ``stability_heatmap`` and ``aggregators_comparison_heatmap``.
  Absolute filenames override the output directory.
- With neither export flag, ``filename`` alone retains legacy single-file
  saving. With no filename or flags, no file is saved.

Frequency and other plots
-------------------------

.. code-block:: python

   frequencies = supports.mean(axis=0)
   fig, ax = Visualizer.plot_topk_frequency(
       feature_names=names, frequencies=frequencies,
       title="Selection frequency",
   )
   plt.close(fig)

The facade also exposes consensus ranking, cumulative agreement, pairwise
agreement curves, stability curves and UpSet intersections. See
:doc:`../api/viz` for the function reference.
