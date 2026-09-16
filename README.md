# Launch Score — Gorak demo

A disposable OpenROAD application used in the [Gorak demo video](https://www.youtube.com/watch?v=zlncaV1mLqM).
Start with 10 points per capsule, make a change in Workbench, then add a fleet bonus
from readable source on disk.

**[Gorak](https://github.com/dougwhite/gorak)** ·
**[Watch the demo](https://www.youtube.com/watch?v=zlncaV1mLqM)** ·
**[Project and updates](https://thingsdougmakes.au/projects/gorak/)**

## Set up a disposable environment

Follow Gorak's [prerequisites and installation guide](https://github.com/dougwhite/gorak/blob/master/docs/getting-started.md)
using current Gorak `master`. You need a licensed OpenROAD development environment
and an independent disposable Ingres database initialized as an OpenROAD source
repository. Gorak does not create that database. Linux clients need an OpenROAD
execution host, for example Windows over SSH.

The clone includes **UnitTestFramework** as readable source in `unittestframework/`.
Gorak imports it before Launch Score. It provides `TestCase`, `G_Assert` and
`executeTests`; see [third-party provenance](THIRD_PARTY.md). This copy uses Windows
`kernel32.dll` (`GetTickCount64`), so the tested demo runtime is Windows OpenROAD.
The licensed OpenROAD installation and standard image libraries remain external.
See Gorak's [runtime environment documentation](https://github.com/dougwhite/gorak/blob/master/docs/run-test.md#trace-and-runtime-environment)
for framework environment settings.

```sh
git clone https://github.com/dougwhite/openroad_demo.git
cd openroad_demo
cp .env.example .env
```

On PowerShell, use `Copy-Item .env.example .env`. This clone is already a Gorak
project; do not run `gorak new` inside it. Edit the ignored `.env` for your target.
For local execution from an initialized OpenROAD command shell:

```dotenv
GORAK_BACKEND=local
GORAK_SQL_BACKEND=local
GORAK_VNODE=myvnode
GORAK_DATABASE=disposabledb
```

For SSH execution, use these settings instead:

```dotenv
GORAK_BACKEND=remote
GORAK_SQL_BACKEND=remote
GORAK_REMOTE_HOST=windows-host.example
GORAK_REMOTE_USER=developer
GORAK_REMOTE_ROOT=C:\Development\gorak
GORAK_VNODE=myvnode
GORAK_DATABASE=disposabledb
```

Replace the example values. Keep vnode and database separate. Then, for SSH only:

```sh
gorak remote install
gorak remote check
```

See [connection configuration](https://github.com/dougwhite/gorak/blob/master/docs/config.md)
and [remote setup](https://github.com/dougwhite/gorak/blob/master/docs/remote.md)
for installation-specific details. Keep credentials, `.env` and `.openroad/` out
of Git. Use a separate clone for a different source database.

## Reconstruct and run the baseline

Close Workbench editors before importing. The first operation on this fresh clone
is a **push**, to create `unittestframework` and then `launch_score` from the
tracked source:

```sh
gorak sync --push
gorak test
gorak compile launch_score
```

Run each command only after the previous one succeeds. `gorak test` runs the
`launch_score.runtests` entry point configured in `gorak.json`; it does not sync
source. The baseline assertions cover 0, 1, 4, 5 and 6 capsules, with scores
0, 10, 40, 50 and 60.

In Workbench, open `launch_score` in the configured source repository and run its
starting frame, `launch_panel`. Enter 1 and then 5 capsules and click **Calculate
score**: expect 10 and 50. From an interactive OpenROAD command shell you can also
run:

```sh
gorak run launch_score --component launch_panel
```

An SSH process completing does not prove a window appeared; verify the GUI in an
interactive OpenROAD session. Close the running frame and its editor before pushes.

The portable source is `gorak.json`, `app.json`, `.w4gl`, `.wml` and inherited
`field_defaults.json` files. Reconstruction needs no original `.openroad` cache or
XML companions. `.openroad/` is local binding, synchronization and recovery state.

Use a target with neither `launch_score` nor `unittestframework` already present.
The push installs both applications in an empty initialized repository. A
non-empty disposable repository may contain unrelated applications; inspect the
push plan before proceeding:

```sh
gorak sync --push --dry-run
```

Do not use this walkthrough to overwrite an existing `launch_score` or
`unittestframework`. Stop on a
conflict or verification failure and keep the reported recovery artifacts; see
[Gorak synchronization](https://github.com/dougwhite/gorak/blob/master/docs/synchronization.md).

## Follow the video

### 1. Change 10 to 12 in Workbench

Start from the baseline above and a clean Git working tree. Create a branch:

```sh
git switch -c demo/twelve-points
gorak sync
```

In Workbench, change `p4_score` to return `capsules * 12`. Update the expected
values in `test_launch_score` to 0, 12, 48, 60 and 72 for 0, 1, 4, 5 and 6 capsules.
Change the frame subtitle to **12 points per capsule**. Save the components, close
the editors, then pull those database edits to disk:

```sh
gorak status
gorak sync
gorak test
git diff
```

Check that the diff contains the procedure, assertions and subtitle changes, then:

```sh
git add launch_score/p4_score.w4gl launch_score/test_launch_score.w4gl launch_score/launch_panel.wml
git commit -m "Set launch score to twelve points per capsule"
```

Run the frame again: five capsules should score 60.

### 2. Add the fleet bonus from disk

```sh
git switch -c demo/fleet-bonus
gorak sync
```

In `launch_score/p4_score.w4gl`, replace the procedure body with:

```text
{
    IF capsules >= 5 THEN
        RETURN capsules * 12 + 20;
    ENDIF;
    RETURN capsules * 12;
}
```

In `launch_score/test_launch_score.w4gl`, change the five-capsule assertion from
60 to 80 and the six-capsule assertion from 72 to 92. Keep the 0, 1 and 4 capsule
checks at 0, 12 and 48. In `launch_score/launch_panel.wml`, change the
`calculate_score` button's `textlabel` to `Calculate launch score` and its `width`
to `2000`. Preserve the entry fields' `gorak_style` selectors.

You can make these edits yourself or ask an agent to implement them following
[AGENTS.md](AGENTS.md). Then, with Workbench editors closed:

```sh
gorak status
gorak sync --push && gorak test
git diff
```

Require a successful push and passing tests. Inspect any layout canonicalization
in the diff. Run the frame in Workbench: **5 capsules → 80 points**. Inspect and
commit the three edited files as above, then review the feature branch in Git.

## Validation and license

See [the acceptance checklist](docs/acceptance.md) for verification performed and
remaining live checks. Static source reconstruction is not OpenROAD compilation
or a visual walkthrough.

[MIT License](LICENSE) for the original demo, matching Gorak. The bundled
UnitTestFramework is third-party source; see [THIRD_PARTY.md](THIRD_PARTY.md).
The MIT grant does not relicense that framework or OpenROAD.
