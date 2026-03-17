Aggregators
===========

The :mod:`pyensemblefs.aggregators` subpackage implements multiple families of
aggregation methods that operate on bootstrap outputs (scores, ranks, or
binary supports). These correspond to the score-based, rank-based, and
subset-based rules described in the paper.

Overview
--------

All aggregators follow a common contract defined in
:class:`pyensemblefs.aggregators.base.BaseAggregator`:

- Input is a 2D array ``results`` of shape ``(n_bootstraps, n_features)``.
- :meth:`aggregate` returns a 1D vector of length ``n_features`` (scores, ranks
  or a binary mask, depending on the subclass).
- :meth:`fit` computes an internal ranking and a selection mask based on
  ``top_k`` and the aggregated values.

Aggregator families
-------------------

Score-based aggregators
~~~~~~~~~~~~~~~~~~~~~~~

Defined in :mod:`pyensemblefs.aggregators.score`, they treat **higher values
as better** and work directly on real-valued matrices of scores
(e.g., feature importances or relevance scores per bootstrap):

- :class:`pyensemblefs.aggregators.score.MeanAggregator`  
  Arithmetic mean of scores across bootstraps.

- :class:`pyensemblefs.aggregators.score.SumAggregator`  
  Sum of scores across bootstraps.

- :class:`pyensemblefs.aggregators.score.MedianAggregator`  
  Median of scores (robust to outliers).

- :class:`pyensemblefs.aggregators.score.TrimmedMeanAggregator`  
  Alpha-trimmed mean, removing a fraction of lowest and highest scores.

- :class:`pyensemblefs.aggregators.score.WinsorizedMeanAggregator`  
  Winsorized mean, clipping extremes to alpha-quantiles.

- :class:`pyensemblefs.aggregators.score.GeometricMeanAggregator`  
  Geometric mean, emphasizing consistently high scores.

- :class:`pyensemblefs.aggregators.score.RankProductAggregator`  
  Rank-product style aggregation on scores (log-domain), returning
  ``-log-product`` so that higher values indicate more stable high scores.

- :class:`pyensemblefs.aggregators.score.WeightedScoreAggregator`  
  Weighted average of scores across bootstraps, using user-provided weights.

- :class:`pyensemblefs.aggregators.score.BordaFromScoresAggregator`  
  Converts per-bootstrap scores to ranks and applies Borda count, summing
  Borda points across bootstraps.

- :class:`pyensemblefs.aggregators.score.SelectionFrequencyAggregator`  
  Converts binary supports into selection frequencies in ``[0, 1]``; useful
  when base selectors return subsets instead of scores.

These aggregators directly implement the **score-based pooling** and
**selection-frequency** strategies summarized in the Aggregation Methods
section of the paper.

Rank-based aggregators
~~~~~~~~~~~~~~~~~~~~~~

Defined in :mod:`pyensemblefs.aggregators.rank`, they operate on score
matrices but internally convert them to **ranks per bootstrap** (1 = best)
and then combine these ranks. They inherit from
:class:`pyensemblefs.aggregators.base.RankAggregator`, where **lower values
are better**:

- :class:`pyensemblefs.aggregators.rank.MeanRankAggregator`  
  Mean rank across bootstraps.

- :class:`pyensemblefs.aggregators.rank.MedianRankAggregator`  
  Median rank across bootstraps.

- :class:`pyensemblefs.aggregators.rank.ConsensusRankAggregator`  
  Conceptually equivalent to mean rank, kept for semantic clarity.

- :class:`pyensemblefs.aggregators.rank.BordaFromRanksAggregator`  
  Borda fusion from rank input; if the input does not look like proper
  ranks, it is automatically converted from scores.

- :class:`pyensemblefs.aggregators.rank.TrimmedMeanRankAggregator`  
  Alpha-trimmed mean of ranks, discarding extreme ranks before averaging.

- :class:`pyensemblefs.aggregators.rank.WinsorizedMeanRankAggregator`  
  Winsorized mean of ranks, clipping extreme ranks to alpha-quantiles.

- :class:`pyensemblefs.aggregators.rank.GeometricMeanRankAggregator`  
  Geometric mean of ranks, emphasizing consistently high positions.

- :class:`pyensemblefs.aggregators.rank.RankProductAggregator`  
  Rank-product aggregation (log-domain), where lower values correspond to
  features consistently near the top.

These correspond to the **rank-based consensus** family discussed in the
paper.

Subset-based (voting) aggregators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Defined in :mod:`pyensemblefs.aggregators.subset`, they assume that the
bootstrap outputs are **binary supports** (0/1), and aggregate them using
frequency and voting rules. They inherit from
:class:`pyensemblefs.aggregators.base.BinaryAggregator` and ultimately
produce a binary mask of selected features:

- :class:`pyensemblefs.aggregators.subset.MajorityVoteAggregator`  
  Uses selection frequencies and applies a majority threshold (e.g. 0.5);
  optionally enforces a maximum ``top_k`` by keeping the most frequent
  features.

- :class:`pyensemblefs.aggregators.subset.TopKBinaryAggregator`  
  Selects exactly ``top_k`` features with highest selection frequency.

- :class:`pyensemblefs.aggregators.subset.ThresholdAggregator`  
  Selects all features whose frequency is above a fixed threshold τ.

- :class:`pyensemblefs.aggregators.subset.QuantileThresholdAggregator`  
  Selects features whose selection frequency is above a given quantile.

- :class:`pyensemblefs.aggregators.subset.WeightedMajorityVoteAggregator`  
  Weighted voting over bootstrap supports; each bootstrap can have a
  different weight.

- :class:`pyensemblefs.aggregators.subset.FDRControlledFrequencyAggregator`  
  Uses a binomial model and Benjamini–Hochberg FDR control to select
  features with statistically significant selection frequency.

- :class:`pyensemblefs.aggregators.subset.ClopperPearsonCIThresholdAggregator`  
  Uses Clopper–Pearson confidence intervals on selection frequency to
  retain features whose lower CI bound exceeds a threshold.

These classes implement the **subset-based voting** and **FDR/CI-based**
frequency rules described in the Aggregation Methods section of the paper.

Core classes
------------

Module reference
----------------

Base classes
~~~~~~~~~~~~

.. automodule:: pyensemblefs.aggregators.base
   :members:
   :undoc-members:
   :show-inheritance:

Score-based aggregators
~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: pyensemblefs.aggregators.score
   :members:
   :undoc-members:
   :show-inheritance:

Rank-based aggregators
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: pyensemblefs.aggregators.rank
   :members:
   :undoc-members:
   :show-inheritance:

Subset / voting aggregators
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: pyensemblefs.aggregators.subset
   :members:
   :undoc-members:
   :show-inheritance:
