"""
Automated regression checks for Part 1 (data helpers, sorting, fractional greedy,
0/1 greedy baseline, 0/1 DP). Exit status is 0 if every check passes.

Run: ``python3 tests.py`` from the repository root. Expected: only ``PASS`` lines
and a final line ``All checks passed.``

Test index (see numbered blocks below):
  Test 1–2:   data and sorting
  Test 3–12:  fractional greedy (``greedy_fractional``)
  Test 13–20: 0/1 greedy vs DP
  Test 21–22: adversarial invariants
"""

from data import (
    make_slot,
    single_platform_slots,
    multi_platform_slots,
    adversarial_slots,
    SINGLE_BUDGET,
    MULTI_BUDGET,
    ADVERSARIAL_BUDGET,
)
from greedy import merge_sort_by_ratio, greedy_fractional
from dp import dp_01_knapsack, greedy_01_no_fraction

passed = 0
failed = 0


def _record(ok, name, detail=None):
    """
    Record one boolean check: increment pass/fail counters and print a line.

    Parameters:
        ok: Whether the check succeeded.
        name: Short label for the test.
        detail: Optional failure message (shown only if ``ok`` is false).

    Returns:
        None (updates module-level ``passed`` / ``failed`` and prints).
    """
    global passed, failed
    if ok:
        passed += 1
        print(f"  PASS  {name}")
    else:
        failed += 1
        print(f"  FAIL  {name}")
        if detail:
            print(f"         {detail}")


def run_test_01(name, slots, budget, expected_greedy_01, expected_dp):
    """
    Compare 0/1 greedy versus DP on one instance.

    Parameters:
        name: Test label (include ``Test N —`` for readability).
        slots, budget: Inputs to both algorithms.
        expected_greedy_01: Expected total reach from ``greedy_01_no_fraction``.
        expected_dp: Expected optimal total reach from ``dp_01_knapsack``.

    Returns:
        None (calls ``_record``; expects DP spend to match sum of selected costs).
    """
    _, g_reach, _ = greedy_01_no_fraction(slots, budget)
    sel, d_reach, d_spent, _, _ = dp_01_knapsack(slots, budget)

    g_ok = g_reach == expected_greedy_01
    d_ok = d_reach == expected_dp
    spent_ok = d_spent == sum(s["cost"] for s in sel)

    ok = g_ok and d_ok and spent_ok
    detail = []
    if not g_ok:
        detail.append(f"0/1 greedy reach {g_reach:,} (expected {expected_greedy_01:,})")
    if not d_ok:
        detail.append(f"DP reach {d_reach:,} (expected {expected_dp:,})")
    if not spent_ok:
        detail.append(f"DP spent {d_spent} != sum of selected costs {sum(s['cost'] for s in sel)}")

    _record(ok, name, "; ".join(detail) if detail else None)


def run_test_frac(name, slots, budget, expected_reach, expected_spent):
    """
    Check ``greedy_fractional`` totals against known-good numbers.

    Parameters:
        name: Test label (include ``Test N —`` for readability).
        slots, budget: Inputs to ``greedy_fractional``.
        expected_reach: Expected rounded total reach.
        expected_spent: Expected total dollars spent.

    Returns:
        None (calls ``_record``).
    """
    _, reach, spent, _ = greedy_fractional(slots, budget)
    ok = reach == expected_reach and spent == expected_spent
    detail = None
    if not ok:
        detail = f"reach {reach} (expected {expected_reach}), spent {spent} (expected {expected_spent})"
    _record(ok, name, detail)


# ---------------------------------------------------------------------------
# Test 1 — make_slot: builds dict with name, platform, cost, reach, ratio
# ---------------------------------------------------------------------------
print("=== Tests 1–2: data and sorting ===\n")

# Test 1 — make_slot: builds dict with name, platform, cost, reach, ratio
s = make_slot("Test", "Google", 1000, 50000)
_record(
    s["name"] == "Test"
    and s["platform"] == "Google"
    and s["cost"] == 1000
    and s["reach"] == 50000
    and s["ratio"] == round(50000 / 1000, 4),
    "Test 1 — make_slot: required fields and ratio",
)

# Test 2 — merge_sort_by_ratio: slots ordered by reach-per-dollar descending
slots_ab = [
    make_slot("low", "G", 100, 100),
    make_slot("high", "G", 100, 500),
    make_slot("mid", "G", 100, 300),
]
sorted_slots = merge_sort_by_ratio(slots_ab)
ratios = [x["ratio"] for x in sorted_slots]
_record(ratios == sorted(ratios, reverse=True), "Test 2 — merge_sort_by_ratio: descending order")


# ---------------------------------------------------------------------------
# Test 3–12 — greedy_fractional (fractional knapsack)
# ---------------------------------------------------------------------------
print("\n=== Tests 3–12: fractional greedy (greedy_fractional) ===\n")

normal_slots = [
    make_slot("Search ad", "Google", 2000, 80000),
    make_slot("Display banner", "Google", 500, 9000),
    make_slot("YouTube", "Google", 4000, 120000),
    make_slot("Feed ad", "Google", 3000, 72000),
    make_slot("Sidebar ad", "Google", 1000, 15000),
]

exact_slots = [
    make_slot("Slot X", "Meta", 4000, 100000),
    make_slot("Slot Y", "Meta", 6000, 150000),
]

