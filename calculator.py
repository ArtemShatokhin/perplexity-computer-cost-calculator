#!/usr/bin/env python3
"""Monthly cost of agent work: Perplexity Computer against Kortix.

Every default in data/prices.json carries the vendor page it was read from and
the date it was read. Nothing here is an estimate of what a vendor "probably"
charges: change an input and the arithmetic follows your input.

    python3 calculator.py                        # defaults from prices.json
    python3 calculator.py --tasks 600 --own-keys # 600 tasks a month, your model keys

Stdlib only. Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent


def load_prices() -> dict:
    return json.loads((HERE / "data" / "prices.json").read_text())


def per_task(monthly_price: float, credits_included: float, credits_per_usd: float,
             credits_per_task: float, tasks: int) -> dict:
    """Cost of `tasks` tasks when credits are metered at credits_per_usd."""
    if credits_per_usd <= 0:
        raise ValueError("credits_per_usd must be positive")
    included_usd = credits_included / credits_per_usd
    used_usd = tasks * credits_per_task / credits_per_usd
    overage_usd = max(0.0, used_usd - included_usd)
    total = monthly_price + overage_usd
    return {
        "tasks": tasks,
        "included_usd": round(included_usd, 2),
        "metered_usd": round(used_usd, 2),
        "overage_usd": round(overage_usd, 2),
        "total_usd": round(total, 2),
        "per_task_usd": round(total / tasks, 4) if tasks else None,
    }


def kortix_computer(seconds_running: float, credit_seconds: float,
                    credits_per_usd: float, monthly_price: float,
                    credits_included: float, model_usd: float) -> dict:
    """Kortix meters the agent computer by the second it runs, and nothing while stopped.

    credit_seconds: credits charged per second of a running computer for the
    size you reserve. model_usd: your model spend, which is 0 with your own
    keys past the documented allowance (see data/prices.json).
    """
    credits = seconds_running * credit_seconds
    computer_usd = credits / credits_per_usd
    covered = credits_included / credits_per_usd
    computer_overage = max(0.0, computer_usd - covered)
    total = monthly_price + computer_overage + model_usd
    return {
        "computer_hours": round(seconds_running / 3600, 1),
        "computer_usd": round(computer_usd, 2),
        "computer_overage_usd": round(computer_overage, 2),
        "model_usd": round(model_usd, 2),
        "total_usd": round(total, 2),
    }


def main() -> None:
    p = load_prices()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tasks", type=int, default=300,
                    help="agent tasks (or task-equivalents) per month")
    ap.add_argument("--credits-per-task", type=float, default=None,
                    help="credits a Perplexity Computer task draws; default from prices.json")
    ap.add_argument("--hours", type=float, default=None,
                    help="agent-computer hours a month on Kortix; default from prices.json")
    ap.add_argument("--own-keys", action="store_true",
                    help="model calls billed by your own provider (Kortix only)")
    args = ap.parse_args()

    pc = p["perplexity_computer"]
    kx = p["kortix"]
    credits_per_task = args.credits_per_task or pc["credits_per_task_default"]
    hours = args.hours if args.hours is not None else kx["hours_default"]

    pc_row = per_task(pc["monthly_price_usd"], pc["credits_in_month"],
                      pc["credits_per_usd"], credits_per_task, args.tasks)
    model_usd = 0.0 if args.own_keys else kx["model_usd_default"]
    kx_row = kortix_computer(hours * 3600, kx["credits_per_second"],
                             kx["credits_per_usd"], kx["monthly_price_usd"],
                             kx["credits_in_month"], model_usd)

    print(f"inputs: {args.tasks} tasks/month, {credits_per_task} credits/task, "
          f"{hours} agent-computer hours on Kortix, "
          f"{'own model keys' if args.own_keys else 'vendor model calls'}")
    print()
    print(f"{'':22}{'Perplexity Computer':>22}{'Kortix':>14}")
    print(f"{'monthly fixed':22}{pc_row['total_usd'] - pc_row['overage_usd']:>22.2f}"
          f"{kx_row['total_usd'] - kx_row['computer_overage_usd'] - kx_row['model_usd']:>14.2f}")
    print(f"{'metered work':22}{pc_row['metered_usd']:>22.2f}{kx_row['computer_usd']:>14.2f}")
    print(f"{'overage':22}{pc_row['overage_usd']:>22.2f}{kx_row['computer_overage_usd']:>14.2f}")
    print(f"{'model calls':22}{0.0:>22.2f}{kx_row['model_usd']:>14.2f}")
    print(f"{'total':22}{pc_row['total_usd']:>22.2f}{kx_row['total_usd']:>14.2f}")
    if pc_row["per_task_usd"] and kx_row["computer_hours"]:
        kx_per_hour = (kx_row["computer_usd"] / kx_row["computer_hours"]) if kx_row["computer_hours"] else 0
        print()
        print(f"Perplexity Computer: ${pc_row['per_task_usd']:.3f} per task")
        print(f"Kortix: ${kx_per_hour:.3f} per agent-computer hour"
              + (" (model calls on your own keys)" if args.own_keys else ""))
    print()
    print("Sources for every default: data/prices.json")


if __name__ == "__main__":
    main()
