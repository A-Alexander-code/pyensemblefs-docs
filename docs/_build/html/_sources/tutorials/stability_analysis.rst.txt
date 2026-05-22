Example: Computing Stability Across Bootstrap Replicates
--------------------------------------------------------

The following example demonstrates how to compute multiple stability
measures from repeated feature selection runs.

We simulate a scenario where a feature selector is executed over
``m`` bootstrap samples, producing either **subsets** or **rankings**.
For the ranking case, the example first converts each ranking into a
top-``k`` subset so it can be evaluated with the subset-oriented metrics
implemented in ``pyensemblefs.stability``.

.. code-block:: python

    import numpy as np
    from pyensemblefs.stability.evaluator import StabilityEvaluator

    # ---------------------------------------------------------------
    # Simulated feature-selection outputs from m bootstrap replicates
    # (For real usage, these should come from your EnsembleSelector)
    # ---------------------------------------------------------------
    m = 5               # number of runs
    p = 10              # total number of features

    # Example: subset-based outputs (indices of selected features)
    subset_outputs = [
        {0, 1, 3, 5},
        {1, 3, 4, 5},
        {0, 2, 3, 5},
        {1, 3, 5},
        {0, 1, 3, 6}
    ]

    # Convert subset outputs to binary matrix (n_runs x n_features)
    subset_matrix = np.zeros((m, p), dtype=int)
    for i, features in enumerate(subset_outputs):
        for f in features:
            if f < p:
                subset_matrix[i, f] = 1

    # ---------------------------------------------------------------
    # Compute pairwise stability for subset-based methods
    # ---------------------------------------------------------------
    evaluator_subset = StabilityEvaluator(
        metrics=["jaccard", "dice", "ochiai", "nogueira"],
        mode="subset"
    )

    results_subset = evaluator_subset.compute(subset_matrix)
    print("Subset-based stability:")
    print("  Jaccard mean:", results_subset.values.get("jaccard", "N/A"))
    print("  Dice mean:", results_subset.values.get("dice", "N/A"))
    print("  Ochiai mean:", results_subset.values.get("ochiai", "N/A"))
    print("  Nogueira (corrected) mean:", results_subset.values.get("nogueira", "N/A"))

    # ---------------------------------------------------------------
    # Compute stability on rankings after converting each ranking to a top-k subset
    # ---------------------------------------------------------------
    ranking_outputs = [
        np.array([3, 1, 5, 0, 2, 4, 6, 7, 8, 9]),
        np.array([1, 3, 5, 0, 4, 2, 6, 7, 9, 8]),
        np.array([3, 5, 1, 0, 2, 4, 7, 6, 8, 9]),
        np.array([1, 3, 0, 5, 2, 4, 6, 7, 8, 9]),
        np.array([3, 1, 5, 2, 0, 4, 6, 7, 9, 8])
    ]

    # Convert rankings to subset selections (select top k=5 features)
    k = 5
    ranking_matrix = np.zeros((m, p), dtype=int)
    for i, ranking in enumerate(ranking_outputs):
        top_k = ranking[:k]
        for f in top_k:
            if f < p:
                ranking_matrix[i, f] = 1

    evaluator_ranking = StabilityEvaluator(
        metrics=["jaccard", "dice", "ochiai", "nogueira"],
        mode="subset"
    )

    results_ranking = evaluator_ranking.compute(ranking_matrix)
    print("\nTop-k stability derived from rankings:")
    print("  Jaccard mean:", results_ranking.values.get("jaccard", "N/A"))
    print("  Dice mean:", results_ranking.values.get("dice", "N/A"))
    print("  Ochiai mean:", results_ranking.values.get("ochiai", "N/A"))
    print("  Nogueira (corrected) mean:", results_ranking.values.get("nogueira", "N/A"))

    # ---------------------------------------------------------------
    # Using the StabilityEvaluator for multiple metrics at once
    # ---------------------------------------------------------------
    evaluator = StabilityEvaluator(
        metrics=["jaccard", "dice", "nogueira"],
        mode="subset"
    )

    results = evaluator.compute(subset_matrix)
    print("\nEvaluator summary:")
    for metric, value in results.values.items():
        print(f"  {metric}: {value:.4f}")