same_ratio_slots = [
    make_slot("Slot P", "Google", 2000, 60000),
    make_slot("Slot Q", "Google", 3000, 90000),
    make_slot("Slot R", "Google", 6000, 180000),
]

# Test 3 — Normal case: several slots, $10,000 budget (expected reach/spend fixed)
run_test_frac("Test 3 — fractional: normal case (multi-slot, $10k)", normal_slots, 10000, 288500, 10000)

# Test 4 — Adversarial instance: fractional can still exhaust budget
run_test_frac(
    "Test 4 — fractional: adversarial instance (data.adversarial_slots)",
    adversarial_slots,
    ADVERSARIAL_BUDGET,
    400000,
    10000,
)

# Test 5 — Exact budget fit: two slots sum to budget
run_test_frac("Test 5 — fractional: exact budget fit (two slots)", exact_slots, 10000, 250000, 10000)

# Test 6 — Single slot that fits entirely
run_test_frac(
    "Test 6 — fractional: single affordable slot",
    [make_slot("Only slot", "TikTok", 3000, 90000)],
    10000,
    90000,
    3000,
)

# Test 7 — Single slot too expensive for full buy; fractional takes a partial
run_test_frac(
    "Test 7 — fractional: single slot, partial purchase only",
    [make_slot("Too expensive", "TikTok", 15000, 500000)],
    10000,
    333333,
    10000,
)

# Test 8 — Empty slot list
run_test_frac("Test 8 — fractional: empty slot list", [], 10000, 0, 0)

# Test 9 — Zero budget
run_test_frac("Test 9 — fractional: zero budget", normal_slots, 0, 0, 0)

# Test 10 — All slots share the same ratio
run_test_frac("Test 10 — fractional: all equal ratio", same_ratio_slots, 10000, 300000, 10000)

# Test 11 — Shared dataset: single-platform list from data.py
run_test_frac(
    "Test 11 — fractional: data.single_platform_slots + SINGLE_BUDGET",
    single_platform_slots,
    SINGLE_BUDGET,
    288500,
    10000,
)

# Test 12 — Shared dataset: multi-platform list (Part 2 hook)
run_test_frac(
    "Test 12 — fractional: data.multi_platform_slots + MULTI_BUDGET",
    multi_platform_slots,
    MULTI_BUDGET,
    1010000,
    30000,
)


# ---------------------------------------------------------------------------
# Test 13–20 — 0/1 greedy vs 0/1 DP (same scenarios, expected reach per algorithm)
# ---------------------------------------------------------------------------
print("\n=== Tests 13–20: 0/1 greedy vs 0/1 DP ===\n")

# Test 13 — Normal case: DP can beat naive 0/1 greedy reach
run_test_01("Test 13 — 0/1: normal case", normal_slots, 10000, 281000, 287000)

# Test 14 — Adversarial: 0/1 greedy stuck; DP optimal higher
run_test_01(
    "Test 14 — 0/1: adversarial (DP strictly better than ratio-greedy)",
    adversarial_slots,
    10000,
    280000,
    350000,
)

# Test 15 — Exact budget fit: both agree
run_test_01("Test 15 — 0/1: exact budget fit", exact_slots, 10000, 250000, 250000)

# Test 16 — Single affordable slot
run_test_01(
    "Test 16 — 0/1: single slot (fits in budget)",
    [make_slot("Only slot", "TikTok", 3000, 90000)],
    10000,
    90000,
    90000,
)

# Test 17 — No slot affordable with 0/1 model
run_test_01(
    "Test 17 — 0/1: single slot (too expensive)",
    [make_slot("Too expensive", "TikTok", 15000, 500000)],
    10000,
    0,
    0,
)

# Test 18 — Empty slot list
run_test_01("Test 18 — 0/1: empty slot list", [], 10000, 0, 0)

# Test 19 — Zero budget
run_test_01("Test 19 — 0/1: zero budget", normal_slots, 0, 0, 0)

# Test 20 — Equal ratios: DP can combine better than ratio-greedy order
run_test_01("Test 20 — 0/1: all equal ratio", same_ratio_slots, 10000, 150000, 270000)


# ---------------------------------------------------------------------------
# Test 21–22 — Invariants on adversarial data (report / demo)
# ---------------------------------------------------------------------------
print("\n=== Tests 21–22: invariants (adversarial instance) ===\n")

_, g_r, _ = greedy_01_no_fraction(adversarial_slots, ADVERSARIAL_BUDGET)
_, d_r, _, _, _ = dp_01_knapsack(adversarial_slots, ADVERSARIAL_BUDGET)
_record(
    d_r > g_r,
    "Test 21 — invariant: DP reach > 0/1 greedy reach (adversarial)",
    f"DP {d_r:,} vs 0/1 greedy {g_r:,}",
)

_, r_frac, _, _ = greedy_fractional(adversarial_slots, ADVERSARIAL_BUDGET)
_record(
    r_frac >= d_r,
    "Test 22 — invariant: fractional reach ≥ DP reach (this instance)",
    f"fractional {r_frac:,} vs DP {d_r:,}",
)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
total = passed + failed
print(f"\n{'─' * 40}")
print(f"Results: {passed} passed, {failed} failed out of {total} checks")
if failed == 0:
    print("All checks passed.")
else:
    print("Some checks failed; see messages above.")
