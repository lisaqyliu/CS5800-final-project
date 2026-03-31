# ─────────────────────────────────────────
#  Test Cases — Greedy & DP Algorithms
#
#  Covers:
#    1. Normal case
#    2. Adversarial case (greedy fails)
#    3. Exact budget fit
#    4. Single slot
#    5. Empty slots
#    6. Budget too small for any slot
#    7. All slots have the same ratio
# ─────────────────────────────────────────

from data import make_slot
from greedy import greedy_fractional
from dp import dp_01_knapsack, greedy_01_no_fraction

passed = 0
failed = 0


def run_test(name, slots, budget, expected_greedy_01, expected_dp):
    """
    Run one test case and check results.
    expected_greedy_01 : expected total reach for 0/1 greedy
    expected_dp        : expected total reach for 0/1 DP
    """
    global passed, failed
    _, g_reach, _ = greedy_01_no_fraction(slots, budget)
    _, d_reach, _, _, _ = dp_01_knapsack(slots, budget)

    g_ok = g_reach == expected_greedy_01
    d_ok = d_reach == expected_dp

    status = "✓ PASS" if g_ok and d_ok else "✗ FAIL"
    if g_ok and d_ok:
        passed += 1
    else:
        failed += 1

    print(f"{status}  {name}")
    if not g_ok:
        print(f"       Greedy got {g_reach:,}, expected {expected_greedy_01:,}")
    if not d_ok:
        print(f"       DP got {d_reach:,}, expected {expected_dp:,}")


# ─────────────────────────────────────────
#  Test 1 — Normal case
#  Budget: $10,000
#  Expected: both algorithms find the same
#  optimal set when no adversarial conflict
# ─────────────────────────────────────────
normal_slots = [
    make_slot("Search ad",      "Google", 2000,  80000),
    make_slot("Display banner", "Google",  500,   9000),
    make_slot("YouTube",        "Google", 4000, 120000),
    make_slot("Feed ad",        "Google", 3000,  72000),
    make_slot("Sidebar ad",     "Google", 1000,  15000),
]
# DP selects: Search ad + YouTube + Feed ad + Sidebar ad = $10,000 → 287,000
run_test("Normal case", normal_slots, 10000,
         expected_greedy_01=281000,
         expected_dp=287000)


# ─────────────────────────────────────────
#  Test 2 — Adversarial case
#  0/1 greedy picks Slot A and gets stuck.
#  DP picks Slot B + Slot C for more reach.
# ─────────────────────────────────────────
adversarial_slots = [
    make_slot("Slot A (high ratio)", "Google", 7000, 280000),
    make_slot("Slot B",              "Google", 5000, 200000),
    make_slot("Slot C",              "Google", 5000, 150000),
]
run_test("Adversarial case (greedy fails)", adversarial_slots, 10000,
         expected_greedy_01=280000,
         expected_dp=350000)


# ─────────────────────────────────────────
#  Test 3 — Exact budget fit
#  Two slots cost exactly the budget.
#  Both algorithms should select both.
# ─────────────────────────────────────────
exact_slots = [
    make_slot("Slot X", "Meta", 4000, 100000),
    make_slot("Slot Y", "Meta", 6000, 150000),
]
run_test("Exact budget fit", exact_slots, 10000,
         expected_greedy_01=250000,
         expected_dp=250000)


# ─────────────────────────────────────────
#  Test 4 — Single slot, fits in budget
# ─────────────────────────────────────────
single_slot = [
    make_slot("Only slot", "TikTok", 3000, 90000),
]
run_test("Single slot (fits)", single_slot, 10000,
         expected_greedy_01=90000,
         expected_dp=90000)


# ─────────────────────────────────────────
#  Test 5 — Single slot, does NOT fit
# ─────────────────────────────────────────
too_expensive = [
    make_slot("Too expensive", "TikTok", 15000, 500000),
]
run_test("Single slot (too expensive)", too_expensive, 10000,
         expected_greedy_01=0,
         expected_dp=0)


# ─────────────────────────────────────────
#  Test 6 — Empty slot list
# ─────────────────────────────────────────
run_test("Empty slot list", [], 10000,
         expected_greedy_01=0,
         expected_dp=0)


# ─────────────────────────────────────────
#  Test 7 — Budget is zero
# ─────────────────────────────────────────
run_test("Zero budget", normal_slots, 0,
         expected_greedy_01=0,
         expected_dp=0)


# ─────────────────────────────────────────
#  Test 8 — All slots same ratio
#  When ratios are equal, both algorithms
#  should still maximize total reach
# ─────────────────────────────────────────
same_ratio_slots = [
    make_slot("Slot P", "Google", 2000, 60000),  # ratio = 30
    make_slot("Slot Q", "Google", 3000, 90000),  # ratio = 30
    make_slot("Slot R", "Google", 6000, 180000), # ratio = 30
]
# Budget $10,000: best combo is Slot P + Slot Q + Slot R... but that's $11,000
# So best is Slot Q + Slot R = $9,000 → 270,000
# or Slot P + Slot R = $8,000 → 240,000
# DP picks Slot Q + Slot R = 270,000
run_test("All same ratio", same_ratio_slots, 10000,
         expected_greedy_01=150000,
         expected_dp=270000)


# ─────────────────────────────────────────
#  Summary
# ─────────────────────────────────────────
print(f"\n{'─' * 40}")
print(f"Results: {passed} passed, {failed} failed out of {passed + failed} tests")
if failed == 0:
    print("All tests passed! ✓")
else:
    print("Some tests failed — check the output above.")