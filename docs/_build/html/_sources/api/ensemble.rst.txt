Ensemble Components
===================

This section documents the ensemble-building components used by
``pyensemblefs`` to combine feature-selection methods, bootstrap
resampling and aggregation strategies.

The ensemble pipeline
---------------------

The ensemble workflow in ``pyensemblefs`` follows a simple but highly
modular structure:

.. code-block:: text

      ┌──────────────────┐
      │  Bootstrapper    │  →  produces a (B × p) matrix
      └──────────────────┘      of scores / ranks / masks
                 │
                 ▼
      ┌──────────────────┐
      │    Aggregator    │  →  combines bootstrap results
      └──────────────────┘      into final ranking/scores
                 │
                 ▼
      ┌─────────────────────────────┐
      │ EnsembleFeatureSelector     │
      └─────────────────────────────┘
                 │
                 ▼
      Selected feature subset


Homogeneous vs heterogeneous ensembles
--------------------------------------

``pyensemblefs`` supports two ensemble regimes, depending on how
feature selectors are used across bootstrap resamples:

- **Homogeneous ensembles** – a single base selector is applied on
  every bootstrap resample.
- **Heterogeneous ensembles** – multiple base selectors are distributed
  across resamples (sequentially or at random), promoting diversity.

Homogeneous ensembles (Bootstrapper)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the homogeneous case, the same feature selector :math:`f` is applied
to each of the :math:`B` bootstrap resamples:

.. code-block:: text

      Data (X, y)
           │
           ├─ bootstrap #1 ──►  f  ──►  result₁
           ├─ bootstrap #2 ──►  f  ──►  result₂
           ├─   ...
           └─ bootstrap #B ──►  f  ──►  result_B

      results_  →  stacked into a matrix R ∈ ℝ^{B×p}
                    (scores / ranks / binary supports)

      R  →  Aggregator  →  final scores / ranks / mask


This is implemented by :class:`pyensemblefs.ensemble.bootstrapper.Bootstrapper`,
which:

- draws :math:`B` bootstrap resamples of :math:`(X, y)`,
- fits the same selector on each resample,
- collects outputs into a matrix ``results_`` of shape ``(B, p)``.

Heterogeneous ensembles (MetaBootstrapper)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the heterogeneous case, a *collection* of base selectors
:math:`𝔽 = {f₁, …, f_M}` is used and distributed across bootstrap
resamples according to a scheduling strategy:

.. code-block:: text

      Data (X, y)
           │
           ├─ bootstrap #1 ──►  f₁  ──►  result₁
           ├─ bootstrap #2 ──►  f₂  ──►  result₂
           ├─ bootstrap #3 ──►  f₃  ──►  result₃
           ├─   ...
           └─ bootstrap #B ──►  f_{σ(B)} ──►  result_B

      where σ(b) encodes the scheduling strategy:
        • sequential  → f₁, f₂, …, f_M, f₁, …
        • random      → f_{σ(b)} ~ Uniform(𝔽)
        • random_weighted → f_{σ(b)} ~ Weighted(𝔽)


The heterogeneous logic is implemented by
:class:`pyensemblefs.ensemble.metabootstrapper.MetaBootstrapper`, which:

- receives a list of base selectors (filters or model-based),
- distributes them over bootstrap resamples according to a chosen strategy,
- builds three matrices when applicable:

  - ``results_``   – binary supports (subset outputs),
  - ``score_mat_`` – stacked score vectors,
  - ``rank_mat_``  – stacked rank vectors,

- records the method used at each resample in ``methods_used_``.

These matrices are then passed to aggregation and stability modules
to quantify consensus and robustness across heterogeneous FS strategies.


Modules
-------

The following classes implement the components of the ensemble pipeline.

Base Ensemble Component
------------------------

.. automodule:: pyensemblefs.ensemble.base
   :members:
   :undoc-members:
   :show-inheritance:


Bootstrapper (homogeneous)
--------------------------

The homogeneous bootstrapper applies a **single feature-selection method**
across all bootstrap iterations.

It produces:

- ``results_`` : array (B, p)  
  Binary selection masks, scores or ranks depending on the selector.

.. automodule:: pyensemblefs.ensemble.bootstrapper
   :members:
   :undoc-members:
   :show-inheritance:


MetaBootstrapper (heterogeneous)
--------------------------------

The heterogeneous bootstrapper cycles or samples from **multiple**
feature selectors, supporting strategies:

- ``sequential``
- ``random``
- ``random_weighted``

It produces:

- ``results_``   : (B, p) binary masks  
- ``score_mat_`` : (B_s, p) stacked score vectors  
- ``rank_mat_``  : (B_r, p) stacked ranking vectors  
- ``methods_used_`` : list of selector names used per bootstrap

.. automodule:: pyensemblefs.ensemble.metabootstrapper
   :members:
   :undoc-members:
   :show-inheritance:


EnsembleFeatureSelector
-----------------------

This is the “glue” component that receives a ``bootstrapper`` and an
``aggregator``, producing a final **ordered list of feature indices**.

It supports:

- ranking-based aggregators  
- score-based aggregators  
- binary input aggregators  

.. automodule:: pyensemblefs.ensemble.featureselector
   :members:
   :undoc-members:
   :show-inheritance:


Minimal example
---------------

.. code-block:: python

    from sklearn.datasets import load_breast_cancer
    from sklearn.feature_selection import SelectKBest, f_classif

    from pyensemblefs.ensemble.bootstrapper import Bootstrapper
    from pyensemblefs.ensemble.featureselector import EnsembleFeatureSelector
    from pyensemblefs.aggregators.rank import BordaFromRanksAggregator

    X, y = load_breast_cancer(return_X_y=True)

    base_fs = SelectKBest(score_func=f_classif, k=10)
    bootstrapper = Bootstrapper(fs_method=base_fs, n_bootstraps=30)

    aggregator = BordaFromRanksAggregator()

    selector = EnsembleFeatureSelector(
        bootstrapper=bootstrapper,
        aggregator=aggregator,
        k=10,
    )

    selector.fit(X, y)
    print(selector.selected_indices_)
