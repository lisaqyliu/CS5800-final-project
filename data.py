# ─────────────────────────────────────────
#  Ad Slot Data Structure
# ─────────────────────────────────────────
# Each ad slot is a dictionary with 4 fields:
#   name     : display name of the ad slot
#   platform : which channel it belongs to
#   cost     : how much it costs to buy (in dollars)
#   reach    : estimated audience size (number of people)

def make_slot(name, platform, cost, reach):
    return {
        "name": name,
        "platform": platform,
        "cost": cost,
        "reach": reach,
        "ratio": round(reach / cost, 4)  # reach per dollar, precomputed
    }


# ─────────────────────────────────────────
#  Synthetic Dataset — Single Platform
#  Budget: $10,000
# ─────────────────────────────────────────
single_platform_slots = [
    make_slot("Search ad",        "Google",  2000,  80000),
    make_slot("Display banner",   "Google",   500,   9000),
    make_slot("YouTube pre-roll", "Google",  4000, 120000),
    make_slot("Feed ad",          "Google",  3000,  72000),
    make_slot("Sidebar ad",       "Google",  1000,  15000),
]

SINGLE_BUDGET = 10000


# ─────────────────────────────────────────
#  Synthetic Dataset — Multi Platform
#  Budget: $30,000
# ─────────────────────────────────────────
multi_platform_slots = [
    # Google
    make_slot("Search ad",        "Google",  2000,  80000),
    make_slot("Display banner",   "Google",   500,   9000),
    make_slot("YouTube pre-roll", "Google",  4000, 120000),

    # Meta
    make_slot("Feed ad",          "Meta",    3000,  90000),
    make_slot("Stories ad",       "Meta",    1500,  40000),
    make_slot("Reels ad",         "Meta",    5000, 160000),

    # TikTok
    make_slot("In-feed ad",       "TikTok",  2500,  75000),
    make_slot("TopView ad",       "TikTok",  8000, 300000),
    make_slot("Branded effect",   "TikTok",  6000, 200000),
]

MULTI_BUDGET = 30000


# ─────────────────────────────────────────
#  Adversarial Case — where 0/1 greedy fails
#  Budget: $10,000
#
#  0/1 Greedy picks Slot A (ratio 40) →
#  spends $7,000, reach = 280,000, $3,000
#  left but no slot fits → total = 280,000
#
#  DP picks Slot B + Slot C → $5,000 + $5,000
#  = $10,000, reach = 200,000 + 150,000
#  = 350,000 ✓ better!
#
#  Note: fractional greedy still does well
#  here since it can buy 60% of Slot B.
#  The failure only applies to 0/1 greedy.
# ─────────────────────────────────────────
adversarial_slots = [
    make_slot("Slot A (high ratio)", "Google", 7000, 280000),  # ratio = 40
    make_slot("Slot B",              "Google", 5000, 200000),  # ratio = 40
    make_slot("Slot C",              "Google", 5000, 150000),  # ratio = 30
]

ADVERSARIAL_BUDGET = 10000


# ─────────────────────────────────────────
#  Helper — print slots in a readable way
# ─────────────────────────────────────────
def print_slots(slots):
    print(f"{'Name':<25} {'Platform':<10} {'Cost':>8} {'Reach':>10} {'Ratio':>8}")
    print("-" * 65)
    for s in slots:
        print(f"{s['name']:<25} {s['platform']:<10} ${s['cost']:>7,} {s['reach']:>10,} {s['ratio']:>8}")

if __name__ == "__main__":
    print("=== Single Platform Slots ===")
    print_slots(single_platform_slots)

    print("\n=== Multi Platform Slots ===")
    print_slots(multi_platform_slots)

    print("\n=== Adversarial Case ===")
    print_slots(adversarial_slots)