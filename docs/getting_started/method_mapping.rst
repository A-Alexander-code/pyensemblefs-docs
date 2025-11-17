Method–Aggregator–Metric Mapping
================================

This guide summarizes how different feature selection outputs should be
combined and evaluated within the ``pyensemblefs`` ecosystem.

Instead of prescribing a single “best” configuration, it provides a
compatibility map between:

- **Selector type** (subset, ranking, score)
- **Recommended aggregation families**
- **Compatible stability metrics**


Selector Types
--------------

We distinguish three main types of selector outputs:

- **Subset selectors** – produce a binary mask :math:`s \in \{0,1\}^p`.
- **Ranking selectors** – output a permutation of feature indices.
- **Score selectors** – assign a real-valued score to each feature,
  which can be converted to ranks or subsets.


Compatibility Table
-------------------

The following table outlines typical choices for ensemble aggregation
and stability assessment, depending on selector type.

+-----------------+-------------------------+-----------------------------------+--------------------------------------+
| Selector Output | Example Methods         | Recommended Aggregators           | Typical Stability Metrics            |
+=================+=========================+===================================+======================================+
| Subset          | SubsetFilter,          | - Selection frequency             | - Jaccard, Dice, Ochiai             |
|                 | MRMRSubset, CFSSubset, | - Majority / threshold voting     | - Hamming, Novovicova, Davis        |
|                 | FCBFSubset             | - ABC voting rules (AV, SAV,      | - Lustgarten, Phi, Kappa            |
|                 |                         |   SeqPAV, Monroe, etc.)          | - Nogueira                           |
+-----------------+-------------------------+-----------------------------------+--------------------------------------+ 
| Ranking         | RankingFilter,         | - Mean / median rank              | - Yu (top-k)                         |
|                 | RankedSubsetFilter,    | - Borda from ranks                | - Zucknick (top-k)                   |
|                 | score-based wrappers   | - Rank product / geometric rank   | - Sechidis-type (similarity-based)   |
+-----------------+-------------------------+-----------------------------------+--------------------------------------+
| Score           | ScoreFilter,           | - Mean / median score             | Use subset metrics after             |
|                 | model-based importances| - Trimmed / winsorized mean       | thresholding or top-k selection      |
|                 | (e.g. RF, L1-LR)       | - Borda from scores (via ranking) | (e.g. Jaccard, Nogueira)            |
+-----------------+-------------------------+-----------------------------------+--------------------------------------+

Practical Guidelines
--------------------

- When working with **heterogeneous ensembles** (different selector families):

  - Convert outputs to a common representation before aggregation
    (e.g., all to ranks or all to binary subsets).
  - For rank-based aggregation across heterogeneous methods, Borda-type
    rules offer a robust baseline.

- To interpret **stability** in practice:

  - Start with uncorrected metrics (Jaccard, Dice) for intuition.
  - Use corrected metrics (Nogueira, Kappa, Lustgarten) when comparing
    methods with different subset sizes.
  - Use ranking-based metrics (Yu, Zucknick) when top-k order matters.

- ABC voting rules are particularly useful when:

  - You want a fixed committee size (number of features).
  - You treat feature selection as a multi-winner voting problem.
  - You wish to explore different approval-based philosophies
    (AV, SAV, SeqPAV, Phragmén, etc.).
