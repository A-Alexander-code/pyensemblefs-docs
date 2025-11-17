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

- :class:`pyensemblefs.stability.base.BaseStability` and its subclasses  
  Simple frequency-based stability scores.

- Adjusted intersection-based measures  
  (:mod:`pyensemblefs.stability.measures_adjusted_intersections`).

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
several measures and returns both individual scores and a summary.

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

Additional adjusted measures such as ``"sechidis"`` and intersection-based
indices are available via lower-level modules but are not included in
``all12`` by default.


Input format
~~~~~~~~~~~~

For the current implementation, ``mode="subset"`` is supported. The
input to :meth:`StabilityEvaluator.compute` is:

- ``results``: a NumPy array of shape ``(n_bootstraps, n_features)``,  
  containing **binary** (0/1 or near-binary) indicators whether each
  feature was selected in each run.

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
   evaluator = StabilityEvaluator(metrics="all12", mode="subset")

   result = evaluator.compute(supports)

   # Dictionary: metric_name -> score
   print(result.values)

   # Global summary (mean of all metric values, ignoring NaNs)
   print("Summary stability:", result.summary)


2. Mathematical definitions (12 core metrics)
---------------------------------------------

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
        \frac{q}{mp} \left(1 - \frac{q}{mp}\right)
     }


Adjusted / similarity-based measures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following measures incorporate additional structure via a
feature–feature similarity matrix (e.g., correlation, RBF, etc.).

They are implemented in
:mod:`pyensemblefs.stability.measures_adjusted_other` and registered
under:

- ``"yu"`` – Yu-type adjustment
- ``"zucknick"`` – Zucknick-type adjustment

and a further variant:

- ``"sechidis"`` – Sechidis-type similarity-based stability (not in
  ``all12`` by default).

All of them operate on the same list of feature subsets and optionally
use a similarity matrix ``sim_mat`` defined over the full feature
universe.


3. Frequency-based stability scores
-----------------------------------

In addition to the 12 core metrics, ``pyensemblefs.stability`` provides
simple frequency- and entropy-based summaries, implemented as subclasses
of :class:`pyensemblefs.stability.base.BaseStability`.

.. automodule:: pyensemblefs.stability.base
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: pyensemblefs.stability.frequency
   :members:
   :undoc-members:
   :show-inheritance:

Example: frequency and entropy stability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import numpy as np
   from pyensemblefs.stability.frequency import (
       SelectionFrequencyStability,
       EntropyStability,
   )

   # Same toy supports as before
   supports = np.array([
       [1, 1, 0, 0, 1, 0, 0, 0],
       [1, 0, 1, 0, 1, 0, 0, 0],
       [1, 1, 0, 0, 1, 0, 0, 0],
       [0, 1, 1, 0, 1, 0, 0, 0],
       [1, 1, 0, 0, 1, 0, 0, 0],
   ])

   freq_metric = SelectionFrequencyStability()
   ent_metric = EntropyStability()

   print("Mean selection frequency:", freq_metric.compute(supports))
   print("1 - mean entropy:",        ent_metric.compute(supports))


4. Similarity matrices and expectations
---------------------------------------

Some adjusted measures (e.g., intersection-based metrics, Yu, Zucknick)
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


5. Adjusted intersection-based measures
---------------------------------------

The module
:mod:`pyensemblefs.stability.measures_adjusted_intersections` implements
a family of intersection-based measures that combine feature subsets
through a similarity matrix and a threshold.

.. automodule:: pyensemblefs.stability.measures_adjusted_intersections
   :members:
   :undoc-members:
   :show-inheritance:

Exported metric dictionaries (stabm-like):

- ``intersection_count``
- ``intersection_mean``
- ``intersection_greedy``
- ``intersection_mbm``
- ``intersection_common``

Each object has the structure:

.. code-block:: python

   {
       "scoreFun": <callable>,
       "maxValueFun": <callable>,
   }

and is compatible with :class:`StabilityEvaluator`’s internal machinery
when registered in the metric registry.


6. Other adjusted measures (Yu, Zucknick, Sechidis)
---------------------------------------------------

The module
:mod:`pyensemblefs.stability.measures_adjusted_other` provides three
additional adjusted measures that can incorporate feature similarity:

.. automodule:: pyensemblefs.stability.measures_adjusted_other
   :members:
   :undoc-members:
   :show-inheritance:

Registered names (as used in :class:`StabilityEvaluator`):

- ``"yu"``       → Yu-type adjusted stability.
- ``"zucknick"`` → Zucknick-type adjusted stability.

and an additional:

- ``"sechidis"`` → Sechidis-type stability (available for custom use).

All three are exposed as dictionaries of the form:

.. code-block:: python

   yu = {"scoreFun": yu, "maxValueFun": ...}
   zucknick = {"scoreFun": zucknick, "maxValueFun": ...}
   sechidis = {"scoreFun": sechidis, "maxValueFun": ...}

and can be combined with expectation-based corrections to build
chance-adjusted stability indices.


Summary
-------

In practice, a typical workflow in ``pyensemblefs`` is:

1. Run an ensemble of feature selectors over :math:`B` bootstrap resamples,
   obtaining a binary matrix ``results`` of shape
   ``(B, p)`` (1 = selected feature, 0 = not selected).
2. Instantiate :class:`StabilityEvaluator` with
   ``metrics="all12"`` (or a custom list).
3. Optionally provide a feature similarity matrix via ``sim_matrix`` for
   adjusted measures (Yu, Zucknick, Sechidis, and intersection-based).
4. Call :meth:`compute` to obtain a dictionary of stability scores and a
   summary scalar.

This design mirrors the theoretical organization in the manuscript,
while keeping the implementation modular and extensible.
