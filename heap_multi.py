"""
Multi-platform ad allocation using a max-heap.

Idea:
Combine ad slots from all platforms into one global priority queue ordered by
reach-per-dollar ratio, then repeatedly pick the best available full slot
until the budget is exhausted.

This is the Part 2 extension of the project:
- input: multi-platform slots + one global budget
- method: max-heap + greedy selection
- output: chosen slots, spend, total reach, and platform-by-platform breakdown
"""

import heapq
from data import multi_platform_slots, MULTI_BUDGET


def build_max_heap(slots):
    """
    Build a max-heap from slot dictionaries using ratio as priority.

    Because Python's heapq is a min-heap, we store negative ratios so that the
    largest original ratio comes out first.

    Parameters:
        slots: List of slot dicts with keys 'name', 'platform', 'cost', 'reach', 'ratio'.

    Returns:
        A heap list of tuples: (-ratio, index, slot)
    """
    heap = []
    for i, slot in enumerate(slots):
        heapq.heappush(heap, (-slot["ratio"], i, slot))
    return heap


def heap_multi_allocate(slots, budget):
    """
    Allocate a single global budget across multiple platforms using a max-heap.

    Rule:
    Always choose the currently highest reach-per-dollar slot that still fits
    in the remaining budget. If a slot is too expensive, skip it and continue.

    Parameters:
        slots: List of slot dicts
        budget: Non-negative integer budget in dollars

    Returns:
        Tuple (selected, total_reach, total_spent, steps, platform_summary)
        - selected: list of chosen slot dicts in selection order
        - total_reach: total audience reach
        - total_spent: total dollars spent
        - steps: per-step decision log
        - platform_summary: dict keyed by platform with spend/reach/count
    """
    heap = build_max_heap(slots)

    remaining = budget
    selected = []
    total_reach = 0
    total_spent = 0
    steps = []

    platform_summary = {}

    while heap:
        neg_ratio, _, slot = heapq.heappop(heap)

        if slot["cost"] <= remaining:
            remaining -= slot["cost"]
            total_spent += slot["cost"]
            total_reach += slot["reach"]
            selected.append(slot)

            platform = slot["platform"]
            if platform not in platform_summary:
                platform_summary[platform] = {
                    "slots_selected": 0,
                    "spent": 0,
                    "reach": 0,
                }

            platform_summary[platform]["slots_selected"] += 1
            platform_summary[platform]["spent"] += slot["cost"]
            platform_summary[platform]["reach"] += slot["reach"]

            steps.append({
                "slot": slot["name"],
                "platform": slot["platform"],
                "ratio": round(-neg_ratio, 4),
                "action": "selected",
                "cost": slot["cost"],
                "reach": slot["reach"],
                "budget_remaining": remaining,
            })
        else:
            steps.append({
                "slot": slot["name"],
                "platform": slot["platform"],
                "ratio": round(-neg_ratio, 4),
                "action": "skipped",
                "cost": slot["cost"],
                "reach": slot["reach"],
                "budget_remaining": remaining,
            })

    return selected, total_reach, total_spent, steps, platform_summary


def print_results(selected, total_reach, total_spent, steps, platform_summary, budget):
    """
    Pretty-print the multi-platform heap allocation results.

    Parameters:
        selected, total_reach, total_spent, steps, platform_summary:
            Outputs from heap_multi_allocate(...)
        budget: Original budget
    """
    print(f"{'Step':<5} {'Slot':<20} {'Platform':<10} {'Ratio':>8} {'Action':<10} {'Cost':>9} {'Reach':>10} {'Budget Left':>12}")
    print("-" * 100)

    for i, s in enumerate(steps, 1):
        print(
            f"{i:<5} "
            f"{s['slot']:<20} "
            f"{s['platform']:<10} "
            f"{s['ratio']:>8} "
            f"{s['action']:<10} "
            f"${s['cost']:>8,} "
            f"{s['reach']:>10,} "
            f"${s['budget_remaining']:>11,}"
        )

    print("-" * 100)
    print(f"\nSlots selected: {[s['name'] for s in selected]}")
    print(f"Budget used:    ${total_spent:,} / ${budget:,}")
    print(f"Total reach:    {total_reach:,}")

    print("\nPlatform breakdown:")
    for platform, stats in platform_summary.items():
        print(
            f"- {platform}: "
            f"{stats['slots_selected']} slot(s), "
            f"spent ${stats['spent']:,}, "
            f"reach {stats['reach']:,}"
        )


if __name__ == "__main__":
    print("=== Multi-platform allocation with max-heap, $30,000 budget ===\n")
    selected, reach, spent, steps, summary = heap_multi_allocate(
        multi_platform_slots,
        MULTI_BUDGET
    )
    print_results(selected, reach, spent, steps, summary, MULTI_BUDGET)
