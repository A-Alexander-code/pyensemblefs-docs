Stability Metrics
=================

The ``pyensemblefs.stability`` subpackage implements a collection of
stability measures and helper tools to quantify how robust feature
selection results are under data perturbations (e.g., bootstrapping)
and across different base selectors.

At a high level, the components are:

- :class:`pyensemblefs.stability.evaluator.StabilityEvaluator`
  High-level entry point to compute a set of stability metrics from
  bootstrap feature-selection results.

- Adjusted similarity-aware measures
  (:mod:`pyensemblefs.stability.measures_adjusted_other`).

- Expectation and correction utilities
  (:mod:`pyensemblefs.stability.expectations`, :mod:`pyensemblefs.stability.config`).

All functions are designed to operate on **collections of feature subsets**
(e.g., one subset per bootstrap resample) and, optionally, a feature–feature
similarity matrix.


.. contents::
   :local:
   :depth: 2


1. High-level interface: StabilityEvaluator
-------------------------------------------

The main user-facing class is
:class:`pyensemblefs.stability.evaluator.StabilityEvaluator`. It aggregates
several measures and returns per-metric scores and execution metadata.

.. automodule:: pyensemblefs.stability.evaluator
   :members: StabilityEvaluator, StabilityResult
   :undoc-members:
   :show-inheritance:

Supported metric names
~~~~~~~~~~~~~~~~~~~~~~

Internally, :class:`StabilityEvaluator` maintains a registry of metric
names and their implementations:

- **Uncorrected**:

  - ``"jaccard"`` – Jaccard index
  - ``"dice"`` – Dice coefficient
  - ``"ochiai"`` – Ochiai index
  - ``"hamming"`` – Hamming-based stability
  - ``"novovicova"`` – Novovicova entropy-based stability
  - ``"davis"`` – Davis stability

- **Corrected for chance**:

  - ``"lustgarten"`` – Lustgarten’s corrected similarity
  - ``"phi"`` – Phi coefficient
  - ``"kappa"`` – Cohen’s kappa–style stability
  - ``"nogueira"`` – Nogueira’s unbiased stability index

- **Adjusted / similarity-based**:

  - ``"yu"`` – Yu-type adjusted similarity
  - ``"zucknick"`` – Zucknick-type adjusted similarity

The convenience string ``metrics="all12"`` expands to all of the above:

.. code-block:: python

   [
       "jaccard", "dice", "ochiai", "hamming", "novovicova", "davis",
       "lustgarten", "phi", "kappa", "nogueira", "yu", "zucknick",
   ]

These are the 12 stability metrics currently exposed in the public
high-level evaluator interface.


Input format
~~~~~~~~~~~~

For the current implementation, ``mode="subset"`` is supported. The
input to :meth:`StabilityEvaluator.compute` is:

- ``results``: a dense NumPy array or SciPy sparse matrix of shape ``(n_bootstraps, n_features)``,
  containing **binary** (boolean or exactly 0/1) indicators whether each
  feature was selected in each run.

At least two runs and one feature are required. Repeated rows are retained.
Optional ``feature_names`` must identify every column in its existing order.
Internally, this is converted to a list of feature-index sets, one per run.


Example: computing all12 stability metrics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   from pyensemblefs.stability.evaluator import StabilityEvaluator

   # Toy example: 5 runs, 8 features
   # Each row is a binary mask: 1 = feature selected in that run
   supports = np.array([
       [1, 1, 0, 0, 1, 0, 0, 0],
       [1, 0, 1, 0, 1, 0, 0, 0],
       [1, 1, 0, 0, 1, 0, 0, 0],
       [0, 1, 1, 0, 1, 0, 0, 0],
       [1, 1, 0, 0, 1, 0, 0, 0],
   ])

   # Create evaluator with the 12 metrics described in the manuscript
   evaluator = StabilityEvaluator(
       metrics="all12", mode="subset",
       sim_matrix=np.eye(supports.shape[1]), threshold=0.7,
       correction_for_chance={"yu": "exact"},
   )

   result = evaluator.compute(supports)

   # Dictionary: metric_name -> score
   print(result.values)

   # Execution details for the selected variant and null model
   print(result.metadata["yu"])


2. Mathematical definitions (12 supported metrics)
--------------------------------------------------

This section summarizes the 12 stability measures described in the
pyensemblefs manuscript. All of them are implemented and accessible via
:class:`StabilityEvaluator`.

Uncorrected measures
~~~~~~~~~~~~~~~~~~~~

Let :math:`V_i` and :math:`V_j` denote two sets of selected features,
and :math:`p` the total number of features.

- **Jaccard** (``"jaccard"``):

  .. math::

     J(V_i, V_j) = \frac{|V_i \cap V_j|}{|V_i \cup V_j|}

- **Dice** (``"dice"``):

  .. math::

     D(V_i, V_j) = \frac{2 |V_i \cap V_j|}{|V_i| + |V_j|}

