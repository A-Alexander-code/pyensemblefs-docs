Introduction
============

What is pyensemblefs?
----------------------

``pyensemblefs`` is an open-source Python library for **ensemble feature selection (EFS)**.
It supports both *homogeneous* and *heterogeneous* ensembles, combining diverse feature
selection (FS) algorithms through bootstrapping, aggregation methods, and stability metrics.
The library is designed for reproducibility, parallel execution, and seamless integration with
standard machine learning workflows such as scikit-learn pipelines.

Features at a glance
--------------------

- **Homogeneous and heterogeneous ensembles** of feature selectors  
- **Bootstrap-based resampling** with deterministic scheduling strategies  
- **Ranking-, score-, and subset-based aggregation methods**  
- **Twelve stability metrics** (corrected, uncorrected, adjusted)  
- **Parallel multiprocessing** for large-scale experiments  
- **Visualization tools** for frequency, ranking, overlap, and stability patterns  
- **scikit-learn–compatible API** for integration with existing ML pipelines  

Description
-----------

``pyensemblefs`` provides a unified and modular framework for ensemble feature selection.
Users can choose among statistical filters, model-based selectors, and custom ranking
criteria, and combine their outputs through robust aggregation techniques. Stability measures
offer insight into selection robustness under perturbations, while visualization utilities enable
analysis of feature relevance, consensus, and agreement structures.

The library follows a modular architecture:

- **Ensemble module**: manages resampling and execution of base selectors  
- **Selectors**: filter-based and model-based FS methods through a unified interface  
- **Aggregators**: pooling strategies for scores, ranks, and binary masks  
- **Stability**: metrics to quantify agreement across bootstrap iterations  
- **Visualizer**: utilities for feature-selection interpretability  
- **Utils**: helper functions for preprocessing, formatting, and score management  
- **scikit-learn compatibility**: seamless integration with classifiers and pipelines  

Installation
------------

Requirements
~~~~~~~~~~~~
- Python 3.9 or higher  
- Virtual environment recommended (``venv`` or ``conda``)

Install from repository (development mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/USER/pyensemblefs.git
   cd pyensemblefs
   python -m venv .venv
   source .venv/bin/activate      # On Windows: .venv\\Scripts\\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install -e .

(Optional) Install from PyPI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If published to PyPI, installation becomes:

.. code-block:: bash

   pip install pyensemblefs

Quick check
~~~~~~~~~~~

To verify that the package and its internal modules load correctly:

.. code-block:: python

   from pyensemblefs.ensemble.featureselector import FeatureSelector

   selector = FeatureSelector(method="variance", k=5)
   print(selector)

Optional dependencies
~~~~~~~~~~~~~~~~~~~~~

For visualization, evaluation, and extended functionality:

- Visualization: ``matplotlib``, ``seaborn``, ``upsetplot``  
- ML utilities: ``scikit-learn``, ``joblib``, ``pandas``

.. code-block:: bash

   pip install matplotlib seaborn upsetplot scikit-learn joblib pandas

Core Design Philosophy
----------------------

The design of ``pyensemblefs`` is guided by four main principles:

Modularity
~~~~~~~~~~

Each component of the library has a clearly delimited responsibility:

- **FS methods** (``fsmethods``) implement individual selection rules.
- **Ensemble modules** (``ensemble``) orchestrate bootstrapping and the
  combination of multiple base selectors.
- **Aggregators** (``aggregators``) define how to fuse scores, ranks or
  subsets across runs.
- **Stability metrics** (``stability``) quantify robustness under
  perturbations.
- **Visualization tools** (``viz``) provide interpretable diagnostics.

This modularity makes it straightforward to replace, extend or combine
parts of the system without breaking others.

Homogeneous and Heterogeneous Ensembles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pyensemblefs`` explicitly supports:

- **Homogeneous ensembles**, where a single FS method is applied across
  all bootstrap replicates.
- **Heterogeneous ensembles**, where multiple FS methods, possibly based
  on different inductive biases, are combined within the same ensemble.

This distinction is central to the library: it allows practitioners to
explore how diversity among selectors impacts stability and predictive
performance.

Bootstrapping as a First-Class Citizen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of treating resampling as an afterthought, ``pyensemblefs``
places bootstrapping at the core of its design. Bootstraps are used to:

- Probe the sensitivity of feature selectors to sampling variation.
- Generate multiple supports or rankings for aggregation.
- Provide the raw material needed for stability metrics.

This makes ensemble feature selection not only a way to improve
predictive performance, but also a framework to *measure* and
*understand* robustness.

Separation of Selection, Aggregation and Evaluation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The library clearly separates three stages:

1. **Selection** – base methods produce subsets, scores or rankings.
2. **Aggregation** – ensemble rules fuse these outputs into a consensus.
3. **Evaluation** – stability metrics and downstream classifiers assess
   the quality and robustness of the selected features.

This separation avoids mixing concerns, facilitates benchmarking and
aligns the implementation with the structure of the accompanying
scientific manuscript.