Feature Selection Methods
=========================

The module ``pyensemblefs.fsmethods`` implements *stand–alone feature
selection algorithms* that can be used directly or combined with the
ensemble mechanisms provided in :mod:`pyensemblefs.ensemble`.

All methods inherit from :class:`pyensemblefs.fsmethods.basefs.FSMethod`,
which standardizes:

- ``selected_features_`` – binary mask  
- ``ranking_`` – rank array (1 = most important)  
- ``feature_importances_`` – raw relevance scores  
- ``target_type`` – ``"classification"`` or ``"regression"``  


Classification of Methods
-------------------------

``pyensemblefs`` organizes feature selection algorithms into three
functional groups:

- **Subset filters** → directly output a *set* of selected features.  
- **Ranking filters** → produce a *full ordering* of features.  
- **Score-based filters** → compute a scoring function, which is then
  converted into a ranking or subset.

This structure mirrors the taxonomy used in the scientific manuscript,
allowing consistent aggregation and stability analysis across methods.


.. contents::
   :local:
   :depth: 2


Subset Methods
--------------

Subset-based methods return a binary mask indicating which features
belong to the selected subset.

SubsetFilter
~~~~~~~~~~~~

Rule-based subset selector.

**Key parameters**:
- ``rule={"variance"}``
- ``k`` – number of features to select  
- ``threshold`` – minimum variance (when ``k`` is not specified)

**Typical use**:
.. code-block:: python

   from pyensemblefs.fsmethods import SubsetFilter
   fs = SubsetFilter(rule="variance", k=10)
   fs.fit(X, y)


MRMRSubset
~~~~~~~~~~

Minimum Redundancy – Maximum Relevance (mRMR) selector.

**Characteristics**:
- Relevance: mutual information (MI)
- Redundancy: MI-based or correlation-based
- Greedy forward selection

**Parameters**:
- ``k`` – number of features  
- ``redundancy={"mi","corr"}``
- ``discrete_features`` – handling of categorical variables

**Example**:
.. code-block:: python

   from pyensemblefs.fsmethods import MRMRSubset
   fs = MRMRSubset(k=8, redundancy="mi")
   fs.fit(X, y)


CFSSubset
~~~~~~~~~

Correlation-based Feature Selection (CFS).

**Merit function**:
- Maximize relevance to target
- Minimize redundancy among selected features

**Example**:
.. code-block:: python

   from pyensemblefs.fsmethods import CFSSubset
   fs = CFSSubset(k=12)
   fs.fit(X, y)


FCBFSubset
~~~~~~~~~~

Fast Correlation-Based Filter (FCBF).

**Procedure**:
1. Discretize features (quantile-based binning).  
2. Compute Symmetrical Uncertainty (SU) w.r.t. the target.  
3. Eliminate redundant features based on SU thresholds.

**Parameters**:
- ``delta`` – minimum SU  
- ``n_bins`` – discretization bins  
- ``k`` – optional maximum number of features  

**Example**:
.. code-block:: python

   from pyensemblefs.fsmethods import FCBFSubset
   fs = FCBFSubset(delta=0.05, n_bins=5)
   fs.fit(X, y)


Ranking Methods
---------------

Ranking-based methods return a complete ordering of features.

RankingFilter
~~~~~~~~~~~~~

Generic ranking selector used internally by score-based and simple ranking rules.

Provided scorers include:
- ``"variance"``  
- custom scorers implemented by the user

Used as:

.. code-block:: python

   from pyensemblefs.fsmethods import RankingFilter
   fs = RankingFilter(scorer="variance")
   fs.fit(X)


VarianceRanking (Deprecated)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Compatibility wrapper.

Equivalent to:

.. code-block:: python

   RankingFilter(scorer="variance")

Included for backward compatibility only.


Score-Based Methods
-------------------

Score-based methods compute a relevance score and then convert it to a
ranking.

ScoreFilter
~~~~~~~~~~~

Base class for score-to-ranking conversion.

Primarily intended for:
- scoring functions producing continuous values  
- methods wishing to override ``compute_scores()``  

Custom usage example:

.. code-block:: python

   class MyScorer(ScoreFilter):
       def compute_scores(self, X, y):
           return X.var(axis=0)

   fs = MyScorer()
   fs.fit(X, y)


API Reference
-------------

.. automodule:: pyensemblefs.fsmethods
   :members:
   :undoc-members:
   :show-inheritance:
