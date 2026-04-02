"""
Fractional knapsack (greedy): allocate budget across ad slots by descending
reach-per-dollar ratio. If the remaining budget is less than a slot's cost,
purchase a fractional share of that slot.

Time complexity: O(n log n) for merge sort, O(n) for the allocation pass.
"""

from data import single_platform_slots, adversarial_slots, SINGLE_BUDGET, ADVERSARIAL_BUDGET


def merge_sort_by_ratio(slots):
    """
    Sort ad slots for the fractional greedy rule (best reach-per-dollar first).

    Returns:
        New list of the same slot dicts, ordered by ``ratio`` descending. Ties keep
        the left sublist’s element first (merge sort behavior).
    """
    if len(slots) <= 1:
        return slots

    mid = len(slots) // 2
    left = merge_sort_by_ratio(slots[:mid])
    right = merge_sort_by_ratio(slots[mid:])

    return merge(left, right)


def merge(left, right):
    """Merge two sorted slot lists into one sorted by ``ratio`` (descending). Internal helper."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
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
    Compute an optimal budget allocation when each slot may be purchased in part
    (fractional knapsack): maximize total reach for at most ``budget`` dollars.

    Parameters:
        slots: Slot dicts with ``cost``, ``reach``, and ``ratio`` (use ``data.make_slot``).
        budget: Non-negative budget in dollars.

    Returns:
        Tuple ``(selected, total_reach, total_spent, steps)``:
        - ``selected``: list of ``(slot_dict, fraction)`` where ``fraction`` is in (0, 1].
        - ``total_reach``: summed audience reach (rounded to nearest integer).
        - ``total_spent``: dollars used (up to ``budget``; less only if the list ends before
          the budget is exhausted).
        - ``steps``: one dict per greedy step with keys ``slot``, ``action``, ``fraction``,
          ``spent``, ``reach_gained``, ``budget_remaining`` for logging or UI.
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
            fraction = 1.0
            spent = slot["cost"]
            reach_gained = slot["reach"]
            action = "fully bought"
        else:
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


def print_results(selected, total_reach, total_spent, steps, budget):
    """
    Display a fractional run: table of steps, then total spend and reach.

    Parameters:
        selected, total_reach, total_spent, steps: Outputs from ``greedy_fractional``.
        budget: Budget cap passed in (for the summary line).

    Returns:
        None (prints only).
    """
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
    print("=== Greedy (fractional) — single platform, $10,000 budget ===\n")
    selected, reach, spent, steps = greedy_fractional(single_platform_slots, SINGLE_BUDGET)
    print_results(selected, reach, spent, steps, SINGLE_BUDGET)

    print("\n=== Greedy (fractional) — adversarial case, $10,000 budget ===\n")
    selected, reach, spent, steps = greedy_fractional(adversarial_slots, ADVERSARIAL_BUDGET)
    print_results(selected, reach, spent, steps, ADVERSARIAL_BUDGET)
    print("\nFractional knapsack may purchase partial slots, so optimality holds under")
    print("that model. For the 0/1 comparison on the same instance, run dp.py.")