- **Ochiai** (``"ochiai"``):

  .. math::

     O(V_i, V_j) = \frac{|V_i \cap V_j|}{\sqrt{|V_i| \, |V_j|}}

- **Hamming-based stability** (``"hamming"``):

  .. math::

     H(V_i, V_j) = \frac{|V_i^c \cap V_j^c| + |V_i \cap V_j|}{p}

- **Novovicova** (``"novovicova"``):
  entropy-based stability using feature selection frequencies
  :math:`h_j` over :math:`m` runs,

  .. math::

     S_{\text{Nov}} =
     \frac{1}{q \log_2 m}
     \sum_{j \in V} h_j \log_2(h_j)

- **Davis** (``"davis"``):
  penalized stability correcting for expected overlap, controlled by a
  penalty parameter (exposed in :class:`StabilityEvaluator` as
  ``penalty``):

  .. math::

     S_{\text{Davis}} =
       \max \left\{ 0,\
       \frac{1}{|V|} \sum_{j=1}^p \frac{h_j}{m}
       - \frac{\mathrm{penalty}}{p}
         \cdot \mathrm{median}(|V_1|,\ldots,|V_m|)
       \right\}


Corrected-for-chance measures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following indices explicitly adjust for agreement expected by chance.

- **Lustgarten** (``"lustgarten"``):

  .. math::

     S_L =
     \frac{|V_i \cap V_j| - \frac{|V_i| |V_j|}{p}}
          {\min(|V_i|, |V_j|) - \max(0, |V_i| + |V_j| - p)}

- **Phi coefficient** (``"phi"``):

  .. math::

     \Phi =
     \frac{|V_i \cap V_j| - \frac{|V_i| |V_j|}{p}}
          {\sqrt{
              |V_i|
              \left(1 - \frac{|V_i|}{p}\right)
              |V_j|
              \left(1 - \frac{|V_j|}{p}\right)
          }}

- **Kappa** (``"kappa"``):

  .. math::

     \kappa =
     \frac{|V_i \cap V_j| - \frac{|V_i| |V_j|}{p}}
          {\frac{|V_i| + |V_j|}{2} - \frac{|V_i| |V_j|}{p}}

- **Nogueira** (``"nogueira"``):
  unbiased stability index based on feature selection frequencies
  :math:`h_j`:

  .. math::

     S_{\text{Nog}} =
     1 -
     \frac{
        \sum_j
        \frac{m}{m-1}
        \frac{h_j}{m}
        \left(1 - \frac{h_j}{m}\right)
     }{
        p \frac{q}{mp} \left(1 - \frac{q}{mp}\right)
     }


Adjusted / similarity-based measures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both metrics require an explicitly supplied similarity matrix and
``0 < threshold <= 1``. Equality is retained when thresholding.
The implemented variants are ``stabm-1.2.2-adaptation-yu`` and
``stabm-1.2.2-adaptation-zucknick``; they are adaptations rather than literal
reproductions of the original papers.

For sets :math:`A, B`, write :math:`a=|A|`, :math:`b=|B|`,
:math:`r=|A\cap B|` and let :math:`S` be the fixed similarity matrix.

**Yu** counts members of :math:`A\setminus B` represented by at least one
member of :math:`B\setminus A` with similarity at least the threshold;
call this count :math:`O_{AB}` and define :math:`O_{BA}` symmetrically.

.. math::

   I = r + (O_{AB}+O_{BA})/2, \qquad
   S_{Yu} = \frac{I-E[I]}{(a+b)/2-E[I]}

Select ``exact`` or ``estimate`` correction explicitly. Higher corrected
values indicate greater stability; negative values are possible. The old
matching-based dissimilarity is no longer the Yu implementation.

**Zucknick** uses

.. math::

   C(A,B) = \frac{1}{b}
     \sum_{x\in A,\ y\in B\setminus A,\ S_{xy}\ge t} S_{xy},
   \qquad S_Z = \frac{r+C(A,B)+C(B,A)}{|A\cup B|}.

Its default is no additional correction; ``exact`` or ``estimate`` is optional.
Uncorrected scores lie in [0,1]. Both metrics support unequal cardinalities
and return NaN when either subset is empty.


3. Similarity matrices and expectations
---------------------------------------

Some adjusted measures (e.g., Yu and Zucknick)
can take advantage of a feature–feature similarity matrix.

The following helpers build and normalize similarity matrices:

.. automodule:: pyensemblefs.stability.helpers
   :members:
   :undoc-members:
   :show-inheritance:

Key utilities:

- :func:`build_similarity`
  builds identities, correlation-based, absolute-correlation, or RBF
  similarity matrices from data.

- :func:`build_exponential_similarity_from_labels`
  builds an exponential-decay similarity matrix based on ordered labels
  (e.g., time, position, or feature index).

Expectation-based corrections and Monte Carlo estimation are implemented
in:

.. automodule:: pyensemblefs.stability.expectations
   :members:
   :undoc-members:
   :show-inheritance:

Configuration defaults for adjusted measures (e.g., choice between
exact expectation vs. Monte Carlo, thresholds, etc.) are collected in:

