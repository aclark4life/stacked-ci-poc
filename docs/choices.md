# Design choices

What GitHub fixes, and what a team can choose.

## Fixed by GitHub

- **Stack structure = base chain.** No separate stack object; a stack exists
  only because each PR's base is the previous branch.
- **Merge order is bottom-up.** You cannot land the middle PR first.
- **The rebase cascade.** A rewritten lower branch forces rebases above it.
- **GITHUB_TOKEN pushes do not trigger workflows**, so bot automation needs
  a PAT or GitHub App token to re-run PR CI.

## Open choices

- **CI shape** — what each level's cheap job runs; whether a rollup branch
  exists; where the full suite runs (per PR, rollup, or merge-queue gated);
  head-SHA vs merge-ref checkout.
- **Merge strategy** — squash the stack to one commit, one merge commit per
  PR, or rebase-merge each PR for linear history.
- **Automation** — native UI only; a bot workflow (you choose when it runs,
  what it does on conflict, and how it discovers stack branches — the POC
  hardcodes them, a real repo would walk PR bases via the API); or local
  tooling (`gh stack`, Graphite). Token type: PAT (simple, personal) vs
  GitHub App (bot identity, survives offboarding).
- **Process** — required per-PR checks vs required rollup checks; review
  bottom-up by delta vs review the rollup in one pass; who triggers merges.
- **Policy** — stacks pay off when PRs live for days (review capacity
  constrained). If PRs land in hours, trunk-based short branches avoid the
  whole problem.

The POC is one point in this space: native stacking, tiered CI, head-SHA
checkout, and a minimal hardcoded-branch rebase bot.
