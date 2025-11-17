Example: Computing Stability Across Bootstrap Replicates
--------------------------------------------------------

The following example demonstrates how to compute multiple stability
measures from repeated feature selection runs.  

We simulate a scenario where a feature selector is executed over
``m`` bootstrap samples, producing either **subsets** or **rankings**.
These outputs can then be evaluated using any metric implemented in
``pyensemblefs.stability``.

.. code-block:: python

    import numpy as np
    from pyensemblefs.stability import (
        Jaccard, Dice, Ochiai, Nogueira,
        Yu, Zucknick, StabilityEvaluator
    )

    # -------------------------------------------------------------
    # Simulated feature-selection outputs from m bootstrap replicates
    # (For real usage, these should come from your EnsembleSelector)
    # -------------------------------------------------------------
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

    # Example: ranking-based outputs (full rankings)
    ranking_outputs = [
        np.array([3, 1, 5, 0, 2, 4, 6, 7, 8, 9]),
        np.array([1, 3, 5, 0, 4, 2, 6, 7, 9, 8]),
        np.array([3, 5, 1, 0, 2, 4, 7, 6, 8, 9]),
        np.array([1, 3, 0, 5, 2, 4, 6, 7, 8, 9]),
        np.array([3, 1, 5, 2, 0, 4, 6, 7, 9, 8])
    ]

    # -------------------------------------------------------------
    # Compute pairwise stability for subset-based methods
    # -------------------------------------------------------------
    jaccard = Jaccard().pairwise(subset_outputs)
    dice = Dice().pairwise(subset_outputs)
    ochiai = Ochiai().pairwise(subset_outputs)
    nogueira = Nogueira(p=p).pairwise(subset_outputs)

    print("Subset-based stability:")
    print("  Jaccard mean:", np.mean(jaccard))
    print("  Dice mean:", np.mean(dice))
    print("  Ochiai mean:", np.mean(ochiai))
    print("  Nogueira (corrected) mean:", np.mean(nogueira))

    # -------------------------------------------------------------
    # Compute pairwise stability for ranking-based methods
    # -------------------------------------------------------------
    yu = Yu(k=5).pairwise(ranking_outputs)
    zucknick = Zucknick(k=5).pairwise(ranking_outputs)

    print("\nRanking-based stability:")
    print("  Yu mean:", np.mean(yu))
    print("  Zucknick mean:", np.mean(zucknick))

    # -------------------------------------------------------------
    # Using the StabilityEvaluator for multiple metrics at once
    # -------------------------------------------------------------
    evaluator = StabilityEvaluator(
        metrics=["Jaccard", "Dice", "Nogueira"],
        p=p,
        k=5
    )

    results = evaluator.evaluate(subset_outputs)
    print("\nEvaluator summary:")
    for metric, value in results.items():
        print(f"  {metric}: {value:.4f}")
