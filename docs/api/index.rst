API Reference
=============

The ``pyensemblefs`` API is organized into thematic modules that reflect the
core functional pillars of the library: *ensemble learning*, *feature selection
methods*, *stability analysis*, *aggregation strategies*, *computational utilities*, 
and *visualization tools*.  

This page provides a structured overview of all available Python modules and
their classes, functions, and workflows.

Navigate each category below to explore the full technical documentation.


Core Ensemble Modules
---------------------

These modules implement the high-level logic for homogeneous and
heterogeneous ensemble feature selection, including bootstrapping,
meta-bootstrapping, and the orchestration of selection workflows.

.. toctree::
   :maxdepth: 2

   ensemble


Aggregation Methods
-------------------

Aggregation rules combine feature selection results across multiple
bootstrap replicates or multiple base selectors.  
This section includes score-based, rank-based, subset-based, and ABC-vote
aggregation rules.

.. toctree::
   :maxdepth: 2

   aggregators


Feature Selection Methods (FS Methods)
--------------------------------------

These are the underlying selector classes that operate on variance, scores,
ranks, or subsets. All are compatible with ensemble pipelines and support
integration with scikit-learn workflows.

.. toctree::
   :maxdepth: 2

   fsmethods


Stability Metrics
-----------------

All stability measures implemented in ``pyensemblefs`` are documented here.
They include uncorrected, corrected, and ranking-adjusted metrics, as detailed
in the accompanying scientific manuscript.

.. toctree::
   :maxdepth: 2

   stability


Estimators & Evaluators
-----------------------

Estimators wrap ensemble selectors into scikit-learn-compatible estimators.
Evaluators implement stability assessment across multiple ensemble runs.

.. toctree::
   :maxdepth: 2

   estimators


Utility Modules
---------------

Tools for dataset loading, feature space management, plotting helpers,
and general utilities used throughout the library.

.. toctree::
   :maxdepth: 2

   utils


Visualization Tools
-------------------

Dedicated plotting functions for rankings, intersections, stability maps,
and comparison visualizations compatible with the library data structures.

.. toctree::
   :maxdepth: 2

   viz
