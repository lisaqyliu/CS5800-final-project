"""
Ad slot representation and synthetic datasets for budget allocation experiments.

Each slot is a dict: name, platform, cost (USD), reach (audience size), and ratio
(reach per dollar, rounded for stable sorting).
"""


def make_slot(name, platform, cost, reach):
    """
    Build one ad slot record for algorithms and tests.

    Parameters:
        name: Label for the placement.
        platform: Channel name (e.g. ``"Google"``).
        cost: Price in dollars (must be > 0 for ``ratio``).
        reach: Estimated audience size.

    Returns:
        Dict with keys ``name``, ``platform``, ``cost``, ``reach``, and ``ratio``,
        where ``ratio`` is ``round(reach / cost, 4)`` (reach per dollar).
    """
    return {
        "name": name,
        "platform": platform,
        "cost": cost,
        "reach": reach,
        "ratio": round(reach / cost, 4),
    }


# Single-platform demo: budget $10,000
single_platform_slots = [
    make_slot("Search ad",        "Google",  2000,  80000),
    make_slot("Display banner",   "Google",   500,   9000),
    make_slot("YouTube pre-roll", "Google",  4000, 120000),
    make_slot("Feed ad",          "Google",  3000,  72000),
    make_slot("Sidebar ad",       "Google",  1000,  15000),
]

SINGLE_BUDGET = 10000


# Multi-platform demo: budget $30,000 (extends to Part 2)
multi_platform_slots = [
    make_slot("Search ad",        "Google",  2000,  80000),
    make_slot("Display banner",   "Google",   500,   9000),
    make_slot("YouTube pre-roll", "Google",  4000, 120000),

    make_slot("Feed ad",          "Meta",    3000,  90000),
    make_slot("Stories ad",       "Meta",    1500,  40000),
    make_slot("Reels ad",         "Meta",    5000, 160000),

    make_slot("In-feed ad",       "TikTok",  2500,  75000),
    make_slot("TopView ad",       "TikTok",  8000, 300000),
    make_slot("Branded effect",   "TikTok",  6000, 200000),
]

MULTI_BUDGET = 30000


# Adversarial instance for 0/1 greedy (budget $10,000):
# Ratio-ordered greedy may take slot A ($7,000), leaving $3,000 with no affordable
# remaining slot (reach 280,000). DP selects B and C ($10,000 total, reach 350,000).
# Under fractional knapsack, partial purchases change the outcome; this contrast is 0/1-specific.
adversarial_slots = [
    make_slot("Slot A (high ratio)", "Google", 7000, 280000),
    make_slot("Slot B",              "Google", 5000, 200000),
    make_slot("Slot C",              "Google", 5000, 150000),
]

ADVERSARIAL_BUDGET = 10000


def print_slots(slots):
    """
    Print slots as a column-aligned table (name, platform, cost, reach, ratio).

    Parameters:
        slots: Iterable of slot dicts from ``make_slot``.

    Returns:
        None (prints only).
    """
    print(f"{'Name':<25} {'Platform':<10} {'Cost':>8} {'Reach':>10} {'Ratio':>8}")
    print("-" * 65)
    for s in slots:
        print(f"{s['name']:<25} {s['platform']:<10} ${s['cost']:>7,} {s['reach']:>10,} {s['ratio']:>8}")


if __name__ == "__main__":
    print("=== Single platform ===")
    print_slots(single_platform_slots)

    print("\n=== Multi platform ===")
    print_slots(multi_platform_slots)

    print("\n=== Adversarial (0/1 greedy vs DP) ===")
    print_slots(adversarial_slots)
