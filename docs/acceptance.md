# Reproducibility acceptance

Rehearsed on 2026-09-16 for [Gorak issue #10](https://github.com/dougwhite/gorak/issues/10),
using Gorak `master` at `0a14ed90647b29795d20f1457f8d5a94b85f76ef` (confirmed
against GitHub), with Linux CLI → SSH → Windows OpenROAD and a disposable Ingres
source database. Private connection identities and runtime artifacts are not tracked.

## Passed

- Fresh Git clones contained all 26 portable components: four Launch Score
  components and 22 bundled UnitTestFramework components. No XML companions or
  original `.openroad` state were copied. Each clone was configured separately
  with local connection settings for the disposable target.
- Local compact reconstruction passed for every component. Both integer entry
  fields explicitly select the single-line palette style. The original frame
  export at commit `443a83a` confirms `focusbehavior=4`, `lines=1` and the capsule
  field's `height=177`, matching style 1 rather than multiline style 2.
- Current `gorak remote install` and `gorak remote check` succeeded.
- Against a newly created, initialized empty source database, `gorak sync --push`
  created both applications, ordered the framework first, verified source and
  completed compilation. Explicit `gorak compile launch_score` also passed.
- Baseline `gorak test`: **2 tests, 0 failures, 0 errors, 0 skipped**. Assertions
  cover 0, 1, 4, 5 and 6 capsules → 0, 10, 40, 50 and 60 points.
- An independent database-authoring checkout changed the procedure, assertions
  and subtitle to 12 points. The acceptance clone used `gorak status` and
  `gorak sync` to pull the three changed components, inspected/committed the Git
  diff, and passed the same suite. This exercises database-to-disk synchronization;
  it does **not** claim a manual Workbench edit.
- The acceptance clone authored the fleet bonus and button change on disk.
  `gorak sync --push && gorak test` passed: **2 tests, 0 failures, 0 errors,
  0 skipped**, including scores 0, 12, 48, 80 and 92.
- After framework whitespace normalization, another fresh clone rehearsed the
  final source in a recreated target containing one unrelated synthetic app.
  Dry-run planned exactly two creations; push created both apps; baseline tests
  passed again. The unrelated app's subsequent sync reported no changes.
- Final pull reported no changes; a repeat push made no updates.
- CLI help checks passed for documented Gorak commands. Git diff whitespace
  checks passed. GitHub documentation/repository and YouTube links returned
  HTTP 200.

A cache-free clone pointed at already present demo applications refused an
ambiguous added/added frame comparison. Its evidence was retained. The README
therefore requires neither demo application to exist before the first push;
existing unrelated applications are supported by the rehearsal above.

## Still manual or unavailable

- [ ] Open/run the fresh baseline in Workbench and visually confirm 1 → 10 and
      5 → 50, including layout and button fit.
- [ ] Perform the actual Workbench 10 → 12 edits from the README and visually
      confirm 5 → 60.
- [ ] Visually confirm the bonus frame's button and 5 → 80 result.
- [ ] Run the documented graphical `gorak run launch_score --component launch_panel`
      from an interactive OpenROAD command shell. An SSH process is not GUI proof.
- [ ] Verify the project/update link in a normal browser: the automated HTTP
      checker received 403 for `https://thingsdougmakes.au/projects/gorak/`.

The framework export had no standalone license file or version metadata; retained
attribution and source provenance are documented in [THIRD_PARTY.md](../THIRD_PARTY.md).
This PR does not claim the remaining issue acceptance gates are complete.
