Visualization Tools
===================

The ``pyensemblefs.viz`` module provides high-level and low-level visualization
tools for analyzing ensemble feature selection results, including:

- Feature frequency plots
- Stability heatmaps
- Ranking consensus visualizations
- Aggregator comparison heatmaps
- Cumulative agreement analysis
- Upset plots for feature intersections

It serves as the preferred interface for visual diagnostics when evaluating
homogeneous or heterogeneous ensemble methods.

This page documents all visualization utilities available in the package.


.. contents::
   :local:
   :depth: 2


High-Level Interface (Visualizer)
---------------------------------

The :class:`pyensemblefs.viz.visualizer.Visualizer` class provides a clean
facade that exposes all visualization functions under a single object.

Example
~~~~~~~

.. code-block:: python

   from pyensemblefs.viz.visualizer import Visualizer

   # Example: visualize top-k feature frequency
   Visualizer.plot_topk_frequency(
       scores_or_selected,
       top_k=15
   )

Available methods
~~~~~~~~~~~~~~~~~

- ``consensus_ranking`` — Computes and visualizes ranking consensus.
- ``plot_topk_frequency`` — Frequency plot for top-k ranked features.
- ``feature_frequency`` — Barplot of feature selection frequency.
- ``stability_heatmap`` — Heatmap of selected features over bootstraps.
- ``stability_over_bootstraps`` — Line plot of stability vs number of bootstraps.
- ``compare_aggregators_heatmap`` — Heatmap comparing multiple aggregators.
- ``cumulative_agreement_plot`` — Agreement curves across aggregators or selectors.
- ``pairwise_cumulative_agreement`` — Pairwise agreement matrix.
- ``topk_upset_plot`` — UpSet-style visualization of top-k intersections.

All methods are accessible via:

.. code-block:: python

   Visualizer.<method_name>(...)


Ranking Visualizations
----------------------

Consensus Ranking
~~~~~~~~~~~~~~~~~

Computes a consensus ordering across ranking-based selectors.

.. autofunction:: pyensemblefs.viz.ranking.consensus_ranking

Top-K Frequency Plot
~~~~~~~~~~~~~~~~~~~~

Plots how often each feature appears in the top-k positions.

.. autofunction:: pyensemblefs.viz.ranking.plot_topk_frequency


Stability Visualizations
------------------------

Feature Frequency
~~~~~~~~~~~~~~~~~

Barplot of how frequently each feature is selected across bootstrap runs.

.. autofunction:: pyensemblefs.viz.stability.feature_frequency

Stability Heatmap
~~~~~~~~~~~~~~~~~

Displays the binary selection matrix (or top-k converted scores) across
bootstraps.

.. autofunction:: pyensemblefs.viz.stability.stability_heatmap

Stability Curve
~~~~~~~~~~~~~~~

Line plot of stability score vs number of bootstraps.

.. autofunction:: pyensemblefs.viz.stability.stability_over_bootstraps


Aggregator Comparison Plots
---------------------------

Aggregator Comparison Heatmap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Computes and visualizes agreement among multiple aggregators.

.. autofunction:: pyensemblefs.viz.comparison.compare_aggregators_heatmap

Cumulative Agreement Plot
~~~~~~~~~~~~~~~~~~~~~~~~~

Displays cumulative agreement curves across different methods.

.. autofunction:: pyensemblefs.viz.comparison.cumulative_agreement_plot

Pairwise Cumulative Agreement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Matrix quantifying agreement between pairs of ranking or subset selectors.

.. autofunction:: pyensemblefs.viz.comparison.pairwise_cumulative_agreement

Top-K UpSet Plot
~~~~~~~~~~~~~~~~

UpSet-style plot showing intersections among the top-k features selected
by different aggregators.

.. autofunction:: pyensemblefs.viz.comparison.topk_upset_plot


API Reference
-------------

.. automodule:: pyensemblefs.viz
   :members:
   :undoc-members:
   :show-inheritance:
   :noindex:
