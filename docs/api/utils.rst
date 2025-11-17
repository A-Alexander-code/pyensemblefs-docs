Utilities
=========

The ``utils`` module provides general-purpose helper functions used across
the ``pyensemblefs`` ecosystem. These include:

- **Dataset utilities** for loading built-in demo datasets.
- **File utilities** for storing experiment results.
- **Plotting helpers** for visualizing confusion matrices.
- **Global constants** used in different modules.

This page summarizes each component and links to full API documentation.


.. contents::
   :local:
   :depth: 2


Dataset Utilities
-----------------

The module :mod:`pyensemblefs.utils.datasets` provides simple access to a
collection of small UCI-style datasets for demonstration, benchmarking, or
testing feature selectors.

Available datasets include:

- ``wine``
- ``iris``
- ``breast_cancer``
- ``glass``
- ``ionosphere``
- ``seeds``

The datasets are automatically downloaded from their original UCI repository
URLs, as defined in :mod:`pyensemblefs.utils.consts`.

**Example**

.. code-block:: python

   from pyensemblefs.utils.datasets import load_dataset

   X, y = load_dataset("wine")
   print(X.shape, y.shape)


Saving Results
--------------

The module :mod:`pyensemblefs.utils.loader` defines helper functions for
storing experiment results in a persistent CSV file.

The function ``save_dataframe_results`` automatically:

1. Creates a ``results/`` directory (if missing).  
2. Appends new experiment results to an existing file.  
3. Uses the DataFrame attribute ``df.attrs['results_name']`` as filename.

**Example**

.. code-block:: python

   import pandas as pd
   from pyensemblefs.utils.loader import save_dataframe_results

   df = pd.DataFrame({"score": [0.81, 0.79]})
   df.attrs["results_name"] = "my_experiment"

   save_dataframe_results(df)


Plotting Helpers
----------------

The module :mod:`pyensemblefs.utils.plotter` provides a simple utility for
visualizing confusion matrices using Matplotlib.

**Example**

.. code-block:: python

   import numpy as np
   from pyensemblefs.utils.plotter import plot_confusion_matrix

   cm = np.array([[50, 10],
                  [ 8, 32]])

   plot_confusion_matrix(cm, class_names=["negative", "positive"])


Global Constants
----------------

The module :mod:`pyensemblefs.utils.consts` contains:

- ``DATASET_REGISTRY`` — a dictionary mapping dataset names to their UCI URLs.
- ``PATH_PROJECT_RESULTS`` — a default output folder for experiment tracking.

These values are used internally by dataset loaders, stability metrics, and
the pipeline.

**Example**

.. code-block:: python

   from pyensemblefs.utils.consts import DATASET_REGISTRY

   print(DATASET_REGISTRY["iris"])


API Reference
-------------

Full automatic documentation for the ``utils`` package:

.. automodule:: pyensemblefs.utils
   :members:
   :undoc-members:
   :show-inheritance:
   :noindex:


Submodules
----------

.. automodule:: pyensemblefs.utils.consts
   :members:
   :show-inheritance:

.. automodule:: pyensemblefs.utils.datasets
   :members:
   :show-inheritance:

.. automodule:: pyensemblefs.utils.loader
   :members:
   :show-inheritance:

.. automodule:: pyensemblefs.utils.plotter
   :members:
   :show-inheritance:
