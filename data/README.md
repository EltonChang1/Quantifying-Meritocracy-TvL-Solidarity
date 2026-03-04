# Results Directory

This directory contains the output from all simulation experiments.

## Structure

- `fixed/` - Fixed solidarity rates experiment results
- `dynamic/` - Dynamic solidarity mechanisms results
- `heterogeneity/` - Agent behavioral heterogeneity results
- `timing/` - Policy timing analysis results
- `multi_dimensional/` - Multi-dimensional policies results
- `sensitivity_analysis/` - Sensitivity analysis results

Each experiment directory contains:
- `summary.json` - Numerical results in JSON format
- `{experiment_name}_analysis.png` - Visualization plots

## Viewing Results

Results can be analyzed using:

```python
import json
import matplotlib.pyplot as plt

# Load results
with open('fixed/summary.json') as f:
    results = json.load(f)

# Access data
print(f"Redistribution rates: {results['redistribution_rates']}")
print(f"Final Gini coefficients: {results['final_gini']}")
```

Or view the PNG files directly in any image viewer or notebook.
