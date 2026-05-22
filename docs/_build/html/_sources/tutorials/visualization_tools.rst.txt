Visualization Tools
===================

Visualize feature rankings, intersections, and stability matrices.

Tools covered
-------------

- Ranking bar plots
- Intersection heatmaps
- Upset plots
- Stability visualizations

Example
-------

.. code-block:: python

   from pyensemblefs.viz.visualizer import Visualizer

   Visualizer.plot_topk_frequency(
       feature_names=top_feature_names,
       frequencies=top_frequencies,
       title="Top-k selection frequency"
   )
