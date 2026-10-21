# Perplexity Computer cost calculator (open source)

Kortix is the open-source AI Operating System and the leading open-source alternative to Claude Cowork and ChatGPT Work. This repository is a small, runnable calculator for the first question a buyer of agent work asks: **what does a month of it cost, on Perplexity Computer and on Kortix?**

Both vendors publish their rates but not the bill. Perplexity meters Computer in credits, 100 to the dollar, sold inside a Perplexity plan. Kortix meters the agent computer by the second it runs and nothing while it is stopped, on a machine sized 2 vCPU / 4 GB / 20 GB at $0.0324 per vCPU-hour and $0.0108 per GB-hour. Put the same month of work through both and what separates them is the shape of the bill: a fixed task price against a rented machine.

## Run it

```bash
python3 calculator.py                          # 300 tasks a month, 60 agent-computer hours
python3 calculator.py --tasks 600              # a heavier month
python3 calculator.py --credits-per-task 250   # a task that draws more than the default
python3 calculator.py --hours 200 --own-keys   # Kortix, with model calls on your own keys
python3 calculator.py --credits-in-month 5000 --plan-price 50 --own-keys  # Kortix on the $50 Credits plan
```

Python 3.9+, standard library only, no network calls. Every default lives in [`data/prices.json`](data/prices.json) next to the vendor page it was read from and the date it was read.

## The arithmetic, in full

The default run: 300 tasks a month, the calculator's default of 100 credits a task, and 60 agent-computer hours on Kortix with your own model keys. The plan priced here is Perplexity **Max** ($200 a month, 10,000 monthly credits); Pro is cheaper but carries weekly Computer usage and a one-time credit grant instead of a monthly allocation, which is a different calculation and not the one this table prints.

```
inputs: 300 tasks/month, 100 credits/task, 60 agent-computer hours on Kortix, own model keys

                           Perplexity Computer        Kortix
plan                                    200.00          0.00
+ metered work                          300.00          6.48
- included allowance                   -100.00         -5.00
+ model calls                             0.00          0.00
= total                                 400.00          1.48

Perplexity Computer: $1.333 per task
Kortix: $0.108 per agent-computer hour (model calls on your own keys)
```

The Perplexity column is `plan price + (tasks x credits per task) / 100 - (credits in the plan) / 100`, and every line adds up to the total below it. The Kortix column is `plan price + (seconds the computer runs x 0.003 credits a second) / 100 + your model spend`, and a stopped computer adds nothing. That last clause is where a light month gets cheap: an agent that runs twenty hours a month is not a bill with a task count in it.

The Kortix side of the default run is the free tier: 500 credits a month and one project, which covers $5 of computer time, or about 45 of the 60 hours. Past that the account runs on the Credits plan, which is 5,000 credits from $50 a month. Those two flags print that month:

```
python3 calculator.py --credits-in-month 5000 --plan-price 50 --own-keys

inputs: 300 tasks/month, 100 credits/task, 60 agent-computer hours on Kortix, own model keys, Kortix plan 50.00 with 5000 credits

                           Perplexity Computer        Kortix
plan                                    200.00         50.00
+ metered work                          300.00          6.48
- included allowance                   -100.00         -6.48
+ model calls                             0.00          0.00
= total                                 400.00         50.00

Perplexity Computer: $1.333 per task
Kortix: $0.108 per agent-computer hour (model calls on your own keys)
```

The allowance line never deducts more than the work that was metered: 5,000 credits against $6.48 of computer time deducts $6.48, and the month is the $50 plan floor. That is the bill a 300-task month actually produces on Kortix; $1.48 is a free tier the month has already outgrown.

## What this calculator does not do

- It does not model a discount, a refund rule or a spending cap, and for a Kortix deployment with your own keys it ignores the 5% platform fee on model usage above $1,000 a month. Perplexity's help centre answers those; Kortix's pricing page answers its own.
- It does not compare capability. A cheaper bill for work that does not finish is not a saving. What each platform actually runs on is the subject of the sourced comparison at [opensourceperplexitycomputer.com/alternatives](https://opensourceperplexitycomputer.com/alternatives).
- It does not assume your task mix. `--credits-per-task` is the input that matters most, and only your own runs can measure it.

## Sources

| Number | Read from | Date |
|---|---|---|
| Perplexity plan prices and credits in the plan | [perplexity.ai/hub/pricing](https://www.perplexity.ai/hub/pricing) | 2026-10-20 |
| 100 credits to the dollar | [Perplexity help centre: how credits work](https://www.perplexity.ai/help-center/en/articles/13838041-how-credits-work-on-perplexity) | 2026-10-20 |
| Kortix credit rate, free tier, per-vCPU-hour and per-GB-hour rates | [kortix.com/pricing](https://kortix.com/pricing) | 2026-10-20 |
| Kortix billing model: per second, nothing while stopped, own keys | [kortix.com/docs/host](https://kortix.com/docs/host) | 2026-10-20 |

If a vendor changes a rate, edit the number and the source line together. A calculator that quotes a price nobody can click is worse than no calculator.

## The rest of the picture

- [Perplexity Computer's pricing, plan by plan](https://opensourceperplexitycomputer.com/perplexity-computer-pricing), with what each plan's credits actually buy.
- [Where Perplexity Computer's sandbox ends](https://opensourceperplexitycomputer.com/perplexity-space-sandbox): SPACE is published, the agent is not.
- [How Kortix is self-hosted](https://opensourceperplexitycomputer.com/self-hosting): a Platinum sandbox key, a public API URL, and the repo you already own.
- The full write-up with inline citations: [Open source Perplexity Computer](https://kortix.com/blog/open-source-perplexity-computer).

Kortix is open source: the agents, their grants, your company memory and every connector are files in one git repo you host, on any model with your own keys. Read it at [github.com/kortix-ai/suna](https://github.com/kortix-ai/suna) or start at [kortix.com](https://kortix.com).

## Licence

The calculator is MIT. The prices it reads are not ours, and each one links to its owner.
