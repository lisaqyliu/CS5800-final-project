# CS5800 Final Project: Ad Placement & Budget Allocation

This repository documents **Part 1 (Qingyang Liu)** and **Part 2 (Siyang Li)** of the project:

- Fractional knapsack with a **Greedy** algorithm
- 0/1 knapsack with **Dynamic Programming (DP)**
- Multi-platform allocation using a **Max-Heap (priority queue)**
- Side-by-side comparison showing where greedy fails for 0/1
- Synthetic datasets and test cases

This README summarizes the completed implementation and current project status.


## What Part 1 Includes

### 1) Shared data model and datasets (`data.py`)

Main helper:

- `make_slot(name, platform, cost, reach)`  
  Returns a slot dictionary with:
  - `name`
  - `platform`
  - `cost`
  - `reach`
  - `ratio` (precomputed as `reach / cost`)

Datasets/constants:

- `single_platform_slots`
- `SINGLE_BUDGET`
- `multi_platform_slots`
- `MULTI_BUDGET`
- `adversarial_slots`
- `ADVERSARIAL_BUDGET`

Utility:

- `print_slots(slots)` for readable console output.

---

### 2) Fractional Greedy implementation (`greedy.py`)

Core functions:

- `merge_sort_by_ratio(slots)`  
  Custom merge sort, descending by `ratio`.

- `greedy_fractional(slots, budget)`  
  Fractional knapsack solver.
  - If a slot fits, buys 100%
  - Otherwise buys a fraction of remaining budget
  - Returns:
    - `selected` list of `(slot, fraction)`
    - `total_reach`
    - `total_spent`
    - `steps` (decision log for display/visualization)

- `print_results(selected, total_reach, total_spent, steps, budget)`  
  Pretty prints greedy run details.

---

### 3) 0/1 DP implementation (`dp.py`)

Core functions:

- `dp_01_knapsack(slots, budget)`  
  Bottom-up DP with 2D table.
  - Builds `dp[i][b]` = max reach using first `i` slots and budget `b`
  - Backtracks to recover selected slots
  - Returns:
    - `selected`
    - `total_reach`
    - `total_spent`
    - `dp` table
    - `steps` (selected/skipped decisions)

- `greedy_01_no_fraction(slots, budget)`  
  0/1 greedy baseline (same ratio ordering, no fractional purchase).
  Used to compare against DP fairly.

- `print_comparison(slots, budget)`  
  Prints reach/spend comparison between 0/1 greedy and 0/1 DP.

- `print_results(...)`  
  Pretty prints DP decisions and final selection.

---

### 4) Test coverage (`tests.py`)

One command (`python3 tests.py`) runs checks grouped by area:

- **`make_slot`** — slot dict and `ratio` field
- **`merge_sort_by_ratio`** — descending order by reach/cost
- **`greedy_fractional`** — fractional knapsack (including `data.py` single- and multi-platform lists)
- **`greedy_01_no_fraction` vs `dp_01_knapsack`** — same edge cases as before (normal, adversarial, exact fit, single slot, empty, zero budget, equal ratios)
- **Invariants** — on adversarial data, DP beats 0/1 greedy; fractional reach is at least DP reach on that example

Current status: all checks pass.

## How to Run

From project root:

- Run tests:  
  `python3 tests.py`

- Run greedy demo (fractional):  
  `python3 greedy.py`

- Run DP demo + greedy-vs-DP comparison:  
  `python3 dp.py`

## Complexity (Part 1)

Let \(n\) be the number of ad slots and \(B\) be the budget (in whole dollars, since the DP table indexes budgets \(0..B\)).

- **Fractional greedy (`greedy.greedy_fractional`)**: time \(O(n \log n)\) (merge sort) + \(O(n)\) selection, space \(O(n)\) (merge sort + output logs).
- **0/1 DP (`dp.dp_01_knapsack`)**: time \(O(nB)\), space \(O(nB)\) for the DP table (plus \(O(n)\) for traceback).
- **0/1 greedy baseline (`dp.greedy_01_no_fraction`)**: time \(O(n \log n)\), space \(O(n)\).

## Key Functions Used in Part 1

- Sorting by ratio: `greedy.merge_sort_by_ratio`
- Fractional single-platform allocation: `greedy.greedy_fractional`
- 0/1 optimal single-platform allocation: `dp.dp_01_knapsack`
- 0/1 greedy baseline for comparison: `dp.greedy_01_no_fraction`
- Shared slot constructor/datasets: `data.make_slot`, constants/lists in `data.py`

## Notes for Consistency

- Slot dictionaries are assumed to contain precomputed `ratio`.
- Existing algorithms expect `cost` and `reach` to be numeric and budgets to be integer dollar units.
- If adding new datasets, use `make_slot(...)` to keep field format consistent.

---

## Part 2 (Siyang Li): Multi-platform Allocation

This part extends the problem from a single platform to a multi-platform setting (e.g., Google, Meta, TikTok) with a shared global budget.

### Approach

We use a max-heap (priority queue) to always select the ad slot with the highest reach-per-dollar ratio across all platforms.

At each step:
- Select the highest ratio slot
- If it fits within the remaining budget, purchase it
- Otherwise, skip it
- Continue until the budget is exhausted

### Key Idea

Instead of optimizing each platform independently, we treat all ad slots as a unified pool and perform global greedy selection.

### Implementation

- File: `heap_multi.py`
- Core method: max-heap based greedy selection
- Input: `multi_platform_slots`, `MULTI_BUDGET`
- Output: selected slots, total reach, total spend, and platform breakdown

### Usage

To run the multi-platform allocation demo (Part 2):

```bash
python3 heap_multi.py
```

### Example

Suppose we have the following ad slots across platforms:

- Google: Search ad (ratio = 40)
- TikTok: TopView ad (ratio = 37.5)
- Meta: Branded effect (ratio = 33.3)

With a fixed budget, the algorithm will:

1. First select the Search ad (highest ratio)
2. Then select the TopView ad
3. Continue selecting the next best option that fits the remaining budget

This demonstrates how the max-heap always ensures we pick the globally optimal next step.
