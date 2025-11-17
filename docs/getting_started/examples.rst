Examples
========

- **Aggregators**: Score/frequency/ranking combination.
- **Stability**: Stability metrics between feature lists.
- **Visualization**: Ranking and stability comparison.

.. code-block:: python

    from pyensemblefs.aggregators.score import MeanAggregator, SelectionFrequencyAggregator
    from pyensemblefs.aggregators.rank import MeanRankAggregator
    from pyensemblefs.aggregators.subset import TopKBinaryAggregator