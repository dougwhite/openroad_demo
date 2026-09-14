# Launch Score — Gorak demo

A disposable OpenROAD application for demonstrating readable source edits,
verified synchronization, deterministic tests and an AI-authored pull request.
The baseline awards 10 points per capsule: 1 → 10 and 5 → 50.

## Setup

Install Gorak from its source checkout. Configure a local-only `.env` for an
independent disposable OpenROAD source database and execution host. Install the
Actian UnitTestFramework as `unittestframework` and configure its runtime libraries.
This repository does not redistribute the framework. SSH users need Gorak remote
helpers version 8 (`gorak remote install`).

For a fresh clone targeting a new disposable database:

```sh
gorak sync --push
gorak test
```

The tracked `.gorak-source` companions preserve complete exported source. Keep
`.env` and `.openroad` private and local. See AGENTS.md for the editing workflow.

## Recording

Start on a clean branch at `demo-baseline-10`. Run `gorak sync`, change the score
multiplier to 12 in `launch_score/p4_score.w4gl`, update the assertions to 12 and 60,
and change the subtitle in `launch_score/launch_panel.wml` to 12 points per capsule.

```sh
gorak sync --push && gorak test
git diff
git add launch_score/p4_score.w4gl launch_score/test_launch_score.w4gl launch_score/launch_panel.wml
git commit -m "Set launch score to twelve points per capsule"
```

Ask Codex:

> Add a fleet bonus to Launch Score: award 20 extra points when the capsule count
> is at least 5, retaining 12 points per capsule. Add deterministic assertions for
> 0, 1, 4, 5 and 6 capsules. Update the Calculate score button to Calculate launch
> score and widen it so the text fits. Follow AGENTS.md: pull, implement on a feature
> branch, push through Gorak, run the tests, inspect the diff, commit, push the branch
> and create a pull request against the branch containing my manual edit. Do not
> merge. Report results and the PR link.

Expected feature scores: 0, 12, 48, 80 and 92 respectively. Open the frame in
Workbench to see the feature. Close its running window and editor before imports.

## Repeat a take

Save intended work in Git first. Switch to `main`, which retains the 10-point
baseline, and synchronize it back into the same disposable database:

```sh
git switch main
gorak sync --push && gorak test
```

For a main branch changed during recording, create a reset branch and restore only
these source paths from the tag, inspect the diff, then push through Gorak and test:

```sh
git switch -c codex/reset-take
git restore --source demo-baseline-10 -- launch_score/p4_score.w4gl launch_score/test_launch_score.w4gl launch_score/launch_panel.wml
gorak sync --push && gorak test
```

A Git switch/restore changes disk source, not the database. Never delete cache,
locks, recovery state or target bindings as a reset shortcut. No force-push or
source database deletion is needed. Stop on a conflict and preserve the evidence.
