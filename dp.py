# ─────────────────────────────────────────
#  DP Algorithm — 0/1 Knapsack
#
#  Idea: build a 2D table where
#    dp[i][b] = max reach using the first
#               i slots with budget b
#
#  For each slot i and each budget b:
#    - skip it:  dp[i][b] = dp[i-1][b]
#    - buy it:   dp[i][b] = dp[i-1][b - cost] + reach
#    - take the better option of the two
#
#  After filling the table, trace back to
#  find exactly which slots were selected.
#
#  Time complexity:  O(N x B)
#  Space complexity: O(N x B)
# ─────────────────────────────────────────

from data import single_platform_slots, adversarial_slots, SINGLE_BUDGET, ADVERSARIAL_BUDGET


def dp_01_knapsack(slots, budget):
    """
    0/1 Knapsack DP algorithm.

    Input:
        slots  : list of ad slot dictionaries
        budget : total budget available (dollars)

    Output:
        selected     : list of chosen slot dictionaries
        total_reach  : maximum audience reach achievable
        total_spent  : total budget spent
        table        : full DP table (for visualization)
        steps        : log of traceback decisions (for visualization)
    """
    n = len(slots)
    B = budget

    # build the DP table — rows = slots (0..n), cols = budget (0..B)
    dp = [[0] * (B + 1) for _ in range(n + 1)]

    # fill the table bottom-up
    for i in range(1, n + 1):
        cost  = slots[i - 1]["cost"]
        reach = slots[i - 1]["reach"]
        for b in range(B + 1):
            # option 1: skip this slot
            skip = dp[i - 1][b]
            # option 2: buy this slot (only if we can afford it)
            buy = dp[i - 1][b - cost] + reach if b >= cost else 0
            dp[i][b] = max(skip, buy)

    selected = []
    steps = []
    b = B
    budget_forward = B  # track budget forward for display purposes
    bought = []

    for i in range(n, 0, -1):
        cost  = slots[i - 1]["cost"]
        reach = slots[i - 1]["reach"]
        if dp[i][b] != dp[i - 1][b]:
            bought.append(i - 1)
            b -= cost

    # replay forward for clean step display
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


# ─────────────────────────────────────────
#  Helper — print results
# ─────────────────────────────────────────
def print_results(selected, total_reach, total_spent, steps, budget):
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
    Greedy WITHOUT fractions — picks slots by ratio order
    but skips any slot it cannot fully afford.
    This is the fair comparison against 0/1 DP.
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
    """Compare 0/1 greedy vs 0/1 DP on the same dataset."""
    _, greedy_reach, greedy_spent = greedy_01_no_fraction(slots, budget)
    _, dp_reach, dp_spent, _, _   = dp_01_knapsack(slots, budget)

    print(f"{'':.<32} {'Greedy (0/1)':>14} {'DP (0/1)':>12}")
    print(f"{'Total reach':<32} {greedy_reach:>14,} {dp_reach:>12,}")
    print(f"{'Budget spent':<32} ${greedy_spent:>13,} ${dp_spent:>11,}")
    if dp_reach > greedy_reach:
        print(f"\n✓ DP found a better solution — {dp_reach - greedy_reach:,} more people reached!")
    elif greedy_reach > dp_reach:
        print(f"\n✓ Greedy found a better solution — {greedy_reach - dp_reach:,} more people reached!")
    else:
        print(f"\n= Both approaches found the same reach on this dataset.")


if __name__ == "__main__":
    print("=== DP 0/1 Knapsack — Single Platform ($10,000 budget) ===\n")
    selected, reach, spent, table, steps = dp_01_knapsack(single_platform_slots, SINGLE_BUDGET)
    print_results(selected, reach, spent, steps, SINGLE_BUDGET)

    print("\n=== DP 0/1 Knapsack — Adversarial Case ($10,000 budget) ===\n")
    selected, reach, spent, table, steps = dp_01_knapsack(adversarial_slots, ADVERSARIAL_BUDGET)
    print_results(selected, reach, spent, steps, ADVERSARIAL_BUDGET)

    print("\n=== Greedy vs DP Comparison — Adversarial Case ===\n")
    print_comparison(adversarial_slots, ADVERSARIAL_BUDGET)