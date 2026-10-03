# Working on this demo

Always spell `gorak` in lowercase, including at the start of sentences and in headings, documentation, UI text, commit messages, PR titles and release titles.

Follow the user's instructions for the requested change.

1. Check `git status` and run `gorak sync` before editing.
2. Make the source and test changes. Close Workbench editors before importing.
3. Run `gorak sync --push && gorak test`; tests execute database source.
4. Inspect `git diff` and report the changes and test results.

Keep `.env` and `.openroad/` out of Git. Preserve existing work and report any
sync failure rather than forcing an overwrite. Commit and publish a PR when
requested; do not merge without instruction.

See the [gorak guide](https://github.com/dougwhite/gorak/blob/master/docs/getting-started.md)
for setup and command details.
