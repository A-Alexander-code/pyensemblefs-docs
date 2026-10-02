Recent changes
==============

This documentation was synchronized with the local library checkout through
commit ``ab14ac3`` (1 October 2026). The checkout's package configuration declares
version ``0.4.1``; the notes below identify changes by commit rather than assuming
a published release date.

1 October 2026 — Aggregator heatmap columns
------------------------------------------

``ab14ac3`` removes columns outside every aggregator's top-k from the comparison
heatmap. Columns selected by at least one aggregator remain in original order.
The input rankings are unchanged. See :doc:`tutorials/visualization_tools`.

30 September 2026 — Heatmap styling and export
---------------------------------------------

``c87fe69`` adds font settings, optional titles, adaptive tick labels, consistent
feature naming and PNG/PDF exports to both heatmaps. Both return open figure and
axes objects. Legacy filename saving remains supported. See :doc:`api/viz`.

30 September 2026 — Stability contracts
--------------------------------------

``2d2d5de`` unifies the support-matrix and subset APIs through a shared engine,
evaluates every unordered pair and validates the full feature universe.
Yu and Zucknick use new similarity-aware variants. Explicit similarity and
threshold are required; Yu additionally requires exact or estimated correction.
Undefined scores propagate by default and the cross-metric ``summary`` property
is deprecated. See :doc:`api/stability` for formulas and migration guidance.
