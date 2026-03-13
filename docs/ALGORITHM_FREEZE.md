PARS Clinical Engine – Algorithm Freeze

The following algorithms are frozen and must never be modified.

Core Clinical Algorithms

1 Remission Score
2 Small Airway Index
3 PEF Variability

These algorithms represent the clinical engine of the PARS system.

Allowed future work:
- add new analytics modules
- add prediction models
- improve data input (OCR, PDF)
- improve visualization

Forbidden changes:
- modify algorithm formulas
- remove clinical indicators
- change clinical interpretation logic
- delete AI Doctor Report logic

Architecture Principle

modules/core
modules/clinical

These directories are protected layers.

All future development must occur in:

modules/input
modules/ui
modules/analytics