.. automodule:: pyensemblefs.stability.config
   :members:
   :undoc-members:
   :show-inheritance:


4. Adjusted similarity-based measures (Yu, Zucknick)
----------------------------------------------------

The module
:mod:`pyensemblefs.stability.measures_adjusted_other` provides the two
additional adjusted measures that can incorporate feature similarity:

.. automodule:: pyensemblefs.stability.measures_adjusted_other
   :members:
   :undoc-members:
   :show-inheritance:

Registered names (as used in :class:`StabilityEvaluator`):

- ``"yu"``       → Yu-type adjusted stability.
- ``"zucknick"`` → Zucknick-type adjusted stability.

The low-level dictionaries expose the raw statistic through ``scoreFun``.
For Yu, this raw statistic is I, not the public corrected score. Use the
high-level evaluator or subset API for correction, validation and aggregation.

Execution contracts and migration
---------------------------------

Pairwise metrics evaluate every unordered pair once, excluding the diagonal
and retaining repeated runs. Davis, Novovicova and Nogueira evaluate the whole
collection once. For example, supports selecting ``{0}, {0}, {1}`` from four
features give mean Jaccard 1/3 rather than the first-pair value 1.

Both public APIs share a registry and computation engine. Beyond ``all12``,
the registry exposes ``somol``, ``wald``, ``sechidis`` and
``intersection.common/count/mean/greedy/mbm``. ``phi.coefficient`` and
``kappa.coefficient`` are aliases; evaluator keys retain the requested spelling.

Correction and undefined values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generic chance correction is applied independently to each pair before
averaging: ``(score - expected) / (reference - expected)``. The reference is
1 except for Yu, which uses mean pair cardinality. The null draws independent
uniform subsets conditional on each observed pair's cardinalities, keeping
similarity fixed.

- ``exact`` enumerates the conditional spaces. ``exact_limit`` defaults to
  1,000,000 score evaluations per metric call; exceeding it raises an error
  without falling back to Monte Carlo.
- ``estimate`` draws ``N`` samples per pair. Yu and corrected Zucknick require
  an explicit positive integer ``N``. Other correctable metrics default to 500.
- ``seed`` is a nonnegative integer; alternatively pass a NumPy ``Generator``
  as ``rng``. They are mutually exclusive. A generator consumes its state.
- Additional correction is rejected for already corrected metrics and for
  Davis, Novovicova, Sechidis and ``intersection.common``.

An undefined correction denominator yields NaN. ``nan_policy="propagate"``
is the default; ``"omit"`` averages valid values and ``"raise"`` rejects
undefined scores. Finite ``impute_na`` replaces NaNs before aggregation.

Similarity validation
~~~~~~~~~~~~~~~~~~~~~

Supplied matrices must have shape ``(p, p)``, finite real values in [0,1],
and symmetry within ``atol=1e-12, rtol=0``. Dense and SciPy sparse formats
are accepted; duplicate stored sparse coordinates are rejected. Validation
preserves values and the diagonal without clipping or normalization.
Neither positive semidefiniteness nor a unit diagonal is required.

Yu additionally requires an exactly symmetric threshold relation
``S >= threshold``. Small asymmetries straddling the threshold raise an error.
Identity similarity is allowed when explicitly supplied.
``build_similarity(X, mode="abs-corr")`` constructs absolute Pearson
similarity from sample-by-feature data; this is separate from validation.
Undefined correlations become zero; construction symmetrizes and clips.

Subset API and reproducible estimation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pyensemblefs.stability import stability

   details = stability(
       features=[[0], [0], [1, 2]], measure="yu",
       p=4, index_base=0, sim_mat=np.eye(4), threshold=0.7,
       correction_for_chance="estimate", N=1000, seed=42,
       penalty=1.0, return_details=True,
   )
   print(details.value, details.metadata)

The subset API requires the full universe through ``p``, ``sim_labels`` or
similarity size; the selected union never defines it. Numeric identifiers
default to 1..p; use ``index_base=0`` for 0..p-1. Explicit labels override
numeric indexing. Unknown identifiers and duplicate labels or subset entries
raise errors. The evaluator defaults to ``penalty=1.0`` whereas the subset
API defaults to ``penalty=None`` (zero); pass the same penalty when comparing.

``StabilityResult.values`` is the per-metric result and ``metadata`` records
execution details. ``summary`` is a deprecated, read-only historical mean
across heterogeneous metrics and warns on access. It is not a scientific
stability measure. Construct results as ``StabilityResult(values, metadata=...)``.

Historical Yu/Zucknick values must be recomputed before comparison with these
variants. ``all12`` requires explicit similarity, threshold and Yu correction.
For CLI usage, ``pyefs-stab`` defaults Yu/Zucknick to subsets; rankings require
``--input-format rankings --topk K``. Options include ``--seed``,
``--nan-policy``, ``--index-base`` and ``--exact-limit``; Yu requires
``--correction-for-chance exact|estimate``.
