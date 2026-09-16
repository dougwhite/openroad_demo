# Launch Score — Gorak demo

A small OpenROAD application for following the Gorak demo: start with 10 points
per capsule, make a change in Workbench, then ask Codex to add a fleet bonus.

**[Gorak](https://github.com/dougwhite/gorak)** ·
**[Watch the demo](https://www.youtube.com/watch?v=zlncaV1mLqM)** ·
**[Project and updates](https://thingsdougmakes.au/projects/gorak/)**

## Get started

Install Gorak using its [getting started guide](https://github.com/dougwhite/gorak/blob/master/docs/getting-started.md)
and create a fresh, blank OpenROAD source database for the demo.

```bat
git clone https://github.com/dougwhite/openroad_demo.git
cd openroad_demo
copy .env.example .env
```

Edit `.env` to point at your demo database, then import the application and run
its tests:

```bat
gorak sync --push
gorak test
```

Open `launch_score` in Workbench and run `launch_panel`, or run it from your
OpenROAD command prompt:

```bat
gorak run launch_score --component launch_panel
```

Enter 1 or 5 capsules and click **Calculate score**: expect 10 or 50 points.
The [OpenROAD UnitTestFramework](https://github.com/ActianCorp/OpenROAD_UnitTestFramework)
is bundled as portable Gorak source. The initial `gorak sync --push` imports it
before `launch_score`.

## Follow the video

### Change 10 to 12 in Workbench

In Workbench, change `p4_score` to return `capsules * 12`. Update the expected
values in `test_launch_score` to 0, 12, 48, 60 and 72 for 0, 1, 4, 5 and 6 capsules.
Change the frame subtitle to **12 points per capsule**, then save and close the
editors.

Pull those changes to disk and inspect the Git diff:

```bat
gorak status
gorak sync
gorak test
git diff
```

Commit the changes:

```bat
git add launch_score/p4_score.w4gl launch_score/test_launch_score.w4gl launch_score/launch_panel.wml
git commit -m "Set launch score to twelve points per capsule"
```

Five capsules now score 60 points.

### Ask Codex to add a fleet bonus

Open this repository in Codex and give it this prompt:

> Please add a one-time score bonus of 20 points when the capsule count is at
> least 5, keeping the existing 12 points per capsule. Update the tests to cover
> 0, 1, 4, 5 and 6 capsules, with expected scores of 0, 12, 48, 80 and 92.
> Change the Calculate score button to Calculate launch score and widen it to fit.
> Follow AGENTS.md: create a feature branch, make the changes, push them through
> Gorak and run the tests. Inspect the diff, commit, push the branch and create a
> pull request for review. Do not merge it.

Run the frame again: **5 capsules → 80 points**.

## License

[MIT](LICENSE). See [third-party attribution](THIRD_PARTY.md) for the test framework.
