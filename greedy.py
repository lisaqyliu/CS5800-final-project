# ─────────────────────────────────────────
#  Greedy Algorithm — Fractional Knapsack
#  
#  Idea: rank slots by reach/cost ratio,
#  pick the best one first, then next best,
#  until budget runs out.
#
#  If the next slot costs more than remaining
#  budget, buy a fraction of it.
#
#  Time complexity: O(N log N) for sorting
# ─────────────────────────────────────────

from data import single_platform_slots, adversarial_slots, SINGLE_BUDGET, ADVERSARIAL_BUDGET


def merge_sort_by_ratio(slots):
    """Sort slots by reach/cost ratio (highest first) using merge sort."""
    if len(slots) <= 1:
        return slots

    mid = len(slots) // 2
    left = merge_sort_by_ratio(slots[:mid])
    right = merge_sort_by_ratio(slots[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        # higher ratio comes first
        if left[i]["ratio"] >= right[j]["ratio"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def greedy_fractional(slots, budget):
    """
    Fractional knapsack greedy algorithm.

    Input:
        slots  : list of ad slot dictionaries
        budget : total budget available (dollars)

    Output:
        selected : list of (slot, fraction_bought) tuples
        total_reach  : total audience reached
        total_spent  : total budget spent
        steps    : log of decisions made (for visualization)
    """
    sorted_slots = merge_sort_by_ratio(slots)

    remaining = budget
    total_reach = 0
    selected = []
    steps = []

    for slot in sorted_slots:
        if remaining <= 0:
            break

        if slot["cost"] <= remaining:
            # buy the whole slot
            fraction = 1.0
            spent = slot["cost"]
            reach_gained = slot["reach"]
            action = "fully bought"
        else:
            # buy a fraction of the slot
            fraction = remaining / slot["cost"]
            spent = remaining
            reach_gained = slot["reach"] * fraction
            action = "partially bought"

        remaining -= spent
        total_reach += reach_gained
        selected.append((slot, fraction))

        steps.append({
            "slot": slot["name"],
            "action": action,
            "fraction": round(fraction, 4),
            "spent": round(spent, 2),
            "reach_gained": round(reach_gained),
            "budget_remaining": round(remaining, 2)
        })

    return selected, round(total_reach), round(budget - remaining, 2), steps


# ─────────────────────────────────────────
#  Helper — print results
# ─────────────────────────────────────────
def print_results(selected, total_reach, total_spent, steps, budget):
    print(f"{'Step':<5} {'Slot':<25} {'Action':<17} {'Fraction':>9} {'Spent':>9} {'Reach':>10} {'Budget Left':>12}")
    print("-" * 92)
    for i, s in enumerate(steps, 1):
        print(f"{i:<5} {s['slot']:<25} {s['action']:<17} {s['fraction']:>9.2%} "
              f"${s['spent']:>8,.0f} {s['reach_gained']:>10,} ${s['budget_remaining']:>11,.0f}")
    print("-" * 92)
    print(f"{'TOTAL':<5} {'':<25} {'':<17} {'':<9} ${total_spent:>8,.0f} {total_reach:>10,}")
    print(f"\nBudget used: ${total_spent:,.0f} / ${budget:,.0f}")
    print(f"Total reach: {total_reach:,}")


if __name__ == "__main__":
    print("=== Greedy — Single Platform ($10,000 budget) ===\n")
    selected, reach, spent, steps = greedy_fractional(single_platform_slots, SINGLE_BUDGET)
    print_results(selected, reach, spent, steps, SINGLE_BUDGET)

    print("\n=== Greedy — Adversarial Case ($10,000 budget) ===\n")
    selected, reach, spent, steps = greedy_fractional(adversarial_slots, ADVERSARIAL_BUDGET)
    print_results(selected, reach, spent, steps, ADVERSARIAL_BUDGET)
    print("\nNote: fractional greedy can purchase partial slots,")
    print("so it still performs well on this example.")
    print("The more interesting failure happens in the 0/1 setting;")
    print("to see that comparison on the same data, run dp.py.")