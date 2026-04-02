"""
0/1 knapsack via dynamic programming: each ad slot is taken or not (no fractions).
State: dp[i][b] = maximum reach using a subset of the first i slots with total cost at most b.

Time complexity: O(n * B). Space complexity: O(n * B), where B is the budget in dollars.
"""

from data import single_platform_slots, adversarial_slots, SINGLE_BUDGET, ADVERSARIAL_BUDGET


def dp_01_knapsack(slots, budget):
    """
    Solve 0/1 knapsack: each slot is taken whole or not; maximize total ``reach``
    with total ``cost`` at most ``budget`` (dynamic programming, exact optimum).

    Parameters:
        slots: Slot dicts with positive integer ``cost`` and ``reach``.
        budget: Non-negative integer capacity in dollars (indexes ``0 .. budget``).

    Returns:
        Tuple ``(selected, total_reach, total_spent, dp, steps)``:
        - ``selected``: list of chosen slot dicts (subset of ``slots``).
        - ``total_reach``: optimal sum of ``reach`` (``dp[n][budget]``).
        - ``total_spent``: sum of ``cost`` over ``selected`` (≤ ``budget``).
        - ``dp``: 2D list, shape ``(n+1) x (budget+1)``, tabulated optimal reach.
        - ``steps``: per-slot rows for display, each with ``action`` ``"selected"`` or
          ``"skipped"``, plus ``cost``, ``reach``, ``budget_remaining``.
    """
    n = len(slots)
    B = budget

    dp = [[0] * (B + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = slots[i - 1]["cost"]
        reach = slots[i - 1]["reach"]
        for b in range(B + 1):
            skip = dp[i - 1][b]
            buy = dp[i - 1][b - cost] + reach if b >= cost else 0
            dp[i][b] = max(skip, buy)

    selected = []
    steps = []
    b = B
    bought = []

    for i in range(n, 0, -1):
        cost = slots[i - 1]["cost"]
        if dp[i][b] != dp[i - 1][b]:
            bought.append(i - 1)
            b -= cost

    b = B
    for i in range(n):
        slot = slots[i]
        if i in bought:
            b -= slot["cost"]
            selected.append(slot)
            steps.append({
                "slot": slot["name"],
                "action": "selected",
                "cost": slot["cost"],
                "reach": slot["reach"],
                "budget_remaining": b
            })
        else:
            steps.append({
                "slot": slot["name"],
                "action": "skipped",
                "cost": slot["cost"],
                "reach": slot["reach"],
                "budget_remaining": b
            })

    total_reach = dp[n][B]
    total_spent = sum(s["cost"] for s in selected)

    return selected, total_reach, total_spent, dp, steps


def print_results(selected, total_reach, total_spent, steps, budget):
    """
    Print the DP solution: per-slot selected/skipped lines, then totals.

    Parameters:
        Same meaning as the return values of ``dp_01_knapsack`` (except ``dp``).

    Returns:
        None (prints only).
    """
    print(f"{'Step':<5} {'Slot':<25} {'Action':<10} {'Cost':>9} {'Reach':>10} {'Budget Left':>12}")
    print("-" * 75)
    for i, s in enumerate(steps, 1):
        print(f"{i:<5} {s['slot']:<25} {s['action']:<10} "
              f"${s['cost']:>8,} {s['reach']:>10,} ${s['budget_remaining']:>11,}")
    print("-" * 75)
    print(f"\nSlots selected: {[s['name'] for s in selected]}")
    print(f"Budget used:    ${total_spent:,} / ${budget:,}")
    print(f"Total reach:    {total_reach:,}")


def greedy_01_no_fraction(slots, budget):
    """
    Heuristic 0/1 allocation: descending ``ratio``, greedily add any affordable slot.
    Not always optimal; used to contrast with ``dp_01_knapsack``.

    Parameters:
        slots: Slot dicts with ``cost``, ``reach``, ``ratio``.
        budget: Non-negative budget in dollars.

    Returns:
        Tuple ``(selected, total_reach, total_spent)``:
        - ``selected``: list of fully purchased slot dicts in greedy order.
        - ``total_reach``: sum of their ``reach`` values.
        - ``total_spent``: sum of their ``cost`` values (≤ ``budget``).
    """
    from greedy import merge_sort_by_ratio
    sorted_slots = merge_sort_by_ratio(slots)
    remaining = budget
    total_reach = 0
    selected = []
    for slot in sorted_slots:
        if slot["cost"] <= remaining:
            remaining -= slot["cost"]
            total_reach += slot["reach"]
            selected.append(slot)
    return selected, total_reach, budget - remaining


def print_comparison(slots, budget):
    """
    Side-by-side summary of 0/1 greedy versus optimal DP on one instance.

    Parameters:
        slots, budget: Same as ``greedy_01_no_fraction`` / ``dp_01_knapsack``.

    Returns:
        None (prints a small table and a one-line verdict).
    """
    _, greedy_reach, greedy_spent = greedy_01_no_fraction(slots, budget)
    _, dp_reach, dp_spent, _, _ = dp_01_knapsack(slots, budget)

    print(f"{'':.<32} {'Greedy (0/1)':>14} {'DP (0/1)':>12}")
    print(f"{'Total reach':<32} {greedy_reach:>14,} {dp_reach:>12,}")
    print(f"{'Budget spent':<32} ${greedy_spent:>13,} ${dp_spent:>11,}")
    if dp_reach > greedy_reach:
        print(f"\nDP higher reach: +{dp_reach - greedy_reach:,} vs 0/1 greedy.")
    elif greedy_reach > dp_reach:
        print(f"\n0/1 greedy higher reach: +{greedy_reach - dp_reach:,} vs DP.")
    else:
        print("\nSame total reach for both methods on this instance.")


if __name__ == "__main__":
    print("=== DP (0/1 knapsack) — single platform, $10,000 budget ===\n")
    selected, reach, spent, table, steps = dp_01_knapsack(single_platform_slots, SINGLE_BUDGET)
    print_results(selected, reach, spent, steps, SINGLE_BUDGET)

    print("\n=== DP (0/1 knapsack) — adversarial case, $10,000 budget ===\n")
    selected, reach, spent, table, steps = dp_01_knapsack(adversarial_slots, ADVERSARIAL_BUDGET)
    print_results(selected, reach, spent, steps, ADVERSARIAL_BUDGET)

    print("\n=== Comparison: 0/1 greedy vs DP (adversarial case) ===\n")
    print_comparison(adversarial_slots, ADVERSARIAL_BUDGET)
