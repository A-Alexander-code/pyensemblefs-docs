Aggregators
===========

The :mod:`pyensemblefs.aggregators` subpackage implements multiple families of
aggregation methods that operate on bootstrap outputs (scores, ranks, or
binary supports). These correspond to the score-based, rank-based, subset-based
and approval-based (ABC) rules described in the paper.

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

Approval-based (ABC) voting aggregators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The module :mod:`pyensemblefs.aggregators.abcvote` connects ensemble feature
selection with **approval-based multi-winner voting** via the
`abcvoting <https://pypi.org/project/abcvoting/>`_ library.

In this setting:

- Each **bootstrap** (or selector run) is interpreted as a *voter*.
- Each **feature** is interpreted as a *candidate*.
- A bootstrap’s **selected features** form that voter’s *approval set*.
- An approval-based voting rule selects a *committee* of size ``top_k``,
  interpreted as the consensus feature subset.

Core classes
------------

- :class:`pyensemblefs.aggregators.abcvote._ABCBase`  
  Internal base class for ABC voting aggregators. It:
  
  - Checks that input ``results`` is a binary matrix of shape
    ``(n_bootstraps, n_features)``.
  - Builds an :class:`abcvoting.preferences.Profile` where each row’s
    approved features become the voter’s approval set.
  - Defines common scoring modes (``"av"``, ``"sav"``, ``"slav"``) used
    by ABC-based aggregators.

- :class:`pyensemblefs.aggregators.abcvote.ABCVotingRule`  
  Generic wrapper around a single `abcvoting` rule. It:

  - Receives a ``compute_func`` (e.g. ``compute_seqpav``, ``compute_cc``).
  - Chooses a **safe algorithm** using :func:`_pick_safe_algorithm`, avoiding
    Gurobi-based algorithms.
  - Computes a winning committee of size ``top_k``.
  - Returns **feature scores** based on ``score_mode``:

    - ``score_mode="av"`` → sum of approvals (Approval Voting-like).
    - ``score_mode="sav"`` → Satisfaction Approval Voting–style normalization:
      each voter distributes weight equally among approved features.
    - ``score_mode="slav"`` → same as ``"sav"`` (Shapley-like satisfaction).

  - Stores:

    - ``self._committee_`` → set of selected feature indices.
    - ``self.selected_features_`` → binary mask of the winning committee.
    - ``self.final_ranking_`` → indices sorted by decreasing score.

- :class:`pyensemblefs.aggregators.abcvote.ABCVoteAggregator`  
  High-level adapter that conforms to a simple interface:

  - Accepts ``boot_results`` as:

    - an iterable of **subsets** (feature indices or names), or
    - an iterable of **1D binary masks** of length ``n_features``.

  - Converts them into a binary matrix ``R`` using ``_to_binary_matrix``.
  - If ``top_k`` is not provided, infers a reasonable **committee size** as
    the median number of approvals per bootstrap.
  - Builds an :class:`ABCVotingRule` via :func:`make_abcvoter`.
  - Returns a :class:`pandas.DataFrame` with columns

    - ``"feature"`` – feature name
    - ``"score"`` – ABC-derived score (AV/SAV/SLAV-like)

    sorted in descending score order.

Available ABC rules in pyensemblefs
-----------------------------------

The catalogue of supported ABC rules is defined in
:data:`pyensemblefs.aggregators.abcvote.SAFE_RULES`.  
Each entry specifies:

- ``rule_id`` – identifier understood by :class:`abcvoting.abcrules.Rule`
- ``func`` – the computing function from :mod:`abcvoting.abcrules`
- ``score`` – scoring mode (``"av"``, ``"sav"``, or ``"slav"``)
- ``prefer`` – preferred algorithms (avoiding Gurobi)

The following rules are currently exposed:

- **Approval Voting family**
  
  - ``"av"``  
    Uses :func:`abcvoting.abcrules.compute_av`, scoring with raw approval
    counts (``score="av"``). Equivalent to selecting features that maximize
    total approvals.

  - ``"sav"``  
    Uses :func:`abcvoting.abcrules.compute_sav`, scoring with satisfaction
    approval voting (``score="sav"``), where each voter splits unit weight
    among approved features.

  - ``"slav"``  
    Uses :func:`abcvoting.abcrules.compute_slav`, with ``score="slav"``.
    Internally uses the same scoring implementation as SAV in this wrapper.

