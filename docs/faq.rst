FAQ & Troubleshooting
=====================

This page collects frequently asked questions and common issues
when using ``pyensemblefs``.


General Usage
-------------

Why do I get different selected features on each run?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ensemble feature selection in ``pyensemblefs`` typically relies on
bootstrapping and/or stochastic base selectors (e.g., random forests).
Small perturbations in the data or random seeds can produce slightly
different selected subsets.

To improve reproducibility:

- Set ``random_state`` for selectors and bootstrapping procedures.
- Increase the number of bootstraps ``B`` to stabilize results.
- Use stability metrics (e.g. Nogueira, Jaccard) to *quantify* variability
  instead of assuming selections should be identical.


Which aggregation method should I choose?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A rough guideline:

- If your selectors output **binary subsets** (0/1 masks):

  - Start with frequency-based aggregators (e.g., selection frequency +
    threshold or top-k).
  - For stricter consensus, consider voting or ABC-based rules.

- If your selectors output **scores or importances**:

  - Use score-based aggregators (mean, median, Borda-from-scores).
  - Convert scores to ranks when comparing across heterogeneous methods.

- If your base methods produce **rankings**:

  - Use rank-based fusion (mean rank, Borda-from-ranks).
  - Consider ranking-aware stability metrics (Yu, Zucknick).


Stability Metrics
-----------------

Why does Nogueira’s stability sometimes become negative?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Nogueira index is a *chance-corrected* stability measure.  
A negative value indicates that the observed agreement between feature
subsets is worse than what would be expected by random selection under
the same average subset size.

If this happens:

- Check whether the base selectors are overly unstable or too small/large
  subsets are being forced.
- Increase the number of bootstraps.
- Consider simplifying the ensemble configuration or using more regularized
  selectors.


Which metrics should I use for subset vs ranking outputs?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- For **subset-based outputs** (0/1 masks):

  - Jaccard, Dice, Ochiai, Hamming, Nogueira, Kappa, Lustgarten, Phi.

- For **ranking-based outputs**:

  - Yu and Zucknick (optionally with a given top-k truncation).

You can combine them via :class:`pyensemblefs.stability.evaluator.StabilityEvaluator`
by selecting appropriate metric names in the ``metrics`` argument.


Why do some metrics return NaN?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some stability measures lose meaning in edge cases, for example:

- Subsets are always empty or always full.
- All runs select *exactly* the same features (no variability to measure).
- Some denominators in corrected metrics become zero.

In such cases, ``pyensemblefs`` may return ``NaN`` rather than a numeric
score to avoid misleading interpretations.

Check:

- That there is sufficient variation across runs.
- That the subset sizes are not degenerate (all-zero or all-one vectors).


Practical Issues
----------------

ImportError: no module named 'sklearn', 'pandas' or 'matplotlib'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Several parts of ``pyensemblefs`` rely on external libraries:

- Core feature selection: ``scikit-learn``, ``numpy``, ``scipy``.
- Dataset handling: ``pandas``.
- Visualization: ``matplotlib``, ``seaborn``, ``upsetplot``.

Install missing dependencies via:

.. code-block:: bash

   pip install scikit-learn pandas matplotlib seaborn upsetplot


StabilityEvaluator raises an error about input shape
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The high-level evaluator currently expects a binary **support matrix**
of shape ``(n_runs, n_features)`` when ``mode="subset"``.

Checklist:

- Ensure you are passing a 2D NumPy array.
- Ensure values are in ``{0, 1}`` (or very close).
- Make sure the number of features is consistent across runs.

For ranking-based metrics, convert rankings into subset masks or use the
ranking-aware metrics (Yu, Zucknick) with appropriate pre-processing.


How can I speed up my ensemble?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Use fewer but more informative base selectors.
- Reduce the number of bootstrap samples in exploratory runs.
- Enable multi-processing in bootstrapping components (e.g., ``n_jobs``).
- Cache intermediate results whenever possible (e.g., scores, rankings).
- Use smaller subsets of features during prototyping and scale up later.