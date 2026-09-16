# Reproducibility acceptance

This checklist tracks the fresh-clone rehearsal requested by
[Gorak issue #10](https://github.com/dougwhite/gorak/issues/10).

## Automated checks

- Current Gorak compact decoder reconstructs all four tracked components from a
  clean checkout with no `.env`, `.openroad` or XML companions.
- Both integer entry fields explicitly select the single-line palette style.
  The original exported frame at commit `443a83a` confirms `focusbehavior=4`,
  `lines=1` and the capsule field's `height=177`; these match style 1, not the
  multiline style 2. Existing explicit layout overrides remain authoritative.
- Baseline scoring source, test expectations and subtitle agree on 10 points per
  capsule. Tests retain the five boundary cases needed by the bonus walkthrough.
- The README command names/options have been checked against current Gorak CLI
  help. This does not establish live execution success.

## Live rehearsal — pending

Use a genuinely fresh clone and an explicitly designated disposable initialized
source repository. Install UnitTestFramework and its runtime dependencies before
pushing. Do not copy the author's `.env`, `.openroad`, or cached exports.

- [ ] Configure the fresh clone using the README and current Gorak `master`.
- [ ] Install/check current SSH helpers if using the remote backend.
- [ ] Push into a target without Launch Score; source verification and compilation
      succeed.
- [ ] Run `gorak test`; retain actual framework counts and failure/error totals.
- [ ] Run/open the reconstructed frame interactively; 1 → 10 and 5 → 50.
- [ ] Make the Workbench 10 → 12 procedure, test and subtitle edits; status, pull,
      tests and Git diff agree; 5 → 60.
- [ ] Make the disk bonus, assertion and button edits; push and tests pass;
      interactively verify 5 → 80.
- [ ] Check the dry-run behavior in a non-empty disposable repository containing
      unrelated applications and the framework, with no existing Launch Score.
- [ ] Execute all applicable README commands and record the Gorak revision used.

No live pass is claimed until this checklist is completed. A failed compile,
missing framework or inaccessible GUI must be reported separately from successful
source reconstruction. Retain private runtime artifacts locally, outside Git.
