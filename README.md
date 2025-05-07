# Causal Inference - Covariate Selection and Back-Door Criterion

## Project Overview

This project demonstrates the process of **covariate selection** for causal inference, specifically using the **back-door criterion** introduced by Judea Pearl. The goal of this project is to identify the minimal sufficient sets of covariates required to adjust for in order to make unbiased causal estimates. 

We will be using the **disjunctive cause criterion** by **VanderWeele**, which suggests that we should include covariates that are either:

- Causes of the treatment/exposure,
- Causes of the outcome/response, or
- Common causes of both the treatment and outcome (i.e., confounders).

The project is based on the **back-door criterion**, which ensures that we identify the correct variables for adjustment to avoid bias in causal inference.

## Key Concepts

1. **Back-Door Criterion**: A set of covariates is sufficient for adjustment if it blocks all back-door paths from the treatment (X) to the outcome (Y) and contains no descendants of the treatment variable (X).

2. **Disjunctive Cause Criterion (VanderWeele)**: This criterion helps identify the relevant covariates to include in the model by considering variables that are causes of the treatment, the outcome, or both.

3. **Covariate Selection**: The process of choosing which variables to control for to prevent confounding and estimate the causal effect correctly. This is a critical part of causal inference in observational studies.

## Approach

1. **Data Representation**: 
   - A causal graph (DAG) is represented using an adjacency matrix.
   - Nodes represent variables (e.g., treatment, outcome, and covariates).
   - Directed edges represent causal relationships between variables.

2. **Algorithm**:
   - **Step 1**: Use **Breadth-First Search (BFS)** to identify all possible paths between the treatment and the outcome.
   - **Step 2**: Check each path to see if it is blocked by any covariates (i.e., if conditioning on those covariates would block the back-door paths).
   - **Step 3**: Ensure that the selected covariates do not contain descendants of the treatment variable.
   - **Step 4**: Identify the **minimal sufficient sets** of covariates that meet these criteria.

3. **Minimal Sets**: 
   - A minimal sufficient set is one where no smaller subset of the covariates can block all back-door paths.
   - The algorithm will output a list of such minimal sets for further analysis.

## Requirements

- Python 3.x
- Libraries:
   - collections (for BFS queue)
   - itertools (for generating subsets)

## Usage

1. Define the adjacency matrix representing your causal graph. For example:

```python
adj_matrix = np.array([
    [0, 1, 0, 0],  # X -> Y
    [0, 0, 1, 0],  # W1 -> X
    [0, 0, 0, 1],  # W2 -> Y
    [0, 0, 0, 0]   # No other connections
])

2. Run the main function to find the minimal adjustment sets:
if __name__ == "__main__":
    find_adjustment_sets()

3. The output will display the minimal adjustment sets that are necessary for unbiased causal estimation.
