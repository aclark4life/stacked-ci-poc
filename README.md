# stacked-ci-poc

Proof of concept: GitHub native **stacked pull requests** plus CI that runs
correctly for every PR in a stack. A 3-PR stack (`s1 -> main`, `s2 -> s1`,
`s3 -> s2`) with a tiered workflow: a cheap `fast` job gates every PR, a
`full` job runs only on `main` and `integration/**` pushes (the rollup branch
`integration/hello-stack` holds the whole stack).

Docs: <https://stacked-ci-poc.readthedocs.io>

- [How the stack is built](https://stacked-ci-poc.readthedocs.io/en/latest/stack.html)
- [CI rules for stacked PRs](https://stacked-ci-poc.readthedocs.io/en/latest/ci.html)
- [What GitHub fixes vs. what teams choose](https://stacked-ci-poc.readthedocs.io/en/latest/choices.html)

Key files: [`.github/workflows/ci.yml`](.github/workflows/ci.yml),
[`.github/workflows/rebase-stack.yml`](.github/workflows/rebase-stack.yml).