- **Sequential proportional rules**

  - ``"seqpav"``  
    :func:`abcvoting.abcrules.compute_seqpav`, sequential PAV-like rule with
    SAV-style scoring (``score="sav"``).

  - ``"seqslav"``  
    :func:`abcvoting.abcrules.compute_seqslav`, sequential SLAV variant.

  - ``"seqphragmen"``  
    :func:`abcvoting.abcrules.compute_seqphragmen`, sequential Phragmén rule
    with ``score="sav"``.

  - ``"seqcc"``  
    :func:`abcvoting.abcrules.compute_seqcc`, sequential Chamberlin–Courant
    with SAV scoring (``score="sav"``).

  - ``"revseqpav"``  
    :func:`abcvoting.abcrules.compute_revseqpav`, reverse sequential PAV.

- **Phragmén-type and resource-sharing rules**

  - ``"phragmen_enestroem"``  
    :func:`abcvoting.abcrules.compute_phragmen_enestroem`, Phragmén–Eneström
    rule, scored via SAV (``score="sav"``).

  - ``"equal_shares"``  
    :func:`abcvoting.abcrules.compute_equal_shares`, Equal Shares rule with
    fractional scoring (``score="sav"``).

  - ``"minimaxphragmen"``  
    :func:`abcvoting.abcrules.compute_minimaxphragmen`, minimax Phragmén rule
    with SAV scoring.

- **Proportional and fairness-oriented rules**

  - ``"rule_x"``  
    :func:`abcvoting.abcrules.compute_rule_x`, a proportional justified
    representation–oriented rule (SAV-based scoring).

  - ``"maximin_support"``  
    :func:`abcvoting.abcrules.compute_maximin_support`, maximin support rule
    focusing on fair representation with SAV scoring.

  - ``"eph"``  
    :func:`abcvoting.abcrules.compute_eph`, an egalitarian proportional heuristic
    with SAV scoring.

  - ``"rsd"``  
    :func:`abcvoting.abcrules.compute_rsd`, Random Serial Dictatorship-based
    rule with AV-style scoring (``score="av"``).

- **Classical multi-winner rules**

  - ``"pav"``  
    :func:`abcvoting.abcrules.compute_pav`, Proportional Approval Voting
    using SAV scoring (``score="sav"``).

  - ``"cc"``  
    :func:`abcvoting.abcrules.compute_cc`, Chamberlin–Courant rule, again
    with SAV-style scoring.

  - ``"monroe"``  
    :func:`abcvoting.abcrules.compute_monroe`, Monroe’s rule with SAV scoring.

  - ``"greedy_monroe"``  
    :func:`abcvoting.abcrules.compute_greedy_monroe`, a greedy approximation
    of Monroe (SAV-based scoring).

  - ``"lexcc"``  
    :func:`abcvoting.abcrules.compute_lexcc`, lexicographic Chamberlin–Courant.

  - ``"lexminimaxav"``  
    :func:`abcvoting.abcrules.compute_lexminimaxav`, lexicographic minimax AV
    rule, with AV-style scoring (``score="av"``).

- **Consensus-oriented rules**

  - ``"consensus_rule"``  
    :func:`abcvoting.abcrules.compute_consensus_rule`, a consensus-based rule
    that works with AV-style scoring.

Using ABCVoteAggregator
-----------------------

A typical workflow is:

.. code-block:: python

   from pyensemblefs.aggregators.abcvote import ABCVoteAggregator

   # boot_results: list of subsets (indices or names) or binary masks
   boot_results = [
       {"f1", "f2", "f5"},
       {"f1", "f3"},
       {"f2", "f5", "f7"},
       # ...
   ]
   feature_names = ["f1", "f2", "f3", "f4", "f5", "f6", "f7"]

   agg = ABCVoteAggregator(rule="seqpav", top_k=10)
   df = agg.aggregate(boot_results, feature_names=feature_names)

   print(df.head())

This yields a :class:`pandas.DataFrame` with features ranked by an
approval-based voting rule, giving a consensus view of which features are
most strongly supported across bootstraps and base selectors.

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

Approval-based voting (ABC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: pyensemblefs.aggregators.abcvote
   :members:
   :undoc-members:
   :show-inheritance:
