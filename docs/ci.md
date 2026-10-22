# CI for stacked PRs

Four rules make per-PR CI work for a stack.

## 1. Trigger with no branch filter

```yaml
on:
  pull_request:      # no branches filter
  push:
    branches: [main, "integration/**"]
```

Stacked PRs target non-default branches. Any `branches:` filter on
`pull_request` means "PRs targeting these branches" and silently skips the
stack.

## 2. Test the PR head, not the merge ref

Actions checks out a merge commit of head into base by default. For a
stacked PR whose base is itself unmerged, that tree was never reviewed.
Check out the PR head commit instead:

```yaml
env:
  HEAD_SHA: ${{ github.event.pull_request.head.sha || github.sha }}
steps:
  - uses: actions/checkout@v4
    with:
      ref: ${{ env.HEAD_SHA }}
```

The `||` fallback must live in a job-level `env`; GitHub rejects it directly
in `with:` (the workflow fails to parse, zero-second failure, no logs).

## 3. Per-PR isolation

A push to one PR's branch runs only that PR's CI. Other PRs keep their
results — they go stale when a lower PR changes, which is what the rebase
automation addresses.

## 4. Tier the checks

- **fast** job: lint + unit tests, runs for every PR and push. Gates each
  stacked PR cheaply.
- **full** job: gated on `github.event_name == 'push'` to `main` or
  `integration/**`. Stands for the expensive suite (e.g. functional tests
  against a real MongoDB server).

For a 3-PR hello-world stack tiering is overkill; for a 14-PR, ~15k-line
stack that needs a live database (the mlflow-mongodb case), it turns 14
expensive runs per change into one.
